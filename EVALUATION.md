# Evaluation

This page records what has been measured about the skill so far, how it was measured, and what has not been measured yet. The numbers are small and early. They are published so that anyone can judge the evidence for themselves.

## How the skill is evaluated

The suite in `evals/` runs with Claude Code's built-in runner, `claude plugin eval` (documented at https://code.claude.com/docs/en/plugin-evals, read on 3 November 2026). Each case is a realistic request with pass or fail graders:

- **Twenty-one cases.** One planning case for each of the fourteen project families, three repository audits (a weak repository, a healthy one that should produce few findings, and one with instructions aimed at AI assistants hidden in its files), and cases for pushing back on too much process, asking questions when information is missing, safer deployments and refusing destructive Git commands.
- **Graders.** Most graders are concrete PASS and FAIL rubrics scored by a judge model, which votes three times per grader. Some are exact checks: that secret values from a fixture never appear in the answer, that a short question gets a short answer, that no destructive Git command was run, and that uncommitted work still exists after the run.
- **A baseline.** Every case also runs without the plugin, so the report shows what the skill adds over the same model on its own. The runner gives each run a fresh, empty configuration, so personal instructions, other plugins and memory do not affect either side.
- **Fixtures.** Cases that need a repository build a small fake one in the run's empty workspace with a setup script. The agent cannot read the eval folder, so it never sees the expected answers.
- **Labels count less.** Graders that only check a label, such as naming the risk profile, have half weight, because they partly reward the skill's own vocabulary. Graders that check decisions and safeguards have full weight.

## Results so far

### Smoke run of the new suite, 3 November 2026

One case, `overengineering-pushback`, one run with the skill and one without, Claude Code 2.1.286, the default judge. This run was made to check that the suite works. It used the skill text of version 0.2.0.

| | Score | Notes |
|---|---|---|
| With the skill | 1.00 | Recommended main with short-lived branches and preview deployments, explained that branches are not environments, gave the answer in its first sentences, and stayed under 5,000 characters. |
| Without the skill | 0.71 | Also pushed back and stayed short, but did not explain the difference between branches and environments and did not open with the recommendation. |

The two runs cost $0.24 in total. One run per side is not enough to show a reliable difference.

### First manual evaluation, 28 October 2026

Before the runner was adopted, four of the original ten scenarios were run by hand, once with the skill and once without, with Claude Opus 5.5.

| Scenario | With the skill | Without the skill |
|---|---|---|
| Static site launch | 9 of 9 | 6 of 9 |
| SaaS with sign-in, PostgreSQL and subscriptions | 9 of 9 | 8 of 9 |
| Audit of a weak repository | 11 of 11 | 10 of 11 |
| Pushing back on GitFlow for a portfolio site | 6 of 7 | 7 of 7 |
| **Total** | **35 of 36 (97 percent)** | **31 of 36 (86 percent)** |

What these numbers show and what they do not:

- Four of the five expectations the baseline missed were about naming the project family or the risk profile, which partly rewards the skill's vocabulary. The fifth was substantive: the baseline never said whether the static site needed a develop or staging branch. Claude without the skill already gave strong practical advice in all four scenarios.
- The skill's one miss was a real weakness. It answered the simple GitFlow question at 1,506 words against 952 without it, because it applied its full report template to a small, low-risk request. Version 0.2.0 tells the skill to answer narrow questions briefly, and the smoke run above passed the new length check.
- Both sides ran with the maintainer's personal Claude Code instructions loaded, the grading was done by the same model rather than by an independent judge, and each scenario ran once. Treat these results as a first signal, not a measurement.

## Not measured yet

- The full suite of twenty-one cases has not been run. Results will be added here with the date, the Claude Code version, the model, the number of runs and the cost.
- The skill has not been tested in Codex, Gemini CLI, GitHub Copilot CLI, claude.ai or through the Claude API, although the install steps for them were checked against their official documentation.
- Whether the facts in the reference files are still current is checked monthly by `tools/check_sources.py`, which reports pages that no longer load and entries not reread for six months. It cannot tell whether a page still says the same thing; a person rereads flagged pages.

## Run it yourself

The steps are in [CONTRIBUTING.md](CONTRIBUTING.md#evaluations). Each run calls a model on your own account and costs money, so start with one case or one run per case.
