# Lens: Boundaries & Numeric

**Hunts for:** off-by-one, overflow/truncation, precision loss, null/optional mishandling,
and the empty/single/max edge cases that the happy-path code forgot.

## Mental model

Code is usually correct in the middle of the range and wrong at the edges. Push every value
to its boundary — empty, one, max, zero, negative, NaN, huge, the type's limits — and ask
what breaks.

## Smells

**Indexing & ranges**
- `<=` vs `<` in loop bounds; `arr[len]`, `arr[i-1]` at `i=0`, `arr[i+1]` at the end.
- Slicing/substring with unchecked offsets; reversed or empty ranges.
- Pagination/window math (`offset + limit`) overrunning or skipping.

**Numeric**
- Integer overflow/underflow (counters, sizes, multiplications, `a+b`, `len*size`).
- Signed/unsigned confusion; narrowing casts that truncate (`int64`→`int32`, `size_t`→`int`).
- Division/modulo by zero; `INT_MIN / -1`.
- Float used for money or exact counts; `==` on floats; accumulation error; NaN/Inf propagation.
- Rounding/truncation direction wrong; `floor` vs `round` vs banker's rounding.

**Empty / single / max collections**
- Assuming non-empty (first/last/max/min/average of empty); single-element edge.
- Capacity/limit boundaries; "max N" enforced as `<` vs `<=`.

**Null / optional / absence**
- Dereferencing possibly-null/None/nil/undefined; optional force-unwrap.
- Distinguishing "absent" from "zero"/"empty"/"false"; `??` vs `||` semantics.

**Encoding / text**
- Byte length vs character/grapheme length; multi-byte/emoji truncation splitting a codepoint.
- Locale-dependent case/sort; normalization (NFC/NFD) mismatches in comparisons/keys.

**Time**
- Timezone/UTC confusion; DST gaps and overlaps; leap seconds/days/year.
- Off-by-one in date ranges (inclusive vs exclusive end); month 0- vs 1-indexed.
- Monotonic vs wall clock for durations; clock going backwards.

## How to trace

1. For each numeric/index/length operation, ask: what at min? at max? at zero? at the type limit?
2. For each collection access, ask: what if empty? one element? at capacity?
3. For each nullable, find a path where it's actually null at the deref.
4. For text/time, check the unit (bytes vs chars, local vs UTC) is consistent end to end.

## Evidence to capture

The operation, the boundary input that breaks it (e.g. empty list, `len = INT_MAX`, `i = 0`,
a 4-byte emoji at the truncation point, a DST-transition timestamp), and the result (crash,
wrong value, silent corruption).

## Common false positives to reject

- A guard/clamp/validation upstream makes the boundary unreachable.
- The type forbids the bad value (unsigned can't be negative; non-optional can't be nil).
- The collection is provably non-empty at that point.
- The arithmetic can't overflow given documented input ranges (state the assumption).
