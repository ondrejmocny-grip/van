# v2-real — v2 on the real van

Started 2026-09-24 as a copy of [v2](../v2/README.md). v2 is a schema: a box van, placeholder
boxes, "+/-50 mm". v2-real is the same layout **on the real Crafter body**, with the wall
build-up we agreed, so it can become a plan to build from. **v2 is frozen.**

![plan](layout.png)

**Viewer:** the **Roof + kit** button (off by default) shows the roof with its real fan
cut-outs, the two MaxxFans, the two solar panels and the Starlink Mini, at catalogue size.

**Open:** [roof.png](roof.png) — the roof from above.

**Open:** [sections.png](sections.png) — three cuts across the van (galley, dinette, garage):
finished walls black, bare rib faces grey, v2's old 1832 box dashed.

Regenerate: `python plan.py v2-real` then `python model3d.py v2-real`, from the project root.
It is also in the combined viewer: `python model3d.py viewer`.

## Where it lives

| File | v2-real block |
|---|---|
| `plan.py` | `VARIANTS["v2-real"]` — its own box list, and `body=`: the VW wall profile, arch, openings, and the build-up |
| `model3d.py` | the v2-real section — `HEIGHTS_V2R`, `EXTRA_V2R`, `APPLIANCES_V2R`, `SITTER_V2R`; the rest (windows, fans, partition, layers) is still v2's |

The frame is v2's: y against the old 1832 box lines, so the real centre line is at y 916 and
the walls stand inside 0 and 1832. A part that does not touch a wall kept v2's numbers.

**The body check is strict.** `python model3d.py v2-real` fails if any part — or any seated
person — runs into the finished walls, past the rear doors, or into the roof. Today: none.

## State on 2026-09-24 — v2's room, fitted to the real body

| | **v2-real** | v2 |
|---|---|---|
| Floor length | **3390** | 3450 |
| Between the finished walls: floor / 900 / from 1555 up | **1756 / 1693 / 1452** | 1832 |
| Finished height | **1811** (bare 1861 − 35 floor − 15 ceiling) | 1781 |
| Wheel arch | x 1817–2728, **266** high | 1863–2763, 350 |
| Slider | x 305–1615, 1687 high | 300–1600 |
| **Galley** | worktops **565** deep each side, aisle **562** | 600 / 632 |
| **Bed across** | **1744** (cushions 44–1788) | 1832 |
| Benches | 557 deep (wall side moved in 43) | 600 |
| Garage | **540** × 1746 × 570 | 600 × 1832 × 570 |
| Overhead lockers | **250** deep over the galley, **220** over the dinette, standing further into the room; the dinette pair 30 higher (110 over a seated head) | 300 / 260 from the box line |
| Wardrobe | 554 deep at the base (WC under it), back follows the lean above 775 | 600, square |
| Shower | 762 → 562 deep at the floor, wet lining follows the lean | 800 → 600 |
| Taps | 130 forward, to the back edge of the bowl | at the back of the deck |
| WC | **≤ 520 deep** (420 × 520 drawn), emptied **inside** — no body hatch | 420 × 570, hatch in the side panel |
| Grey tank | **~85 L inside, under the raised footwell** (made to size); the spare wheel stays in VW's bay | 70 L underslung, on the rear differential |

**Two things the lean costs that are easy to miss:**

- **Seated people sit ~100 further into the room.** Your hips are on the cushion at the wall,
  but your shoulders meet the wall ~100 further in (at 1480 the wall is 176 in). So at the
  dinette the trunk, thighs and shins all move toward the table. The check now carries that.
  The table still clears the knees.
- **Up high, depth moves into the room.** Every locker is ~140 nearer the centre than in v2 to
  stay usable. Over the galley the locker front is at 1392 against a worktop front at 1197.

## Wall, floor and ceiling build-up — thin, agreed 2026-09-24

**The key fact:** VW's widths are measured to the **rib faces** (the lashing rails). Behind
the rib face there is a cavity of roughly **70–110 mm** to the outer skin (read from section
C-C). **Insulation goes in that cavity and costs no room inside.** What costs room is only
what sits *over* the ribs: a thermal break and the panel.

Our use sets the priorities ([about-us](../doc/about-us.md)): warm weather, no heater, Morocco
in winter, EU in summer. So the job is **keeping the sun out and stopping condensation**, not
holding heat in. The roof matters most; the walls need less than a winter build.

| Layer | **Thin (agreed)** | Standard | Battened |
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

## Payload — just under the limit (2026-09-24)

`python payload.py` writes **[payload.md](payload.md)**: every item with its weight, its
source and its place along the van, against 3500 kg, the two axles and the roof.

**Changed 2026-09-24 (Ondrej):** **bikes left out** for now; **solar cut to one ~200 W
panel**, relying more on charging while driving; **awning added** (Thule Omnistor 6300,
3.25 m); **batteries stay 300 Ah** (2 x 150).

| | Poplar furniture | Birch furniture |
|---|---|---|
| **Total, full fresh water (~108 L)** — full gas, 2 panels, tarp, C95L, passenger 55 kg, MultiPlus C 12/2000 (2026-09-25) | **3471 — 29 under** | 3594 — 94 over |
| Rear axle (max 2100) | 1997 | 2098 |
| Front axle (max 1800) | 1473 | 1496 |
| Roof load (max 150) | 51 | 51 |

| **Registration test** — empty converted van + 75 kg x 2 seats + 90 kg luggage allowance | **3344 — 155 under** (stricter, with water + gas: 3464) | — |

**Two different limits:**

- **Registration (the STK, once):** the converted van **empty**, plus the other two seats at
  75 kg and a luggage allowance, must stay under 3500 — otherwise it is not approved with 3
  seats. **We pass by 146 kg** (poplar).
- **On the road (every day):** the van **as loaded** must stay under 3500 and each axle under
  its limit. That is the 3491 above — the tight one. It is the law, not comfort: over it is a
  fine at a roadside weigh check, a possible insurance problem after an accident, and brakes,
  tyres and axles working beyond what they were rated for.

**Read on that:**

- **Poplar furniture is a must.** With it the van is inside every limit — only just.
- **8 kg is no margin.** Driving with ~40 L of fresh water instead of 108 gives ~85 kg of room.
- **The biggest unknown is still the van itself** (2440 is the listing; VW allows ±3-5 %).
  **Weigh it, per axle, before the build.**
- **The rear axle got its room back** with the bikes gone (93 kg under). Bikes on the rear
  doors would cost ~1.4 kg on that axle per kg of bike.

**Less solar, more alternator:** one ~200 W panel gives roughly 0.6–0.8 kWh on a sunny day.
To lean on driving instead, the DC-DC charger can go from 30 A to **50 A** (~0.65 kWh per hour
of driving) — a daily energy check is the next thing to do before settling the size.

The furniture is estimated from the model's boxes (±20 %); the passenger (55 kg) and child
(25 kg with seat) weights are confirmed by Ondrej 2026-09-25.

## Changed 2026-09-25 — full gas, tarp, bigger fridge, galley at 920

- **Full gas:** a **Thetford Topline 922** 2-burner gas hob in the induction hob's slot (12 V ignition), a **Truma B10** gas water heater
  where the calorifier was, a **6 kg bottle** in a sealed locker in the garage. Solar back to
  **2 panels**.
- **Tarp** on a keder rail instead of the Thule awning (−25 kg).
- **Vitrifrigo C95L** fridge: 95 L with a 12.8 L freezer, standing low under the hob.
- **The galley is 920 high** (v2: 900) to give the fridge room — the carcasses are 562 deep
  now, since the wall is 3 further in at 920; taps and sink moved up with it. The dinette table
  stays at 900.

**Also decided 2026-09-25:**

- **The gas bottle stays in the garage** (6 kg) and the oven stays under the sink. Considered and
  dropped: the oven at eye level in the sink locker's place, with the bottle under the counter —
  it fits (even an 11 kg bottle), but a hot drop-down oven door at 1.4 m and the lost locker
  were not worth it. Also dropped: a longer hob run forward — it would close the sliding door
  entry from ~690 to ~290.
- **An outside fresh water filler** — lockable, marked WATER.

**Every hole in the body, as of 2026-09-25:**

| Opening | Where | Size |
|---|---|---|
| 3 x Dometic S4 windows | in VW's stamped window fields | cut-outs 902 x 448 (2), 500 x 348 |
| 2 x MaxxFan | roof, clear of the known bows (measure the rest first) | 400 x 400 |
| Fresh water filler | passenger side, x ~2900, low, above the tank | ~60 |
| Campsite power inlet | driver side, x ~2990, low, at the garage | ~70 |
| Truma B10 flue | passenger side, x ~3200, low | ~70 |
| Grey tank drain + valve | floor, under the footwell | ~40 |
| Fresh tank vent / overflow | floor, by the tank | ~20 |

The side ones are in the model and the viewer (as small hatches). No hole in a pillar;
corrosion protection on every cut.

## Energy — 3 panels, 50 A DC-DC, lean use (2026-09-25; then full gas, 2 panels)

`python energy.py` writes **[energy.md](energy.md)**: every load per day type, and a
simulated week (work Monday to Friday parked, drive 2 h on Wednesday and 4 h on Saturday) for
several set-ups, in three seasons.

**Chosen:** **3 panels (~600 W)**, a **50 A DC-DC** (Orion XS), batteries **300 Ah**, and
**lean use**: **Starlink Mini** (25–40 W instead of 75–100), the inverter in **search mode**,
**hot water only from the engine or at a campsite**.

| One week | Morocco, winter | EU, summer |
|---|---|---|
| v2 plan: 1 panel, 30 A | empty — 19 kWh short | empty — 19 kWh short |
| **Chosen, no campsite** | empty — 2.7 kWh short | just ok (lowest 3 %) |
| Chosen + campsite once a week (Friday) | empty — 2.7 kWh short | just ok |
| **Chosen + campsite twice a week** | **ok — lowest 9 %** | **ok — lowest 45 %** |
| Chosen, **cooking on gas** — no campsite | **ok — lowest 75 %** | **ok — lowest 100 %** |

- **"Occasional campsite" means about every 3 days** off the summer sun: once a week comes too
  late, the shortfall builds up from Monday.
- **Cooking is the biggest load** (~1.1 kWh a day). Taking it off the battery - on gas - makes
  the van self-sufficient in every season without any campsite. See the question below.

**Full gas** (cooking + hot water on gas, asked 2026-09-25): with **2 panels** the week is ok
in summer and just reaches a Moroccan winter week (lowest 7 %, with the smaller MultiPlus C
12/2000 in search mode - it was 0.2 kWh short with the 12/3000); with 3 panels it is self-sufficient
everywhere. Hot water on gas is **comfort, not energy**: lean use already takes it off the
battery — gas gives hot showers on parked days too.

**A parked working day, lean:** ~2.9 kWh. Usable battery 3.46 kWh; 3 panels 1.8–2.5 kWh a day;
driving 0.67 kWh per hour.

## Kitchen — proposed 2026-09-24

Isotherm Cruise 85 fridge, Bosch PIB375FB1E hob (limited to 2000 W), Quadron Anthony 50 sink
(440 x 440), Tefal Optimo OF4448 hot-air oven — see [products.md](../doc/products.md). In the
model: the fridge 85 L at the hob run's front, the sink 80 deeper with the **taps aft of the
bowl**, the oven 288 tall and 462 wide — which **fixes v2's oven running 20 mm into the sink
bowl**. The check now tests built sink parts against the appliances.

## Windows and fans — chosen 2026-09-24

From the product register ([doc/products.md](../doc/products.md), numbers in `products.py`).
The body check now also fails a window outside VW's stamped window fields, or a roof cut-out
over a known roof bow.

| | Product | Where (x, height above floor) |
|---|---|---|
| Over the sink | Dometic S4 500 x 350 | driver, x 1165–1665, z 1040–1388 — under the sink locker (1400) |
| Dinette, driver | Dometic S4 900 x 450 | x 1940–2842, z 1000–1448 |
| Dinette, passenger | Dometic S4 900 x 450 | x 1940–2842, z 1000–1448 — cross-flow over the bed |
| Front fan | MaxxFan Deluxe, cut 400 x 400 | x 560–960, centre line — VW's roof-hatch pressing, over the lobby |
| Rear fan | MaxxFan Deluxe, cut 400 x 400 | x 2660–3060, over the dinette / head of the bed — moved aft from 2200 on 2026-09-25 to make room for the solar panels. **Bow positions to measure first** |

**Changed from v2:** v2 had four windows — one crossed the pillar between the two driver
fields, and three stood above the fields' top (~1473). **The shower window is gone for now**:
inside the field the shower is 470 wide, and the smallest S4 still sold is 500.

**What having no shower window costs** (the smallest S4 still sold is 500 wide; the shower is
470 inside the field):

| Lost | How much it matters |
|---|---|
| Daylight in the shower | little: a short shower in daylight is lit through the 450 opening from the lobby; LED strip for the rest |
| A direct vent for the steam | the real one. The front fan is ~150 from the shower's opening, and the curtain leaves the top open, so run the fan while showering. Condensation lands on the wet lining, which is made for it |
| A view | none worth having in a shower |

| Gained | |
|---|---|
| One hole less in the wall | no leak or rot point in the one wall that is always wet |
| €260–400 and a frame | |
| A continuous wet lining | simpler to seal |

**Decided 2026-09-24: no shower window** — the front fan does the job that matters.

**Also decided 2026-09-24:**

- **No window in the sliding door** — it gets a **fly screen** instead — chosen: the **VanQuito** magnetic net; the Horrex pleated door is
  made for the FWD door height (1822) and our 4MOTION opening is 1722. If a screen ever needs
  room: the shoe locker may shrink, the galley may not. See [products.md](../doc/products.md).
- **No cassette hatch in the body.** The WC's waste tank comes out **inside**, through a door
  in the wardrobe base on the lobby side, and is carried ~1 m to the sliding door. That was
  the only cut outside VW's window fields — no VW letter needed now. A portable WC with its
  own flush tank (e.g. Thetford Porta Potti 565E, 386 x 450 x 447) fits this best.

**Still open:** roof bows 2-3 and 5-6 — measure on the real van before cutting either fan hole.

## The roof — drawn 2026-09-25

See [roof.png](roof.png). From the front:

| Item | Where (x along the van) | Size | Why there |
|---|---|---|---|
| Starlink Mini | x 90–389, centre line | 299 x 259 | front, clear of the panels' shade; one short cable down the lobby |
| Front fan (MaxxFan) | x 560–960 cut, outer 465–1050 | outer 585 x 417 | VW's hatch pressing, over the lobby and shower |
| 2 solar panels, side by side | x 1068–2553, on rails 40 above the roof | 1485 x 668 each | the longest clear stretch between the fans |
| Rear fan (MaxxFan) | x 2660–3060 cut | outer 585 x 417 | over the head of the bed |
| Tarp keder rail | passenger edge, full length | — | the awning side |

- **Roof load:** 51 kg of VW's 150 (see [payload.md](payload.md)).
- **Tight:** ~15 mm between each fan's outer frame and the panels. Fine on paper; on the van
  the panel rails may need to move a little. A panel may also shade a fan lid a bit — no problem.
- **Bows:** only 0, 1688 and 3265 are known. VW's roof-rack points (from the rear: 133, 395,
  661, 852, 1133, 1482, 1759, 2179, 2599, 2878) may sit on bows. The rear fan's cut contains
  the point near x 2870 — **measure before cutting**; the fan can move ~100 either way.
- **Room for a 3rd panel?** No — not without dropping a fan or the Starlink. With full gas, 2 panels are enough ([energy.md](energy.md)).

## Electrics and water products — proposed 2026-09-25

Full list and reasons in [doc/products.md](../doc/products.md). What it changes in the model:

| | Product | In the model |
|---|---|---|
| Batteries | 2 x Ective LC 150 LT, 353 x 175 x 190 | stand across the driver bench, x 2100–2275 and 2340–2515, 190 high (was 240) |
| Inverter | **Victron MultiPlus C 12/2000/80** — replaces the 12/3000 | 520 x 255 x 125 on the shelf over the cells, z 240–365 |
| MPPT, DC-DC, shunt, 230 V box | SmartSolar 100/30, Orion XS 50 A, SmartShunt, 2-pole RCD + 2 MCB | the board in the garage, under the power inlet (unchanged) |
| Fresh tank | made to size, ~108 L | same box; 118 L was the outside volume |
| Grey tank | made to size, ~85 L | same box |
| Pumps | Shurflo Trail King 7 (galley), Whale Gulper 220 (shower tray) | pump in the plumbing box; the Gulper under the shower tray |

- **Weight:** 3471 kg with full water — **29 under** (was 12). The smaller inverter gives 6 kg,
  the real fresh volume 10 kg.
- **Energy:** the MultiPlus C idles at 3 W in search mode (the 12/3000: 8–10 W). The
  Moroccan winter week now just holds (lowest 7 %) instead of 0.2 kWh short.
- **To check:** the MultiPlus C's real size (Victron's datasheet and the shops disagree); the
  Orion XS needs an ignition / D+ wire, because the Crafter's smart alternator can fool it.

## Wiring, gas and water — routed 2026-09-25

Open [systems.png](systems.png) (the routes from above) and [systems.md](systems.md) (every run
with its length, cable size, fuse, and a shopping list). Made by `python systems.py` from the
model's boxes.

**How it is laid out:**

| Where | What |
|---|---|
| **Driver bench, beside the batteries** | the distribution box: a fuse per battery, SmartShunt, busbars, Orion XS DC-DC, the 12 V fuse block; the MultiPlus over the cells; 230 V box B (RCD + 2 MCB) |
| **Garage, driver wall** | MPPT 100/30 and 230 V box A (RCBO), under the power inlet and where the solar cable comes down |
| **Floor channel, centre line** | the starter battery cable from the cab, and the cables to the passenger galley |
| **Up the driver wall, along the ceiling** | fans, lights, Starlink |
| **Passenger side, low** | the gas pipe to the hob (behind the fridge), and the water to and from the Truma B10 |

**Numbers:** ~120 m of 12 V cable, ~12 kg (the thick ones: 95 mm² to the MultiPlus, 50 mm² per
battery, 35 mm² from the starter battery, 5.5 m). 230 V: 8 m. Gas: 5 m of 8 mm copper. Water:
~19 m of 12 mm pipe (7.5 m of it hot and insulated), plus the grey lines.

**What routing it showed:**

- **Water never passes the batteries.** Everything wet crosses the van in the floor at x 1930,
  the galley's aft end, and runs back along the passenger side.
- **The hot water runs are long** (~7.5 m): the Truma B10 is in the garage, the taps are
  forward. ~0.1 L of cold water per metre before hot arrives. Insulate the hot pipe.
- **The shower is the far end of everything:** its drain pump, both water pipes and a light go
  through the WC base. That base needs a removable service panel.
- **The starter battery take-off** is drawn in the cab floor, driver side — find the real
  point on the van (VW's converter guidelines) before buying the 35 mm² cable.
- **The Orion XS moved** from the garage board into the bench, next to the batteries: its
  thick cables stay short.

## The grey tank — inside, under the footwell (agreed 2026-09-24)

**Why it moved at all:** v2 hung it under the middle of the van (x 2100–2800), which on a
4MOTION is the **propshaft and the rear differential**. VW's AWD underbody drawing leaves one
clear bay big enough — the **spare wheel's**, behind the rear axle — and the spare wheel has
to stay there: **the rear doors are kept free for a bike rack**, so there is no spare wheel
carrier on them, and the wheel (~711 across) does not fit anywhere inside.

| | |
|---|---|
| Where | under the raised footwell floor, x 1950–2830, y 616–1216, z 10–190 |
| Size | **880 × 600 × 180 = 95 L gross, ~85 usable** — custom tank |
| Sink | drains by gravity: bowl bottom ~700, tank top 190 |
| Shower | the tray drains at floor level, below the tank top: a **small shower drain pump** |
| Emptying | outlet through the floor at the tank's low point, valve under the van |
| Smell | sealed lid, vent to outside, trap on every inlet |
| Table post | can no longer bolt through the footwell floor: a small frame over the tank carries it |
| Lost | the footwell drawer, ~0.1 m³ |

**The spare wheel bay sets a limit on tyres.** It measures ~730 on VW's drawing for the 712
factory wheel. Bigger all-terrain tyres ([ref/offroad-upgrades](../ref/offroad-upgrades/README.md))
- 744 for 225/75 R16, 774 for 245/75 R16 - may not fit it, which would reopen this question.
Check with the real bay before choosing a tyre size.

The ready-made underslung Crafter tanks never fitted anyway: the Wydale 90 L and 63 L say
"does not fit LHD", the 90 L also "not MWB", and the 82 L runs down the centre where a
4MOTION has its propshaft.

## Where the spare wheel could go — the options we compared, 2026-09-24

The rear-door carrier is out: the rear doors are for a bike rack. The spare is a 235/65 R16: **~711 across,
~235 wide, ~25 kg**. VW's drawing also lists a temporary spare (Notrad) at 15–18.5 kg.

| | Option | Spare wheel | Grey tank | Costs | Verdict |
|---|---|---|---|---|---|
| **A** | **Grey tank INSIDE, under the raised footwell floor** | **stays in its bay, as VW made it** | ~880 × 600 × 180 = **95 L gross, ~85 usable**, x 1950–2830, y 616–1216 | the footwell drawer; a small shower drain pump; a frame for the table post | **chosen** |
| B | Two small tanks under the driver side, between the fuel tank and the rear axle | stays in its bay | 2 × ~26 = ~53 L | two tanks, more plumbing, next to the fuel tank and brake lines, 30 % less capacity | fallback |
| C | Spare on a tow-bar swing-away carrier | on the back, outside | spare wheel bay, 104 L | +~300 length, swing it away for every rear door opening, needs a tow bar | no |
| D | No spare — sealant + compressor | none | spare wheel bay | a torn sidewall on a Moroccan piste ends the trip | no |
| E | Inside: garage or bench | — | — | does not fit: garage 540 deep and 570 high, wheel 711 | impossible |

**Why A won:**

- **The spare stays where VW put it.** Nothing new hangs under the van; the carrier, the
  winch-down and the ground clearance stay as they are.
- **The tank sits in the best place in the van for weight:** low, on the centre line,
  between the axles. Full it is ~85 kg; the spare wheel bay is behind the rear axle.
- **The footwell is already lifted 220 for nothing but storage.** That drawer becomes the tank
  — and we have been cutting storage on purpose anyway ([about-us](../doc/about-us.md)).
- **Gravity still works for the sink:** the bowl bottom is at ~700, the tank top at ~190.
- **The shower tray drains at floor level**, below the tank top, so it needs a small shower
  drain pump either way. An underslung tank at the far end of the van would have needed a long
  falling pipe past the fuel tank instead.
- **Emptying:** an outlet through the floor at the tank's low point, valve under the van.
- **Warm-weather use means no freezing risk** — the usual argument for inside tanks, not against.

**What A costs, honestly:** the footwell drawer (~0.1 m³); a tank inside the living space
needs a sealed lid, a vent to outside and a trap, or it smells; and the table post can no
longer bolt through the footwell floor into the floor pan — it needs a small frame beside or
over the tank, or the tank splits into two either side of the post.

## The plan: from schema to buildable

Order matters: each step sets the limits for the next.

### 1. The real van body — done 2026-09-24

2026-09-24: VW's official body builder drawings are in
**[ref/vw-crafter-bodybuilder](../ref/vw-crafter-bodybuilder/README.md)**. The big findings:
the walls lean in (~1775 wide low down, ~1475 near the roof, not 1832), the floor is 3390 long
not 3450, the arch is 301 high, and **the grey tank as drawn sits on the rear differential**.
In the model, and v2's layout is fitted to it - see the state above.

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

### 2. Wall, floor and ceiling build-up — thin build agreed 2026-09-24

In the model as `floor_build`, `ceiling_build` and `clad` in `body=` (see above). Still to do:
the actual products per layer, and the 70–110 mm cavity depth checked on the real van.

### 3. Product register — started 2026-09-24

[doc/products.md](../doc/products.md) and `products.py`: windows and fans so far.

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
| 5 | Batteries, inverter, MPPT, DC-DC, calorifier, heater | need airflow and service access — **proposed 2026-09-25**, see below |
| 6 | Shower tray | probably custom — size it last |

### 4. From boxes to parts — not started

Panels at real board thickness → cut list; fixing points to ribs / rivnuts; wiring and
plumbing diagrams with lengths; cut-out drawings from body landmarks; check against Czech
motor-caravan homologation before building.
