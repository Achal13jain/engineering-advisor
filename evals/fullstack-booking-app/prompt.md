---
tags: [planning, full-stack]
expected_outcome: "Moderate-risk full-stack app: authorization and integration tests, migrations, tested restores, reliable reminders, automated deploys with rollback, no microservices."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We're building a booking app for a chain of three yoga studios: customers sign up, book classes and get email reminders, and staff manage the schedules. Payments happen at the studio, not online. It's a Next.js frontend with a Node API and PostgreSQL on a single cloud VM. Two developers, launching in two months. What engineering workflow should we set up?
