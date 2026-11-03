"""Run every structural check on the skill in one go: python tools/check_skill.py

Checks: the frontmatter rules of the Agent Skills specification (plus the skill-creator
validator when it is installed locally), description and SKILL.md length, links from
SKILL.md to every reference file, a Contents section in long reference files, the house
style (no em dashes, en dashes or double hyphens in prose), the eval case files, the plugin and
marketplace manifests for Claude Code and Codex, the version in CHANGELOG.md, and that every source URL in the
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
NAME = "engineering-advisor"
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
        + glob.glob(os.path.join(ROOT, ".github", "**", "*.*"), recursive=True)
        + glob.glob(os.path.join(ROOT, "evals", "**", "*.md"), recursive=True))
for f in docs:
    t = open(f, encoding="utf-8").read()
    body = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)  # frontmatter holds patterns, not prose
    prose = re.sub(r"`[^`]*`", "", re.sub(r"```.*?```", "", body, flags=re.S))
    for ch, label in (("—", "em dash"), ("–", "en dash")):
        if ch in t:
            fail(f"{os.path.relpath(f, ROOT)}: {label}")
    for line in prose.splitlines():
        if "--" in line and not re.fullmatch(r"\s*(---|\|?[\s:|-]+\|?)\s*", line):
            fail(f"{os.path.relpath(f, ROOT)}: double hyphen: {line.strip()[:80]}")

# 5. Eval cases in the claude plugin eval format (https://code.claude.com/docs/en/plugin-evals)
PROMPT_KEYS = {"schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome", "model",
               "max_turns", "timeout_seconds", "allowed_tools", "append_system_prompt", "env"}
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}
cases = sorted(glob.glob(os.path.join(ROOT, "evals", "*", "prompt.md")))
graders = 0
for p in cases:
    case = os.path.dirname(p)
    label = os.path.basename(case)
    t = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)", t, re.S)
    keys = set(yaml.safe_load(m.group(1))) if m else set()
    if not m or not m.group(2).strip() or keys - PROMPT_KEYS:
        fail(f"eval {label}: prompt.md needs frontmatter with known keys and a prompt, unknown {sorted(keys - PROMPT_KEYS)}")
    files = glob.glob(os.path.join(case, "graders", "*.md"))
    graders += len(files)
    for g in files:
        gm = re.match(r"^---\n(.*?)\n---", open(g, encoding="utf-8").read(), re.S)
        if not gm or yaml.safe_load(gm.group(1)).get("type") not in GRADER_TYPES:
            fail(f"eval {label}: {os.path.basename(g)} has no valid grader type")
    if not files:
        fail(f"eval {label}: no graders")
    if os.path.exists(os.path.join(case, "case.yaml")):
        cy = yaml.safe_load(open(os.path.join(case, "case.yaml"), encoding="utf-8"))
        script = (cy.get("context") or {}).get("scaffold_script")
        if cy.get("name") != label or (script and not os.path.exists(os.path.join(case, script))):
            fail(f"eval {label}: case.yaml name differs from the folder, or its scaffold script is missing")
if not cases:
    fail("no eval cases found in evals/")
print(f"evals: {len(cases)} cases, {graders} graders")

# 6. Plugin and marketplace manifests, version in CHANGELOG.md
plugin = json.loads(read(".claude-plugin", "plugin.json"))
market = json.loads(read(".claude-plugin", "marketplace.json"))
entries = market.get("plugins", [])
if plugin.get("name") != NAME or [p.get("name") for p in entries] != [NAME] or entries[0].get("source") != "./":
    fail("plugin.json and marketplace.json must both name the plugin and point the entry at ./")
# Codex reads the root plugin.json (Agent Plugins format) and .agents/plugins/marketplace.json
# (https://developers.openai.com/codex/plugins/build, read 3 November 2026).
portable = json.loads(read("plugin.json"))
PORTABLE_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license",
                 "keywords", "extensions"}
if (portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json" or set(portable) - PORTABLE_KEYS
        or portable.get("name") != NAME or portable.get("version") != plugin.get("version")):
    fail("plugin.json must use the Agent Plugins schema, its known fields, the plugin name and the same version as .claude-plugin/plugin.json")
codex = json.loads(read(".agents", "plugins", "marketplace.json")).get("plugins", [])
if [p.get("name") for p in codex] != [NAME] or codex[0].get("source") != "./" or not {"policy", "category"} <= set(codex[0]):
    fail(".agents/plugins/marketplace.json must hold one entry for the plugin with source ./, a policy and a category")
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
