# Contributing

Thank you for helping improve the Engineering Advisor. The most useful contribution is a report of advice that was wrong, out of date or out of proportion for a real project, because the skill's whole purpose is to recommend the right amount of process.

## Reporting advice problems

Open an issue with the "Problem with the advice" form. Include the prompt you used, the kind of project (what it does, who uses it, whether it handles money or personal data, how it is released), what the skill recommended, and what you expected instead and why. A short excerpt of the answer is enough; do not paste secrets or private code.

For security problems, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Rules for changing the skill

The skill lives in `skills/engineering-advisor/`. These rules keep it accurate and usable on every surface that loads skills.

1. **Proportion first.** Process has a cost. New guidance should say which risk it reduces, what it costs, and when it is not needed. Size never lowers the security floor; money and sensitive data raise it.
2. **Verify facts about third-party tools at the source.** Anything about a provider's features, defaults, limits, retention, pricing or versions must come from the provider's current official page. Read the page, then add its URL to `tools/verified_sources.json` with the date you read it and a note of the exact fact. The check script fails on any URL in the references that is not in that file.
3. **No frozen versions.** Do not write action versions, runtime versions or other facts that go stale into the skill. The skill tells the assistant to look them up when it is used.
4. **Keep the structure.** `SKILL.md` stays under 500 lines. Reference files are linked directly from `SKILL.md` and never from each other. A reference file over 100 lines starts with a Contents section. Use forward slashes in paths.
5. **Keep the frontmatter portable.** `SKILL.md` has only `name` and `description`, because every surface accepts those two. The description stays under 1,024 characters, in the third person, and says what the skill does and when to use it.
6. **House style.** Write in full sentences and plain words. Do not use em dashes, en dashes or double hyphens in prose; the check script enforces this for Markdown files.

## Making a change

1. Fork the repository and create a short-lived branch from `main`.
2. Make the change, and add a line describing it to the newest entry in `CHANGELOG.md`. The maintainer sets the version number when releasing.
3. Run the checks. They need Python 3 and PyYAML (`pip install pyyaml`):

   ```bash
   python tools/check_skill.py
   ```

   If you have Claude Code installed, also run `claude plugin validate .` from the repository root. If you changed a source in `tools/verified_sources.json`, run `python tools/check_sources.py` too; it fetches every listed page and also runs monthly in the Sources workflow.
4. If the change affects what the skill recommends, run the relevant evaluation cases (below) and mention the results in the pull request.
5. Open a pull request and fill in the template. CI runs the same check script.

## Evaluations

`evals/` holds twenty-one cases for Claude Code's built-in eval runner, `claude plugin eval` (see https://code.claude.com/docs/en/plugin-evals; it needs Claude Code 2.1.269 or later). Each case folder has a `prompt.md` with the request and run limits, and a `graders/` folder with one file per check. Cases that need a repository also have a `case.yaml` and a `fixture.sh` that builds a small fake repository in the run's empty workspace. [EVALUATION.md](EVALUATION.md) explains the design and records the results.

Every run calls a model on your account and costs money. The runner runs each case three times with the plugin and three times without it unless you say otherwise, so start small. From the repository root:

```bash
# One case, one run on each side
claude plugin eval . --scaffold --no-publish --case overengineering-pushback --runs 1

# The twenty cases that need no shell, one run each, with a spending limit in US dollars
claude plugin eval . --scaffold --no-publish --runs 1 --max-cost-usd 20 --tag planning --tag audit --tag pushback --tag clarifying
```

- `--scaffold` lets the fixture scripts run. They only write files and Git state inside the run's temporary workspace, but they run as you, so read them first.
- `--no-publish` keeps the HTML report on your machine instead of publishing it to claude.ai.
- The case `protect-uncommitted-work` also needs `--allow-tools Bash`. The runner then confines shell commands to its sandbox, which needs macOS, Linux or WSL2; native Windows has no sandbox, so run that case from WSL2 there.
- Results are written to `evals/results/`, which Git ignores. Open the `report.html` in that folder for the scores with and without the skill.

When you report results in a pull request or in EVALUATION.md, give the date, the Claude Code version, the model, the number of runs and the cost.

## Releasing

These steps are for the maintainer.

1. Set the version in `.claude-plugin/plugin.json` and in the root `plugin.json` (the Codex manifest), and replace "not yet released" in the newest `CHANGELOG.md` heading with the release date. The check script fails if the versions differ. Claude Code users receive an update only when this version changes.
2. Run `python tools/check_skill.py` and `claude plugin validate .`.
3. Build the ZIP for claude.ai, which has the skill folder at its root, and a checksum file for it:

   ```bash
   python -m zipfile -c dist/engineering-advisor.zip skills/engineering-advisor
   python -c "import hashlib, pathlib; z = pathlib.Path('dist/engineering-advisor.zip'); pathlib.Path('dist/SHA256SUMS').write_text(hashlib.sha256(z.read_bytes()).hexdigest() + '  ' + z.name + '\n', newline='\n')"
   ```

4. Tag the release as `vX.Y.Z`, push the tag, and create a GitHub release from it with `engineering-advisor.zip` and `SHA256SUMS` attached and the changelog entry as notes.

## License

By contributing, you agree that your contributions are licensed under the MIT License in [LICENSE](LICENSE).
