# Contributing

Thank you for helping improve the Project Engineering Advisor. The most useful contribution is a report of advice that was wrong, out of date or out of proportion for a real project, because the skill's whole purpose is to recommend the right amount of process.

## Reporting advice problems

Open an issue with the "Problem with the advice" form. Include the prompt you used, the kind of project (what it does, who uses it, whether it handles money or personal data, how it is released), what the skill recommended, and what you expected instead and why. A short excerpt of the answer is enough; do not paste secrets or private code.

For security problems, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Rules for changing the skill

The skill lives in `skills/project-engineering-advisor/`. These rules keep it accurate and usable on every surface that loads skills.

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

   If you have Claude Code installed, also run `claude plugin validate .` from the repository root.
4. If the change affects what the skill recommends, run the relevant evaluation scenarios (below) and mention the results in the pull request.
5. Open a pull request and fill in the template. CI runs the same check script.

## Evaluations

`evals/evals.json` holds ten scenarios in the format used by Anthropic's skill-creator plugin. Each has a prompt, the expected outcome and pass or fail expectations. Run each scenario twice, once with the skill and once without, so the results show what the skill adds.

Scenarios 6, 7 and 10 run against fixture repositories. Create a fresh copy for every run, outside this repository, and never point a run at a real repository:

```bash
python evals/setup_fixture.py evals/files/weak-ci-app RUN_DIR/repo              # scenario 6
python evals/setup_fixture.py evals/files/portfolio-site RUN_DIR/repo --main-only # scenario 7
python evals/setup_fixture.py evals/files/weak-ci-app RUN_DIR/repo --dirty      # scenario 10
```

Point with-skill runs at a copy of `skills/project-engineering-advisor/` rather than at this repository, so that the run cannot read the expected answers in `evals/`. When you report results, give the model, the date, and the number of runs.

## Releasing

These steps are for the maintainer.

1. Set the version in `.claude-plugin/plugin.json` and replace "not yet released" in the newest `CHANGELOG.md` heading with the release date. The check script fails if the two versions differ. Claude Code users receive an update only when this version changes.
2. Run `python tools/check_skill.py` and `claude plugin validate .`.
3. Build the ZIP for claude.ai, which has the skill folder at its root:

   ```bash
   python -m zipfile -c dist/project-engineering-advisor.zip skills/project-engineering-advisor
   ```

4. Tag the release as `vX.Y.Z`, push the tag, and create a GitHub release from it with the ZIP attached and the changelog entry as notes.

## License

By contributing, you agree that your contributions are licensed under the MIT License in [LICENSE](LICENSE).
