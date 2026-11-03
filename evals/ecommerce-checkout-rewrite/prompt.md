---
tags: [planning, e-commerce]
expected_outcome: "High-risk transactional release: idempotent payments and reconciliation, checkout journey tests, flag or traffic-share rollout with a fast switch back, care around the peak, tax correctness verified with authoritative sources."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We sell handmade furniture online with a custom checkout built on Laravel and Stripe, about 300 orders a month. We're replacing the checkout and adding international shipping and tax. Black Friday is our biggest week. Three developers. How should we release the new checkout safely?
