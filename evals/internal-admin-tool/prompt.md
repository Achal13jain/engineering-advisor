---
tags: [planning, internal-tool]
expected_outcome: "Internal tool that still touches money and personal data: real authentication and permissions despite the VPN, audit logs, light process for one maintainer, no public-product machinery."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Our operations team of six uses an internal admin dashboard we built in Django to look up customers, issue refunds of up to $50 and edit shipping addresses. It's only reachable on the company VPN. One developer maintains it part-time. What engineering practices does it need?
