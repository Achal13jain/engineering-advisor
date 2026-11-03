"""Report on the sources in tools/verified_sources.json: python tools/check_sources.py [--max-age DAYS]

Fetches every listed page and reports pages that no longer load and entries whose
verification date is older than --max-age days (default 180). It cannot tell whether a page
still says what the note records, so a maintainer rereads each flagged page, updates the
skill if the fact changed, and sets the new date. Exit code 1 if any page fails to load;
stale dates alone are a warning. Needs only Python 3. The monthly Sources workflow runs it.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
max_age = int(sys.argv[sys.argv.index("--max-age") + 1]) if "--max-age" in sys.argv else 180
today = datetime.date.today()
sources = json.load(open(os.path.join(ROOT, "tools", "verified_sources.json"), encoding="utf-8"))

broken, stale = [], []
for s in sources:
    req = urllib.request.Request(s["url"], headers={"User-Agent": "engineering-advisor-source-check"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    except (urllib.error.URLError, TimeoutError) as e:
        status = getattr(e, "reason", e)
    if status != 200:
        broken.append(f"- {s['url']}: {status}")
    age = (today - datetime.date.fromisoformat(s["accessed"])).days
    if age > max_age:
        stale.append(f"- {s['url']}: checked {s['accessed']}, {age} days ago. Recorded fact: {s['note']}")

report = [f"# Source check, {today}", "",
          f"{len(sources)} sources. {len(broken)} did not load, {len(stale)} were last checked more than {max_age} days ago.", ""]
if broken:
    report += ["## Pages that did not load", "",
               "Some sites refuse automated requests; open each page in a browser before changing anything.", ""] + broken + [""]
if stale:
    report += ["## Pages to reread", ""] + stale + [""]
text = "\n".join(report)
print(text)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
        f.write(text + "\n")
sys.exit(1 if broken else 0)
