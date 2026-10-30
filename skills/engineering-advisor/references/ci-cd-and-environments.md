# CI/CD, environments and deployment

## Contents
- Integration, delivery and deployment
- Pipeline stages
- CI security
- Keeping CI fast and cheap
- Writing CI configuration
- Environments
- Configuration and secrets
- Database migrations
- Feature flags
- Rollout strategies
- Detecting failure and rolling back
- Sources

## Integration, delivery and deployment

- **Continuous integration**: everyone merges into the shared mainline at least daily, and each merge is verified by an automated build and tests.
- **Continuous delivery**: every change that passes the pipeline could be released at any time.
- **Continuous deployment**: every change that passes is released automatically.

Recommend continuous deployment when tests are trusted, rollback is fast and a bad deploy is cheap. Recommend a manual approval before production when releases cannot be recalled, involve outside parties or carry regulatory obligations.

## Pipeline stages

| When | What runs | Blocks |
|---|---|---|
| Every pull request | Build, lint, types, unit and integration tests, secret scanning, dependency review, family checks (breaking-change check, evaluations, data tests on changed models). Preview deployment for web projects. | The merge |
| Merge to main | Build the release artifact once, deploy to the first environment, smoke test. | Promotion |
| Before production | Smoke tests on staging where staging exists; manual approval only at High risk or for releases that cannot be recalled. | The release |
| After deployment | Health check or smoke test against production; watch error rates for a short period; automatic rollback where the platform supports it. | Nothing; it alerts or rolls back |
| On a schedule | Vulnerability scans, link checks, long end-to-end or load suites, certificate and domain expiry checks, evaluation drift. Each has a named reader. | Nothing; it alerts |

For released software (stores, registries, firmware), "deploy" becomes "build, sign, publish to a test track or pre-release tag, then promote".

## CI security

- Give each workflow the least permissions it needs. On GitHub Actions, set a restrictive top-level `permissions:` block (for example `contents: read`) and widen it only in the job that needs more.
- Scope deployment credentials to the environment they deploy to. Prefer short-lived credentials through OpenID Connect over long-lived cloud keys stored as secrets.
- GitHub recommends pinning third-party actions to a full commit SHA, because tags can be moved. At minimum pin to a major version and keep actions updated with automated dependency updates.
- Avoid `pull_request_target` for untrusted code, and pass untrusted input such as pull request titles through environment variables rather than inline expressions.
- Never print secrets in logs. Secrets for production should be unreachable from pull request workflows from forks.
- On GitHub, environments can require reviewers before a job that targets them runs. On the Free, Pro and Team plans this protection is available only for public repositories, so check the plan before recommending it for a private repository.

## Keeping CI fast and cheap

- Keep the pull request pipeline fast enough that people wait for it rather than work around it. Move slow suites to merge or a schedule.
- Cancel superseded runs for the same branch (on GitHub Actions, a `concurrency` group with `cancel-in-progress: true`).
- Cache dependency downloads; build once and reuse the artifact across jobs.
- Path filters save minutes, but a required check from a workflow skipped by a path filter stays pending on GitHub. Filter inside jobs, or do not require that workflow.
- Every job either blocks something or has an owner. Remove jobs that do neither.

## Writing CI configuration

1. Read the existing workflows, package manifests, lockfiles and scripts first. Match the package manager, runtime version and commands the project already uses.
2. Look up the current major version of every action you use before writing it, for example with `gh api repos/actions/checkout/releases/latest --jq .tag_name` or the action's releases page. Do not write versions from memory. If you cannot check, mark the version as unverified in your answer.
3. Use the runtime version the project and its host already use (for example the `engines` field, `.nvmrc`, `.python-version` or the hosting platform's setting). Check the runtime's release schedule before recommending an upgrade.
4. Explain each job in one line, mark placeholders in capitals, and state assumptions.
5. Validate the syntax where a tool is available, and say plainly if you could not run the workflow.

Skeleton for a Node.js web application (illustrative; replace `vN` with the verified current major, or a full commit SHA):

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@vN
      - uses: actions/setup-node@vN
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
      - run: npm run build
```

Add a database service container for integration tests, a breaking-change check for APIs, or an evaluation job for AI changes, depending on the family.

## Environments

| Environment | Purpose | Typically needed by |
|---|---|---|
| Local | Fast development with a reproducible setup | Every project |
| Preview | One short-lived deployment per pull request for review by people and automated checks | Web projects of every risk level |
| Integration | A shared place where several services or teams meet | APIs and distributed systems with several teams |
| Staging | Production-like configuration, integrations and data shape, for the final check of the exact build | Moderate projects when previews fall short; High and Critical projects |
| Production | Real users and data, with its own secrets and access | Every project |

Justify staging by a concrete need: production-like integrations, data volume, configuration that previews cannot reproduce, or a release that cannot be recalled. Give a shared staging environment a named owner, or it drifts and becomes untrusted.

## Configuration and secrets

- Build once and promote the same artifact; only configuration differs between environments.
- Read environment-specific configuration at runtime or inject it at deploy time. Values baked in at build time (common for static sites and frontend bundles) must never contain secrets, because they ship to every visitor.
- Secrets differ per environment, live in the platform's secret store, and are listed (names only) in an example environment file in the repository.
- Rotate any secret that was ever committed, even after removing it, because it remains in Git history.

## Database migrations

- Make every migration backward compatible with the version currently running, so the previous version still works if you roll back.
- For breaking changes, use expand and contract: add the new structure, write to both, backfill, move reads, and remove the old structure in a later release. Only the last step is irreversible.
- Run migrations as a separate, observable deploy step before the new code, not as a side effect of application start-up on many instances.
- Test migrations against a production-like copy of the schema; watch for long locks on large tables.
- Take or confirm a recent backup before an irreversible migration.

## Feature flags

- Use release flags to separate deploying code from releasing a feature, and to turn a feature off without a deploy.
- Give every release flag an owner and an expiry date, and remove it once the feature is fully released. Permanent operational kill switches are the exception.
- Do not use flags to maintain per-customer versions of the product.

## Rollout strategies

| Strategy | What it does | Justified when |
|---|---|---|
| Atomic deploy with instant rollback | Host switches traffic to the new build and can switch back | Static and simple web apps |
| Rolling deploy | Replace instances gradually | Most server applications |
| Blue-green | Run old and new side by side and switch traffic at once | Fast full rollback is needed and running two copies is affordable |
| Canary | Send a small share of traffic to the new version and compare metrics | Enough traffic to measure, High risk or critical paths |
| Flag-based progressive release | Enable a feature for growing groups of users | Risky features in any family, including AI prompt changes |
| Staged store rollout | Release to a growing percentage of users and halt on crashes | Mobile apps |
| Staged fleet cohorts | Update devices in waves and halt on telemetry | Firmware |

Do not recommend blue-green, canary analysis or service meshes for a small, low-traffic project; atomic deploys with rollback and good smoke tests cover it.

## Detecting failure and rolling back

- Detect: smoke test or health check after each deploy, error-rate and latency alerts, and for released software crash rates per version.
- Undo with the cheapest safe option: turn off the flag, then redeploy the previous artifact, then roll forward with a small fix.
- Roll back when the previous version is still compatible with the data and the fix is not obvious. Roll forward when a migration has already changed data in a way the previous version cannot handle and the fix is small and understood.
- Rehearse a rollback at least once before launch, and write the steps down.

## Sources

Checked 27 October 2026. Recheck before relying on tool behavior.
- Continuous integration: https://martinfowler.com/articles/continuousIntegration.html
- Continuous delivery: https://martinfowler.com/bliki/ContinuousDelivery.html
- GitHub Actions secure use (SHA pinning, token permissions): https://docs.github.com/en/actions/reference/security/secure-use
- GitHub OpenID Connect: https://docs.github.com/en/actions/concepts/security/openid-connect
- GitHub environments and plan limits: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- Required checks and skipped workflows: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks
- Parallel change (expand and contract): https://martinfowler.com/bliki/ParallelChange.html
- Feature toggles: https://martinfowler.com/articles/feature-toggles.html
