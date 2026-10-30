"""Run every structural check on the skill in one go: python tools/check_skill.py

Checks: the frontmatter rules of the Agent Skills specification (plus the skill-creator
validator when it is installed locally), description and SKILL.md length, links from
SKILL.md to every reference file, a Contents section in long reference files, the house
style (no em dashes, en dashes or double hyphens in prose), evals.json, the plugin and
marketplace manifests, the version in CHANGELOG.md, and that every source URL in the
references is listed in tools/verified_sources.json. Exit code 1 if anything fails.
Needs Python 3 and PyYAML.
"""
import glob
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "project-engineering-advisor"
SKILL = os.path.join(ROOT, "skills", NAME)
# The skill-creator plugin cache path includes a version hash; take the newest copy if present.
VALIDATORS = sorted(glob.glob(os.path.expanduser(
    "~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/quick_validate.py")),
    key=os.path.getmtime)

failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL", msg)


def read(*parts):
    return open(os.path.join(ROOT, *parts), encoding="utf-8").read()


# 1. Frontmatter (https://agentskills.io/specification and the platform overview page)
text = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read()
fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---", text, re.S).group(1))
name, desc = fm.get("name", ""), fm.get("description", "")
if set(fm) != {"name", "description"}:
    fail(f"frontmatter should hold only name and description, found {sorted(fm)}")
if name != NAME or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
    fail(f"name {name!r} breaks the naming rules or does not match the folder")
if re.search(r"anthropic|claude", name) or re.search(r"[<>]", desc) or not desc:
    fail("name uses a reserved word, or description is empty or has angle brackets")
if VALIDATORS:
    r = subprocess.run([sys.executable, VALIDATORS[-1], SKILL], capture_output=True, text=True)
    print("skill-creator validator:", r.stdout.strip())
    if r.returncode:
        fail("skill-creator validator")
else:
    print("skill-creator validator: not installed here, built-in frontmatter checks only")

# 2. Length
lines = text.count("\n")
print(f"description: {len(desc)} of 1024 characters; SKILL.md: {lines} of 500 lines")
if len(desc) > 1024 or lines >= 500:
    fail("description or SKILL.md too long")

# 3. Links and reference files
refs = sorted(glob.glob(os.path.join(SKILL, "references", "*.md")))
linked = set(re.findall(r"\(references/([\w-]+\.md)\)", text))
for r in refs:
    ref, body = os.path.basename(r), open(r, encoding="utf-8").read()
    if ref not in linked:
        fail(f"{ref} is not linked from SKILL.md")
    if body.count("\n") > 100 and "## Contents" not in body:
        fail(f"{ref} is over 100 lines without a Contents section")
    if re.search(r"\]\([^)]+\.md\)", body):
        fail(f"{ref} links to another .md file (keep references one level deep)")
for ref in linked:
    if not os.path.exists(os.path.join(SKILL, "references", ref)):
        fail(f"SKILL.md links to missing references/{ref}")
print(f"references: {len(refs)} files")

# 4. House style
docs = (glob.glob(os.path.join(SKILL, "**", "*.md"), recursive=True) + glob.glob(os.path.join(ROOT, "*.md"))
        + glob.glob(os.path.join(ROOT, ".github", "**", "*.*"), recursive=True))
for f in docs:
    t = open(f, encoding="utf-8").read()
    prose = re.sub(r"`[^`]*`", "", re.sub(r"```.*?```", "", t, flags=re.S))
    for ch, label in (("—", "em dash"), ("–", "en dash")):
        if ch in t:
            fail(f"{os.path.relpath(f, ROOT)}: {label}")
    for line in prose.splitlines():
        if "--" in line and not re.fullmatch(r"\s*(---|\|?[\s:|-]+\|?)\s*", line):
            fail(f"{os.path.relpath(f, ROOT)}: double hyphen: {line.strip()[:80]}")

# 5. Evals
evals = json.loads(read("evals", "evals.json"))
if evals.get("skill_name") != NAME:
    fail("evals.json skill_name does not match the skill name")
for e in evals["evals"]:
    for path in e.get("files", []):
        if not os.path.isdir(os.path.join(ROOT, path)):
            fail(f"eval {e['id']}: fixture {path} not found")
print(f"evals: {len(evals['evals'])} scenarios, {sum(len(e['expectations']) for e in evals['evals'])} expectations")

# 6. Plugin and marketplace manifests, version in CHANGELOG.md
plugin = json.loads(read(".claude-plugin", "plugin.json"))
market = json.loads(read(".claude-plugin", "marketplace.json"))
entries = market.get("plugins", [])
if plugin.get("name") != NAME or [p.get("name") for p in entries] != [NAME] or entries[0].get("source") != "./":
    fail("plugin.json and marketplace.json must both name the plugin and point the entry at ./")
top = re.search(r"^## \[?(\d+\.\d+\.\d+)", read("CHANGELOG.md"), re.M)
if not top or top.group(1) != plugin.get("version"):
    fail(f"plugin.json version {plugin.get('version')} does not match the newest CHANGELOG.md entry")
print(f"plugin: version {plugin.get('version')}")

# 7. Source URLs were verified
known = {s["url"].rstrip("/") for s in json.loads(read("tools", "verified_sources.json"))}
for r in refs:
    for u in re.findall(r"https?://[^\s)]+", open(r, encoding="utf-8").read()):
        if u.rstrip("/.,") not in known:
            fail(f"{os.path.basename(r)}: unverified URL {u} (read the page, then add it to tools/verified_sources.json)")

# Not a failure: placeholders the maintainer fills in before publishing.
pending = [p for p in ("LICENSE", "README.md", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json")
           if re.search(r"\b(OWNER|AUTHOR_NAME)\b", read(p))]
if pending:
    print("note: placeholders OWNER or AUTHOR_NAME remain in", ", ".join(pending))

print("ALL CHECKS PASSED" if not failures else f"{len(failures)} check(s) failed")
sys.exit(1 if failures else 0)
