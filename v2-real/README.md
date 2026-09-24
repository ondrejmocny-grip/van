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

## State on 2026-09-24

Identical to v2. The 3D model is the same geometry; `check()` passes on all 15 appliances.

## The plan: from schema to buildable

Order matters: each step sets the limits for the next.

### 1. The real van body — not started

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
