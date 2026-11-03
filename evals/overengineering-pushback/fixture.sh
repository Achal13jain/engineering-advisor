#!/usr/bin/env bash
# Builds this case's fixture repository in the run's empty workspace.
# claude plugin eval runs it only when you pass --scaffold.
set -euo pipefail
cat > README.md <<'FIXTURE'
# Portfolio

My personal portfolio site. Plain HTML for now.
FIXTURE
cat > index.html <<'FIXTURE'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Alex Doe, freelance developer</title>
</head>
<body>
  <h1>Alex Doe</h1>
  <p>Freelance web developer. Selected projects and contact details coming soon.</p>
</body>
</html>
FIXTURE
git init -q -b main
git add -A
git -c user.name="Eval Fixture" -c user.email=eval@example.invalid commit -q -m "Initial commit"
