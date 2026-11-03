---
tags: [planning, ai]
expected_outcome: "AI playbook: golden-set evaluations gating prompt and model changes, versioned prompts and model ids, timeouts and fallback, cost tracking, prompt injection defenses, staged rollout, provider terms verified rather than stated."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We're adding an AI assistant to our help center. It answers customer questions using our documentation (RAG) and calls an external LLM API. The product team keeps tweaking prompts and wants to try a newer model next month. How should we test and release this safely?
