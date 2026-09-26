# Base vehicle — VW T4 Transporter LWB, 2.5 TDI, 1997

[← back to overview](README.md)

The van under the camper. Main source: **VW's T4 body builder guide** (Aufbaurichtlinien,
edition 05/2007) — [PDF](https://umbauportal.volkswagen-nutzfahrzeuge.ch/download/Technische%20Informationen/Aufbaurichtlinien/Transporter/Archiv/Aufbaurichtlinien_fm_Transporter_T4_DE_05-2007.pdf).
Other sources are linked per row. Labels as in the [overview](README.md#read-in-this-order).

## VIN

`WV1 ZZZ 70 Z V H 088958`

| Part | Value | Meaning |
|---|---|---|
| 1–3 | WV1 | VW **Commercial Vehicles** (a Caravelle / Multivan bus would be WV2) |
| 4–6 | ZZZ | filler |
| 7–8 | 70 | T4 |
| 9 | Z | filler |
| 10 | V | model year **1997** (could be built from mid-1996) |
| 11 | H | **Hannover** plant |
| 12–17 | 088958 | serial number |

Source: [vwt4forum decode](https://www.vwt4forum.co.uk/threads/decode-your-chassis-number.10621/).
The VIN does not say engine, roof or weight rating. Those are on the **data sticker** (spare
wheel well or service book). PR codes worth reading there: **0J2 / 0J3 / 0J5** (payload class),
**1LE** (heavy front brakes), **1D6** (factory tow bar).

## Engine

| | Value | Source |
|---|---|---|
| Code | **ACV** (1995–2003) | [auto-data](https://www.auto-data.net/en/volkswagen-transporter-t4-facelift-1996-panel-van-2.5-tdi-102hp-l2h1-50435) |
| Type | inline 5, 10 valves, direct injection, turbo + intercooler | [truck1](https://www.truck1.eu/blog/volkswagen-caravelle-t4-2-5-tdi-syncro-102-hp-tech-specs-t32061) |
| Displacement, bore × stroke | 2,461 ccm, 81.0 × 95.5 mm | auto-data |
| Power | **75 kW / 102 PS** at 3,500 rpm | listing, [Wikipedia](https://en.wikipedia.org/wiki/Volkswagen_Transporter_(T4)) |
| Torque | **250 Nm** at 1,900–2,300 rpm | auto-data |
| Compression | 19.0 : 1 or 19.5 : 1 (sources differ) | auto-data, truck1 |
| Injection pump | Bosch **VP37** electronic distributor pump | [RWC](https://www.rwcmotorsport.com/tech/tdi-common-problems.php) |
| Timing | **two belts**: main cam belt (also drives the water pump) + a separate injection-pump belt | [atlib](https://atlib.info/en/blog/182-vw-transporter-25-tdi-acv-t-belt--high-pressure-fuel-pump-belt-replacement) |
| Belt interval | 60,000 km to 80,000 miles depending on source. **No proof of change → change both right after buying** | [autodoc](https://www.autodoc.co.uk/car-parts/timing-belt-10504/vw/transporter/transporter-iv-bus-70xb-70xc-7db-7dw/5281-2-5-tdi), [vwt4forum](https://www.vwt4forum.co.uk/threads/2-5tdi-cam-belt-replacement-interval.4809/) |

## Gearbox and drive

| | Value | Source |
|---|---|---|
| Gearbox | **02G, 5-speed manual** (listing: 5-speed) | [vwt4forum](https://www.vwt4forum.co.uk/threads/the-02g-tdi-gearbox.43862/) |
| Ratios | 3.909 / 2.118 / 1.346 / 0.972 / 0.729, final drive 3.905 | forum, not VW |
| Drive | **front-wheel drive** (no Syncro) | VW guide |

## Driving

| | Value | Source |
|---|---|---|
| Top speed | ≈ 155–157 km/h (bare van; a high-roof camper will cruise at 100–110) | auto-data |
| 0–100 km/h | ≈ 18–20 s bare van; slower as a loaded camper | truck1, guess |
| Fuel, combined | **≈ 10.1 L/100 km** factory; owners report 8.5–9 L at 100–110 km/h (bare van). The high roof adds drag — expect **10–12 L** | auto-data, [spritmonitor](https://www.spritmonitor.de/en/detail/840436.html), guess |
| Fuel tank | **80 L** → ≈ 700 km range | auto-data |
| AdBlue | none | — |
| Turning circle | **12.9 m** | auto-data |
| Steering | rack and pinion, power assisted | guess |
| Towing | **2,000 kg braked** (12 % slope), 700 kg unbraked, 100 kg on the ball. Tow bar **seen** | VW guide p.30 |
| Roof load | 100 kg (in practice the GRP roof has no rails) | VW guide p.13 |
| Licence | B (under 3.5 t) | — |

## Size

The camper sizes first, then the bare VW van for reference.

| | Value | Source |
|---|---|---|
| **Camper length** | ≈ 5,055–5,190 mm. VW: short nose 5,107, long nose 5,189. This van has the **long nose** (TDI facelift look, **seen**) → **≈ 5,190** | VW, [truck1](https://www.truck1.eu/blog/volkswagen-caravelle-t4-2-0i-84hp-lwb-tech-specs-t32001), typical |
| **Camper height** | **≈ 2,750 mm** (Carthago high roof) — check before car parks, ferries, tolls | typical ([ski-web24](https://www.ski-web24.de/Wohnmobil/Malibu/page1.htm)) |
| Width | **1,840 mm** body, **2,175 mm** with mirrors | Wikipedia, auto-data |
| Wheelbase | **3,320 mm** (long) | [T4-Wiki](https://www.t4-wiki.de/wiki/Radstand) |
| Track front / rear | 1,589 / 1,554 mm | auto-data |
| Overhang front / rear | 886 / 901 mm (short nose; long nose ≈ +80 at the front) | auto-data |
| **Ground clearance** | **≈ 150 mm** bare van; the under-floor water tanks may hang lower — measure | truck1, guess |
| Approach / departure angle | not found | — |
| Load floor of the bare van | 2,885 long × 1,620 wide, **1,220 between the arches**, 515 mm above the road | [vandimensions](https://vandimensions.com/database/volkswagen/transporter-t4), VW guide p.7 |
| Sliding door opening | 1,040 × 1,286 mm | vandimensions |

**A note on the nose:** VW's guide lists TDI panel vans (WV1) with the *short* front. The long
nose was normal on Caravelle / Multivan / California. Either this van left the factory with a
long nose on a commercial VIN, or the front was changed. Worth asking; it changes length by 80 mm.

## Weights

VW factory table for 5-cylinder TDI, long wheelbase (VW guide p.11–12):

| Version | Max weight (GVW) | Front / rear axle max | Bare van empty | Bare van payload |
|---|---|---|---|---|
| Panel van **0J2** (standard) | **2,730 kg** | 1,510 / 1,410 | 1,735 | 995 |
| Panel van 0J3 | 2,800 kg | 1,510 / 1,490 | 1,735 | 1,065 |
| Panel van 0J5 / 1LE | 2,890 kg | 1,510 / 1,490 | 1,735 | 1,155 |
| Chassis cab 0J4 (campers only) | 3,300 kg | 1,600 / 1,800 | 1,505 | 1,795 |

**What this means here:**

- The listing's **2,730 kg is exactly the 0J2 GVW** → this is almost surely the plated max
  weight, not the empty weight.
- **No 3.5 t T4 van exists.** The dealer's "do 3,5 t" is about the licence class.
- Carthago Malibu 32.2 units in forum listings: **empty ≈ 2,060–2,240 kg**, GVW 2,640–2,890 kg,
  so **real payload ≈ 300–450 kg** for people, water, gas, food and luggage.
- 2 people (≈ 140 kg) + full water (≈ 60 kg) + gas (≈ 20 kg) + fuel is ≈ 250 kg before any
  luggage. **Weigh it before buying.**
- Uprating to 2,890 kg is possible by single approval with the 1LE brake, steel wheels and
  0J3 springs ([T4-Wiki Auflastung](https://www.t4-wiki.de/wiki/Auflastung)).

## Chassis

| | Value | Source |
|---|---|---|
| Front suspension | double wishbones, **torsion bars** | [de.wikipedia](https://de.wikipedia.org/wiki/VW_T4) |
| Rear suspension | independent semi-trailing arms, **coil springs** | de.wikipedia |
| Brakes | ABS. Front vented disc 280 × 24; rear disc 280 × 12 (1996–2003) — check | [Cool Air VW](https://www.coolairvw.co.uk/product/7d0615301c-t4-front-brake-discs-vented-280x24mm-pr-code-1le-1lu/), [Just Kampers](https://www.justkampers.com.au/7d0-615-601-rear-brake-disc-280mm-x-12mm-for-all-t4-1996-2003.html) |
| Tyres | 195/70 R15C or **205/65 R15C** (205 needed for 2,890 kg) | auto-data, VW guide p.46 |
| Wheels | 6J × 15, **5 × 112**, centre bore 57.1, M14 × 1.5 radius-seat bolts, ET 35–50 | [Vee Dub Transporters](https://www.veedubtransporters.co.uk/2026/05/29/vw-transporter-wheel-fitment-guide/) |
| Seen on photos | steel wheels with plastic caps | seen |

## Vehicle electrics

| | Value | Source |
|---|---|---|
| Alternator | **90 A** standard (120 A on some; VW also offered a 2nd 90 A alternator) | [vwt4forum](https://www.vwt4forum.co.uk/threads/alternator-amp.809570/) |
| Starter battery | ≈ 77–88 Ah lead-acid | forum, guess |
| Cab A/C | yes (listing) | listing |

## Emissions and city zones

| | Value | Source |
|---|---|---|
| Class | **Euro 2** (key no. 0427 / 0633 before week 36/2000) | [T4-Wiki Feinstaub](https://www.t4-wiki.de/wiki/Feinstaub) |
| Germany | **red sticker** → **not allowed** into most German Umweltzonen (they need green). A particle filter retrofit gives green **only for M1 (car) registrations under 2.8 t** | T4-Wiki |
| Czechia | no low-emission zone in force anywhere (2026) | [MŽP](https://mzp.gov.cz/cz/agenda/ochrana-ovzdusi/zdroje-znecistovani-ovzdusi/doprava/nizkoemisni-zony) |
| Elsewhere | France Crit'Air 5 or excluded, many Italian / Spanish / Dutch / Belgian city zones exclude Euro 2 diesel — **check each city** | guess |
