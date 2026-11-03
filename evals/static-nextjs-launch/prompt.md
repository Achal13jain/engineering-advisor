---
tags: [planning, static-site]
expected_outcome: "Classifies a static content site at Low risk, or Moderate because of the form, at the pre-launch stage; main plus preview deployments, a short CI and a launch checklist, without enterprise process."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm launching a static Next.js website for a small consulting company in about three weeks. It has 8 pages, a blog written in markdown, and a contact form. I'm the only developer and it will be hosted on Vercel. Help me set up the repository and the deployment workflow properly before launch.
