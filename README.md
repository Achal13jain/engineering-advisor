# Engineering Advisor

**Home page:** [engineering-advisor.pages.dev](https://engineering-advisor.pages.dev/)

Get an engineering plan that fits the project you actually have. This open skill classifies a project by family, risk, maturity, and release style, then recommends practical engineering steps without adding process for its own sake.

![Project flow: understand the project, size the safeguards, and build a phased plan](docs/readme-flow.svg)

## What it does

- Inspects an available repository read-only before making recommendations.
- Classifies the project and explains the decisions that matter.
- Builds a plan for what to do now, next, and later.
- Keeps the security floor tied to real risk, even for a small project.

It covers architecture, Git workflow, testing, CI/CD, environments, deployment, rollback, security, and maintenance. It also explains when practices such as GitFlow, staging branches, microservices, or Kubernetes are unnecessary.

## Install

In Claude Code, use either the plugin or a copied skill folder, not both, or the skill is listed twice.

### Claude Code

Add the repository marketplace and install the plugin:

```text
/plugin marketplace add Achal13jain/engineering-advisor
/plugin install engineering-advisor@engineering-advisor
```

Invoke it directly with `/engineering-advisor:engineering-advisor`, or ask Claude Code an engineering workflow question. To use a copied folder instead, put `skills/engineering-advisor` in `~/.claude/skills/` for all your projects, or in a repository's `.claude/skills/`.

### Codex

In the Codex CLI, add the repository as a plugin marketplace:

```bash
codex plugin marketplace add Achal13jain/engineering-advisor
```

Then enter `/plugins` in Codex, install Engineering Advisor from that marketplace, and start a new session. Plugins are not available in the Codex IDE extension; there, copy the skill folder instead. Codex reads personal skills from `~/.agents/skills` and a repository's skills from `.agents/skills`:

```bash
git clone https://github.com/Achal13jain/engineering-advisor.git
mkdir -p ~/.agents/skills
cp -r engineering-advisor/skills/engineering-advisor ~/.agents/skills/
```

Mention it with `$engineering-advisor`, or run `/skills` to pick it. Gemini CLI and Copilot CLI also read `~/.agents/skills`, so this one copy works in all three.

### Skills CLI

One command installs the skill into the agents you choose, including Claude Code, Codex, Gemini CLI and GitHub Copilot:

```bash
npx skills add Achal13jain/engineering-advisor
```

Choose agents with `-a`, for example `-a codex`, and add `-g` to install it for all your projects.

### Gemini CLI

```bash
gemini skills install https://github.com/Achal13jain/engineering-advisor.git --path skills/engineering-advisor
```

Add `--scope workspace` to install it for the current project only, and enter `/skills reload` in a running session.

### GitHub Copilot CLI

Copilot CLI reads personal skills from `~/.copilot/skills` and a repository's skills from `.github/skills`:

```bash
git clone https://github.com/Achal13jain/engineering-advisor.git
mkdir -p ~/.copilot/skills
cp -r engineering-advisor/skills/engineering-advisor ~/.copilot/skills/
```

Enter `/skills reload`, then check it with `/skills list`.

### claude.ai and the Claude API

Download `engineering-advisor.zip` from the [latest release](https://github.com/Achal13jain/engineering-advisor/releases/latest) and upload it in claude.ai as a custom skill. To check the download, compare it with the `SHA256SUMS` file attached to the same release: run `sha256sum -c SHA256SUMS` on Linux or in Git Bash, `shasum -a 256 -c SHA256SUMS` on macOS, or `Get-FileHash engineering-advisor.zip -Algorithm SHA256` in PowerShell and compare the result by eye. For the Claude API, upload the skill folder through the Skills API. Skills there run without network access, so the skill marks any tool versions it cannot check as unverified.

## Try it

- “Do I need a develop or staging branch for this project?”
- “Review this repository and identify the most important gaps before launch. Do not change anything.”
- “We are adding payments to our SaaS. What safeguards should be in place before release?”

## Project contents

- `skills/engineering-advisor/` is the portable skill.
- `.claude-plugin/` contains the Claude Code plugin and marketplace manifests, and `plugin.json` with `.agents/plugins/marketplace.json` make the repository a Codex plugin and marketplace.
- `docs/` contains the project home page and its local assets.
- `evals/` contains twenty-one evaluation cases for `claude plugin eval`.
- `tools/check_skill.py` runs the structural checks in CI, and `tools/check_sources.py` reports monthly on the official pages listed in `tools/verified_sources.json`.

## Evaluation

Version 0.2.0 is an early release. A first, small evaluation is published in [EVALUATION.md](EVALUATION.md): in four scenarios run once each, answers with the skill met 35 of 36 expectations and answers without it 31 of 36, which is too few runs to prove a difference. The repository now has twenty-one cases for Claude Code's built-in eval runner, covering all fourteen project families; the full suite has not been run yet. The skill has been used in Claude Code only so far.

## Safety

The skill inspects repositories read-only by default. It does not discard work, run destructive Git commands, or change repository, deployment, or production settings without explicit approval. It is an advisor, not a security auditor or a source of legal or compliance advice.

## Privacy

The skill is Markdown only: instructions and reference files, with no scripts. It collects nothing and sends nothing anywhere by itself. What you share while using it goes to the AI tool you use it in, under that tool's terms. When it checks a fact about a third-party tool, it asks your AI tool to open that provider's public documentation. The home page loads nothing from other sites and uses no analytics scripts; it remembers your light or dark choice in your browser.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) to report advice problems or propose changes. Report security issues privately as described in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE). Created and maintained by [Achal Jain](https://github.com/Achal13jain).
