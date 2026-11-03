---
tags: [planning, library]
expected_outcome: "Library: SemVer, changelog, test matrix, publishing from CI with trusted publishing or provenance, contributor files, maintenance branches only for supported old majors."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

I maintain a TypeScript date-parsing library on npm with about 40k weekly downloads. Contributors send pull requests, and releases are me running npm publish from my laptop when I remember. How should I set up the workflow?
