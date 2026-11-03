---
tags: [planning, deployment]
expected_outcome: "Incremental path: automated deployment of one artifact, expand and contract migrations run separately and tested for locks, health checks, a rehearsed rollback, roll back versus roll forward, tested restores. No big-bang re-platform."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Our Django app has been in production for two years with about 5,000 daily users. We deploy by SSHing into the server, running git pull, then migrations, then restarting. Last month a migration locked a big table and we were down for 40 minutes, and we couldn't roll back. How do we make deployments and rollbacks safer without rebuilding everything?
