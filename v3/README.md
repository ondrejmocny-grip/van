# v3 — VW Crafter L3H3, slide-out bed at the front, bathroom at the back

Started 2026-09-21. Reworked 2026-09-22 — the bed now sleeps **across** on a slide-out.
**Plan only — geometry not yet checked in 3D.**

![plan](layout.png)

Regenerate: `python plan.py v3`, from the project root.

Same van and same cab as v2 (Crafter L3H3, 3-seat cab, partition at x = 0), turned around:
bed to the front, bathroom and a full-height closet to the back.

## The slide-out is what makes this work

The sliding door is at x 300–1600 — the **front half** of the van. A bed at the front and a
door at the front want the same floor. The answer is that the bed **is not there during the
day**:

| | The front, x 760–1520, full width |
|---|---|
| **Day** | Platform stowed inside the bench. **Open floor, 760 × 1832.** Step in, walk through, sit at the table. |
| **Night** | Platform pulled 760 mm aft. **Bed 1520 × 1832**, sleeping across. |

The bench against the bulkhead is **760 deep and the full 1832 wide**. The platform lives
inside it, at seat level, on full-extension runners, and pulls out exactly its own depth —
so it needs no second stage and no folding.

**The table is not part of the bed.** It is a lift-off top on a single pedestal. At night it
comes off and slides into the closet. That is what frees the bed from the table's shape, and
it is why the bed can be a clean rectangle.

## What the crosswise bed gives back

Turning the bed across the van recovers everything the fore-aft version had to pay for:

| | fore-aft version (first draft) | **crosswise slide-out** |
|---|---|---|
| Bed | 1800 × 1400 | **1520 × 1832** |
| Two sleeping | 700 each | **760 each** |
| Three sleeping | 466 each | **507 each** |
| Night walkway to the bathroom | 432 mm squeeze | **none needed** — you step off the foot of the bed straight into the aisle |
| Entry clear at the door | 700 by day | **840** |
| Worktop | 1.14 m² | **1.31 m²** |
| Sink | 1.5 bowl (run only 850) | **two full bowls** (run 1130) |

The night walkway is the big one. With the bed across, its aft edge is at x 1520 and the
aisle starts there — **getting up for the toilet at 3 a.m. costs nothing.** In the fore-aft
version it cost a 432 mm squeeze along the passenger wall, and that was the weakest part of
the design.

## The front, measured

| Piece | Size (mm) | Holds |
|---|---|---|
| Bench against the bulkhead | **760 × 1832**, top 450 | the slide-out platform; **~120 L fresh tank**; drawers under |
| Sofa, driver leg | **760 × 600**, top 450 | batteries, inverter |
| Slide-out platform | **760 × 1232**, top 450 | — |
| Table | **600 × 660** at 700, lift-off pedestal | — |
| **Bed made up** | **1520 × 1832** | 760 each for two, 507 for three |
| Headroom over the bed | 1431 | |

**Day layout.** L-sofa around the front driver corner — bench along the bulkhead, leg down
the driver side — with the table in the corner between them. Clear walkway y 0–560 runs from
the sliding door aft into the aisle.

**The conversion, at night.** Pull two platform panels aft (they carry their own drop-down
legs at the outer edge), lift the table top off and slide it into the closet, and flip the
bulkhead backrest cushions down flat — they *are* the platform's mattress. Under a minute.

**Storage under the bench.** The platform takes only the top ~100 mm. Below it, z 0–330
across 760 × 1832 is drawers and the water tank, all opening aft into the footwell.

**The bench is the step to the cab.** It is full width at 450 high, so the partition's
pass-through sits directly above it. No separate shoe locker needed — v2 had to build one.

## The galley, in the middle

| Run | Size (mm) | Holds |
|---|---|---|
| Driver | **1130 × 600**, worktop 900 | **two bowls** (340 wash + 260 rinse, as v2), 20 L oven and the pump under |
| Passenger — by the door | **1050 × 600**, worktop 900 | induction 300 × 520 at the door end, **70 L drawer fridge** over the arch, prep board |
| Aisle | 1130 × **632** | |

**Worktop 1.31 m²** — the most of any version (v1: 0.66; v2: 1.18 including a fold-down leaf
that blocked the door). No leaf, nothing to fold.

**The fridge is a 70 L drawer, and that is deliberate.** Both runs sit over the wheel arch
(x 1863–2763). A 90 L upright cannot live over a 300 mm arch under a 900 worktop — the
arithmetic does not close. A drawer unit at ~525 high sits on a plinth on top of the arch and
clears. It also kills v2's open item #4: no ~530 mm hinged door swinging into a 632 aisle.

## The rear: bathroom and closet, behind a pair of sliding panels

| | Size (mm) | |
|---|---|---|
| **Bathroom**, driver side | **800 × 1000**, 1881 clear | sit-down shower + cassette WC, both permanent |
| **Garage closet**, passenger side | **800 × 832**, full height 1881 | hanging rail + shelves; the table top stows here |

**The sliding door, as asked — you walk in from the galley.** A pocket door does not fit: a
600 mm door needs 600 mm of pocket, and neither the 1000 mm forward face nor the 832 mm
divider wall is long enough to hide one.

So the whole rear face becomes the door: **a 1832 mm track carrying two surface-mounted
panels**, full height.

- Slide one panel across and the **bathroom opening is 700 mm wide**, straight off the aisle.
- Slide them the other way and the **closet** is open instead.
- Only one of the two is open at a time. That is the cost, and for a bathroom and a wardrobe
  it does not matter.

**Water tightness.** A surface slider is a room door, not a shower screen. Inside, the tray
gets a **40 mm upstand at the door line and its own curtain**. The sliding panel keeps the
steam and the privacy in; the curtain keeps the water in.

**The WC sits in the aft-driver corner on the diagonal.** That is what makes the knee room
work: across the corner you have ~1280 mm, where square to a wall you would only have 500.
The shower seat folds off the forward wall.

**The wheel arch just reaches in.** It runs to x 2763, so it pokes 113 mm into both forward
corners of the rear block, 226 mm wide. On the bathroom side the nib sits under the fold-down
seat. On the closet side it is inside a cupboard. **No raised floor anywhere** — v1's "+360
step into the wet cubicle" is not coming back.

**The closet is v2's garage rebuilt vertically.** v2: 1.10 m² of floor at ~400 clear ≈ 0.44 m³.
v3: 0.67 m² of floor by 1881 high ≈ **1.25 m³**, and you can hang a jacket in it. It replaces
v2's separate wardrobe as well.

## Water, weight and services

| Service | Where |
|---|---|
| Fresh tank ~120 L, 800 × 500 × 300 | under the bulkhead bench, lying across the van |
| Batteries + inverter | under the driver-side sofa leg |
| Calorifier | under the driver galley, aft end — short runs to the sink and the shower |
| Pump + filter | under the sink |
| Grey | underslung |
| Cassette hatch | driver-side rear quarter panel, x ~2850–3300 |

**No wheel arch at the front**, so the tank is a **plain rectangular off-the-shelf box** —
v2's open item #2 (a semi-custom 1020 × 374 × 310) goes away.

**Axle loading improves.** Rear axle ≈ x 2313, front axle ≈ x −2177. The tank's centre at
x ≈ 380 puts about **57 %** of its weight on the rear axle. v2's tank at x ≈ 2440 put **103 %**
on it. The rear axle is what runs out first in a camper, so moving water forward buys margin —
and the rear bathroom (x ≈ 3050, **116 %**) is what spends it.

## v3 against v2

| | v2 | v3 | |
|---|---|---|---|
| Bed | 1520 × 1832 across, rear | **1520 × 1832 across, front** | same size |
| Bed left made up? | yes, most days | **no — converted daily** | worse |
| Conversion | drop the table, infill | **pull a slide, flip cushions** | faster |
| Bathroom | 700 × 800 = 0.56 m² | **800 × 1000 = 0.80 m²** | +43 % |
| WC | slides in from a drawer under the wardrobe | **permanent, in the bathroom** | simpler |
| Bathroom door | glass screen off the lobby | **sliding panel off the galley aisle** | as asked |
| Hanging | 450 × 600, ~1281 clear | **832 × 800, full height** | much more |
| Closet / garage volume | ~0.44 m³ | **~1.25 m³** | +180 % |
| Worktop | 1.18 m² with a fold-down leaf | **1.31 m², no leaf** | +11 % |
| Fridge | 90 L hinged, blocks the aisle | **70 L drawer** | −20 L, no door swing |
| Entry clear at the door | 690 | **840** | +150 |
| Galley aisle | 632 | 632 | = |
| Fresh tank | semi-custom, 103 % on the rear axle | **off-the-shelf, 57 %** | better |
| Rear doors | open into the garage | **open into the bathroom and the closet** | worse |
| Travelling seats | 3 | 3 | = |

## Open on v3

1. **The bed must be converted every day.** [about-us](../doc/about-us.md) says we are happy
   to *leave the rear bed made up and live in the front lounge*. A front bed removes that
   option — the platform out blocks the entry and the lounge both. The slide makes the
   conversion fast, but it does not make it optional. **This is the real cost of v3 and it is
   worth being sure about before going further.**
2. **No clear rear exit at night.** The rear doors are the bathroom and the closet; the
   slider is behind the bed. Exits at night are: over the bed through the slider, or over the
   bench and through the cab. Both work — but check it against the motor-caravan registration
   rules, which may have something to say.
3. **Slide-out runners.** 760 × 1232 of platform plus two people is 200 kg-plus. Full-extension
   runners rated for it are heavy and expensive; drop-down legs at the outer edge are the cheap
   way to carry it. Decide which before the bench is built.
4. **Where the backrest cushions go.** They are the platform's mattress, so they must stand up
   against the bulkhead by day: ~0.94 m² of cushion against ~0.92 m² of backrest. It fits, just.
   Mock it with foam offcuts.
5. **Rear doors.** Confirm the bike rack swings away, and decide whether the bathroom gets a
   window in the rear door or in the driver-side panel.
6. **The two sliding panels.** Only one of the bathroom and the closet is open at a time.
   Confirm that is acceptable before committing to one track.
7. **WC on the diagonal.** Works on paper at ~1280 mm across the corner. Sit on a real cassette
   inside a 800 × 1000 box before the walls are cut.
8. **Drawer fridge on a plinth over the arch.** 300 arch + ~525 unit = 825 under a 900 worktop.
   75 mm of margin. Confirm with the actual model before ordering.
9. **No 3D yet.** `model3d.py` has no `REGISTRY` entry for v3, so nothing has been checked for
   fit. That is the next step, and it is where v1 and v2 both found real clashes.
