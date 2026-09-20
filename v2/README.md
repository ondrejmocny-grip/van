# v2 — VW Crafter L3H3, 3-seat cab

Started 2026-09-20. **Schema only — iterating.** No 3D, no impressions yet.

![plan](layout.png)

Regenerate: `python plan.py v2` from the project root.

Brisa's layout ported to our van: shower in the front driver corner, galley split across the
aisle, rear U-dinette. See [ref/doracamper-brisa-ducato-l2h2](../ref/doracamper-brisa-ducato-l2h2/README.md).

## What changed from v1, and why

- **Base vehicle is the Crafter L3H3 only.** Ondrej has one in mind.
- **Three front seats** (driver + double bench), so **swivel seats are dropped**. They were
  never going to work against a 3-seat bench, and dropping them also removes the handbrake
  lowering kit and the "does the Crafter have an electronic parking brake" question.
- **Partition wall behind the cab at x = 0**, with a door on the passenger side into the
  entry. Both reference vans do this; it is what pays for the shower position.
- **Consequence: there is no front lounge.** All living moves to the rear U and the entry
  lobby. This contradicts [about-us.md](../doc/about-us.md) — *"live in the front lounge"* —
  and is the single thing to sanity-check before going further.
- **Three belted travelling seats** instead of two, which also makes the motor-caravan
  registration case simpler, not harder.

## Every area, measured

| Area | Size (mm) | Contains |
|---|---|---|
| Shower | **700 × 800**, floor level, 1881 clear | cassette WC 420 × 570 |
| Entry / lobby | **980 × 1032** | partition door to the cab |
| Galley — sink side (driver) | **900 × 600**, worktop 900 high | sink 400 × 340, 20 L oven, pump + filter |
| Galley — hob side (passenger) | **620 × 600** | induction domino 300 × 520, fridge under |
| Galley aisle | **620 × 632** | |
| Bench, driver | **1400 × 600 × 450** | 2 × 150 Ah battery, 3000 W inverter |
| Bench, passenger | **1400 × 600 × 450** | 110 L fresh tank, long side fore-aft |
| Table → bed | **1400 × 632** infill | |
| Rear bench | **450 × 1832 × 450** | garage under, ~400 clear, from the rear doors |
| **Bed made up** | **1850 × 1832**, full width | sleeps 3 across if it ever needs to |
| Entry gap at the open slider | **680** of the 1300 aperture | hob counter takes the rest |

## v2 against v1

| | v1 | v2 | |
|---|---|---|---|
| Bed length | 1730 | **1850** | +120 |
| Bed width | 1832 head, **1132** at the foot over 630 | **1832 throughout** | notch gone |
| Shower footprint | 750 × 700 = 0.53 m² | 700 × 800 = **0.56 m²** | +7% |
| Shower headroom | 1681 (floor is +200 over the wheel well) | **1881** | +200, and no step |
| Galley worktop | 1100 × 600 = 0.66 m² | 0.54 + 0.37 = **0.91 m²** | +38% |
| Galley aisle | 1232 | **632** | −600 |
| Corridor past the cubicle | 532 | none | gone |
| Entry gap at the slider | 1300 (whole door clear) | **680** | −620 |
| Front lounge | 620 × 1832, 2 swivel seats | none | gone |
| Bench storage | 730 × 600 + 650 × 700 | **2 × 1400 × 600** | roughly doubled |
| Garage | 450 × 1832 | 450 × 1832 | same |
| Travelling seats | 2 | **3** | +1 |

## Open on v2

1. **Where the office goes.** Candidates: a pop-up table plus a seat in the 980 × 1032 lobby;
   or the rear U with a table on a height-adjustable sliding pillar, Brisa-style. Not designed
   yet.
2. **The hob counter is only 620 long** — 300 of induction plus a 320 board. Lengthening it
   aft costs bed length 1:1; lengthening it forward costs the entry gap 1:1. Three dials,
   one length.
3. **Entry gap 680** and **aisle 632**. Both are Brisa numbers and both are a real step down
   from v1. Two people cannot pass in the galley.
4. **Fridge is no longer height-limited.** v1's 70 L drawer was forced by a 450 mm bench;
   under a 900 worktop there is ~850 of height, so the 90–100 L upright v1 rejected is back
   on the table. Worth revisiting — it was a real loss.
5. **Cassette service hatch** moves to the driver-side front panel, roughly x 100–500.
   Check it against the actual Crafter body before committing.
6. **Window in the shower** (Brisa's trick) in the front driver-side panel, which is otherwise
   blank.
7. **Wheel-well depth.** v2 uses 226 mm, which is correct for a 1832 / 1380 Crafter.
   `v1` still carries the Transit's 195 — worth fixing when that variant is next
   touched.
