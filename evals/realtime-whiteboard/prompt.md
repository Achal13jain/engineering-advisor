---
tags: [planning, real-time]
expected_outcome: "Real-time playbook: concurrency and conflict tests, reconnection and ordering, load tests sized to use, deploys that do not drop sessions, connection monitoring, durable board state."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We're building a collaborative whiteboard where up to 20 people edit the same board live, using WebSockets, a Node server and Redis, with boards saved to PostgreSQL. We're a startup with four engineers and a public beta in three months. What should our engineering workflow and testing look like?
