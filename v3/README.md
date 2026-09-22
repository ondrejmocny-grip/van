# v3 — VW Crafter L3H3, front office seat, split convertible bed, rear bathroom

Started 2026-09-21. Reworked several times; current shape from 2026-09-22.
**Plan only — geometry not yet checked in 3D.**

![plan](layout.png)

Regenerate: `python plan.py v3`, from the project root.

Same van and cab as v2 (Crafter L3H3, 3-seat cab, partition at x = 0). Order from the back:
**bathroom + garage, bed, galley, office seat.**

## The shape in one line

**Two parallel benches, not a U** — and the 632 mm gap between them is a corridor that runs
from the galley straight to the bathroom door. At night the table drops and that corridor
becomes the middle of the bed.

| | Day | Night |
|---|---|---|
| The gap between the benches | **corridor, 632 wide**, to the bathroom | **the middle third of the bed** |
| The table in it | folds and slides out of the way | dropped to 450, cushions over |
| Bathroom | walk to it | cross the bed to it |

This is the fix for the problem the fixed-bed version had: with a permanent full-width bed,
the bathroom behind it could **only** ever be reached by climbing over. Now it is a normal
walk all day, and only a night trip costs anything.

## The budget closes to the millimetre

| Driver side | mm |
|---|---|
| Office seat | 450 |
| Larder | 200 |
| Sink run | 780 |
| Bed / dinette | 1520 |
| Bathroom + garage | 500 |
| **Total** | **3450** = the van |

**450 is enough for the seat because you sit crosswise.** Sitting across the van, the only
thing the seat's fore-aft dimension holds is your hips — about 400 mm seated. The depth that
has to be generous is the 400 mm of cushion plus the whole lounge floor for your legs. A
lengthwise bench would need 600 deep *and* 450 wide, and cost three times the floor.

Those 450 mm are exactly what buys **v2's bed (1520) and v2's galley (0.94 m²)** in the same
van as a bathroom and a garage.

## Front, x 0–1430 — office, galley, larder

| Piece | Size (mm) | Holds |
|---|---|---|
| **Office seat** | **450 × 400**, top 450 | shoes, books |
| Desk | folds off the partition at **720** | stows flat against the bulkhead |
| **Larder** | **200 × 600**, full height 1881 | ~0.23 m³ — tins, jars, dry goods, one bottle deep |
| Sink, driver | **780 × 600**, worktop 900 | two bowls (340 wash + 260 rinse, as v2), oven and pump under |
| Hob + fridge, passenger | **780 × 600**, worktop 900 | induction 300 × 520 at the door end, **90 L drawer fridge** |
| Aisle | 980 × **632** | runs straight into the corridor |
| Entry clear at the door | **650** | of the 1300 aperture |

**The office.** A 450 × 400 bench in the front driver corner, against the driver wall. You
**sit crosswise** — facing the sliding door, legs into the open floor at y 1032–1432. The desk
is a board hinged on the partition, dropping to horizontal at 720 over your knees.

| | |
|---|---|
| Why crosswise | the legroom is the lounge floor, so the seat costs only 450 mm of length |
| Why a fold-down and not a swing arm | v2 drew two swing-arm office tables straight through the sitter's chest before it was caught by eye. A board on the bulkhead cannot do that |
| View | out of the sliding door, across the van — daylight, not a wall |
| Cab | the pass-through is directly over this seat. The seat is the step |

**The fridge is a 90 L drawer and it dodges nothing.** The wheel arches start at x 1863; the
galley ends at 1430. No appliance in this van sits over an arch. That fixes v2's open item #4
(a 530 mm hinged door swinging into a 632 aisle) and gets 20 L back at the same time.

**Galley 0.94 m² — v2 exactly**, with no fold-down leaf blocking the door while you cook.

## Middle, x 1430–2950 — the split bed

| | Size (mm) | Holds |
|---|---|---|
| Bench, driver | **1520 × 600**, top 450 | batteries, inverter, calorifier |
| Bench, passenger | **1520 × 600**, top 450 | **118 L fresh tank**, inboard of the arch |
| Corridor between | **1520 × 632** | the table |
| Table | **900 × 512** at 700 | folds in half and slides fore-aft on its pedestal |
| **Bed made up** | **1520 × 1832** | **760 each for two**, 507 for three |
| Headroom over the bed | 1431 | |

**Why two benches and not a U.** A U needs a third bench across the back — and the back is now
the bathroom and the garage. Two parallel benches leave the middle open, and that open middle
is what the bathroom needs to be reachable.

**Why the table has to move, not just drop.** Parked in the middle of the corridor it blocks
the walk to the bathroom. So the top folds in half over its pedestal, and the pedestal slides
fore-aft in a floor track: fold and push it forward and the run aft is clear. At night it
drops to 450 and the two folded halves open flat as the bed's centre panel.

**The conversion.** Drop the table, open its halves, lay the centre cushions. Under a minute,
and only the middle 632 mm ever changes — the two benches are already at bed height.

## Rear, x 2950–3450 — bathroom beside a garage

The back is 500 mm deep and **split**, not full width:

| | Size (mm) | |
|---|---|---|
| **Bathroom**, driver side | **500 × 1232** = 0.62 m², 1881 clear | sit-down shower **and** a permanent cassette WC |
| **Garage**, passenger side | **500 × 600**, full height 1881 ≈ 0.56 m³ | loads through the **rear door** |

**A real pocket door fits here, and that is why the bathroom is this width.** The bathroom's
forward face is 1232 long: a 600 mm door plus a 632 mm pocket is exactly 1232. Nothing
surface-mounted, nothing swinging into the corridor.

**The WC stays put — no sliding drawer.** At 1232 wide the room holds both. The cassette sits
at the driver end facing across, which gives **782 mm of knee room**; the shower is the other
end, with a fold seat on the passenger wall and the whole 1232 for your legs when seated. v2
had to slide its WC in and out of a 700 × 800 cubicle; this one does not.

**The garage is full height, so it can hang clothes.** 600 wide × 500 deep is enough for a
rail across the width (hangers are ~430). Half rail, half shelves, loaded from the back —
that closes the "nowhere to hang anything" gap the earlier drafts had.

## Water, weight and services

| Service | Where |
|---|---|
| Fresh tank 118 L, 1020 × 374 × 310 | passenger bench, **inboard of the wheel arch**, x 1900–2920 |
| Batteries + inverter | driver bench, forward end, inboard of the arch |
| Calorifier | driver bench, aft end — next to the bathroom wall |
| Oven, pump, filter | under the sink |
| Grey | underslung |
| Cassette hatch | driver-side rear quarter panel, x ~3050–3400 |

**The tank is v2's tank again, with v2's problem.** 1020 × 374 × 310 is a semi-custom size, and
sitting at x ≈ 2410 it puts about **102 %** of its weight on the rear axle (rear axle ≈ x 2313).
Options, all open: have one made, plumb two slim off-the-shelf tanks in series, or cut it to
~90 L and move it forward into the bench's front third. See open item 3.

## v3 against v2

| | v2 | **v3** | |
|---|---|---|---|
| Bed | 1520 × 1832 across, rear | **1520 × 1832 across, middle** | same |
| Bed made from | rear U | **two parallel benches** | corridor survives |
| Bathroom reachable by day without crossing the bed | yes | **yes — the corridor** | = |
| Bathroom | 700 × 800 = 0.56 m² | **500 × 1232 = 0.62 m²** | +11 % |
| Bathroom door | glass screen off the lobby | **pocket door** off the corridor | better |
| WC | slides in from a drawer | **permanent** | simpler |
| Galley | 0.94 m² with a fold-down leaf | **0.94 m², no leaf** | = |
| Fridge | 90 L hinged, over the arch, blocks the aisle | **90 L drawer, no arch** | better |
| Dedicated work seat | none | **450 × 400 + fold-down desk** | new |
| Hanging space | wardrobe 450 × 600 | **garage rail, 600 × 500 full height** | ≈ |
| Garage | rear bench 1.10 m², ~400 clear ≈ 0.44 m³ | **0.56 m³ full height** + 2 benches under the bed | ≈ |
| Entry clear at the door | 690 | 650 | −40 |
| Travelling seats | 3 | 3 | = |

## Open on v3

1. **Night trip to the bathroom.** By day the corridor works. At night the bed is full width,
   so the aft sleeper rolls off straight into the bathroom and the forward sleeper crosses
   ~760 mm of their partner. Better than a fixed bed, not free.
2. **The table has to fold *and* slide.** Two mechanisms in one small table, and it doubles as
   the bed's centre panel. Mock it in cardboard before it is built — this is the part most
   likely to be annoying every day.
3. **Fresh tank.** Semi-custom shape and 102 % on the rear axle. Decide between a made-to-fit
   tank, two slim tanks in series, or 90 L moved forward.
4. **Bathroom 500 deep.** Fine seated, tight standing. Stand in a 500 mm gap before agreeing.
5. **Garage 600 wide.** Confirm what actually has to go in it — if it is only clothes, a rail
   and two shelves; if bulky gear, it may want to be wider at the bathroom's expense.
6. **Fold-down desk at 720 over a 450 seat.** 270 mm of thigh clearance is the minimum and this
   is exactly at it.
7. **Entry 650**, aisle 632 — two people cannot pass in the galley.
8. **Driver seat swivel.** A 3-seat front never blocked the *driver* side — the double bench
   cannot swivel in any van, but it is on the other side of the cab and is not in the driver
   seat's way. If it works, the swivelled seat replaces the 450 × 400 bench at no cost in floor
   (knees land inside the same 450) and gives a far better chair for an eight-hour day. The
   blockers are the handbrake lever (lowering kit) and an open driver-side partition. **Worth
   answering when the van is chosen: lever or electronic parking brake?**
9. **No 3D yet.** `model3d.py` has no `REGISTRY` entry for v3, so nothing has been checked for
   fit. That is where v1 and v2 both found real clashes.
