# Git workflows and releases

## Contents
- Branches, environments and release channels
- Choosing a workflow
- Default rules for main
- How the workflow changes with team size
- Hotfixes
- Release branches and maintenance branches
- Commits, tags, versions and changelogs
- Anti-patterns to flag
- Sources

## Branches, environments and release channels

Keep three ideas separate, because mixing them is the most common workflow mistake:

- A **branch** is a line of development in Git.
- An **environment** is a running deployment with its own configuration, secrets and data: local, preview, staging, production.
- A **release channel** is how users receive a version: a web deploy, a store track, a registry tag, a firmware cohort.

Environments receive builds from `main` by promotion, not by merging between branches. A permanent `develop`, `testing` or `staging` branch that mirrors an environment creates separate builds and diverging histories, so production runs code that was never tested in that exact form. Release channels for installed software are the one place where extra branches pay off, and those branches follow versions, not environments.

## Choosing a workflow

| Workflow | How it works | Fits | Costs |
|---|---|---|---|
| GitHub Flow (default) | Create a branch, commit, open a pull request, get review and checks, merge to `main`, delete the branch. `main` is always deployable. | Most web apps, APIs, SaaS, internal tools, data projects, solo developers and small teams. | Needs CI and a way to keep unfinished work hidden (small slices or flags). |
| Trunk-based development | Everyone merges small changes into `main` at least daily; branches live hours; unfinished work sits behind feature flags. | Teams that deploy many times a day, distributed systems, larger teams with strong CI. | Requires fast, trusted tests, flag discipline and a habit of small changes. |
| Release branches on top of either | Cut `release/x.y` from `main` to stabilize and patch a shipped version; tag each shipped build. | Mobile and desktop apps, firmware, self-hosted products, libraries that support old majors. | Fixes must be carried to every live branch; keep the number of live branches small. |
| GitFlow | Permanent `develop` and `main`, plus feature, release and hotfix branches. | Scheduled, versioned releases with several supported versions at once. | Slow integration, merge overhead and environment confusion. Its author recommends a simpler workflow such as GitHub Flow for software delivered continuously. |

Recommend GitHub Flow unless a specific condition in this table applies, and name that condition when recommending anything else.

## Default rules for main

Set these through branch protection or rulesets on GitHub (or the equivalent elsewhere). On GitHub, rulesets and classic branch protection rules can coexist; when several rules apply, the most restrictive wins. Describe the settings; do not change repository settings without explicit authorization.

| Setting | Low risk, solo | Moderate | High or Critical |
|---|---|---|---|
| Changes only through pull requests | Yes, even when self-merging, so checks run | Yes | Yes |
| Required approvals | 0 | 1 | 1 to 2, plus code owners for sensitive paths |
| Required status checks | Build, lint | Build, lint, unit and integration tests, family checks | All of those plus security checks the team triages |
| Block force pushes and deletion of main | Yes | Yes | Yes |
| Dismiss stale approvals on new commits | Optional | Recommended | Yes |
| Require branches to be up to date, or a merge queue | No | When main breaks often | Merge queue when many merges a day |

Pitfall worth checking: on GitHub, a required check from a workflow that was skipped by path or branch filtering stays pending and blocks the merge, while a job skipped by an `if` condition reports success. Require only checks that always run, or gate inside the job.

Branch names that read well: `feat/short-description`, `fix/issue-123-short-description`, `chore/upgrade-node`, `docs/...`, `release/2.4`, `hotfix/2.4.1`. Keep pull requests small enough to review in one sitting, and keep branches to days, not weeks.

## How the workflow changes with team size

| Team | Reviews | Ownership | Integration |
|---|---|---|---|
| 1 developer | Pull requests with self-review so checks run; optional reviewer for risky changes | README and decision notes | Merge when green |
| 2 to 5 | One approval; pull request template | Shared ownership, named owner per system | Small pull requests, daily merges |
| 6 to 15 | One approval plus code owners for sensitive areas | CODEOWNERS file, on-call rotation if users depend on it | Merge queue if main breaks; feature flags; move toward trunk-based development |
| More than 15 or several teams | Code owners per module or service | Team ownership per module; service catalog | Trunk-based with flags; split repositories or services only along real team boundaries |

Growing the team changes reviews and ownership first. It does not by itself justify GitFlow, extra permanent branches or microservices.

## Hotfixes

- **Web and server software**: branch from `main` (or from the deployed tag if `main` contains unreleased work behind no flag), fix, run the normal checks, merge and deploy like any change. If the issue is severe, first mitigate with a flag or a rollback, then fix calmly.
- **Released software with a release branch**: either fix on `main` and cherry-pick to `release/x.y`, or fix on the release branch and merge it back. Choose one convention and use it consistently, so no fix is lost in the next version. Tag and ship the patch version.
- Record each hotfix in the changelog or release notes, and consider whether a test would have caught it.

## Release branches and maintenance branches

- Cut a release branch only when a version must be frozen while `main` moves on: store submissions, firmware lines, self-hosted products, or libraries with a supported previous major.
- Allow only fixes on a release branch, never features.
- Delete or archive the branch when that version is no longer supported, and publish the support window.
- For libraries, a maintenance branch such as `2.x` exists only while you publicly promise fixes for that major.

## Commits, tags, versions and changelogs

- Conventional Commits 1.0.0: `type(scope): description`. A `fix` maps to a patch release, a `feat` to a minor release, and `!` after the type or a `BREAKING CHANGE:` footer to a major release. Useful when releases are generated from history; optional for small web projects.
- Semantic Versioning 2.0.0 for anything others install or depend on: MAJOR for incompatible API changes, MINOR for backward-compatible functionality, PATCH for backward-compatible fixes. Before 1.0.0 the public API is not considered stable.
- Web applications can identify releases by commit or deployment identifier; semantic versions are optional there.
- Tag shipped versions on the exact commit that was built: `git tag -a v2.4.1 -m "v2.4.1"` then push the tag.
- Keep a changelog for humans, with an Unreleased section at the top and entries grouped as Added, Changed, Deprecated, Removed, Fixed and Security. Release tooling such as release-please or Changesets can generate it; check each tool's current documentation before configuring it.

## Anti-patterns to flag

| Anti-pattern | Better alternative | Exception |
|---|---|---|
| GitFlow where a simpler flow would do | GitHub Flow with a protected main | Several supported versions on a schedule |
| Permanent branches per environment | Build once, promote one artifact | Rarely any |
| Permanent branches without a written purpose | Each extra branch has a purpose, owner and end | Maintenance branches for supported versions |
| Long-lived feature branches | Small merges behind feature flags | Throwaway experiments |
| Direct pushes to main | Pull requests with required checks | A documented emergency, reviewed afterwards |

## Sources

Checked 27 October 2026. Recheck before relying on tool behavior.
- GitHub flow: https://docs.github.com/en/get-started/using-github/github-flow
- GitHub rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Required checks and skipped workflows: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks
- GitFlow author's note: https://nvie.com/posts/a-successful-git-branching-model/
- Trunk-based development: https://trunkbaseddevelopment.com/
- Conventional Commits: https://www.conventionalcommits.org/en/v1.0.0/
- Semantic Versioning: https://semver.org/
- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
