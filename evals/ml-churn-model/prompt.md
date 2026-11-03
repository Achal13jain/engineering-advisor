---
tags: [planning, machine-learning]
expected_outcome: "ML playbook at a proportionate size: reproducible training with versioned data, code and model, an evaluation gate against the current model, monitoring for drift, rollback to the previous model, care with customer data."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We trained a churn prediction model in Python with scikit-learn, and our sales team uses its scores every week to decide which customers to call. Two data scientists retrain it by hand in a notebook every month and copy the model file to a server. How should we put proper engineering around this?
