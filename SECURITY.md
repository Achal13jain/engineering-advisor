# Security policy

This project is a set of instructions for an AI assistant. The skill itself contains no executable code, but its instructions can still cause harm if they are wrong. Examples of what counts as a security problem here:

- An instruction that could lead an assistant to run a destructive command, discard uncommitted work, or change repository, deployment or production settings without the user's explicit approval.
- An instruction that could make an assistant print, copy or commit a secret.
- A weakness that lets repository content, issue text or a fetched web page steer the skill against the user's interest (prompt injection).
- A real credential committed to this repository.

The evaluation fixture scripts in `evals/` (the `fixture.sh` files) contain deliberately fake secrets, such as the `.env` values in `audit-weak-ci-repo`. They exist to test that the skill reports secrets without repeating them, and they are not a vulnerability.

## Reporting a problem

Please do not open a public issue for a security problem. Report it privately through GitHub: open the repository's "Security and quality" tab and choose "Report a vulnerability". Include the prompt you used, what the assistant did, the surface you used (Claude Code, claude.ai, the API or another agent) and the version of the skill.

The maintainer will acknowledge the report, keep you informed while it is being fixed, and credit you in the changelog unless you prefer otherwise.

## Supported versions

Only the latest release receives fixes.
