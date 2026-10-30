# Security, reliability and maintenance

## Contents
- Safeguards by risk profile
- Application security checklist
- Backups and recovery
- Monitoring and alerts
- Incident response
- Long-term maintenance
- Signals to add or remove process
- Sources

## Safeguards by risk profile

Each profile includes everything in the profiles above it.

| Area | Low | Moderate | High | Critical |
|---|---|---|---|---|
| Access | Protected main; owners for domain and hosting accounts, with more than one person able to reach them | Least-privilege roles; reviewed admin access | Single sign-on for staff, audit logs, periodic access reviews | Separation of duties for irreversible operations |
| Secrets | Out of the repository; secret scanning | Per-environment secrets in a secret store | Short-lived credentials (OIDC), rotation procedure | Hardware-backed keys where relevant, such as firmware signing |
| Dependencies | Automated update pull requests | Vulnerability scanning with a named triager | Dependency review blocks risky new packages | Supply-chain controls such as provenance and pinned builds |
| Authentication and authorization | Not applicable without accounts | Proven library or provider; authorization tests per role | Tenant-isolation tests; security testing before major releases | Independent security review |
| Input and abuse | Spam protection on forms | Validation at every boundary; rate limits on logins, forms and APIs | Abuse monitoring, bot protection on money-moving flows | Formal threat modeling |
| Privacy | Know what forms collect and where it goes | Inventory of personal data, retention and deletion | Data processing agreements checked; export and erasure paths | Regulatory evidence and audits |
| Recovery | Git holds the code; CMS content backed up | Database backups with a tested restore | Point-in-time recovery, agreed RTO and RPO, runbooks | Disaster recovery drills, multi-region where the RTO demands it |
| Monitoring | Uptime check, certificate and domain expiry | Error tracking, structured logs, alerts with owners | SLOs, on-call duty, dashboards per critical flow | Error budgets, automated rollback |
| Incidents | Know how to roll back | Short written incident procedure | Defined roles, status communication, blameless reviews | Practiced response, regulatory notification paths |

Size never lowers this floor. Money, personal data and regulated data raise it.

## Application security checklist

Use the current OWASP Top 10 as the checklist for web applications and APIs. The 2025 edition lists: broken access control, security misconfiguration, software supply chain failures, cryptographic failures, injection, insecure design, authentication failures, software or data integrity failures, security logging and alerting failures, and mishandling of exceptional conditions. For LLM features, use the OWASP Top 10 for LLM Applications (2025 edition), which starts with prompt injection and sensitive information disclosure and includes excessive agency and unbounded consumption. Check both pages for newer editions before citing them.

For a deep security review, recommend a dedicated security review or audit tool or skill if one is available, rather than treating this advisor's checklist as an audit.

## Backups and recovery

- Back up every store of data that cannot be regenerated: databases, uploaded files, CMS content, configuration that lives outside Git.
- Agree a recovery time objective and recovery point objective with the business, even roughly; they decide backup frequency and whether point-in-time recovery is needed.
- Restore a backup into a separate environment and time it before launch, then on a schedule. An untested backup is a hope, not a safeguard.
- Keep at least one copy outside the account or region that could fail or be compromised, where the risk profile justifies it.

## Monitoring and alerts

- Start with error tracking, structured logs with request identifiers, and an outside uptime or health check.
- For services, watch the four golden signals: latency, traffic, errors and saturation.
- Alert on symptoms users would notice, route each alert to a person who can act, and keep alerts few. Pages that fire often and require nothing get ignored, and then the real one is missed.
- Add SLOs and error budgets when users depend on availability and there is enough traffic to measure.

## Incident response

1. Declare an incident early, as soon as users are or might be affected. Standing down is cheaper than starting late.
2. Give one person incident command; separate operational work and communication when more than one person is involved.
3. Mitigate first (flag off, rollback), diagnose afterwards.
4. Tell users through an agreed channel what you know, what you are doing and when you will update them.
5. Keep a timeline as you go.
6. Hold a blameless review that looks for contributing causes in the system, and track its actions to completion.

## Long-term maintenance

- **Dependencies**: automated update pull requests on a weekly or monthly cadence, grouped to reduce noise (Dependabot supports groups and a cooldown period; Renovate is an alternative). Security updates are reviewed promptly by a named person.
- **Runtimes and frameworks**: track end-of-support dates from the official schedules (for example the Node.js release schedule) and plan upgrades before them, one major version at a time.
- **Technical debt**: record it where work is planned, tie it to the risk or cost it creates, and reserve regular capacity for it.
- **Documentation**: update the README, runbooks and decision records in the same pull request as the change they describe.
- **Triage**: one place for bugs and requests, triaged on a known schedule by a named person.
- **Ownership**: every system, repository and external account (domain, hosting, providers) has an owner, and access never depends on one person.
- **Operational review**: periodically review incidents, alerts, costs and delivery metrics. The DORA metrics (change lead time, deployment frequency, failed deployment recovery time, change fail rate, deployment rework rate) measure delivery outcomes better than activity counts.

## Signals to add or remove process

Add process when there is evidence: repeated incidents of the same kind, reviews that take days, deployments people fear, onboarding that takes weeks, main breaking often, customers or contracts demanding commitments, new money or sensitive data, or a new team.

Remove process when it no longer pays: checks nobody reads, environments nobody uses, services that always deploy together, queues that carry a handful of messages, release ceremonies for software that can be rolled back in minutes.

## Sources

Checked 27 October 2026. Recheck before relying on tool behavior or editions.
- OWASP Top 10 2025: https://top10.owasp.org/2025/
- OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/
- Monitoring distributed systems (golden signals): https://sre.google/sre-book/monitoring-distributed-systems/
- Managing incidents: https://sre.google/sre-book/managing-incidents/
- Blameless postmortems: https://sre.google/sre-book/postmortem-culture/
- DORA metrics: https://dora.dev/guides/dora-metrics/
- Dependabot options: https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
- Node.js release schedule: https://github.com/nodejs/Release
