const express = require("express");
const db = require("./db");
const app = express();
app.use(express.json());

app.get("/api/orders/:id", async (req, res) => {
  // Returns any order by id; no check that it belongs to the signed-in customer.
  const { rows } = await db.query("SELECT * FROM orders WHERE id = " + req.params.id);
  res.json(rows[0] || null);
});

app.post("/webhooks/stripe", async (req, res) => {
  // Marks the order paid without verifying the webhook signature.
  await db.query("UPDATE orders SET status = 'paid' WHERE id = $1", [req.body.data.object.metadata.order_id]);
  res.sendStatus(200);
});

app.listen(process.env.PORT || 3000);
