---
tags: [planning, distributed]
expected_outcome: "Distributed systems playbook: idempotent consumers, dead-letter queues with alerts and replay, correlation identifiers and tracing, event contracts between teams, infrastructure as code, AWS facts verified rather than recited."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Our order processing runs on AWS Lambda functions connected by SQS queues and EventBridge: about 15 functions, owned by two teams. Lately we've had duplicate emails and orders stuck with no error anywhere. How should we improve our engineering practices?
