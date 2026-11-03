---
tags: [planning, iot]
expected_outcome: "Firmware playbook: signed images, A/B partitions with automatic revert, staged cohorts with health checks and a halt, real-device testing, version tracking per device, a fail-safe valve state."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We make smart irrigation controllers: ESP32 firmware written in C, about 2,000 devices installed in customers' gardens, updated over the air from our cloud. One firmware engineer and one backend engineer. An update last spring bricked 40 devices. How should we set up the release process?
