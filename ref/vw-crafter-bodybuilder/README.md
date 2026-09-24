# VW Crafter — official body builder data

Found 2026-09-24. VW publishes this for converters on the **CustomizedSolution Portal**. It is
free and needs no login. It covers our van: Crafter panel van (Kasten) **L3H3, AWD (4MOTION)**,
model year 2017 and later.

**Open this first:** [sheet.png](sheet.png) — the four views that matter, on one page.

## The files

The source files are big (up to 700 MB unpacked), so **they are not in git**. Download them from
here:

| File | What it holds | Size |
|---|---|---|
| [Construction dimensions, panel van L3-L5 / H2-H4](https://storage.customized-solution.com/csp-public/content/Technische-Informationen/Crafter/Technische-Zeichnungen/2024/7C0_000_011____DRW_N2D_014_____BMZ_CNF-TGE_KASTEN_MIT_E-CNF___20250210.pdf) (PDF, 1 sheet A0+4, scale 1:10) | outside and inside dimensions, sections, underbody for each drive type | 24 MB |
| [Same drawing as DXF](https://storage.customized-solution.com/csp-public/content/Technische-Informationen/Crafter/Technische-Zeichnungen/2024/7C0_000_011____DRW_N2D_014_____BMZ_CNF-TGE_KASTEN_MIT_E-CNF___20250210.zip) | CAD lines, for exact geometry later | 59 MB zip, 704 MB DXF |
| [Converter guidelines EN, Sept 2026](https://storage.customized-solution.com/csp-public/content/Technische-Informationen/Crafter/2026/Converter-guidelines-The-Crafter-EN-36-2026.pdf) | the rules: what you may cut, drill, fix | 17 MB, 393 pages |
| [Body builder guidelines EN, 2023 edition](https://storage.customized-solution.com/csp-public/content/Technische-Informationen/Crafter/Body-builder-guidelines-Crafter-EN-48-2023_01.pdf) | older edition, closer to our 2023 van | 16 MB |
| [Foil template L3H3 (TGE = MAN twin, same body)](https://storage.customized-solution.com/csp-public/content/Technische-Informationen/Crafter/2026/Beklebungsvorlagen/7C0_000_011____DRW_TZ__002_____FOILTEMPLATES_PV___L3H3___MAN__20260720.pdf) · [DXF](https://storage.customized-solution.com/csp-public/content/Technische-Informationen/Crafter/2026/Beklebungsvorlagen/7C0_000_011____DRW_TZ__002_____FOILTEMPLATES_PV___L3H3___MAN__20260720.dxf.zip) | outside panel outlines — for window positions later | 5 / 12 MB |

Portal page: [customized-solution.com → Crafter → Technical information](https://www.customized-solution.com/en/en/models/the-crafter/technical-information).

VW's own warning on the drawing: *the dimensions are standard values; measure the real vehicle
before planning.* So these replace our brochure numbers, and the tape measure replaces these.

## How the numbers below were read

- The sections in the drawing are drawn on the **low floor** (FWD). Our 4MOTION van has the
  **high floor**: the same body, with the floor **100 mm higher**. VW's own tables confirm it:
  inside height 1961 → **1861**, slider opening height 1822 → **1722**, rear door opening
  1840 → **1740**. So every height below is **already converted to our floor** (low floor − 100).
- Heights of section lines were read off the drawing at 1:10 — about **±10 mm**. Numbers VW
  writes on the drawing are exact (for VW), and are marked **VW**.
- **Our x.** Our x = 0 is the front bulkhead (the partition) at floor level. On the drawing
  that is about **VW X 1370** (VW X = 0 is the front axle). This is derived: the rear axle
  (VW X 3640) sits at the centre of the wheel arch, and the floor is 3390 long. So
  **our x ≈ VW X − 1370**.
- **Our y.** The real centre line is y = 916 in our model. Widths below are wall to wall
  (to the lashing rails, the inner face of the ribs).

## What the body really is

### Cross-section (width of the load area, by height above OUR floor)

| Height above our floor | Width, wall to wall | Where from | Our model today |
|---|---|---|---|
| ~300 | **1776** (888 + 888) | slider section C-C, **VW** 888 | 1832 |
| ~810 | **1771** (880 + 891) at the slider · **1760** at the rear axle | C-C and D-D, **VW** | 1832 |
| ~1590 | **1477** (736 + 741) | C-C, **VW** | 1832 |
| ~1730 | **1473** | D-D, **VW** "H3 = 1473" | 1832 |
| 1861 | roof (bare metal) | **VW** inside height, high floor | 1781 finished |

**The walls lean in.** From about 800 up to about 1600 each wall comes in by ~150 mm, about
**11°**. Above ~1600 it stays at ~1475 up to the roof. Below 800 it is almost vertical.
**1832 (the brochure width) exists nowhere at a useful height** — our model's box is too wide
by ~55 at the floor and ~350 at the ceiling.

### Along the van

| | Real | Where from | Our model today |
|---|---|---|---|
| Floor length, partition to rear door | **3390** | **VW** L502-2 | 3450 |
| Length at ~900 high, with VW's own partition | 3201 — the VW partition bulges ~190 aft | **VW** L502-1 | — |
| Wheel arch, along x | **x ≈ 1817 – 2728** (911 long) | **VW** 911, position read | 1863 – 2763 |
| Wheel arch height above our floor | **301** | **VW** 401 on the low floor | 350 (WELL_H) |
| Between the arches | **1380** | **VW** W202 | 1380 ✓ |
| Rear axle centre | **x ≈ 2270** | section D-D | — |
| Slider opening | **1311** wide (**1280** at the handle), **1722** high | **VW** L508, H508 | 1300 wide |
| Slider position | centre **x ≈ 960** → about **305 – 1615** | section C-C position | 300 – 1600 ✓ |
| Rear door opening height | **1740** | **VW** H202 | — |
| Door sill (road to floor) | ~670 | brochure | — |

### Under the floor (4MOTION, L3) — see view 4 in the sheet

The view is **from below**, so the driver side is at the **top** of that picture.

| What | Our x (≈) | Side |
|---|---|---|
| Fuel tank | 130 – 1080 | **driver** side, across most of the half |
| Exhaust, catalyst and muffler, then the tail pipe | runs to ~1400 | centre → passenger |
| Box beside the exhaust (probably the SCR / AdBlue tank) | 690 – 1050 | centre |
| **Propshaft** | whole length, to the rear axle | **centre line** |
| **Rear differential** | ~2270 | centre |
| Spare wheel | 2430 – 3230 | centre |
| Lowest point: SCR tank | ground clearance **194 – 212** (**VW**) | — |

## What this means for v2-real

Ranked by how much it changes.

1. **The grey tank does not fit where v2 put it.** v2 has it underslung at x 2100–2800,
   y 400–900 — that is the **rear differential and the propshaft**. Places to check instead:
   the passenger side at x ~0–1400, outboard of the exhaust; or the spare wheel bay
   (x 2430–3230) if the spare goes. The DXF gives exact outlines for this.
2. **The overhead lockers are ~150 mm too deep.** At 1400–1700 the wall is 140–180 mm
   *inboard* of where the model thinks it is. A 300-deep locker measured from the model's
   wall is really ~140 deep. Either they reach further into the room (worse headroom over the
   dinette) or they get shallower.
3. **The bed across the van is short.** Bare width at bed height (630) is ~**1776**, not 1832.
   After wall insulation and cladding (~30 per side) that is **~1715** — Ondrej is 171 cm.
   v2 counted ~1760. This needs a decision, not just a redraw.
4. **The floor is 60 mm shorter** (3390, not 3450). The rear bench / garage loses it, or
   everything shifts.
5. **The galley and benches lose a little aisle.** At worktop height the wall is ~30–40 mm
   inboard per side. The 632 aisle becomes ~570 before cladding, unless carcasses get
   shallower.
6. **Small moves that the model can simply take:** wheel arch x 1817–2728 and 301 high;
   slider 305–1615. All of v2's clearances against the arch still hold (the fridge stops
   ~37 mm short of it instead of 83).

## Rules from the converter guidelines that affect us

| Rule | Page | Why it matters |
|---|---|---|
| **Windows only in the stamped window outlines** in the side panels. Cutting a bigger hole needs a VW letter of non-objection and added stiffness | 209–210 | Window positions are **fixed by the body**, not chosen freely. The foil template / DXF shows where the outlines are |
| Window frames must be sturdy and fixed force-locking to the body | 209 | framed windows, not just glued in |
| **Factory hexagon holes + rivnuts N.909.278.01: max 900 N pull per hole.** Several neighbouring points → use a load rail to spread the load | 332 | how every cabinet, bed and locker is fixed |
| **The tank cap area at the B-pillar must not be covered or blocked** | 332 | **our shower sits in the front driver corner** — check what is inside the body there before drawing the shower wall |
| Door mechanism parts (guide rails, hinges) must stay reachable | 332 | slider rail behind furniture needs a service opening |
| Roof cross struts must not be removed; roof load is limited | 218 | fan and hatch cut-outs must go between the struts |
| At least one anti-roll bar on the front axle (higher centre of gravity) | 333 | check what the van has |

## Still to read

- Chapter 7.6.5 "Shelf installation / installations in vehicle interior" — exact hexagon hole
  positions.
- Chapter 4.3.8 "Vehicle roof / roof load" — for solar, fans and roof rails.
- The DXF: exact wall contour at several x positions, rib positions, and the underbody
  outlines for the grey tank.
