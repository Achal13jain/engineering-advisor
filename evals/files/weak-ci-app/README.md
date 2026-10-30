# Orders portal

Customer portal for viewing orders and paying invoices. In production since March; about 400 business customers.

## Deploy

1. SSH into the production server.
2. `git pull` on the `production` branch.
3. Run any new SQL from `db/schema.sql` by hand.
4. `pm2 restart orders`.

Only Ravi knows the server password.
