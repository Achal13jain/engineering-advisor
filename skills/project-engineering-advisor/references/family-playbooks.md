# Family playbooks

Defaults for a typical project of each family in early production (Stage 3). Move up or down with the risk profile and the stage. Use the family section for specifics, and the dimension reference files for how to implement them.

## Contents
- Defaults at a glance
- Static and content websites
- Dynamic and full-stack web applications (including PWAs)
- SaaS, multi-tenant platforms and marketplaces
- E-commerce and transactional platforms
- Internal tools and admin dashboards
- Real-time and collaborative applications
- APIs, backend services and monoliths
- Distributed, event-driven, serverless and high-traffic systems
- AI-powered applications (LLMs, RAG, agents)
- Machine learning systems
- Data pipelines and analytics
- Mobile and desktop applications
- Libraries, SDKs, CLIs and open source
- IoT and hardware-integrated software

## Defaults at a glance

| Family | Usual risk | Git workflow | Branches beyond main | Environments | Deploy frequency |
|---|---|---|---|---|---|
| Static and content websites | Low (Moderate with forms or CMS) | GitHub Flow | None | Local, preview, production | On demand |
| Dynamic and full-stack web | Moderate | GitHub Flow | None | Local, preview, production; staging when needed | Daily to weekly |
| SaaS and marketplaces | High | GitHub Flow, trunk-based as team grows | None | Local, preview, staging, production | Daily |
| E-commerce and transactional | High | GitHub Flow, freezes at peaks | None | Local, preview, staging, production (sandbox payments outside prod) | Weekly to daily |
| Internal tools | Moderate | GitHub Flow, light review | None | Local, preview or staging with synthetic data, production | On demand |
| Real-time and collaborative | Moderate | GitHub Flow | None | Staging with at least two connection servers | Weekly |
| APIs, backends, monoliths | Moderate to High | GitHub Flow, contract changed with code | Release branches only for self-hosted products | Local, preview or integration, staging, production | Daily |
| Distributed and high-traffic | High | Trunk-based or GitHub Flow per service | None | Ephemeral per service, integration, staging, production with canary | Many times a day |
| AI-powered applications | Moderate to High | GitHub Flow; prompts, model ids and eval sets in the repo | None | Local, preview, staging, production with flags | Code daily; prompt and model changes gated by evaluations |
| Machine learning systems | Moderate to High | GitHub Flow for code; data and models versioned outside Git | None | Development, staging with shadow traffic, production with canary | Models on a schedule or when evaluation passes |
| Data pipelines and analytics | Moderate (High with personal or financial reporting) | GitHub Flow | None; environments are schemas | Developer schemas, CI schema per pull request, production | Daily |
| Mobile and desktop | Moderate | GitHub Flow plus short-lived release branch per version | Release branch per version | Internal tracks, beta, staged production rollout | Weekly to monthly |
| Libraries, SDKs, CLIs | Moderate (supply chain) | GitHub Flow with tags | Maintenance branches only for supported old majors | CI only, pre-releases on the registry | On demand |
| IoT and hardware | High to Critical | GitHub Flow plus release branch per firmware line | Release branch per supported firmware line | Dev boards, lab rack, test fleet, staged fleet cohorts | Monthly or slower for firmware |

## Static and content websites

- **Examples and traits**: brand sites, landing pages, portfolios, blogs, documentation, headless-CMS marketing sites. Pages built at build time or cached; no accounts; failures are visible to the first visitor.
- **Before launch**: a clean build, an internal link check, automated accessibility and SEO checks, and a review of the preview deployment on real devices.
- **Essentials**: a static host or CDN that builds from Git, deploys on merge to main and offers instant rollback. Preview deployments per pull request do the job a staging environment would do. Document and own the domain, DNS and certificate renewal. Send form submissions somewhere monitored, protect forms from spam, and say where personal data from forms goes. For a self-hosted CMS such as WordPress, patch plugins on a schedule and back up content.
- **Watch out**: neglect, such as an expired domain, an unpatched CMS plugin, a broken form nobody noticed, or a framework upgrade postponed until it becomes a rewrite.
- **Usually unnecessary**: permanent develop or staging branches, a separate staging environment, GitFlow, end-to-end suites beyond a smoke check, Kubernetes, multiple approvals for a solo maintainer.
- **Add process when**: the site gains accounts or server workflows (it becomes a full-stack app); it becomes a measurable revenue source (make a performance budget blocking, add real-user monitoring); a design system grows (visual regression tests); many editors need approvals (use CMS roles, not more Git process). A client who wants to review batches of changes can use a temporary review deployment, not a permanent branch.

## Dynamic and full-stack web applications

- **Examples and traits**: booking apps, customer portals, community sites, project trackers, installable PWAs. A database, sessions, server code per request, background jobs, schema changes that outlive one deploy.
- **Before launch**: unit tests for business logic, integration tests against a real database of the same engine and version as production, end-to-end tests of the critical journeys, and migration tests.
- **Essentials**: authentication from a proven library or provider, never custom crypto. Migrations backward compatible with the running version and run as a separate deploy step. Database backups with a tested restore. Error tracking and structured logs. For PWAs, a service worker update strategy so users do not stay on stale code.
- **Watch out**: postponed database changes and dependency upgrades; mocked databases that hide real query bugs; a service worker that serves stale code.
- **Usually unnecessary**: microservices, a permanent staging branch, multi-region deployment, canary analysis at low traffic.
- **Add process when**: previews cannot reproduce production data shape or integrations (add a staging environment); several developers break main often (merge queue, code owners); customers depend on it during business hours (SLOs and on-call); a predictable traffic peak is coming (load test).

## SaaS, multi-tenant platforms and marketplaces

- **Examples and traits**: B2B products, HR platforms, analytics services with workspaces, two-sided marketplaces. Tenants, roles within tenants, subscriptions, shared infrastructure, contractual expectations.
- **Before launch**: everything for full-stack apps, plus tenant-isolation tests that prove one customer cannot see another's data, an authorization matrix per role, and billing webhook tests.
- **Essentials**: a tenant identifier on every row and every query (row-level security is one option); audit logs; one version for all tenants released with feature flags; staging with production-like configuration and third-party sandboxes; data export and deletion paths; subscriptions through a billing provider with verified webhooks; point-in-time recovery. Marketplaces add trust and safety, payouts through a provider built for split payments, and fraud monitoring.
- **Watch out**: per-customer special cases in branches, flags or configuration that turn one product into many.
- **Usually unnecessary**: per-customer branches or deployments, microservices before team boundaries exist, a silo per tenant by default (start pooled, silo only the customers or components that need it).
- **Add process when**: enterprise customers ask for single sign-on, provisioning and audit export; one tenant is far larger or more regulated than the rest; releases keep causing incidents (progressive delivery); teams block each other's releases.

## E-commerce and transactional platforms

- **Examples and traits**: online shops, ticketing, digital downloads, B2B ordering. Orders with a lifecycle, payments through a provider, contested inventory, refunds, taxes, seasonal peaks.
- **Before launch**: pricing and order-state unit tests, payment flows in the provider's sandbox, webhook and idempotency tests, an inventory concurrency test, and a load test before the first peak.
- **Essentials**: keep card data out of your systems with the provider's hosted fields or redirect, which reduces payment card compliance scope (confirm obligations with the provider or an assessor). Idempotency keys on every money-moving call; verify webhook signatures and deduplicate events; model orders as a state machine; reconcile your records with the provider regularly. Sandbox keys everywhere except production. A change freeze around peak trading.
- **Watch out**: drift between your order records and the provider's records, discovered only when money is missing. Do not test with real cards in live mode.
- **Usually unnecessary**: building payment processing yourself, storing card numbers, microservices for a single shop.
- **Add process when**: minutes of downtime become costly (SLOs, on-call, canary for checkout); new countries bring tax, currency and residency work; marketplace payouts appear; peaks keep causing incidents (formal readiness review before each).

## Internal tools and admin dashboards

- **Examples and traits**: support consoles, back-office order tools, approval workflows, operations dashboards, data correction tools. Known users behind single sign-on, few concurrent users, workflows that change often, direct reach into production data.
- **Before launch**: unit tests on business rules, authorization tests for each role, and a smoke test of the main workflows.
- **Essentials**: single sign-on from the organization's identity provider (OIDC or SAML); least-privilege roles; an audit log of every change; writes through the product's service API rather than directly into the production database; a named owner and a second person who understands it.
- **Watch out**: a tool one person built, only that person understands, and everyone depends on. Admin tools with broad production write access.
- **Usually unnecessary**: heavy release ceremony, staging plus preview plus QA environments, high test coverage targets for simple screens.
- **Add process when**: the tool carries revenue-critical or legal processes (full-stack app practices); outside partners get access (it becomes a product); many internal tools exist (a shared platform with common authentication and audit).

## Real-time and collaborative applications

- **Examples and traits**: chat and support widgets, live dashboards, notification feeds, delivery tracking, shared documents and whiteboards. Server push, long-lived connections, per-channel ordering, presence, concurrent edits.
- **Before launch**: unit tests on message handling and merge logic, protocol and integration tests, reconnection and conflict-resolution tests, and one realistic connection load test.
- **Essentials**: store messages with sequence numbers before publishing so clients resume after reconnecting; fan out through a pub/sub layer once there is more than one connection server; drain connections gradually during deploys; version the protocol; choose WebSockets, server-sent events or polling by need, not fashion. For collaborative editing, use an established CRDT or operational transformation library.
- **Watch out**: reconnection storms during deploys, protocol drift between old and new clients, tests that rely on fixed sleeps.
- **Usually unnecessary**: a custom sync algorithm, real-time where polling every few seconds would do.
- **Add process when**: a second connection server appears; collaborative editing is added (property-based merge tests); mobile or desktop clients join (protocol negotiation, minimum version); messages carry money or regulated data (risk becomes High).

## APIs, backend services and monoliths

- **Examples and traits**: backends for web and mobile apps, public or partner APIs, internal platform services, GraphQL layers, modular monoliths. A published contract, consumers with different release cadences, data ownership, authorization at every endpoint.
- **Before launch**: unit tests, integration tests against a real database, response validation against the contract, a breaking-change check on the API description, and object-level authorization tests.
- **Essentials**: change the contract (for example an OpenAPI document) in the same pull request as the code; never break consumers silently: add, deprecate with notice, measure usage, then remove; consistent error format; rate limiting; one image built once and promoted. Keep a modular monolith with enforced module boundaries until a module needs a different scaling profile, release cadence or failure isolation.
- **Watch out**: accidental breaking changes; mocked databases; old endpoints that somebody still calls; mobile clients that never update.
- **Usually unnecessary**: microservices for one team; URL versioning for every small additive change; GitFlow.
- **Add process when**: a consumer you do not deploy (mobile app, partner) appears (breaking-change check becomes blocking, deprecation policy, usage by version); several teams own consumers (consumer-driven contract tests); customers self-host (release branches and a support policy).

## Distributed, event-driven, serverless and high-traffic systems

- **Examples and traits**: services owned by separate teams, queues and workers, media processing, webhook ingestion, event-triggered functions, cache-heavy high-traffic sites. Partial failure, at-least-once delivery, independent deploys, horizontal scaling.
- **Before launch**: unit and integration tests per service, idempotent-consumer tests, event schema compatibility checks, and load and resilience tests.
- **Essentials**: assume duplicates and out-of-order messages; make consumers idempotent; use a transactional outbox when a change must also publish an event; dead-letter queues with an owner; distributed tracing with context in every message; SLOs with error budgets; canary releases for critical paths; respect serverless timeouts and cold starts as documented by the provider.
- **Watch out**: hidden coupling through shared databases and event schemas; observability gaps; dead-letter queues nobody watches.
- **Usually unnecessary**: microservices without team or scaling boundaries; a service mesh for a handful of services; Kubernetes when a managed platform suffices.
- **Add process when**: several teams deploy into one system (service catalog, contract tests); incidents take long to locate (tracing everywhere); a peak approaches the last load test. Also remove process: merge services that always deploy together; drop queues that carry a handful of messages a day.

## AI-powered applications (LLMs, RAG, agents)

- **Examples and traits**: support assistants over company documents, extraction and classification, writing features, internal copilots, agents that act on records. Non-deterministic outputs, an external model dependency, cost per request, prompts that behave like code.
- **Before launch**: deterministic tests of the surrounding code, an evaluation suite on a golden dataset with thresholds (plus a held-out part not used for prompt tuning), prompt-injection and safety tests, and provider failure tests.
- **Essentials**: version prompts, model identifiers, retrieval settings and evaluation sets in the repository; route every model call through one gateway with timeouts, retries, fallback, rate limits and a cost budget; release prompt and model changes behind flags to a small group first; log a trace per answer (prompt version, model, retrieved sources, tokens, cost, latency); give agents least-privilege tools and human approval for actions with real effects. Use the current OWASP Top 10 for LLM Applications as the threat checklist. Check provider retention, region and deprecation terms on the provider's current pages; never state them from memory.
- **Watch out**: silent quality regressions when a prompt, model or index changes; prompts tuned to pass the golden set; model retirements on the provider's schedule; unbounded cost.
- **Usually unnecessary**: training or fine-tuning before prompting and retrieval are exhausted; a vector database when a few documents fit in context; agent autonomy where a fixed workflow works.
- **Add process when**: the feature takes actions with real effects (adversarial tests, approvals); the domain is regulated or advice is relied on (documented risk assessment, human oversight); AI spend becomes noticeable (per-feature budgets, cost in release criteria); you start training models (machine learning practices).

## Machine learning systems

- **Examples and traits**: ranking, fraud scoring, forecasting, churn prediction, classifiers, fine-tuned models. Code, data and model as separate versioned artifacts; retraining as routine; offline and online metrics that disagree; training-serving skew.
- **Before launch**: data validation, a reproducible training run, evaluation against thresholds and against the current model (overall and per important segment), and serving tests with a skew check.
- **Essentials**: data and model versions with immutable identifiers; experiment tracking; a model registry so promotion and rollback are pointer changes; shadow deployment before canary; drift and data-quality monitoring; a list of who consumes the predictions.
- **Watch out**: silent degradation through drift; undeclared consumers; hidden data dependencies.
- **Usually unnecessary**: a feature store or full pipeline automation for one model retrained rarely.
- **Add process when**: predictions decide outcomes that affect people (per-segment evaluation, human approval, model cards); manual retraining leaves models stale (automate the training pipeline); several models share features (shared feature package or store).

## Data pipelines and analytics

- **Examples and traits**: warehouse loads, SQL transformation layers, finance dashboards, near-real-time metrics. Inputs you do not control, scheduled runs, decisions made on the results, failures that are often silent.
- **Before launch**: data tests for keys and required fields, freshness checks on sources, unit tests for complex transformations, and CI that builds only the changed models in a temporary schema.
- **Essentials**: idempotent, re-runnable jobs; environments as schemas or databases, not branches; raw data kept unchanged so results can be rebuilt; one owner per model and per alert; documented metric definitions; personal data governed by purpose and retention.
- **Watch out**: silent quality decay from upstream changes; unowned models; alert noise that people learn to ignore.
- **Usually unnecessary**: streaming when daily batches meet the decision need; a separate staging warehouse when CI schemas suffice.
- **Add process when**: stakeholders find data problems before your alerts do (volume checks, reconciliation); other teams build on your tables (contracts, deprecation policy); figures reach regulators or leave the company (staging run with sign-off, reconciliation, retained evidence).

## Mobile and desktop applications

- **Examples and traits**: consumer iOS and Android apps, field-service apps with offline storage, cross-platform desktop tools. Signed binaries, store review or notarization, slow adoption of new versions, local data that must survive upgrades.
- **Before launch**: unit tests, UI tests on critical flows, a device and operating system matrix, and upgrade tests from the previous released version including local data migration.
- **Essentials**: a short-lived release branch per version cut from main; every shipped build tagged; internal and beta testing tracks; staged rollouts that can be halted; signing keys in CI secrets with restricted access; crash reporting; remote feature flags; a minimum supported version enforced by the API. Fixes go to main and are cherry-picked to the release branch, or are made on the release branch and merged back.
- **Watch out**: old versions that never update; yearly platform and store changes that break builds or eligibility; shipping code outside the store review in ways the store rules forbid.
- **Usually unnecessary**: GitFlow with a permanent develop branch; long-lived release branches after the version stops shipping.
- **Add process when**: releases slip for one unfinished feature (fixed release train with flags); many versions are in use (per-version API contract tests); several teams work in the app (feature modules, code owners, release captain rotation).

## Libraries, SDKs, CLIs and open source

- **Examples and traits**: packages on public registries, SDKs for an API, developer CLIs, framework plugins. A public API, versioned releases instead of deployments, users on many versions, outside contributors.
- **Before launch**: unit tests, a compatibility matrix across supported runtimes and operating systems, a public API or type check, and a packaging test that installs the built package.
- **Essentials**: semantic versioning (incompatible changes raise the major, compatible features the minor, fixes the patch); a human-readable changelog; Conventional Commits or changesets to drive releases; publishing from CI only, with trusted publishing and provenance where the registry supports it; LICENSE, README, CONTRIBUTING and SECURITY files; issue forms; a written support and deprecation policy.
- **Watch out**: maintainer burnout; an unclear support policy that leaves users on unpatched versions; breaking changes in minor releases.
- **Usually unnecessary**: preview deployments, staging environments, GitFlow.
- **Add process when**: large organizations depend on you (signed releases, provenance, security policy); breaking changes slip through (public API report in CI); several packages release together (monorepo with a release tool).

## IoT and hardware-integrated software

- **Examples and traits**: connected thermostats with apps, industrial sensors, gateways, configuration tools for hardware. Firmware, backend and app released separately; offline, constrained, long-lived devices; physical consequences.
- **Before launch**: unit tests of device logic, simulation, hardware-in-the-loop tests, and over-the-air update and rollback tests including power loss during update.
- **Essentials**: a compatibility matrix between firmware, backend and app versions; signed firmware with protected signing keys; unique per-device credentials; A/B partitions so a failed update reverts by itself; staged fleet rollouts that halt on telemetry; a release branch per supported firmware line; field telemetry and remote diagnostics. Check applicable security baselines and regulation with current official sources.
- **Watch out**: supporting old hardware and firmware for years, including patches for components no longer made.
- **Usually unnecessary**: continuous deployment of firmware; one release cadence for firmware, backend and app.
- **Add process when**: the fleet outgrows manual watching (automated rollout gates); several hardware revisions exist (a test rack per revision); the product can cause harm (safety and regulatory specialists).
