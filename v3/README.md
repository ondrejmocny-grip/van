# v3 — VW Crafter L3H3, L-galley, split convertible bed, rear bathroom

Started 2026-09-21. Reworked several times; current shape from 2026-09-22.
**Plan and 3D model — iterating.** No photoreal impressions yet.

![plan](layout.png)

Regenerate: `python plan.py v3` then `python model3d.py v3`, from the project root.

Same van and cab as v2 (Crafter L3H3, 3-seat cab, partition at x = 0). Order down the driver
side, back to front: **bathroom + garage · bed · office seat · larder · galley.**

## The 3D model

**Viewer: [v3 Crafter](https://claude.ai/artifact/53pg4zZh6jgR2B4MFKnLHJ)** — drag to orbit,
scroll to zoom. Also written locally to `v3/viewer.html`, `v3/model.obj` and `v3/3d/*.png`. Everything in it is
extruded from the box list in `plan.py`, so the model cannot disagree with the drawing above.

| Layer | What it holds |
|---|---|
| Bed made up | the corridor infilled to 1520 × 1832; hides the table and its post |
| Bathroom door shut | the pocket-door leaf out of its pocket, closing the 600 across the corridor |
| Table at the desk | the top in its forward socket at 745; off, it is in the corridor at 700 |
| Lockers | three overhead runs, kept clear of the door head and the windows |
| Appliances | the kit at real catalogue sizes, and it ghosts the carcasses so you see in |
| Body + glass | panels with real holes: slider, four windows, the cassette hatch, two fans, the partition with its pass-through over the shoe locker |
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
was caught by eye. It is why the desk here is a top on a floor pedestal instead.

**Two tool changes the L needed.** The galley crosses the bulkhead, so its runs are turned 90°
from every run v1 and v2 were built on:

- `sink_wells()` gained an **axis**: the two bowls now sit side by side across the van, not
  along it. Without it a 600 mm-deep counter got two bowls stacked front to back.
- the registry gained a **yaw** table, a per-variant quarter turn for a prop whose mesh was
  modelled on a run running the other way. Only the oven needs it today.

**The bathroom is drawn as a carcass the viewer ghosts**, not built from panels the way v2's
shower was. v2 had a glass screen worth building; here the interesting things are inside —
the WC, the tray, the shower head — and a pocket door has nothing to draw when it is open,
because the leaf is inside the wall. So the door is one box, in its shut position, off by
default.

### Three numbers the 3D corrected

- **WC knee room is 662 mm, not 782.** A 420 × 570 cassette against the driver wall leaves
  662 across the room, not the 782 estimated from a shallower pan. Still enough to sit.
- **The desk height is 745, not 720.** At 720 with a 20 mm top the underside lands at 700,
  only 250 above a 450 seat. 745 gives the 270 of thigh clearance that is the minimum.
- **The desk top overhangs the bed bench by 70 mm.** A 900 top in front of the office seat
  does not fit between the galley and the bench — but at 725 it passes 275 mm over the bench
  top, so the overhang is free. The first draft had it 70 mm into the galley worktop instead,
  which the overlap check caught.

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

## Front, x 0–1430 — the L-galley, larder and office seat

The galley turns the corner behind the driver instead of splitting across the aisle. That
corner used to be the office seat and a patch of open floor; now it is worktop, and the seat
moves aft into a nook between the larder and the bed.

| Piece | Size (mm) | Holds |
|---|---|---|
| **Galley, long leg** — across the bulkhead | **600 × 1382**, worktop 900 | hob at the door end, **90 L drawer fridge** under it, **sink in the corner**, oven and pump under |
| **Galley, return** — down the driver wall | **180 × 600**, worktop 900 | free counter, the drainer end |
| Shoe locker | **600 × 450**, top 450 | shoes; the step to the cab, pass-through over it |
| **Larder** | **200 × 600**, full height 1881 | ~0.23 m³ — tins, jars, dry goods, one bottle deep |
| **Office seat** | **450 × 400**, top 450 | in the nook between the larder and the bed |
| Aisle | **632** | runs straight into the corridor |
| Entry clear at the door | **830** | of the 1300 aperture |

**Why the L is worth it.** Two things fall out of moving the galley into the corner:

- **The entry goes from 650 to 830.** The passenger side of the front zone is now nothing but
  the shoe locker and open floor, so the only thing narrowing the sliding door is the locker.
- **The seat gets a nook.** Larder on one side, bed bench on the other, window at your
  shoulder. Better to work in than a corner beside a cooker.

**One top, two floor sockets — there is no separate desk any more.** The dinette table lifts
off and drops into a second socket in front of the office seat. That deletes the fold-down
board off the partition, which was one more mechanism to build and would now be nowhere near
the seat anyway.

| | |
|---|---|
| Aft socket, in the corridor | table at **700** — dinette, benches both sides |
| Forward socket, in the aisle | table at **745** — desk, 270 of thigh clearance over the 450 seat |
| Bed | the aft pedestal drops to **450** and the top becomes the bed's centre panel |
| At the desk | the top overhangs the bed bench by 70 mm — 275 mm above it, so it clears |

**The office.** A 450 × 400 bench against the driver wall at x 980–1430. You **sit crosswise**
— facing the sliding door, legs into the aisle. The seat costs only 450 mm of the driver
side's length because the legroom is floor the van already had.

**Why not a swing arm.** v2 drew two swing-arm office tables straight through the sitter's
chest before it was caught by eye. A top on a floor pedestal cannot do that, and
`model3d.check()` now carries the sitter to prove it.

**The cab pass-through moves to the passenger corner**, over the shoe locker — the galley owns
the driver corner now, which is the whole point of the L.

**The fridge is a 90 L drawer and it dodges nothing.** The wheel arches start at x 1863; the
galley ends at 1430. No appliance in this van sits over an arch. That fixes v2's open item #4
(a 530 mm hinged door swinging into a 632 aisle) and gets 20 L back at the same time.

**Galley 0.94 m² — v2 exactly** (0.83 in the long leg, 0.11 in the return), with no fold-down
leaf blocking the door while you cook.

## Middle, x 1430–2950 — the split bed

| | Size (mm) | Holds |
|---|---|---|
| Bench, driver | **1520 × 600**, top 450 | batteries, inverter, calorifier |
| Bench, passenger | **1520 × 600**, top 450 | **118 L fresh tank**, inboard of the arch |
| Corridor between | **1520 × 632** | the table, in its aft socket |
| Table | **900 × 512** | one top, two sockets — 700 aft, 745 forward, 450 as bed |
| **Bed made up** | **1520 × 1832** | **760 each for two**, 507 for three |
| Headroom over the bed | 1431 | |

**Why two benches and not a U.** A U needs a third bench across the back — and the back is now
the bathroom and the garage. Two parallel benches leave the middle open, and that open middle
is what the bathroom needs to be reachable.

**Why the table lifts off instead of sliding.** Parked in the corridor it blocks the walk to
the bathroom. A floor track long enough to reach the desk position would have to run 1850 mm,
across the bed line. Two sockets and a lift-off top do the same job with no track at all — and
lifting it out is also how you clear the corridor.

**The conversion.** Lift the top off, drop the pedestal to 450, put the top back, lay the
centre cushions. Under a minute,
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
| Dedicated work seat | none | **450 × 400 in a nook + the table at 745** | new |
| Hanging space | wardrobe 450 × 600 | **garage rail, 600 × 500 full height** | ≈ |
| Garage | rear bench 1.10 m², ~400 clear ≈ 0.44 m³ | **0.56 m³ full height** + 2 benches under the bed | ≈ |
| Galley shape | two runs across the aisle | **L into the corner behind the driver** | |
| Entry clear at the door | 690 | **830** | +140 |
| Travelling seats | 3 | 3 | = |

## Open on v3

1. **Night trip to the bathroom.** By day the corridor works. At night the bed is full width,
   so the aft sleeper rolls off straight into the bathroom and the forward sleeper crosses
   ~760 mm of their partner. Better than a fixed bed, not free.
2. **One top doing three jobs.** Dinette at 700, desk at 745, bed panel at 450, in two floor
   sockets. That needs a pedestal with three clamp positions and somewhere to park the top
   while you move it. Mock it before it is built — it is the part most likely to annoy daily.
3. **Fresh tank.** Semi-custom shape and 102 % on the rear axle. Decide between a made-to-fit
   tank, two slim tanks in series, or 90 L moved forward.
4. **Bathroom 500 deep.** Fine seated, tight standing. Stand in a 500 mm gap before agreeing.
5. **Garage 600 wide.** Confirm what actually has to go in it — if it is only clothes, a rail
   and two shelves; if bulky gear, it may want to be wider at the bathroom's expense.
6. **The table at 745 over a 450 seat.** That is 270 mm of thigh clearance — the minimum. Sit
   at a 745 desk on a 450 chair before agreeing.
7. **Aisle 632** — two people still cannot pass in the galley, even with the entry at 830.
   And working at the forward socket blocks the aisle until you lift the top off.
8. **Driver seat swivel.** A 3-seat front never blocked the *driver* side — the double bench
   cannot swivel in any van, but it is on the other side of the cab and is not in the driver
   seat's way. If it works, the swivelled seat replaces the 450 × 400 bench at no cost in floor
   (knees land inside the same 450) and gives a far better chair for an eight-hour day. The
   blockers are the handbrake lever (lowering kit) and an open driver-side partition. **Worth
   answering when the van is chosen: lever or electronic parking brake?**
9. **The oven's quarter turn is a guess.** `YAW_V3` turns it 90° so its door faces the aisle
   rather than the bulkhead; 90 against 270 was not something the box list could settle. Check
   it in the viewer, and `props.py face` is there to correct it.
10. **No photoreal impressions yet.** `impressions.py` has not been run on v3.

**The pocket door stays a coloured box, on purpose.** Its slot is 40 × 600 × 1881 and the
viewer stretches a mesh to fill its box, so any door leaf becomes a flat slab — which is what
the box already looks like. The only thing a mesh would add is a recessed finger pull. The
prompt is written in `props.py` if we ever change our mind; nothing else is.
