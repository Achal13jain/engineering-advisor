#!/usr/bin/env bash
# Builds this case's fixture repository in the run's empty workspace.
# claude plugin eval runs it only when you pass --scaffold.
set -euo pipefail
mkdir -p .github/workflows db src test
cat > README.md <<'FIXTURE'
# Orders portal

Customer portal for viewing orders and paying invoices. In production since March; about 400 business customers.

## Deploy

1. SSH into the production server.
2. `git pull` on the `production` branch.
3. Run any new SQL from `db/schema.sql` by hand.
4. `pm2 restart orders`.

Only Ravi knows the server password.
FIXTURE
cat > .env <<'FIXTURE'
DATABASE_URL=postgres://orders:FAKE-PASSWORD-FOR-EVAL-ONLY@db.example.internal:5432/orders
STRIPE_SECRET_KEY=fake-stripe-secret-for-eval-only-not-a-real-key
FIXTURE
cat > .github/workflows/ci.yml <<'FIXTURE'
name: build
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm run build
FIXTURE
cat > db/schema.sql <<'FIXTURE'
CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, total_cents INT, status TEXT);
ALTER TABLE orders ADD COLUMN paid_at TIMESTAMP;
FIXTURE
cat > package.json <<'FIXTURE'
{
  "name": "orders-portal",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "node src/server.js",
    "build": "node -e \"console.log('nothing to build')\"",
    "test": "node --test test/"
  },
  "dependencies": {
    "express": "^4.19.2",
    "pg": "^8.11.3",
    "stripe": "^14.0.0"
  }
}
FIXTURE
cat > src/db.js <<'FIXTURE'
const { Pool } = require("pg");
module.exports = new Pool({ connectionString: process.env.DATABASE_URL });
FIXTURE
cat > src/server.js <<'FIXTURE'
const express = require("express");
const db = require("./db");
const app = express();
app.use(express.json());

app.get("/api/orders/:id", async (req, res) => {
  const { rows } = await db.query("SELECT * FROM orders WHERE id = " + req.params.id);
  res.json(rows[0] || null);
});

app.post("/webhooks/stripe", async (req, res) => {
  await db.query("UPDATE orders SET status = 'paid', paid_at = now() WHERE id = $1", [req.body.data.object.metadata.order_id]);
  res.sendStatus(200);
});

app.listen(process.env.PORT || 3000);
FIXTURE
cat > test/smoke.test.js <<'FIXTURE'
const test = require("node:test");
const assert = require("node:assert");
test("arithmetic still works", () => assert.strictEqual(1 + 1, 2));
FIXTURE
git init -q -b main
git add -A
git -c user.name="Eval Fixture" -c user.email=eval@example.invalid commit -q -m "Initial commit"
git branch production
