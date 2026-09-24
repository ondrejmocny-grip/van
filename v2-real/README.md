# v2-real — v2 on the real van and real products

Started 2026-09-24 as an **exact copy of [v2](../v2/README.md)**. v2 is a schema: a box van,
placeholder boxes, "+/-50 mm". v2-real turns that same layout into a plan you can build from.

**v2 is now frozen.** All new work happens here. v2-real is built as a copy of v2's tables
plus its own changes, so a later edit to v2 would also change v2-real. Do not edit v2.

![plan](layout.png)

Regenerate: `python plan.py v2-real` then `python model3d.py v2-real`, from the project root.
It is also in the combined viewer: `python model3d.py viewer`.

## Where the changes live

| File | v2-real block |
|---|---|
| `plan.py` | `VARIANTS["v2-real"]` — deep copy of v2, then its own changes below it |
| `model3d.py` | `REGISTRY["v2-real"]` — deep copy of v2's 3D tables, then its own changes below it |

The difference between v2 and v2-real is always what is written in those two blocks.

## State on 2026-09-24 — the real body is in, the furniture is still v2's

**Open:** [sections.png](sections.png) — three cuts across the van (galley, dinette, garage):
the real wall in black, v2's old 1832 box dashed, parts the wall cuts in red. Then
[layout.png](layout.png) — the plan with the real wall in red (solid at the floor, dashed at
1600 high).

### What is modelled now

| | Real (v2-real) | v2 had |
|---|---|---|
| Floor length | **3390** | 3450 |
| Width at the floor → at 900 → from 1540 up | **1776 → 1708 → 1472** | 1832 everywhere |
| Wheel arch | x **1817–2728**, **251** above the finished floor, solid in 3D | 1863–2763, 350, not drawn |
| Slider | x **305–1615**, **1672** high | 300–1600, 1550 |
| Rear door opening | **1690** high | 1700 |
| Ceiling | 1781 finished (unchanged) | 1781 |

All from [ref/vw-crafter-bodybuilder](../ref/vw-crafter-bodybuilder/README.md). The walls in
3D are a staircase of 40 mm bands (boxes cannot slope), never more than 3 mm off the line.

**Placeholder:** the finished floor is taken as 50 above bare metal, the ceiling 30 below the
roof. Wall cladding is **not** in yet - the walls here are bare metal (rib faces). Step 2
replaces both with the real build-up, which takes another ~20-40 mm per side.

### What the real body breaks — 37 parts

`python model3d.py v2-real` prints the full list. It is a report, not a failure, while
`body.strict` is False in `plan.py`; set it True once the list is empty, and from then on a
part hitting the wall fails the build. In groups:

| Group | Parts | How far in | What it needs |
|---|---|---|---|
| **Everything against a wall, low down** | benches, rear bench, bed cushions, shoe locker, cassette, plumbing, electrics | **28–36** | the van is 56 narrower at the floor: carcasses 30 shallower, or the aisle / footwell gives it up |
| **Galley carcasses** (top at 900) | sink and hob runs, worktop leaf, backrest, hob | **50–61** | worktop 60 shallower each side, or the aisle 632 → ~510 |
| **Up high, against the lean** | 4 overhead lockers | **180** | redesign: from 1540 up the wall is 180 in. A 300-deep locker is ~120 deep there |
| **Full-height parts** | wardrobe, 3 shower walls, shower riser | **180 at the top**, 28 at the floor | their outer faces must follow the lean; the shower loses width up high |
| **Taps** | mixer, drinking tap | **96–112** | they stand at the back edge of the deck; move them forward |
| **Length** | rear bench, rear bed cushion, calorifier | **60** (calorifier 10) | the garage is 540 deep now, not 600, or the U moves forward |

Nothing new clashes with the wheel arch or the tyres. The arch is lower and a little further
forward than drawn: the fridge now stops ~37 short of it (was 83).

**Not in this report:** the grey tank (underslung - see below) and the bed length across the
van: 1766 between the bare walls at 570-630, before cladding. **Decided 2026-09-24: the bed
stays across.**

## Decisions 2026-09-24

| | Decision | Status |
|---|---|---|
| Bed | **Stays across the van**, ~1735 after a thin wall build | agreed |
| Galley | **Middle ground** between shallower worktops and a narrower aisle | waits for the cladding number |
| Grey tank | **In the spare wheel bay**, behind the rear axle | modelled; spare wheel home open |
| Cladding | thin build proposed - see below | **to agree with Ondrej** |

## Wall, floor and ceiling build-up — proposal, to agree

**The key fact:** VW's widths are measured to the **rib faces** (the lashing rails). Behind
the rib face there is a cavity of roughly **70–110 mm** to the outer skin (read from section
C-C). **Insulation goes in that cavity and costs no room inside.** What costs room is only
what sits *over* the ribs: a thermal break and the panel.

Our use sets the priorities ([about-us](../doc/about-us.md)): warm weather, no heater, Morocco
in winter, EU in summer. So the job is **keeping the sun out and stopping condensation**, not
holding heat in. The roof matters most; the walls need less than a winter build.

| Layer | Thin (**recommended**) | Standard | Battened |
|---|---|---|---|
| Wall cavity | closed-cell foam on the skin + fill — **0 inside** | same | same |
| Over the ribs | 3 mm thermal-break strip | 10 mm foam | 20 mm battens |
| Panel | 6 mm ply on rivnuts in the factory holes | 6 mm ply | 6 mm ply |
| **Wall, per side** | **~10** | ~16 | ~26 |
| Behind furniture | carcass back on the break strip, ~10 | ~16 | ~26 |
| Wiring | in the cavity and inside carcasses | same | behind the battens |
| **Floor** | 20 XPS between battens + 12 ply + 2 vinyl = **~35** | ~35 | ~35 |
| **Ceiling** | foam between the roof bows + 6 ply = **~15** | ~20 | ~30 |

What each option gives (bare numbers from the VW drawing):

| | Thin | Standard | Battened | v2-real today |
|---|---|---|---|---|
| Bed across (bare 1766) | **~1746** | ~1734 | ~1714 | — |
| Finished height (bare 1861) | **~1811** | ~1806 | ~1796 | 1781 (placeholder 50 + 30) |
| Standing on the 60 mm shower tray | ~1751 — **4 cm over Ondrej** | ~1746 | ~1736 | ~1720 |

**Why thin:** it is the cheapest in room exactly where the van is short (the bed across and
the galley aisle), and it gives back ~30 mm of headroom over the placeholder. It does not
insulate less: the insulation is in the cavity either way. What it gives up is a service
space behind the panels - the wiring runs in the cavity through the existing holes instead,
which is how most Crafter builds do it anyway.

**The galley "middle ground" with the thin build:** the wall at worktop height is 61 in from
v2's line, +10 cladding = 71. Splitting that between the carcasses and the aisle gives
worktops **~565 deep** each side and an aisle **~560** (v2: 600 and 632).

## The grey tank, moved to the spare wheel bay

v2's spot (x 2100–2800 under the middle) is the **propshaft and the rear differential** on a
4MOTION. Read from VW's AWD underbody drawing, the only clear bay big enough is the spare
wheel's: behind the rear axle, between the two chassis rails.

| | |
|---|---|
| Bay (VW) | X ~3830–4560, Y −470…+460, under two crossmembers |
| Bay (ours) | x 2460–3190, y 456–1386 — under the garage |
| Tank drawn | **650 × 800 × 200 = 104 L gross, ~90 usable**, x 2500–3150, y 516–1316 |
| Ground clearance | the tank hangs where the wheel hangs, so no worse than today; the lowest point stays the SCR tank (194–212, VW) |
| Product | **custom tank.** The ready-made Crafter underslung tanks (Wydale 90 L, 63 L) say "does not fit LHD" and the 90 L also "not MWB"; the 82 L one runs between chassis rails over 1700 mm, which on a 4MOTION is the propshaft |
| Drain | at the rear, reachable behind the rear bumper |

The other free spots, both too small alone: driver side between the fuel tank and the rear
axle (~350 × 400, twice), and the passenger side, which the exhaust and the muffler fill.

**Open: where the spare wheel goes.** 235/65 R16 is ~711 across and ~235 wide. It does not fit
the garage (540 deep, 570 high). Likely a **carrier on the rear door**; the alternative is
tyre sealant plus a compressor, which is a poor bet for Morocco.

## The plan: from schema to buildable

Order matters: each step sets the limits for the next.

### 1. The real van body — modelled 2026-09-24

2026-09-24: VW's official body builder drawings are in
**[ref/vw-crafter-bodybuilder](../ref/vw-crafter-bodybuilder/README.md)**. The big findings:
the walls lean in (~1775 wide low down, ~1475 near the roof, not 1832), the floor is 3390 long
not 3450, the arch is 301 high, and **the grey tank as drawn sits on the rear differential**.
Now in the model - see the state above. Next: adapt the layout to it.

| What | Why it matters |
|---|---|
| Wall slope (width at floor, 900, 1700) | the 600-deep galley and lockers lose width higher up |
| Ribs and pillars, positions along x | windows, WC hatch and fans must sit between ribs; furniture fixes to them |
| Real wheel arch shape | batteries have 16 mm, the fridge 83 mm — the real arch is curved, not a box |
| Real slider opening and step | lobby and entry are sized to it |
| **4MOTION underbody** | propshaft, exhaust, fuel and AdBlue tanks, spare wheel — does the underslung 70 L grey tank fit at all? **Biggest unknown.** |
| Roof ribs | fan cut-outs, solar rail feet |
| Cab bench | middle backrest folds? head restraint lifts out? — the crawl-through needs both |

Sources, best first: VW body builder guidelines for the Crafter (drawings; CAD data for
converters to be checked), then **measuring the real van** once bought — measured data
replaces brochure data.

### 2. Wall, floor and ceiling build-up — not started

Model the layers (metal → insulation → battens → cladding, each with a thickness) and
calculate the finished interior from them, instead of assuming "finished" sizes.

### 3. Product register — not started

One entry per real product: brand + model, shop (CZ or EU), outer size, **required
clearances** (ventilation, service access, hose and cable exits), weight, price, power.
Appliance sizes then come from the register. The same data gives the v2-real budget, the
weight/payload check and the daily energy use.

| Priority | Item | Note |
|---|---|---|
| 1 | Windows (Crafter-specific), roof fans | they cut the metal |
| 2 | WC | fixed cassette vs portable — sliding into the shower is non-standard; max ~520 deep |
| 3 | Fridge 90 L, sink + tray, hob, oven | set the galley carcasses |
| 4 | Fresh and grey tanks | catalogue size, or a custom tank |
| 5 | Batteries, inverter, MPPT, DC-DC, calorifier, heater | need airflow and service access |
| 6 | Shower tray | probably custom — size it last |

### 4. From boxes to parts — not started

Panels at real board thickness → cut list; fixing points to ribs / rivnuts; wiring and
plumbing diagrams with lengths; cut-out drawings from body landmarks; check against Czech
motor-caravan homologation before building.
