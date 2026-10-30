# Worked examples

These condensed examples show how much the advice should differ between projects. Use them to calibrate proportion, not as templates to copy.

## Contents
- Example 1: a static business website before launch
- Example 2: a new SaaS with authentication, PostgreSQL and subscriptions
- Example 3: a team growing from one developer to five

## Example 1: a static business website before launch

Request: "I'm launching a static Next.js website for a consulting company next month. Help me set up the repository and deployment workflow."

**Classification**: static and content website; Low risk (Moderate if the contact form stores personal data); Stage 2 pre-launch; web deploy that can be rolled back in minutes.

**Key decisions**
- GitHub Flow with only `main`. Pull requests run checks and produce a preview deployment; merging to `main` deploys production. A permanent `develop` or `staging` branch would add merges and drift without reducing any real risk, because the preview already shows the exact build.
- A Git-connected host with preview deployments and instant rollback; no separate staging environment.
- CI on pull requests: install, lint, type check, build, internal link check, automated accessibility check. Keep it under a few minutes.
- Protect `main`: pull requests required, the CI check required, force pushes blocked. No required approvals for a solo maintainer.

**Plan**
- Essential before launch: domain and DNS ownership documented with two people able to access the registrar; HTTPS confirmed; form submissions delivered to a monitored inbox with spam protection; privacy notice for form data; 404 page, titles and meta descriptions; one rehearsed rollback.
- Next: automated dependency updates monthly; uptime and certificate expiry monitoring.
- Later: performance budget as a blocking check if the site becomes a lead-generation channel; visual regression if a component library grows.

**What not to recommend**: GitFlow, a staging environment, Kubernetes, end-to-end suites beyond a smoke check, semantic versioning for releases.

## Example 2: a new SaaS with authentication, PostgreSQL and subscriptions

Request: "I'm starting a B2B SaaS with sign-in, a Postgres database and paid subscriptions. Design the engineering workflow before I start building."

**Classification**: SaaS and multi-tenant platform; High risk (business customer data, money through a billing provider); Stage 1 moving to Stage 2; web deploy.

**Key decisions**
- Modular monolith in one repository, with a tenant identifier on every table from the first migration. Splitting into services now would multiply operational work without a team boundary to justify it.
- GitHub Flow with one approval once a second developer joins; feature flags for unfinished work.
- Authentication from a proven provider or library; subscriptions through a billing provider, with webhook signature verification and idempotent handlers.
- A migration tool from the first table, with backward-compatible migrations and expand and contract for breaking changes.
- Environments: local, preview per pull request with seeded data, staging with production-like configuration and billing sandbox, production. Staging is justified here because billing and identity integrations cannot be fully reproduced in previews.

**Plan**
- Essential before the first paying customer: tenant-isolation tests and an authorization matrix in CI; integration tests against real Postgres; billing webhook tests; point-in-time recovery enabled and one restore tested; error tracking and uptime monitoring; audit log of administrative actions; secrets in the platform's store; a short incident procedure and a rehearsed rollback.
- Next: dependency updates with a named triager; data export and deletion paths; SLOs once customers depend on it during working hours.
- Later: canary releases, single sign-on for enterprise customers, silo deployment for a large or regulated tenant, each when its signal appears.

**What not to recommend**: microservices, Kubernetes, per-customer branches, a permanent staging branch, multi-region before customers or contracts require it.

## Example 3: a team growing from one developer to five

Request: "Our team is going from just me to five developers next quarter. How should branching, review and releases change?"

**Classification**: depends on the product; assume a full-stack web app at Moderate risk moving from Stage 3 to Stage 4.

**What changes**
- Reviews: one required approval on every pull request; a pull request template with testing notes; small pull requests reviewable in one sitting.
- Ownership: a CODEOWNERS file for sensitive areas such as billing and authentication; a named owner for CI, dependencies and each external account.
- Integration: keep GitHub Flow; add a merge queue only if `main` starts breaking from concurrent merges; use feature flags so unfinished work can merge early.
- Onboarding: README that gets a new developer to a running app and a passing test suite in a day; decision records for past choices.
- Operations: written deployment and rollback steps anyone can run; an on-call or incident rotation if users depend on the app during working hours.

**What does not change**: no GitFlow, no environment branches, no microservices. Growing from one to five developers changes reviews and ownership first, not the branching model.
