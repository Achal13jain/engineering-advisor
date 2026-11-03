#!/usr/bin/env bash
# Builds this case's fixture repository in the run's empty workspace.
# claude plugin eval runs it only when you pass --scaffold.
set -euo pipefail
mkdir -p .github/workflows spec src
cat > README.md <<'FIXTURE'
# tiny-slug

Turns any string into a URL-safe slug. Zero dependencies.

```bash
npm install tiny-slug
```

```ts
import { slugify } from "tiny-slug";
slugify("Hello, World!"); // "hello-world"
```

## Development

`npm ci`, then `npm test` and `npm run lint`. Releases are published from CI when a version tag is pushed; see CONTRIBUTING.md.
FIXTURE
cat > LICENSE <<'FIXTURE'
MIT License

Copyright (c) 2026 Sam Rivera

Permission is hereby granted, free of charge, to any person obtaining a copy of this software, to deal in the software without restriction.
FIXTURE
cat > CHANGELOG.md <<'FIXTURE'
# Changelog

## 2.1.0

- Add the `separator` option.

## 2.0.0

- Drop support for Node.js versions that have reached end of life.
FIXTURE
cat > CONTRIBUTING.md <<'FIXTURE'
# Contributing

Open an issue before large changes. Run `npm test` and `npm run lint` before opening a pull request, and add a line to CHANGELOG.md.

Releases: the maintainer bumps the version, updates CHANGELOG.md, and pushes a `vX.Y.Z` tag. The release workflow publishes to npm with provenance.
FIXTURE
cat > SECURITY.md <<'FIXTURE'
# Security

Report vulnerabilities privately through GitHub's private vulnerability reporting on this repository.
FIXTURE
cat > package.json <<'FIXTURE'
{
  "name": "tiny-slug",
  "version": "2.1.0",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "lint": "eslint ."
  },
  "devDependencies": {
    "eslint": "^9.0.0",
    "typescript": "^5.6.0",
    "vitest": "^3.0.0"
  }
}
FIXTURE
cat > package-lock.json <<'FIXTURE'
{
  "name": "tiny-slug",
  "version": "2.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {}
}
FIXTURE
cat > tsconfig.json <<'FIXTURE'
{ "compilerOptions": { "outDir": "dist", "declaration": true, "strict": true, "target": "ES2022", "module": "ES2022" }, "include": ["src"] }
FIXTURE
cat > vitest.config.ts <<'FIXTURE'
import { defineConfig } from "vitest/config";
export default defineConfig({ test: { include: ["spec/**/*.spec.ts"] } });
FIXTURE
cat > eslint.config.js <<'FIXTURE'
export default [{ files: ["src/**/*.ts"], rules: {} }];
FIXTURE
cat > renovate.json <<'FIXTURE'
{
  "extends": ["config:recommended"],
  "schedule": ["before 6am on monday"]
}
FIXTURE
cat > src/index.ts <<'FIXTURE'
export interface Options { separator?: string }

export function slugify(input: string, options: Options = {}): string {
  const sep = options.separator ?? "-";
  return input
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, sep)
    .replace(new RegExp(`^${sep}|${sep}$`, "g"), "");
}
FIXTURE
cat > spec/slugify.spec.ts <<'FIXTURE'
import { describe, expect, it } from "vitest";
import { slugify } from "../src/index";

describe("slugify", () => {
  it("lowercases and joins words", () => expect(slugify("Hello, World!")).toBe("hello-world"));
  it("strips accents", () => expect(slugify("Crème brûlée")).toBe("creme-brulee"));
  it("uses a custom separator", () => expect(slugify("a b", { separator: "_" })).toBe("a_b"));
  it("returns an empty string for symbols only", () => expect(slugify("!!!")).toBe(""));
});
FIXTURE
cat > .github/workflows/ci.yml <<'FIXTURE'
name: CI
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [20, 22, 24]
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
FIXTURE
cat > .github/workflows/release.yml <<'FIXTURE'
name: Release
on:
  push:
    tags: ["v*"]
permissions:
  contents: read
  id-token: write
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: npm
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: 24
          registry-url: https://registry.npmjs.org
      - run: npm ci
      - run: npm test
      - run: npm run build
      - run: npm publish --provenance --access public
FIXTURE
cat > .gitignore <<'FIXTURE'
node_modules/
dist/
FIXTURE
git init -q -b main
git add -A
git -c user.name="Eval Fixture" -c user.email=eval@example.invalid commit -q -m "Initial commit"
