# v4 — VW Crafter L3H3, thin rear bathroom, fixed bed, front office seat

Started 2026-09-22. Office seat cut to 450 on 2026-09-22 — see below, it changes everything.
**Plan only — geometry not yet checked in 3D.**

![plan](layout.png)

Regenerate: `python plan.py v4`, from the project root.

Same van and cab as v2 and v3 (Crafter L3H3, 3-seat cab, partition at x = 0). Order from
the back: **bathroom, bed, galley, office.**

**[v5](../v5/README.md) is this same layout with the driver seat on a swivel** instead of a
bench. Everything else is identical.

## The 450 mm seat pays for the whole van

The first draft of v4 was **150 mm over length** and had to cut 120 off the bed and 30 off
the sink to fit. Cutting the office seat from 600 to **450** gives all 150 back:

| | first draft | **now** |
|---|---|---|
| Office seat | 600 × 400 | **450 × 400** |
| Bed | 1400 | **1520** — v2's bed |
| Sink run | 750 | **780** — v2's run |
| Galley | 0.90 m² | **0.94 m²** — v2 exactly |

**450 is enough because you sit crosswise.** Sitting across the van, the only thing the seat's
fore-aft dimension has to hold is your hips — about 400 mm seated. Depth, the part that needs
to be generous, is the 400 mm of cushion plus the whole lounge floor for your legs. A
lengthwise bench would have to be 600 deep *and* 450 wide and would cost three times the floor.

**The budget now closes to the millimetre:**

| Driver side | mm |
|---|---|
| Office seat | 450 |
| Larder | 200 |
| Sink run | 780 |
| Bed | 1520 |
| Bathroom | 500 |
| **Total** | **3450** = the van |

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

**Middle, x 1430–2950 — the bed, fixed, 1520 × 1832 across**

| | |
|---|---|
| Sleeping | **760 each for two**, 507 for three — v2's numbers |
| Body length | 1832 gross, ~1760 after the wall build |
| Top | 450, headroom above 1431 |
| **Never converted** | it is made up, all the time |
| Garage under | 1520 × 1832 at **400 clear ≈ 1.11 m³** |

**Both wheel arches disappear into the garage.** The arches run x 1863–2763 — entirely under
the bed. No appliance anywhere in this van has to dodge one. That is what lets the fridge go
back to **90 L as a drawer**, with no arch to climb over and no door to swing into the aisle.
v2 and v3 both lost that argument.

**Front, x 0–1430 — galley, office, larder**

| Piece | Size (mm) | Holds |
|---|---|---|
| Hob + fridge, passenger | **780 × 600**, worktop 900 | induction 300 × 520 at the door end, **90 L drawer fridge** |
| Sink, driver | **780 × 600**, worktop 900 | two bowls (340 wash + 260 rinse, as v2), oven and pump under |
| **Larder** | **200 × 600**, full height 1881 | ~0.23 m³ — tins, jars, dry goods, one bottle deep |
| **Office seat** | **450 × 400**, top 450 | batteries + inverter under |
| Desk | folds off the partition at **720** | stows flat against the bulkhead |
| Aisle | 980 × **632** | |
| Entry clear at the door | **650** | of the 1300 aperture |

**The office, in detail.** A 450 × 400 bench in the front driver corner, against the driver
wall. You **sit crosswise** — facing the sliding door, legs into the open floor at y 1032–1432.
The desk is a board hinged on the partition, dropping to horizontal at 720 over your knees,
folding flat against the bulkhead when you are done.

| | |
|---|---|
| Why crosswise | the legroom is the lounge floor, so the seat costs only 450 mm of length |
| Why a fold-down and not a swing arm | v2 drew two swing-arm office tables straight through the sitter's chest before it was caught by eye. A board on the bulkhead cannot do that |
| View | out of the sliding door, across the van — daylight, not a wall |
| Cab | the pass-through is directly over this seat. The seat is the step |

**The galley matches v2 exactly.** 780 + 780 at 600 deep = **0.94 m²**. No fold-down leaf, so
nothing blocks the door while you cook.

## Water, weight and services

| Service | Where |
|---|---|
| Fresh tank ~127 L, 1400 × 350 × 260 | in the garage, along the bed's forward edge (x 1480–1830) |
| Batteries + inverter | under the office seat |
| Calorifier | garage, aft end — right behind the bathroom wall |
| Oven, pump, filter | under the sink |
| Grey | underslung |

**Axle loading, middling.** Rear axle ≈ x 2313, front ≈ x −2177. The tank at x ≈ 1655 puts
**85 %** of its weight on the rear axle — between v2 (103 %) and v3 (57 %). Pushing it further
forward costs garage depth at the front edge; it is a dial, not a decision.

## The thing to decide before anything else

**The bathroom is behind the bed, so you cross the bed to use it — by day as well as at
night.**

A full-width crosswise bed cuts the van in two: anything aft of it can only be reached over
it. With a fixed bed there is no day mode that opens a path.

| | |
|---|---|
| Person sleeping on the aft side | steps straight down into the bathroom. Fine |
| Person on the forward side | crosses ~760 mm of their partner's mattress |
| Daytime | kneel on the bed, cross 1520 mm, step down 450 into the bathroom |

For six-month stretches with a working day inside the van, that is a lot of trips.

**If it is unacceptable, the fix is structural:** the bathroom has to come forward beside the
galley, the way v1 and v2 both did it — and then it stops being a thin full-width slot, it
takes a corner, and the front zone loses ~700 mm.

## Other costs

- **No hanging space.** v2 had a wardrobe, v3 a full-height closet. v4 has the garage (flat
  things) and the larder (food). Clothes hang nowhere. For 70 L per person this may be fine —
  but it is a real deletion, not an oversight.
- **Rear doors open into the bathroom**, not a garage. The garage loads from inside only, over
  the bed — long-term storage, not daily.
- **Entry 650** against v2's 690. The aisle is still 632: two people cannot pass in the galley.

## v4 against the others

| | v2 | v3 | **v4** |
|---|---|---|---|
| Bed converted daily? | no | **yes** | **no** |
| Bed | 1520 × 1832 | 1520 × 1832 | **1520 × 1832** |
| Bathroom | 0.56 m² | 0.80 m² | **0.92 m²**, thin |
| Bathroom reachable without crossing the bed | yes | yes | **no** |
| Galley | 0.94 m² | 1.31 m² | **0.94 m²** |
| Fridge | 90 L hinged, blocks aisle | 70 L drawer | **90 L drawer, no arch** |
| Garage / closet volume | ~0.44 m³ | ~1.25 m³ | **~1.11 m³** + larder 0.23 |
| Hanging space | wardrobe | full-height closet | **none** |
| Dedicated work seat | none | none | **yes — 450 × 400 + fold-down desk** |
| Entry clear at the door | 690 | 840 | 650 |
| Appliance dodging a wheel arch | fridge | fridge | **none** |

**v4 is the only version with a real work seat and a bed you never touch** — and it no longer
gives up anything to v2 to get them. That is what [about-us](../doc/about-us.md) asks for: an
office five days a week, and a bed left made up. It pays with the bathroom walk.

## Open on v4

1. **Crossing the bed for the bathroom.** The headline. See above.
2. **No hanging space.** Decide whether that is acceptable, or whether the larder becomes a
   half-height wardrobe instead.
3. **WC sliding aft out of the garage.** It must clear the bed frame above and the bathroom's
   forward wall at floor level. A 415 × 450 cassette in a 400 mm clear garage is tight on
   height — confirm against a real unit; it may need a local 500 mm pocket.
4. **Bathroom 500 deep.** Fine seated, tight standing. Stand in a 500 mm gap before agreeing.
5. **Fold-down desk at 720 over a 450 seat.** 270 mm of thigh clearance is the minimum and
   this is exactly at it.
6. **Garage loads over the bed only.** Confirm before deleting the rear-door access.
7. **90 L drawer fridge** — confirm a real unit fits under a 900 worktop in a 600 carcass.
8. **No 3D yet.** `model3d.py` has no `REGISTRY` entry for v4, so nothing is fit-checked.
