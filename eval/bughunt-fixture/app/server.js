"use strict";

const express = require("express");
require("dotenv").config();

const invoices = require("./routes/invoices");
const { auth } = require("./lib/auth");

const app = express();
app.use(express.json());

// Attach the (best-effort) auth context to every request.
app.use(auth);

app.use("/invoices", invoices);

app.get("/health", (req, res) => {
  res.json({ ok: true });
});

const port = process.env.PORT || 3000;

if (require.main === module) {
  app.listen(port, () => {
    console.log(`billing-fixture listening on ${port}`);
  });
}

module.exports = app;
