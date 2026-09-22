# v3 — VW Crafter L3H3, front office seat, split convertible bed, rear bathroom

Started 2026-09-21. Reworked several times; current shape from 2026-09-22.
**Plan and 3D model — iterating.** No photoreal impressions yet.

![plan](layout.png)

Regenerate: `python plan.py v3` then `python model3d.py v3`, from the project root.

Same van and cab as v2 (Crafter L3H3, 3-seat cab, partition at x = 0). Order from the back:
**bathroom + garage, bed, galley, office seat.**

## The 3D model

**Viewer: [v3 Crafter](https://claude.ai/artifact/53pg4zZh6jgR2B4MFKnLHJ)** — drag to orbit,
scroll to zoom. Also written locally to `v3/viewer.html`, `v3/model.obj` and `v3/3d/*.png`. Everything in it is
extruded from the box list in `plan.py`, so the model cannot disagree with the drawing above.

| Layer | What it holds |
|---|---|
| Bed made up | the corridor infilled to 1520 × 1832; hides the table and its post |
| Bathroom door shut | the pocket-door leaf out of its pocket, closing the 600 across the corridor |
| Desk out | the front desk deployed; off, it hangs folded flat down the partition |
| Lockers | three overhead runs, kept clear of the door head and the windows |
| Appliances | the kit at real catalogue sizes, and it ghosts the carcasses so you see in |
| Body + glass | panels with real holes: slider, three windows, the cassette hatch, two fans, the partition with its pass-through over the office seat |
| Cab + seats | the 3-seat cab, dash, wheel, and the four road wheels |
| Schema overlay | the plan itself painted onto the model |
| Sizes | every block labelled with its name and size in mm |

`model3d.check()` passes on all **15 appliances**: each one inside the van, inside a carcass,
clear of its neighbours, and clear of the tyres. Three results worth keeping:

- **Nothing overlaps a wheel arch at all.** Not one warning — a first for this project. The
  galley ends at x 1430 and the arches start at 1863, so no appliance is even near one. It is
  what lets the fridge be a 90 L drawer instead of v2's hinged 90 L or v1's 70 L.
- **The batteries stop 17 mm short of the driver tyre.** The tyre runs x 1957–2669; the aft
  battery ends at 1940. Tight, and real.
- **The fresh tank sits exactly on the arch line.** Its outboard face is at y = 226, which is
  where the arch ends. Nothing to spare, nothing over.

`check()` also carries **a person sitting crosswise on the office seat** — trunk, thighs,
shins — and fails the build if any furniture runs through them. That test exists because two
rounds of v2's office table were drawn with a swing arm through the sitter's chest before it
was caught by eye. It is why the desk here hinges on the partition instead.

**The bathroom is drawn as a carcass the viewer ghosts**, not built from panels the way v2's
shower was. v2 had a glass screen worth building; here the interesting things are inside —
the WC, the tray, the shower head — and a pocket door has nothing to draw when it is open,
because the leaf is inside the wall. So the door is one box, in its shut position, off by
default.

### Two numbers the 3D corrected

- **WC knee room is 662 mm, not 782.** A 420 × 570 cassette against the driver wall leaves
  662 across the room, not the 782 estimated from a shallower pan. Still enough to sit.
- **The desk top is 740, not 720.** At 720 with a 20 mm top the underside lands at 700, which
  is only 250 above a 450 seat. 740 gives the 270 of thigh clearance that is the minimum.

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
| Desk, front | **440 × 530** at **740** | folds flat down the partition; 270 of thigh clearance |
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
at the driver end facing across, which gives **662 mm of knee room**; the shower is the other
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
6. **Fold-down desk at 740 over a 450 seat.** That is 270 mm of thigh clearance — the minimum,
   and the 3D moved it up 20 mm to get there. Sit at a 740 desk on a 450 chair before agreeing.
7. **Entry 650**, aisle 632 — two people cannot pass in the galley.
8. **Driver seat swivel.** A 3-seat front never blocked the *driver* side — the double bench
   cannot swivel in any van, but it is on the other side of the cab and is not in the driver
   seat's way. If it works, the swivelled seat replaces the 450 × 400 bench at no cost in floor
   (knees land inside the same 450) and gives a far better chair for an eight-hour day. The
   blockers are the handbrake lever (lowering kit) and an open driver-side partition. **Worth
   answering when the van is chosen: lever or electronic parking brake?**
9. **No photoreal impressions yet.** `impressions.py` has not been run on v3, and no prop
   meshes have been generated for its new kinds — the 90 L drawer fridge and the pocket door
   are still coloured boxes in the viewer.
