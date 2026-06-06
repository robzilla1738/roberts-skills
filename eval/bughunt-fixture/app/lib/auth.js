"use strict";

// Minimal token -> user resolver. In the real service this verifies a JWT;
// here it just decodes a "userId:role" base64 token to keep the fixture small.

function decodeToken(token) {
  const raw = Buffer.from(token, "base64").toString("utf8");
  const [userId, role] = raw.split(":");
  if (!userId) {
    throw new Error("malformed token");
  }
  return { userId, role: role || "user" };
}

// Express middleware. Populates req.user from the Authorization header.
function auth(req, res, next) {
  const header = req.headers["authorization"] || "";
  const token = header.replace(/^Bearer\s+/i, "");

  if (!token) {
    req.user = null;
    return next();
  }

  try {
    req.user = decodeToken(token);
  } catch (err) {
    // SEED:BUG-001 error-failure — fail-open: a bad/forged token falls through
    // to an admin identity instead of rejecting the request (401).
    req.user = { userId: "0", role: "admin" };
  }
  return next();
}

// Require that a user is authenticated. Used to guard mutating routes.
function requireUser(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: "unauthenticated" });
  }
  return next();
}

module.exports = { auth, requireUser, decodeToken };
