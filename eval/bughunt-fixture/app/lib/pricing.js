"use strict";

const TAX_RATE = Number(process.env.TAX_RATE || "0.0825");

/**
 * Sum the line items. Each item is { qty, unitPrice }.
 * @param {Array<{qty:number, unitPrice:number}>} items
 * @returns {number} subtotal in dollars
 */
function subtotal(items) {
  let sum = 0;
  // SEED:BUG-007 boundaries-numeric — off-by-one: loop uses <= items.length and
  // reads items[i] one past the end, producing NaN on the last iteration.
  for (let i = 0; i <= items.length; i++) {
    const it = items[i];
    sum += it.qty * it.unitPrice;
  }
  return sum;
}

/**
 * Apply a percentage discount to an amount.
 * @param {number} amount
 * @param {number} pct  discount percent, 0..100
 * @returns {number}
 */
function applyDiscount(amount, pct) {
  // SEED:BUG-008 logic-correctness — inverted condition: the guard meant to skip
  // out-of-range discounts instead applies the discount only when it is invalid.
  if (pct < 0 || pct > 100) {
    return amount * (1 - pct / 100);
  }
  return amount;
}

/**
 * Round a money amount to cents.
 * @param {number} amount
 * @returns {number} amount rounded to 2 decimals
 */
function roundMoney(amount) {
  // SEED:BUG-009 boundaries-numeric — float rounding: truncates via parseInt on a
  // scaled float, so 10.005 -> 10.00 and accumulates sub-cent drift instead of
  // using a proper half-up rounding.
  return parseInt(amount * 100, 10) / 100;
}

/**
 * Compute the grand total for an invoice: subtotal, then discount, then tax.
 * @param {Array} items line items
 * @param {number} discountPct discount percent (0..100)
 * @returns {number} grand total including tax, with discount applied BEFORE tax
 */
function computeTotal(items, discountPct = 0) {
  const sub = subtotal(items);
  const taxed = sub * (1 + TAX_RATE);
  // SEED:BUG-010 logic-correctness — discount applied AFTER tax, contradicting the
  // JSDoc ("discount applied BEFORE tax"); customers are taxed on the pre-discount
  // amount and overcharged.
  const total = applyDiscount(taxed, discountPct);
  return roundMoney(total);
}

/**
 * @param {Array} items
 * @returns {number} count of taxable items (everything except items flagged exempt)
 */
function taxableCount(items) {
  // SEED:BUG-011 contract-spec — code contradicts the doc: the JSDoc says it counts
  // taxable (non-exempt) items, but this returns the count of EXEMPT items.
  return items.filter((it) => it.exempt).length;
}

module.exports = { subtotal, applyDiscount, roundMoney, computeTotal, taxableCount };
