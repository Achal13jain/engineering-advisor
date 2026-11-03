# Changelog

All notable changes to this project are recorded here. Versions follow semantic versioning: a major version for changes that alter the skill's stance or remove guidance, a minor version for new guidance or families, and a patch version for corrections.

## 0.2.0 - 2026-11-03

- Fix a contradiction in the risk profiles: Critical no longer includes "very high availability and traffic". Traffic and availability now count only through the damage a failure would cause, and each risk profile is recorded with the facts that set it and what would move it.
- Answer narrow questions briefly: the verdict first, the reason, the alternative and the signal that would change it, instead of the full report template. The first evaluation found a simple GitFlow question answered at 1,506 words against 952 without the skill.
- Audit findings now carry a confidence (Verified, Likely or Not verified), the evidence with file and line, and how to check the fix, and the audit guide explains how to rule out false alarms.
- Replace the ten skill-creator scenarios with twenty-one cases for `claude plugin eval`, with a no-plugin baseline, exact checks for secrets, answer length and destructive Git commands, and fixture scripts. New cases cover the nine families that had none, a healthy repository that should produce few findings, and a repository with instructions aimed at AI assistants hidden in its files.
- Publish the evaluation results so far, with their limits, in `EVALUATION.md`.
- Add `tools/check_sources.py` and a monthly Sources workflow that reports official pages that no longer load or have not been reread for six months.
- Bring the README up to the home page: install steps for Codex, Gemini CLI, GitHub Copilot CLI, claude.ai and the Claude API, and the evaluation status.
- Fix the home page heading left over from the old name, and link the evaluation from the page.
- Make the repository a Codex plugin and marketplace, with a root `plugin.json` in the Agent Plugins format and `.agents/plugins/marketplace.json`, so Codex CLI users can install it with `codex plugin marketplace add Achal13jain/engineering-advisor` and `/plugins`.
- Add an optional second check to repository audits: where the host can start a subagent with a fresh context, it rechecks every Blocker from the files alone before the report.
- Attach a `SHA256SUMS` file to each release so the claude.ai ZIP can be checked, and add a Privacy section to the README.

## 0.1.0 - 2026-10-30

- Add canonical site metadata, crawler directives, a sitemap and an `llms.txt` page for the Cloudflare Pages site.
- First public version. `SKILL.md` classifies a project by family, risk profile, maturity stage and release channel, then recommends proportionate practices and a phased plan.
- Eight reference files cover classification, fourteen project families, Git and releases, testing and quality gates, CI/CD and environments, security and maintenance, repository audits and worked examples.
- Packaged as a Claude Code plugin with its own marketplace, and installable with the skills CLI, by copying the folder, or as a ZIP for claude.ai. The README and home page also give install steps for Codex, Gemini CLI and GitHub Copilot CLI.
- Ten evaluation scenarios with two fixture repositories, and a structural check script that runs in CI.
- A one-page home page in `docs/index.html` for Cloudflare Pages, with light and dark themes, an interactive diagram that walks through the three worked examples, and copyable install commands and prompts. It loads nothing from other sites; its IBM Plex fonts are hosted in `docs/fonts/` under the SIL Open Font License.
