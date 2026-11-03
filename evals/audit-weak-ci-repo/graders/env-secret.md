---
type: llm
---

PASS if the answer flags the tracked .env file as exposed secrets and recommends rotating them.
FAIL if the tracked .env is not flagged, or rotation is not recommended.
