---
tags: [audit, false-positive]
expected_outcome: "Recognizes a well-run solo library: tests in spec/, Renovate, CI on pull requests, release from CI with provenance. Few or no gaps, no invented process, unseen settings listed as not verified."
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Review this repository and tell me what engineering practices are missing. It's a small open-source library I maintain on my own. Don't change anything.
