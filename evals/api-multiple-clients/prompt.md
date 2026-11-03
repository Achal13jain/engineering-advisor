---
tags: [planning, api]
expected_outcome: "API with external consumers; contract in the repository, automated breaking-change check, additive changes with deprecation, support for old mobile versions."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We run a REST API in Node and TypeScript that our React web app, our iOS and Android apps, and two partner companies call. Last month a field rename broke the Android app for users who hadn't updated. What should our engineering workflow look like so this stops happening?
