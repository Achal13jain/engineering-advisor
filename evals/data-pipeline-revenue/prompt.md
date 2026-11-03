---
tags: [planning, data-pipeline]
expected_outcome: "Data pipeline playbook: data tests in CI and on schedule, reviewed changes built against non-production data, anomaly and freshness alerts with an owner, sign-off before figures leave, raw data kept."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We have nightly dbt jobs on Snowflake that build the revenue dashboards our finance team sends to the board each month. Last quarter a join bug double-counted revenue and nobody noticed for two weeks. Two analytics engineers. What should we change?
