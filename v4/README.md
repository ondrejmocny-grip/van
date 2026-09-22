# v4 — VW Crafter L3H3, thin rear bathroom, fixed bed, front office seat

Started 2026-09-22. **Plan only — geometry not yet checked in 3D.**

![plan](layout.png)

Regenerate: `python plan.py v4`, from the project root.

Same van and cab as v2 and v3 (Crafter L3H3, 3-seat cab, partition at x = 0). Order from
the back: **bathroom, bed, galley, office.**

**This is a new version, not a rewrite of v3.** v3 (bed at the front on a slide-out) is kept
for comparison — the two answer the same brief in opposite ways.

## First, the arithmetic — the brief is 150 mm too long

Written out literally, the ask needs:

| | mm |
|---|---|
| Bathroom, thin, full width | 500 |
| Bed, crosswise, v2 size | 1520 |
| Sink run, v2 size | 780 |
| Larder, thin | 200 |
| Office seat behind the driver | 600 |
| **Total the driver side must carry** | **3600** |
| Van | **3450** |
| | **over by 150** |

Closed by taking **120 off the bed** (1520 → 1400) and **30 off the sink** (780 → 750).
Nothing else was cut. Where that hurts, and the two levers to undo it, are at the bottom.

## The layout, measured

**Rear, x 2950–3450 — bathroom, 500 × 1832**

A slot across the whole back. 0.92 m² of floor, 1881 clear.

| | |
|---|---|
| Shower | sit-down. Fold seat on the driver end wall; you sit facing across, **1832 mm of legroom** |
| Head and riser | on the rear wall |
| WC | **slides aft out of the garage** through a hatch in the bathroom's forward wall |
| Cassette | out through the driver-side rear quarter panel, x ~3050–3400 |
| Depth | 500 — thin to stand in, generous to sit in, which is how we said we would use it |

**Middle, x 1550–2950 — the bed, fixed, 1400 × 1832 across**

| | |
|---|---|
| Sleeping | **700 each for two**, 466 for three |
| Body length | 1832 gross, ~1760 after the wall build |
| Top | 450, headroom above 1431 |
| **Never converted** | it is made up, all the time |
| Garage under | 1400 × 1832 at **400 clear ≈ 1.03 m³** |

**Both wheel arches disappear into the garage.** The arches run x 1863–2763 — entirely under
the bed. No appliance anywhere in this van has to dodge one. That is worth more than it
sounds: it is what lets the fridge go back to **90 L as a drawer**, with no arch to climb
over and no door to swing into the aisle. v2 and v3 both lost that argument.

**Front, x 0–1550 — galley, office, larder**

| Piece | Size (mm) | Holds |
|---|---|---|
| Hob + fridge, passenger | **800 × 600**, worktop 900 | induction 300 × 520 at the door end, **90 L drawer fridge** |
| Sink, driver | **750 × 600**, worktop 900 | two bowls (340 wash + 260 rinse, as v2), oven and pump under |
| **Larder** | **200 × 600**, full height 1881 | ~0.23 m³ — tins, jars, dry goods, one bottle deep |
| **Office seat** | **600 × 400**, top 450 | batteries + inverter under |
| Desk | folds off the partition at **720** | stows flat against the bulkhead |
| Aisle | 950 × **632** | |
| Entry clear at the door | **750** | of the 1300 aperture |

**The office, in detail.** The seat is a 600 × 400 bench in the front driver corner, against
the driver wall, and you **sit crosswise** — facing the sliding door, legs into the open
floor at y 1032–1432. The desk is a board hinged on the partition, dropping to horizontal at
720 over your knees, and folding flat against the bulkhead when you are done.

| | |
|---|---|
| Why crosswise | the legroom is the lounge floor, so the seat costs only 400 mm of depth |
| Why a fold-down and not a swing arm | v2 drew two swing-arm office tables straight through the sitter's chest before it was caught. A board on the bulkhead cannot do that |
| View | out of the sliding door, across the van — daylight, not a wall |
| Cab | the pass-through is directly over this seat. The seat is the step |

**The galley matches v2.** 800 + 750 at 600 deep = **0.93 m²**, against v2's 0.94 (two runs of
780). No fold-down leaf, so nothing blocks the door while you cook.

## Water, weight and services

| Service | Where |
|---|---|
| Fresh tank ~127 L, 1400 × 350 × 260 | in the garage, along the bed's forward edge (x 1600–1950) |
| Batteries + inverter | under the office seat |
| Calorifier | garage, aft end — right behind the bathroom wall |
| Oven, pump, filter | under the sink |
| Grey | underslung |

**Axle loading, middling.** Rear axle ≈ x 2313, front ≈ x −2177. The tank at x ≈ 1775 puts
**88 %** of its weight on the rear axle — between v2 (103 %) and v3 (57 %). Pushing it further
forward means giving up garage depth at the front edge; it is a dial, not a decision.

## The thing to decide before anything else

**The bathroom is behind the bed, so you cross the bed to use it — by day as well as at
night.**

This is not a detail. A full-width crosswise bed cuts the van in two: anything aft of it can
only be reached over it. With a fixed bed there is no day mode that opens a path.

| | |
|---|---|
| Person sleeping on the aft side | steps straight down into the bathroom. Fine |
| Person on the forward side | crosses ~700 mm of their partner's mattress |
| Daytime | kneel on the bed, cross 1400 mm, step down 450 into the bathroom |

For six-month stretches with a working day inside the van, that is a lot of trips.

**If it is unacceptable, the fix is structural:** the bathroom has to come forward beside the
galley, the way v2 and v1 both did it — and then it is no longer a thin full-width slot, it
takes a corner, and the front zone loses ~700 mm. Say the word and I will draw that as v5.

## Other costs

- **No hanging space.** v2 had a wardrobe, v3 had a full-height closet. v4 has the garage
  (flat things) and the larder (food). Clothes hang nowhere. For 70 L per person this may be
  fine — but it is a real deletion, not an oversight.
- **Bed for three is 466 each** (v2: 507). See the levers below.
- **Rear doors open into the bathroom**, not a garage. The garage loads from inside only,
  over the bed — so it is long-term storage, not daily.
- **Entry 750** is good, but the aisle is still 632: two people cannot pass in the galley.

## What v4 wins

| | v2 | v3 | **v4** |
|---|---|---|---|
| Bed converted daily? | no | **yes** | **no** |
| Bed for two | 760 each | 760 each | 700 each |
| Bathroom | 0.56 m² | 0.80 m² | **0.92 m²**, thin |
| Bathroom reachable without crossing the bed | yes | yes | **no** |
| Galley | 0.94 m² | 1.31 m² | 0.93 m² |
| Fridge | 90 L hinged, blocks aisle | 70 L drawer | **90 L drawer, no arch** |
| Garage / closet volume | ~0.44 m³ | ~1.25 m³ | **~1.03 m³** + larder 0.23 |
| Hanging space | wardrobe | full-height closet | **none** |
| Dedicated work seat | none | none | **yes — 600 × 400 + fold-down desk** |
| Entry clear at the door | 690 | 840 | 750 |
| Appliance dodging a wheel arch | fridge | fridge | **none** |

**v4 is the only version with a real office seat and a bed you never touch.** That is exactly
what [about-us](../doc/about-us.md) asks for — a working office five days a week, and a bed
left made up. It pays for both with the bathroom walk.

## Two levers, if the trims hurt

| Want | Cost |
|---|---|
| **Bed 1500** (750 each for two, 500 for three) | sink run drops to 650 → galley 0.87 m², **7 % under v2** |
| **Sink run 950** (galley 1.05 m², **12 % over v2**) | drop the larder entirely |

Both are one-line changes in `plan.py`.

## Open on v4

1. **Crossing the bed for the bathroom.** The headline. See above.
2. **No hanging space.** Decide whether that is acceptable or whether the larder becomes a
   half-height wardrobe instead.
3. **WC sliding aft out of the garage.** It has to clear the bed frame above it and the
   bathroom's forward wall at floor level. A 415 × 450 cassette unit in a 400 mm clear garage
   is tight on height — confirm against a real unit, it may need a local 500 mm pocket.
4. **Bathroom 500 deep.** Fine seated, tight standing. Stand in a 500 mm gap before agreeing.
5. **Fold-down desk at 720 off the partition.** Check the knee height against the 450 seat —
   270 mm of thigh clearance is the minimum and this is exactly at it.
6. **Garage loads over the bed only.** Confirm that is acceptable before deleting the rear
   door access.
7. **90 L drawer fridge** — confirm a real unit fits under a 900 worktop in a 600 carcass.
8. **No 3D yet.** `model3d.py` has no `REGISTRY` entry for v4, so nothing has been checked
   for fit.
