# Testing and quality gates

## Contents
- How to choose tests
- Test types
- Specialized tests by family
- Gate matrix: what blocks what
- Coverage, flaky tests and test debt
- What can be introduced later

## How to choose tests

Start from the failures that would hurt this project most, and make sure each has at least one automated test or check that would catch it. A test portfolio built this way is smaller and more useful than one built to fill a pyramid or hit a coverage number. A successful build only proves the code compiles; it says nothing about whether checkout, sign-up or data loads work.

For each recommended test, say what failure it catches, when it runs, and what it costs to maintain.

## Test types

| Type | Catches | Typically runs | Essential when |
|---|---|---|---|
| Static checks (format, lint, types) | Whole classes of mistakes, cheaply | Every pull request | Always |
| Unit tests | Logic errors in business rules, pricing, parsing, state machines | Every pull request | Any non-trivial logic |
| Integration tests against real dependencies | Query, constraint, transaction, migration and serialization bugs | Every pull request (database in a container) | Any database or queue; do not mock the database |
| Contract or schema tests | Breaking changes for API consumers | Every pull request | APIs with consumers you do not deploy |
| End-to-end tests | Broken critical journeys across the whole stack | On merge or before release; a few on pull requests | Sign-up, login, checkout, the core task; keep the set small |
| Authorization and tenant-isolation tests | Users or tenants reaching data they should not | Every pull request | Any multi-role or multi-tenant system |
| Migration tests | Migrations that fail, lock tables or break the running version | Every pull request that touches the schema | Any database |
| Accessibility checks | Missing labels, contrast, keyboard traps | Every pull request (automated part) | Public websites and apps; automated checks catch only part of the issues |
| Visual regression | Unintended layout changes | Pull requests touching UI, when there is a design system | Many templates or a shared component library |
| Performance and load tests | Slow pages, capacity limits | Scheduled, and before known peaks | Traffic peaks, SLOs, high-traffic systems |
| Security tests (dependency audit, secret scan, static analysis, authorization tests, periodic review) | Known vulnerable packages, leaked secrets, injection, access control flaws | Pull requests and scheduled | Always for scanning; deeper testing at High risk |
| Smoke tests after deploy | A deploy that is up but broken | After every deployment | Always for deployed software |

## Specialized tests by family

- **AI applications**: an evaluation suite on a golden dataset with thresholds for quality, cost and latency, compared with the current baseline; an adversarial set for prompt injection and unsafe output; a held-out part of the dataset not used during prompt tuning; provider failure tests (timeouts, rate limits, malformed output). Run evaluations on any change to prompts, models, retrieval or tools. LLM-as-judge scoring helps at scale but needs spot checks by people.
- **Machine learning**: data validation on training inputs, reproducible training, evaluation against thresholds and against the current model including key segments, training-serving skew checks.
- **Data pipelines**: data tests for uniqueness, not-null, accepted values and relationships; freshness checks on sources; unit tests for complex transformations; CI that builds changed models and their downstream models in a temporary schema; reconciliation for financial figures.
- **Libraries, SDKs, CLIs**: a compatibility matrix across supported runtime versions and operating systems; public API and type checks; a packaging test that installs the built artifact in a clean environment.
- **Mobile and desktop**: UI tests on critical flows, a device and operating system matrix, upgrade tests from the previous release including local data migration.
- **Real-time**: protocol tests, reconnection and resume tests, conflict-resolution tests (property-based for merge logic), connection load tests. Wait for explicit conditions instead of fixed sleeps.
- **Distributed systems**: idempotent-consumer tests with duplicated and reordered messages, event schema compatibility, resilience tests for dependency failures.
- **IoT**: simulation, hardware-in-the-loop on each supported hardware revision, over-the-air update and rollback including interrupted updates.

## Gate matrix: what blocks what

| Check | Blocks merge | Blocks release | Scheduled, alerts an owner |
|---|---|---|---|
| Build, lint, types | Yes | | |
| Unit and integration tests | Yes | | |
| Contract or breaking-change check | Yes, once outside consumers exist | | |
| Secret scanning | Yes | | Yes, for history |
| Dependency review of new packages | Yes at Moderate risk and above | | |
| Dependency vulnerability scan | | High risk: critical findings | Yes, with a named triager |
| Evaluation suite (AI) | Yes, for prompt, model or retrieval changes | Yes | Yes, against drift |
| Data tests | Yes, for changed models | Yes, in production runs | Yes |
| End-to-end on critical journeys | A small set | Yes | Full suite nightly |
| Load tests | | Before known peaks | Periodic |
| Smoke test after deploy | | Triggers rollback or alert | |

A check that blocks nothing must have an owner who reads its results on a schedule; otherwise remove it.

## Coverage, flaky tests and test debt

- Use coverage to find untested risky code, not as a target. A floor on critical modules (billing, authorization) can be reasonable.
- Quarantine a flaky test immediately, give it an owner and a deadline, then fix or delete it. Retrying flaky tests until they pass teaches the team to ignore red builds.
- Add a test with every bug fix where practical, so the same failure cannot return silently.

## What can be introduced later

Large end-to-end suites, visual regression, load testing outside known peaks, mutation testing, chaos experiments and formal performance budgets can wait until a signal appears: repeated regressions in one area, a design system, a traffic peak, an SLO, or an incident the existing tests would not have caught.
