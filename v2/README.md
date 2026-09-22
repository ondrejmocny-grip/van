# v2 — VW Crafter L3H3, 3-seat cab

Started 2026-09-20. **Plan and 3D model — iterating.** No photoreal impressions yet.

![plan](layout.png)

Regenerate: `python plan.py v2` then `python model3d.py v2`, from the project root.

## The 3D model

**Viewer: [v2 Crafter](https://claude.ai/artifact/4zfKdrCzAheAzWhmKarVFe)** — drag to orbit,
scroll to zoom. Also written locally to `v2/viewer.html`, `v2/model.obj` and `v2/3d/*.png`.

Everything in it is extruded from the box list in `plan.py`, so the model cannot disagree
with the drawing above. What the 3D adds on top of the plan:

| Layer | What it holds |
|---|---|
| Bed made up | the U closed to 1520 × 1832; hides the dinette table and its post |
| Shower + wardrobe | the cubicle's panels, tray and glass screen, and the wardrobe with the WC bay open |
| Worktop leaf out | deploys the galley's fold-down leaf; off, it hangs folded down the galley end |
| Lockers | three overhead runs, kept clear of the door head and the windows |
| Appliances | the kit at real catalogue sizes, and it ghosts the carcasses so you see in |
| Body + glass | panels with real holes: slider, four windows, the cassette hatch, two fans, the partition with its pass-through |
| Cab + seats | the 3-seat cab, dash, wheel, and the four road wheels |
| Detailed props | generated meshes instead of coloured boxes — v2 adds its own for the wardrobe (open WC bay), the shoe locker, the hinged-door fridge, the double sink, both taps and the inline filter. The shower is built from panels, a tray and a glass screen instead |
| **Schema overlay** | the plan itself painted onto the model — pair it with the **Plan** view |
| Sizes | every block labelled with its name and size in mm |

`model3d.check()` passes on all 13 appliances: each one inside the van, inside a carcass,
clear of its neighbours, and clear of the tyres. Two results worth keeping:

- **The fresh tank crosses the bench-to-garage joint and is still housed**, because the U is
  one carcass. The check now accepts a run of carcasses that meet, not only a single box.
- **Nothing touches a tyre or a wheel arch.** The batteries sit 16 mm inboard of the driver
  tyre and the 90 L fridge stops 83 mm short of the arch — both are tight, and both are real.

Brisa's layout ported to our van: shower in the front driver corner, galley split across the
aisle, rear U-dinette. See [ref/doracamper-brisa-ducato-l2h2](../ref/doracamper-brisa-ducato-l2h2/README.md).

## What changed from v1, and why

- **Three front seats** (driver + double bench), so **swivel seats are dropped**. They were
  never going to work against a 3-seat bench, and dropping them also removes the handbrake
  lowering kit and the "does the Crafter have an electronic parking brake" question.
- **Partition wall behind the cab at x = 0**, with a pass-through beside the shoe locker.
- **Three belted travelling seats** instead of two, which also makes the motor-caravan
  registration case simpler, not harder.
- **The bed turned sideways.** 1520 mm fore-aft is enough, even with a child, so you sleep
  **across** the van.
- **No office.** Dropped 2026-09-21. The front corner is a shoe locker and the galley's
  worktop carries on forward over it as a fold-down leaf.
- **The WC left the shower floor.** It stows under the wardrobe and slides forward into the
  shower only when needed — Scarlet & Seth's trick, adapted to a cassette.

## The front corner, and the worktop leaf

No office here any more. What is left is a shoe locker, the step through to the cab, and
the galley reaching forward over it when you need prep space.

| | |
|---|---|
| Shoe locker | **400 × 450**, top at 450 — shoes inside, and the step to the cab |
| Worktop leaf | **400 × 600** at **900**, the galley's own height — fold-down |
| Mount | hinged on the hob unit's forward end panel, swing-out bracket under it |
| Folded | hangs flat down that same panel, x 1090–1150 |
| Cab pass-through | beside the locker, **432 wide**, in the bulkhead |
| Clear floor in front of the shower | **582** between the locker and the screen, up from 432 |

The locker earns two jobs from one box: shoe store, and the thing you put a knee on going
through to the cab. It lost 50 mm fore-aft and 150 mm across to give the lobby in front of
the shower more room.

**With the leaf down, the side door is blocked** — the clear entry drops from 690 mm to
about 290. It folds in a second, and unlike a table nobody is sitting at it, so the cost is
only while you are actually cooking.

Both positions are in the 3D model. **Folded is the default**, because that is the state the
entry gap assumes — the **Worktop leaf out** button deploys it.

`model3d.check()` carries a **person perched on the locker** — trunk, thighs, shins — and
fails the build if any furniture runs through them. Two rounds of the old office table were
drawn with a swing arm through the sitter's chest before it was caught by eye.

## Water at the sink

Resolved 2026-09-21. **Two bowls and two taps.**

| | |
|---|---|
| Sink top | one pressed **580 × 360** inset, two bowls side by side |
| Bowls | **250 × 310** each, 150 deep, 30 mm divider — detergent one side, rinse the other |
| Where | pushed to the **aft end** of the run, x 1350–1930 |
| Prep beside it | **200 mm × 600** of free counter forward of the sink |
| Mixer tap | over the wash bowl, the usual pumped cold and calorifier hot |
| **Drinking tap** | dedicated gooseneck beside the mixer, 250 above the worktop |
| Filter | **inline carbon block**, 2 × 10 inch, teed off the cold line after the pump |

**Why a separate tap and not a 3-way mixer:** filtered water never touches the mixer
cartridge or the hose that has been sitting in the tank, it is a third of the price, and a
failed mixer does not take the drinking water with it. Cost: one more 12 mm hole in the
worktop.

**Why an inline cartridge and not a sump housing:** there is 380 mm of height under the
bowls and a slimline sump needs about 400 to drop the cartridge out of it. An inline
cartridge is swapped by pulling its two hose fittings and can lie on its side — it sits
behind the oven at x 1600–1860, y 1700–1760.

### The drinking water parts, end to end

Five parts, roughly **€90–150** all in:

| | Part | Where |
|---|---|---|
| 1 | Gooseneck drinking faucet | one 12 mm hole beside the mixer, x 1620–1670, 250 above the worktop |
| 2 | Inline carbon block, 2 × 10 inch, quick-connect | behind the oven, x 1600–1860, y 1700–1760, lying on its side |
| 3 | T-piece on the cold line, **after the pump** | the filter needs pressure behind it |
| 4 | Shut-off valve before the filter | so a cartridge change is not a system drain |
| 5 | 8 or 10 mm hose | pump → valve → filter → tap |

**No extra power, and no extra pump.** The 12 V diaphragm pump at 1.5–2 bar pushes a carbon
block fine. You get about **1.5 l/min** at that tap instead of 4 — which is what a drinking
tap should give anyway.

**Cartridge grade — still to decide.** A 0.5 micron carbon block with bacteriostatic silver
covers taste, particulates and most bacteria, which suits filling from campsite taps. Add a
sediment pre-filter only if we expect doubtful sources. Swap every 6–12 months or ~3000 L.

**What this does not solve.** The filter protects what comes out of the tap, not what grows
in the tank. A tank left full and warm for weeks still needs cleaning out — the filter only
means we are not drinking the result.

### Where the prep space comes from

Updated 2026-09-22. 780 mm of run cannot hold two bowls **and** a prep area in the middle, so
both runs now put their kit at one end and keep the counter in one piece:

| Run | Kit | Free counter |
|---|---|---|
| Driver, sink | double sink **aft**, x 1350–1930 | **200 mm** forward of it |
| Passenger, hob | hob **aft**, x 1560–1860 | **410 mm** forward, running straight into the 400 leaf = **810 mm** in one line |

Worktop with the leaf out: **1.18 m² gross, 0.81 m² free** once the sink top and the hob are
off it.

**The cost, and it is a real one: the bowls are 250 × 310.** A 320 mm dinner plate only lies
flat across the diagonal. Making the top 660 wide would give 290 × 310 bowls and leave
120 mm of prep instead of 200. Worth settling with a plate and a washing-up bowl in hand
before the top is cut.

## The bathroom

**Shower: curtain or sliding door, never a swinging one.** That is what lets the shower keep
its 800 mm width without stealing clearance from the lobby. The 3D model draws it as a
**glass screen** on the lobby side — three wall panels, a tray and the screen, built from
the box list rather than from a generated mesh, so you can see into the cubicle from the
aisle and the drawing cannot lie about which side opens.

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
| Shower | **700 × 800**, floor level, 1881 clear | glass screen on the lobby side; WC slides in when needed |
| Wardrobe | **450 × 600** | hanging above (~1281 clear), **WC drawer below** |
| Shoe locker | **400 × 450 × 450** | shoes; doubles as the step to the cab |
| Worktop leaf | **400 × 600** at 900 | fold-down off the galley's end panel |
| Entry, clear at the door | **690** of the 1300 aperture | cab pass-through 432 beside the locker |
| Galley — sink side (driver) | **780 × 600**, worktop 900 | double sink 580 × 360 aft, **200 prep** forward; 20 L oven at the aisle edge, pump behind it |
| Galley — hob side (passenger) | **780 × 600** | induction 300 × 520 aft, **410 prep** forward into the leaf; **90 L fridge** under |
| Galley aisle | **780 × 632** | |
| Bench, driver | **920 × 600 × 450** | 2 × 150 Ah battery, 3000 W inverter |
| Bench, passenger | **920 × 600 × 450** | **118 L fresh tank**, 1020 × 374 × 310, inboard of the arch, running into the rear bench |
| Table → bed | **920 × 632** infill | |
| **Rear bench / garage** | **600 × 1832 × 450**, ~400 clear | calorifier, electrics board |
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
| Galley worktop | 1100 × 600 = 0.66 m² | 2 × 780 × 600 + a 400 × 600 leaf = **1.18 m²** gross, 0.81 free | +79% |
| Hanging space | none | **450 × 600**, ~1281 clear | new |
| Work position | swivel seat + Lagun table | **none** — dropped 2026-09-21 | −1 |
| Fridge | 70 L drawer | **90 L, hinged door** | +20 L |
| Galley aisle | 1232 | **632** | −600 |
| Corridor past the cubicle | 532 | none | gone |
| Entry gap at the slider | 1300 | **690** | −610 |
| Bench storage | 0.89 m² | 2 × 920 × 600 = **1.10 m²** | +24% |
| **Garage** | 450 × 1832 = 0.82 m² | **600 × 1832 = 1.10 m²** | **+33%** |
| Travelling seats | 2 | **3** | +1 |

## Open on v2

1. **The deployed worktop leaf blocks the side door.** 690 mm of entry drops to ~290. It
   folds in a second — but worth feeling before it is built.
2. **Tank shape.** 1020 × 374 × 310 is a semi-custom size. Either have one made, or plumb
   two off-the-shelf slim tanks in series. Confirm before the benches are cut.
3. **Cassette hatch** in the driver-side body panel at x 700–1150. Check it against the actual
   Crafter body — flat panel expected, but confirm.
4. **Fridge door swing.** The 90 L unit is a **hinged door, not a drawer** — a ~530 mm door
   into a 632 aisle blocks it completely while open. Hinge side is a real decision, and it
   matters more at 90 L than it did at 65.
5. **Entry gap 690** and **aisle 632**. Two people cannot pass in the galley.
8. **Bowls at 250 × 310 vs prep at 200 mm.** A 660-wide top would give 290 × 310 bowls and
   drop the prep strip to 120. Decide with a dinner plate and a washing-up bowl in hand.
9. **Drinking water cartridge grade**, and whether a sediment pre-filter earns its space.
6. **Window in the shower** (Brisa's trick) at x 0–700 of the driver-side panel. Clear of the
   cassette hatch at 700–1150.
7. **Wheel-well depth.** v2 uses 226 mm, correct for a 1832 / 1380 Crafter. `v1` still carries
   the Transit's 195 — worth fixing when that variant is next touched.
