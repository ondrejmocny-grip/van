# v2 — VW Crafter L3H3, 3-seat cab

Started 2026-09-20. **Schema only — iterating.** No 3D, no impressions yet.

![plan](layout.png)

Regenerate: `python plan.py v2` from the project root.

Brisa's layout ported to our van: shower in the front driver corner, galley split across the
aisle, rear U-dinette. See [ref/doracamper-brisa-ducato-l2h2](../ref/doracamper-brisa-ducato-l2h2/README.md).

## What changed from v1, and why

- **Three front seats** (driver + double bench), so **swivel seats are dropped**. They were
  never going to work against a 3-seat bench, and dropping them also removes the handbrake
  lowering kit and the "does the Crafter have an electronic parking brake" question.
- **Partition wall behind the cab at x = 0**, with a pass-through beside the seat locker.
- **Three belted travelling seats** instead of two, which also makes the motor-caravan
  registration case simpler, not harder.
- **The bed turned sideways.** 1520 mm fore-aft is enough, even with a child, so you sleep
  **across** the van.
- **The office sits at the bulkhead**, behind the passenger seats.
- **The WC left the shower floor.** It stows under the wardrobe and slides forward into the
  shower only when needed — Scarlet & Seth's trick, adapted to a cassette.

## The office

A seat at the bulkhead, behind the passenger seats, facing **aft** down the van with the
sliding door at your left shoulder.

| | |
|---|---|
| Seat / locker | **450 × 600**, top at 450 (520 with cushion) — **shoes inside** |
| Table | **450 × 600** on a swing arm, top at 760 — same part as v1 |
| Thigh clearance | 240 mm, the number v1 already accepted |
| Cab pass-through | beside the locker, **432 wide**, in the bulkhead |

The locker earns three jobs from one box: seat, shoe store, and the thing you put a knee on
going through to the cab.

**With the table deployed, the side door is blocked** — the clear entry drops from 700 mm to
about 250. It swings away, so it is a 2-second cost, but it is a daily one.

## The bathroom

**Shower: curtain or sliding door, never a swinging one.** That is what lets the shower keep
its 800 mm width without stealing clearance from the lobby.

**The WC stows under the wardrobe.** A cassette unit, roughly 420 × 570, sits in the wardrobe
base and **slides forward into the shower** when you need it. The **cassette itself comes out
sideways through a hatch in the driver-side body panel**, at x 700–1150.

What this buys:

- The shower floor is clear when showering, and holds the WC when it is not.
- The wardrobe pays for itself twice — hanging space above, WC below.
- The shower can be the minimum size and still work, because nothing lives in it.

Hanging length above the WC is about **1281 mm** — fine for shirts and jackets, not for a
full-length coat.

## The bed sleeps across the van

| | |
|---|---|
| Platform | **1520 fore-aft × 1832 across** |
| Body length | across the van: **1832 gross, ~1760 after the wall build** |
| Sleeping width | **760 each** for two · **507 each** for three |

**This is not a regression on v1.** v1's bed is 1730 mm long net; v2 gives ~1760. At 171 cm
both are "touching both ends"; v2 touches 30 mm later. v1's "crosswise needs ~1800, the van
gives ~1710" was the **Transit's** 1784 width — the Crafter's 1832 changes the answer.

**Worth doing:** thin the wall build to a shallow **shoulder niche** at bed height on both
side walls. Recovers 40–60 mm, takes it to ~1810, no holes in the body.

## Every area, measured

| Area | Size (mm) | Contains |
|---|---|---|
| Shower | **700 × 800**, floor level, 1881 clear | curtain; WC slides in when needed |
| Wardrobe | **450 × 600** | hanging above (~1281 clear), **WC drawer below** |
| Seat / shoe locker | **450 × 600 × 450** | shoes; doubles as the step to the cab |
| Office table | **450 × 600** at 760 | swing arm, parks against the bulkhead |
| Entry, clear at the door | **700** of the 1300 aperture | cab pass-through 432 beside the seat |
| Galley — sink side (driver) | **780 × 600**, worktop 900 | sink 400 × 340, 20 L oven under |
| Galley — hob side (passenger) | **780 × 600** | induction 300 × 520 + 480 board, fridge under |
| Galley aisle | **780 × 632** | |
| Bench, driver | **920 × 600 × 450** | 2 × 150 Ah battery, 3000 W inverter |
| Bench, passenger | **920 × 600 × 450** | **118 L fresh tank**, 1020 × 374 × 310, inboard of the arch, running into the rear bench |
| Table → bed | **920 × 632** infill | |
| **Rear bench / garage** | **600 × 1832 × 450**, ~400 clear | calorifier, electrics board, pump + filter |
| **Bed made up** | **1520 × 1832** | 2 at 760 each, or 3 at 507 |

Driver side adds up: shower 700 + wardrobe 450 + sink 780 = **1930**, then the bed.

**The wardrobe is now 600 deep, aligned with the sink**, so the aisle runs clear past it. Only
the shower still stands 200 mm proud of that line, and it does so at the very front where the
lobby is widest.

## The fresh tank runs the bench corner

Resolved 2026-09-21. **The U is one continuous carcass**, so the tank does not have to live in
one bench — it runs from the passenger side bench into the rear bench, across the junction at
x = 2850.

But it runs **inboard of the wheel arch**, not across the full 600 mm depth:

| | |
|---|---|
| Tank | **1020 × 374 × 310 ≈ 118 L** |
| Position | x 1930–2950, y 226–600, on the floor |
| Clears | the wheel arch, which intrudes y 0–226 over x 1863–2763 |

**Why inboard rather than straight back into the garage.** Running it full-depth would have
meant starting aft of the arch at x 2790, putting all 118 kg **behind the rear axle** (centred
~2313) and eating 0.32 m² of the new garage. Inboard, the tank straddles the axle — centred
about 127 mm behind it — and the garage stays whole.

What it costs: the strip over the arch, y 0–226, becomes shallow storage for flat things
rather than tank volume. Cheap at the price, and it is dead space in every other layout too.

This also **closes the clash v1 never resolved** — v1 put a 620 mm-deep tank in a 700 mm bench
sitting over the same arch.

## v2 against v1

| | v1 | v2 | |
|---|---|---|---|
| Body length in bed | 1730 (along the van) | **~1760** (across, after wall build) | +30 |
| Bed shape | 1730 × 1832 head, **1132 at the foot** | **1520 × 1832**, no notch | notch gone |
| Shower footprint | 750 × 700 = 0.53 m² | 700 × 800 = **0.56 m²** | +7% |
| Shower headroom | 1681 (floor is +200 over the wheel well) | **1881** | +200, no step |
| Shower floor when showering | cassette in it | **clear** | WC stows away |
| Galley worktop | 1100 × 600 = 0.66 m² | 2 × 780 × 600 = **0.94 m²** | +42% |
| Hanging space | none | **450 × 600**, ~1281 clear | new |
| Work position | swivel seat + Lagun table | bulkhead seat + swing table | 1 either way |
| Galley aisle | 1232 | **632** | −600 |
| Corridor past the cubicle | 532 | none | gone |
| Entry gap at the slider | 1300 | **700** | −600 |
| Bench storage | 0.89 m² | 2 × 920 × 600 = **1.10 m²** | +24% |
| **Garage** | 450 × 1832 = 0.82 m² | **600 × 1832 = 1.10 m²** | **+33%** |
| Travelling seats | 2 | **3** | +1 |

## Open on v2

1. **The deployed table blocks the side door.** 700 mm of entry drops to ~250. Swing-arm, so
   it is recoverable in seconds — but worth feeling before it is built.
2. **Tank shape.** 1020 × 374 × 310 is a semi-custom size. Either have one made, or plumb
   two off-the-shelf slim tanks in series. Confirm before the benches are cut.
3. **Cassette hatch** in the driver-side body panel at x 700–1150. Check it against the actual
   Crafter body — flat panel expected, but confirm.
4. **Fridge door swing.** Brisa's 65 L unit is a **hinged door, not a drawer** — a ~500 mm door
   into a 632 aisle blocks it completely while open. Hinge side is a real decision.
5. **Entry gap 700** and **aisle 632**. Two people cannot pass in the galley.
6. **Window in the shower** (Brisa's trick) at x 0–700 of the driver-side panel. Clear of the
   cassette hatch at 700–1150.
7. **Wheel-well depth.** v2 uses 226 mm, correct for a 1832 / 1380 Crafter. `v1` still carries
   the Transit's 195 — worth fixing when that variant is next touched.
