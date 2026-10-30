# Changelog

All notable changes to this project are recorded here. Versions follow semantic versioning: a major version for changes that alter the skill's stance or remove guidance, a minor version for new guidance or families, and a patch version for corrections.

## 0.1.0 - not yet released

- First public version. `SKILL.md` classifies a project by family, risk profile, maturity stage and release channel, then recommends proportionate practices and a phased plan.
- Eight reference files cover classification, fourteen project families, Git and releases, testing and quality gates, CI/CD and environments, security and maintenance, repository audits and worked examples.
- Packaged as a Claude Code plugin with its own marketplace, and installable with the skills CLI, by copying the folder, or as a ZIP for claude.ai. The README and home page also give install steps for Codex, Gemini CLI and GitHub Copilot CLI.
- Ten evaluation scenarios with two fixture repositories, and a structural check script that runs in CI.
- A one-page home page in `docs/index.html` for GitHub Pages, with light and dark themes, an interactive diagram that walks through the three worked examples, and copyable install commands and prompts. It loads nothing from other sites; its IBM Plex fonts are hosted in `docs/fonts/` under the SIL Open Font License.
