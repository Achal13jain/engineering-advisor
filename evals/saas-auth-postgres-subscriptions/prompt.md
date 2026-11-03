---
tags: [planning, saas]
expected_outcome: "High risk SaaS; modular monolith, GitHub Flow, tenant isolation tests, verified idempotent billing webhooks, expand and contract migrations, a justified staging environment, point-in-time recovery."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm about to start building a B2B SaaS for small accounting firms: user sign-in, a PostgreSQL database, team workspaces, and monthly subscriptions through Stripe. Two developers, launch planned in four months. Design the engineering workflow before we write code.
