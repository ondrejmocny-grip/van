# v3 — VW Crafter L3H3, bed at the front, bathroom at the back

Started 2026-09-21. **Plan only — first draft, geometry not yet checked in 3D.**

![plan](layout.png)

Regenerate: `python plan.py v3`, from the project root.

Same van and same cab as v2 (Crafter L3H3, 3-seat cab, partition at x = 0). Everything
else is turned around:

| | v2 | v3 |
|---|---|---|
| Bed | rear, across the van | **front, along the van** |
| Bed made from | rear U-dinette | **front L-sofa** |
| Shower | front driver corner | **rear driver corner** |
| WC | drawer under the wardrobe, slides into the shower | **stays in the bathroom** |
| Hanging space | wardrobe 450 × 600 | **full-height closet 800 × 832** |
| Garage | rear bench, 600 × 1832, ~400 clear | **the closet — full height instead of wide** |

## The one thing that decides this layout

**The sliding door is at x 300–1600 — the front half of the van.** A bed at the front and
a door at the front want the same floor. Every choice below falls out of solving that.

A bed **across** the van at the front (v2's bed, moved forward) would be 1520 × 1832 and
would cover the door completely. Worse, by day the table sits exactly where you step in,
and there is then no way past it to the galley — the front becomes a cul-de-sac.

So in v3 the bed runs **fore-aft along the driver side**, and a strip of floor on the
passenger side survives in both states:

| | Clear passenger strip |
|---|---|
| Day, sofa mode | **700 mm** — step in, walk aft into the aisle |
| Night, bed made up | **432 mm** — squeeze, but the rear bathroom stays reachable |

That 432 mm is the whole reason the bathroom can be at the back. Take it away and you have
to climb over a sleeping person to reach the toilet at 3 a.m.

## The L, and how it converts

Two fixed carcasses at seat height 450, in an L around the front driver corner:

| Piece | Size (mm) | Holds |
|---|---|---|
| Long leg — driver wall | **1800 × 600** | **118 L fresh tank** + storage |
| Short leg — bulkhead | **600 × 532** | batteries, inverter |
| Shoe locker | **400 × 700**, top 450 | shoes; the step through to the cab |
| Table | **1000 × 532** at 700, on a drop pedestal | — |

**Day.** L-sofa for 3–4 around the table. Clear floor in front of it, 1200 × 700, straight
off the sliding door.

**Night.** The table drops to 450, the cushions go over it, and two loose boards fill the
strip at y 432–700. Result: **1800 × 1400**, sleeping fore-aft.

| | |
|---|---|
| Body length | **1800** — head at the partition, feet aft |
| Width | **1400** — 700 each for two |
| Headroom over the bed | 1431 |
| Boards to move | table down + 2 infill boards. About a minute. |

**1800 is the longest bed this project has drawn.** v1 was 1730 along the van, v2 ~1760
across after the wall build. At 171 cm that stops being a consideration.

### But three people is worse than v2

1400 ÷ 3 = **466 mm each**, against v2's 507. Small kid included, it is tight.

The fix, when the kid is aboard: **one more board at y 232–432**, taking the bed to
**1600 wide** (533 each — better than v2). The price is the night walkway: gone, so the
bathroom run means crossing the bed. Acceptable on kid nights, not as the default.

## The rear: bathroom and closet, side by side

The rear 800 mm of the van, full width, split down the middle:

| | Size (mm) | |
|---|---|---|
| **Bathroom**, driver side | **800 × 1000**, 1881 clear | sit-down shower + cassette WC, both permanent |
| **Garage closet**, passenger side | **800 × 832**, **full height 1881** | hanging rail + shelves; loaded from the aisle and from the rear door |

**The bathroom is 0.80 m² against v2's 0.56** — 43 % bigger, and it no longer has to play
the sliding-WC trick. The WC lives in the aft-driver corner **on the diagonal**, which is
what makes the knee room work: across the corner you have ~1280 mm, where square to a wall
you would only have 500. Shower seat folds off the forward wall, over the arch nib.

**The wheel arch just reaches in.** The arch runs to x 2763, so it pokes 113 mm into both
forward corners of the rear block, 226 mm wide. On the bathroom side that nib sits under
the fold-down shower seat and disappears. On the closet side it is inside a cupboard. No
raised floor anywhere — v1's "+360 step into the wet cubicle" is not coming back.

**The closet is v2's garage rebuilt vertically.** v2 had 1.10 m² of floor at 400 mm clear
under the rear bench = ~0.44 m³. v3 has 0.67 m² of floor by 1881 high = **~1.25 m³**, and
you can hang a jacket in it. For two people carrying 140 L of belongings, this is more than
enough, and it replaces v2's separate wardrobe as well.

**What it costs: the rear doors.** They now open into the bathroom and the closet, not into
a garage. With bikes on a rear rack they were not a loading route anyway — but confirm the
rack swings away before this is built.

## The galley, in the middle

Both runs sit over the wheel arch (x 1863–2763). That is fine for worktops and forced one
real change:

| Run | Size (mm) | Holds |
|---|---|---|
| Passenger — by the door | **1050 × 600**, worktop 900 | induction 300 × 520 at the door end, **70 L drawer fridge** raised over the arch, prep board |
| Driver | **850 × 600**, worktop 900 | **1.5 bowl** sink (340 wash + 180 rinse), 20 L oven and the pump under |
| Aisle | 1050 × **632** | |

**The fridge goes back to a 70 L drawer, and that is a win, not a loss.** A 90 L upright
cannot live over a 300 mm arch under a 900 worktop — the arithmetic does not close. A
drawer unit at ~525 high sits on a plinth on top of the arch and clears. This also kills
v2's open item #4: no ~530 mm hinged door swinging into a 632 aisle.

**Worktop: 1.14 m²** (v2: 1.18 including its fold-down leaf; v1: 0.66). Near enough, with
no leaf to fold and no door to block.

**The sink is drawn as the 1.5-bowl**, because the driver run is only 850. Two full bowls
(640 + divider) still fit and leave 210 mm of counter — the fallback written up in v2 is
the default here.

## Water, weight and where things sit

**The fresh tank moves to the front, under the long sofa.** Two things follow:

- **No wheel arch at the front**, so this is a **plain rectangular off-the-shelf tank**
  (about 1000 × 400 × 300 ≈ 120 L). v2's open item #2 — a semi-custom 1020 × 374 × 310 —
  goes away.
- **Axle loading gets better, not worse.** Rear axle sits at about x 2313, front axle at
  about x −2177. A mass at the tank's centre (x ≈ 900) puts **68 %** on the rear axle. v2's
  tank at x ≈ 2440 put **103 %** on it. The rear axle is the one that runs out first in a
  camper, so moving water forward buys margin — and the rear bathroom (x ≈ 3050, **116 %**)
  is spending it.

| Service | Where |
|---|---|
| Fresh tank ~120 L | under the long sofa, x 300–1300, driver side |
| Batteries + inverter | under the bulkhead sofa, x 0–600 |
| Calorifier | under the driver galley, aft end — short runs to both the sink and the shower |
| Pump + filter | under the sink |
| Grey | underslung |
| Cassette hatch | driver-side rear quarter panel, x ~2850–3300 |

## v3 against v2

| | v2 | v3 | |
|---|---|---|---|
| Bed body length | ~1760 across | **1800 fore-aft** | +40 |
| Bed for two | 760 each | **700 each** | −60 |
| Bed for three | 507 each | **466** (533 with the extra board) | worse |
| Bathroom | 700 × 800 = 0.56 m² | **800 × 1000 = 0.80 m²** | +43 % |
| WC | slides in from a drawer | **permanent** | simpler |
| Hanging | 450 × 600, ~1281 clear | **832 × 800, full height** | much more |
| Storage volume, closet/garage | ~0.44 m³ | **~1.25 m³** | +180 % |
| Worktop | 1.18 m² (with the leaf) | **1.14 m²**, no leaf | ≈ |
| Fridge | 90 L hinged, blocks the aisle | **70 L drawer** | −20 L, no door swing |
| Entry, clear at the door | 690 | **700 by day**, 432 at night | ≈ |
| Galley aisle | 632 | 632 | = |
| Fresh tank | semi-custom, 103 % on rear axle | **off-the-shelf, 68 %** | better |
| Rear doors | open into the garage | **open into the bathroom and closet** | worse |
| Travelling seats | 3 | 3 | = |

## Open on v3

1. **432 mm night walkway.** Passable sideways, and it is the single assumption the rear
   bathroom rests on. Tape it out on the floor before committing.
2. **Three sleeping at 466 mm.** The extra board takes it to 533 and costs the walkway.
   Decide which state is the normal one when the kid is aboard.
3. **Rear doors.** Confirm the bike rack swings away, and decide whether the bathroom gets
   a window in the rear door or in the driver-side panel.
4. **WC on the diagonal.** Works on paper at ~1280 mm across the corner. Sit on a real
   cassette in a 800 × 1000 box before the walls are cut.
5. **Shower seat over the arch nib.** 113 × 226 in the forward driver corner. Seat height
   has to clear it — check against a real Crafter arch, not the 226 mm figure.
6. **Drawer fridge on a plinth over the arch.** 300 arch + ~525 unit = 825 under a 900
   worktop. 75 mm of margin. Confirm with the actual model before ordering.
7. **Front-heavy water.** 68 % rear is better than v2, but the tank is now next to the
   batteries and the sofa people sit on. Check the front axle load with the tank full and
   three people in the cab.
8. **No 3D yet.** `model3d.py` has no `REGISTRY` entry for v3, so nothing has been checked
   for fit. That is the next step, and it is where v1 and v2 both found real clashes.
