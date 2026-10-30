-- Applied by hand on the server. Edited in place when the schema changes.
CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, total_cents INT, status TEXT);
