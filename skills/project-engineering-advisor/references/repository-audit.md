# Repository audit

## Contents
- Read-only inspection
- What files signal
- Classification evidence
- Audit checklist with severity
- Anti-patterns to detect
- Gap report format

## Read-only inspection

Inspect before recommending, and change nothing during an audit. Useful commands:

```bash
git status --short          # uncommitted work: never discard it
git branch -a               # permanent branches and naming
git log --oneline -20       # commit style, release tags, activity
git tag --sort=-creatordate | head
git ls-files | head -200    # what is tracked
```

Do not print remote URLs or files that may contain credentials. If a tracked file looks like it holds secrets (for example `.env`, `*.pem`, `credentials.json`), report the path only, never the contents, and recommend rotation.

Repository settings such as branch protection, rulesets and environment reviewers are not visible in the files. Ask the user, or read them with an authenticated, read-only call such as `gh api repos/OWNER/REPO/rulesets` only if the user allows it.

## What files signal

| Look for | Tells you |
|---|---|
| `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Cargo.toml`, `Gemfile`, `composer.json` and their lockfiles | Stack, scripts, whether builds are reproducible |
| `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml` | Existing CI, which checks run, triggers, permissions, deployment steps |
| `vercel.json`, `netlify.toml`, `Dockerfile`, `docker-compose.yml`, `fly.toml`, `render.yaml`, `serverless.yml`, Kubernetes manifests, Terraform, Pulumi or CDK code | Hosting and deployment model, infrastructure as code |
| Test folders, test scripts, `playwright.config.*`, `cypress.config.*`, coverage configuration | Test portfolio and gaps |
| Linter, formatter and type-checker configuration, `pre-commit` | Automated quality checks |
| `.github/dependabot.yml`, `renovate.json` | Dependency update automation |
| `README`, `CONTRIBUTING`, `CODEOWNERS`, `SECURITY.md`, `LICENSE`, `CHANGELOG`, decision records | Documentation, ownership, support policy |
| Migration folders (for example `prisma/migrations`, `alembic`, `db/migrate`, `drizzle`) | Schema change discipline |
| `.env.example` versus tracked `.env` files, `.gitignore` | Configuration and secret handling |
| Prompt files, evaluation datasets, model identifiers in configuration | AI evaluation discipline |
| `dbt_project.yml`, orchestration DAGs | Data pipeline practices |

## Classification evidence

Let the code confirm or correct the user's description:
- Payment SDKs or webhook handlers suggest money movement: High risk.
- Authentication libraries, user tables or session handling suggest accounts and personal data: at least Moderate.
- A tenant or organization identifier on most tables suggests multi-tenant SaaS.
- AI provider SDKs or prompt files mean the AI playbook applies to that part.
- A static export setting, no server routes and no database suggest a static site.
- Store build configuration, signing setup or firmware toolchains point to installed-software release channels.

## Audit checklist with severity

Rate each finding: **Blocker** (fix before launch or now, real current risk), **Important** (fix soon), **Improvement** (when a signal appears). Severity depends on the risk profile and stage; a missing restore test is a Blocker for a High-risk app in production and an Improvement for a prototype.

- **Repository**: README explains run, test and deploy; lockfile committed; one command builds from a clean checkout; secrets not tracked; example environment file lists required variables; license for public code.
- **Git**: main protected with pull requests and required checks; no permanent branches without purpose; no environment branches; short-lived branches; conventions for commits and tags where releases are versioned.
- **Testing**: tests exist for the failures that would hurt most; integration tests use a real database; authorization and tenant isolation tested where relevant; family-specific checks present; flaky tests handled.
- **CI/CD**: CI runs on every pull request and is required; least-privilege workflow permissions; deployment automated and repeatable; artifact built once and promoted; failed deploys detected; actions pinned and kept updated.
- **Environments**: each environment has a purpose and an owner; configuration separated from code; migrations backward compatible; rollback rehearsed.
- **Security**: dependency and secret scanning on with an owner; input validation and rate limiting at public entry points; personal data inventory and retention.
- **Recovery and operations**: backups for all irreplaceable data with a tested restore; error tracking, logs and uptime checks; alerts routed to a person; a written incident procedure.
- **Maintenance**: dependency updates automated; runtime and framework end-of-support dates known; owners for systems and external accounts; triage cadence.

## Anti-patterns to detect

| Signal in the repository | Anti-pattern | Better alternative |
|---|---|---|
| `develop`, `staging`, `testing` branches each deployed to an environment | Branches used as environments | Build once from main and promote |
| `develop` plus `release/*` and `hotfix/*` on a continuously deployed web app | GitFlow where a simpler flow fits | GitHub Flow |
| Branches months old with large diffs | Long-lived feature branches | Small merges behind flags |
| CI that only builds, or no CI | A green build treated as correctness | Tests for the riskiest failures, required on pull requests |
| Many CI jobs, none required, red runs ignored | Expensive pipeline without gates | Fewer jobs that each block something or have an owner |
| Retries on failing tests, skipped tests | Flaky tests left in place | Quarantine with an owner and a deadline |
| Deploy steps in a README run from a laptop | Manual deployment that depends on one person | Automated, documented pipeline |
| Schema changes edited in place, no migrations folder | No migration or rollback plan | Migration tool with expand and contract |
| Scanner configured, findings never triaged | Security tool without an owner | Named owner and cadence |
| Many services for one small team | Microservices too early | Modular monolith |
| Feature flags older than a year in code | Flags never removed | Expiry dates and removal tasks |

## Gap report format

```markdown
## Classification
Family, risk profile, stage, release channel, with the evidence found.

## What is already good
Practices that fit and should be kept.

## Gaps
| Severity | Area | Finding (with file path) | Why it matters | Recommended fix | Effort |

## Plan
Essential now, Next, Later (with the trigger for each Later item).

## Not verified
Settings or behavior that could not be checked from the repository.
```
