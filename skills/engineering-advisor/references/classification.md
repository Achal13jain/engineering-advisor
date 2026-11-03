# Classification and maturity

## Contents
- Questions that change the answer
- Risk profiles and recovery objectives
- Release channels
- Choosing the family
- Hybrid projects
- Maturity stages
- What to establish early and what can wait
- When to classify again

## Questions that change the answer

Answer these from the repository and the conversation first; ask the user only for the ones that remain unknown and matter.

| # | Question | What the answer changes |
|---|---|---|
| 1 | Is it static, dynamic, transactional or data-intensive? | The family, and with it every default. |
| 2 | Does it have a backend, a database, authentication or authorization? | Migrations, backups, integration tests and authorization tests become necessary. |
| 3 | Does it handle payments, personal, confidential or regulated data? | Raises the risk profile; adds reviews, audit logs, recovery objectives and privacy work. |
| 4 | Does it depend on external APIs, AI models, queues, scheduled jobs or real-time events? | Adds timeouts, retries, idempotency, failure tests and monitoring of each dependency. |
| 5 | How does a change reach users? | Decides how much testing must happen before release and whether release branches are justified (see Release channels). |
| 6 | How often will code be deployed? | Frequent deploys need automation and fast rollback; rare deploys need rehearsed procedures. |
| 7 | One developer or a team, and how many? | Reviews, code ownership and merge rules grow with the team, not with the code size. |
| 8 | How much do availability, latency, consistency and data recovery matter? | Sets recovery objectives, SLOs and the deployment strategy. |
| 9 | Are there regulatory, privacy or data residency requirements? | Adds retention rules, region choices and evidence of controls. Recommend confirming obligations with a qualified person. |
| 10 | What are the budget and operational constraints? | Favors managed services and fewer environments when money or people are scarce. |
| 11 | Prototype, pre-launch, production or mature? | Sets the maturity stage. |
| 12 | How much downtime or data loss can the business tolerate? | Sets the recovery time and recovery point objectives. |
| 13 | Who will operate and maintain it after launch? | Decides how much documentation, automation and handover is needed. |

## Risk profiles and recovery objectives

| Profile | Definition | Examples | What it adds |
|---|---|---|---|
| Low | Public information only, no user accounts, no money; failure is embarrassing but cheap. | Brand website, portfolio, documentation site, prototype with test data. | The essential floor: version control, protected main, CI that builds, automated deploys with rollback, dependency updates. |
| Moderate | User accounts or personal data; business workflows depend on it; outages cost money or trust. | Full-stack app, internal business tool, community site. | Integration and authorization tests, backups with tested restores, error tracking, previews or staging. |
| High | Money movement; sensitive personal data such as health, financial or children's data; regulated data; contractual availability. | Online shop, B2B SaaS with service levels, clinic booking, payroll. | Required reviews, production approval or progressive delivery, point-in-time recovery, SLOs, incident process, audit logs, security testing. |
| Critical | Failure can cause physical harm, large financial loss or legal breach at scale. | Payment processor, medical device software, industrial control. | Progressive delivery with automatic rollback, disaster recovery drills, independent security review, formal change control for irreversible operations. |

Assign the profile from the riskiest thing the system does, not from its size or traffic. Traffic and availability count only through the damage a failure would cause: a contractual availability commitment makes a system at least High, and an outage that would itself cause large financial loss or harm makes it Critical. High traffic on its own raises the maturity stage and may point to the distributed systems family, not to a higher risk profile.

Record the drivers with the profile: the one to three facts that set it, taken from these factors, and what would move it up or down.

| Driver | Raises the profile when |
|---|---|
| Money | The system takes, holds or moves money, or a failure costs customers money. |
| Data sensitivity | It stores personal data (Moderate), or health, financial, children's or other sensitive data (High). |
| Regulation | A law, regulator or contract sets obligations for the data or the service. |
| Availability commitment | Customers have a contractual or safety-related availability promise. |
| Harm and blast radius | A failure could injure people, damage equipment, or affect many customers or other organizations at once. |
| Reversibility | Mistakes cannot be undone: shipped binaries, firmware, published packages or figures, destroyed data. |

For example: "High, because it takes card payments through a provider and stores customers' order history; it would become Critical only if it moved money between accounts itself."

Recovery objectives, agreed with the business even roughly:
- **Recovery time objective (RTO)**: how long the system can stay in recovery before the damage becomes unacceptable.
- **Recovery point objective (RPO)**: the point in time to which data must be recovered, which tells you how much recent data the business can afford to lose.

Definitions follow the NIST glossary (csrc.nist.gov/glossary/term/recovery_time_objective and recovery_point_objective, checked 27 October 2026).

## Release channels

| Channel | Can a bad release be undone quickly? | Consequence |
|---|---|---|
| Web or server deploy | Yes, in minutes, by rollback or flag | Invest in fast detection, smoke tests and rollback; continuous deployment is often fine. |
| App store or signed desktop installer | No; installed versions persist and review delays fixes | Short-lived release branch per version, beta tracks, staged rollouts that can be halted, minimum supported version. |
| Package registry (libraries, CLIs, SDKs) | No; published versions are immutable and consumers pin them | Semantic versioning, compatibility matrix, changelog, deprecation policy, maintenance branches only for supported old majors. |
| Firmware over the air | No, and failures can brick devices | Signed images, A/B partitions with automatic revert, staged fleet cohorts, release branch per firmware line. |
| Scheduled data runs and published figures | Partly; data can be rebuilt only if raw data is kept | Idempotent jobs, data tests, keeping raw data, sign-off for figures that leave the company. |

## Choosing the family

Ask in this order and stop at the first yes. The order puts the families with the hardest-to-reverse release channels first.

1. Do other developers install it as code? Libraries, SDKs, CLIs and open source.
2. Does it run on hardware that you ship? IoT and hardware-integrated software.
3. Is it installed on phones or desktops? Mobile and desktop applications.
4. Is its main output data or trained models? Data pipelines and analytics; if it trains models, machine learning systems.
5. Only pages and content, no user data? Static and content websites.
6. Is it mainly an API for other clients? APIs, backend services and monoliths; with many services, events or extreme traffic, distributed systems.
7. Do several organizations share it? SaaS, multi-tenant platforms and marketplaces.
8. Is selling or moving money the core flow? E-commerce and transactional platforms.
9. Are the users only internal colleagues? Internal tools and admin dashboards.
10. Live updates or collaborative editing? Real-time and collaborative applications.
11. Otherwise: dynamic and full-stack web applications.

At any step, a feature that relies on LLMs or external AI models also follows the AI-powered applications playbook for that feature.

## Hybrid projects

Most real projects are hybrids, for example a SaaS product with an AI assistant and a reporting pipeline.

- Use the primary family's defaults for the whole project.
- Apply the stricter practices of each other family only to the part that carries that risk: evaluation gates for the AI feature, data tests for the pipeline, payment idempotency for checkout.
- Isolate the risky part behind a clear boundary (a module, a service or a provider) so its safeguards do not spread to everything else.
- Take the highest risk profile of any part for shared foundations such as access control, secrets and backups.

## Maturity stages

| Stage | Priority | Establish now | Can still wait | Move on when |
|---|---|---|---|---|
| 1 Prototype | Answer a question cheaply: can it be built, do users want it. | Version control, secrets outside the code, a README. | Most tests, staging, monitoring. | Someone outside the team will rely on it. |
| 2 Pre-launch | Release readiness, security and recovery. | Protected main, CI with tests for critical paths, automated deployment, backups with a tested restore, error tracking, a rollback plan. | SLOs, on-call duty, load tests unless a peak is known. | Real users depend on it. |
| 3 Early production | Reliable releases and steady maintenance. | Dependency update cadence, alerts with owners, a short incident procedure, bug triage. | Formal change control, multi-region setups. | Team or traffic grows and coordination starts to hurt. |
| 4 Growing product or team | Coordination, ownership, predictable releases. | Code owners, merge queues, broader test coverage, SLOs, on-call duty, onboarding documentation. | Dedicated platform and reliability teams. | Failures become expensive enough to fund dedicated reliability work. |
| 5 Mature or high-scale | Reliability, security, compliance and efficiency where justified. | Error budgets, progressive delivery, disaster recovery drills, independent security review. | Nothing that the risks justify. | The product winds down; moving down a stage is legitimate. |

A small or low-risk project never has to reach Stage 5. The risk profile sets the floor at every stage: a High-risk product needs its security and recovery safeguards even as a Stage 2 project.

## What to establish early and what can wait

Establish early, because each is cheap now and expensive later:
- Version control with a protected main branch from the first day.
- CI that builds and runs whatever tests exist.
- Secrets kept out of the repository from the first commit.
- Backups that have been restored at least once.
- A migration tool from the first database table.
- Automated dependency updates in small, regular batches.
- A license decision before anyone else contributes, for public code.
- Structured logging and error tracking with request identifiers.
- Data choices that are hard to reverse: UTC timestamps, stable identifiers, a tenant identifier on every row in multi-tenant systems.
- A README and a short record of decisions.

Can safely wait:
- Microservices, Kubernetes, service meshes and multiple regions, until a measured need appears.
- A shared staging environment, while preview deployments and integration tests give enough confidence.
- SLO tooling, canary analysis and error budgets, until traffic is large enough to measure.
- Large end-to-end suites; a few tests on critical journeys give most of the value.
- Performance tuning, until measurements show where time goes.
- Change boards, release managers and compliance programs, until a regulator, a contract or the organization's size requires them.

## When to classify again

Re-run the classification when the project gains money movement, personal or regulated data, a new kind of client (a mobile app, a partner API consumer), a new team, a contractual availability commitment, or a jump in traffic. Each of these can change the family, the risk profile or the stage, and with them the right workflow.
