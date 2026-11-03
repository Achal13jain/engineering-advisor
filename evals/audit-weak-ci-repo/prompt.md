---
tags: [audit]
expected_outcome: "Read-only gap report for a High-risk transactional app: tracked .env, unauthorized order access and SQL from input, unverified webhook, weak CI, one-person manual deploy, hand-applied schema, a production branch used as an environment."
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Can you review this repository and tell me what engineering practices are missing? We have real customers on it. Don't change anything yet, I just want the assessment.
