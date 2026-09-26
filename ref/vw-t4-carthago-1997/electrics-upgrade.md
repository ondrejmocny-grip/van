# Upgrading the electrics — can this van run an office day?

[← back to overview](README.md) · factory electrics are in [living.md](living.md#electrics)

Written 2026-09-26. **Short answer: yes.** It is a well-known upgrade for old campers, and
this van suits it better than you might think: it does **all heat on gas** (fridge, cooking,
hot water, heating). So the battery only has to run the office, lights and the pump.

## 1. What we need per day

The Crafter's lean day is ≈ 2.9 kWh ([v2-real](../../v2-real/README.md)) because it cooks and
cools on electricity. Here those run on gas, so the day is much smaller:

| Load | Power | Hours | Wh / day |
|---|---|---|---|
| Laptop, via a 12 V USB-C charger (no inverter) | 50–60 W | 9 | ≈ 500 |
| Monitor (12 V or USB-C) | 20 W | 8 | ≈ 160 |
| 4G / 5G router + roof antenna | 10 W | 24 | ≈ 240 |
| LED lights (after swapping the halogen spots) | 10 W | 4 | ≈ 40 |
| Water pump, phones, small things | — | — | ≈ 50 |
| Truma heater fan (only in cold weather) | 10–15 W | — | 0–100 |
| **Total** | | | **≈ 1.0 kWh** (1.1 with heating) |

**Not on the battery:** the RM 185 fridge. It runs on **gas when parked**. On 12 V it draws
≈ 10 A, which is why the factory only lets it run on 12 V while the engine runs. Keep it that way.

## 2. What charges the battery

| Source | Gives | Notes |
|---|---|---|
| **Alternator via a DC-DC charger, 30 A** | **≈ 0.40 kWh per hour of driving** | the same figure as our Crafter model at 30 A |
| **Portable solar 200 W** | **≈ 0.6–0.8 kWh a sunny day** | can be aimed at the sun and parked in shade; less in winter |
| Portable solar 2 × 200 W | ≈ 1.2–1.6 kWh a sunny day | covers a full day by itself in summer |
| Shore power (campsite) | full charge overnight | needs a lithium charger (see §3) |

**Parked week, no driving, 200 Ah battery (≈ 2.3 kWh usable):**

| Solar | Per day | The battery lasts |
|---|---|---|
| none | −1.0 kWh | ≈ 2 days |
| 200 W portable | −0.2 to −0.4 kWh | **≈ 6–10 days** |
| 400 W portable | ≈ 0 or better | **indefinitely in sun** |
| 200 W + **1 hour of driving every 2–3 days** | ≈ 0 | indefinitely |

So: **DC-DC + 200 Ah lithium + one 200 W portable panel** is enough for our pattern — we
drive regularly anyway. A second panel makes a sunny parked week self-sufficient.

## 3. The upgrade, part by part

| Part | Choice | Why | € (from our budgets) |
|---|---|---|---|
| **Battery** | **LiFePO4 200 Ah** (e.g. Power Queen 200 Ah, as in [low budget](../../v2-real/lowbudget/budget.md)) — or 100 Ah if the space is small | ≈ 22 kg vs ≈ 18 kg for the old 60 Ah lead-acid → **almost no weight added**, 6× the usable energy | ≈ 510 |
| **DC-DC charger** | **Victron Orion XS 12/12-50** set to **30 A** in the app — or Renogy **DCC30S** (DC-DC + MPPT in one box) | a 90 A alternator also feeds the engine, lights and cab A/C — 30 A is the safe share. Lithium needs its own charge profile; the old relay cannot give it | 200–250 |
| **Solar controller** | **Victron MPPT 75/15** (for 200 W) or 100/30 (for 400 W) — not needed with the Renogy DCC30S | portable "suitcase" panels often bring their own controller; pick panels **without** one and use a fixed MPPT inside | 70–120 |
| **Solar inlet** | an **Anderson / SAE socket** on the body near the sliding door, or through a window seal | one small hole low on the steel body — **not in the roof** (the roof joint is this model's weak point) | 20–40 |
| **Portable panel** | **200 W folding blanket or suitcase panel**, 12 V (Voc ≈ 22–24 V), 5–10 m extension cable | stored in the garage or under the bench, set out when parked | 200–350 |
| **Mains charger** | **Victron Blue Smart IP22 12/15 or 12/20** | the factory **Schaudt LA 110 is for lead-acid only** — it must **not** charge lithium. Disconnect it from the leisure battery | 90–130 |
| **Battery monitor** | Victron SmartShunt or Junctek shunt | the Schaudt panel LEDs read lead-acid voltages; they will lie with lithium | 40–80 |
| **12 V USB-C PD sockets** | 2 × 100 W USB-C PD (laptop + monitor) | charges the laptop **without an inverter** → ≈ 10–15 % less energy lost | 40–80 |
| **LED bulbs** | replace the halogen spots | halogen ≈ 10–20 W each, LED ≈ 2 W | 30–60 |
| **Fuses and cable** | main fuse at the battery (the early Malibu had **none**), 16–25 mm² to the DC-DC | the Schaudt box stays for distribution | 60–120 |
| **Inverter** (optional) | a small one, e.g. Victron Phoenix 12/500 | only for things that need 230 V off-grid. Skip if the laptop runs on USB-C | (130–160) |
| **Total** | | | **≈ €1,250–1,700** (+ inverter) |

This is lower than the ≈ €2–3k guess in [vs-our-plan.md](vs-our-plan.md#money-rough). The
reason: no big inverter and no fixed roof panels.

## 4. How it wires into the old Schaudt box

```
 alternator ──► starter battery ──► DC-DC 30 A ──► LiFePO4 ──fuse──► Schaudt EZ 90 (12 V out)
                      │                              ▲    ▲
                      │ (D+ relay, stays)             │    │
                      └──► fridge 12 V while driving │    └── MPPT ◄── Anderson socket ◄── portable panel
                                                     │
                     230 V shore ──► Blue Smart charger (the old LA 110 disconnected from the battery)
```

- **Keep the Schaudt relay for the fridge.** Only take the **leisure battery** off the relay and
  put the DC-DC between the batteries instead. Otherwise the relay would bypass the DC-DC.
- The DC-DC can start on the **D+ signal**, which the Schaudt box already has.
- The T4 alternator is an **old, non-smart type** (Euro 2) — a steady 14 V+. That makes the DC-DC
  simple. No "smart alternator" mode is needed.
- **Read the alternator label first:** 90 A or 120 A. With 120 A the DC-DC can go to ≈ 40 A.

## 5. Where it goes

- **Battery:** in the old battery's place, if a 200 Ah case fits (≈ 520 × 240 × 220 mm). If
  not, **2 × 100 Ah** in two spots, or 100 Ah only (then 1–2 panels become more important).
  **Measure the space when you see the van.**
- **LiFePO4 must be inside**, not under the floor. It must not charge below 0 °C, but we chase
  warm weather, so this is fine.
- **DC-DC, MPPT, shunt:** close to the battery, short cables.

## 6. Why portable solar, not roof

| | Portable | Fixed on the GRP roof |
|---|---|---|
| Holes | one small one in the steel side | roof cable gland + glued mounts, **on the roof this model leaks from** |
| Park in shade | **yes** — the van stays cool, the panel sits in the sun | no — the van must stand in the sun |
| Aim at the sun | yes → more energy in winter / morning | flat |
| Charges while driving | no | yes |
| Can be stolen / must be set up | yes | no |
| Roof space | — | tight: two hatches, ≈ 1 panel of 150–200 W at most |
| Height | unchanged | +≈ 50 mm (≈ 2.80 m) |

For Morocco and Turkey, **parking in shade and putting the panel in the sun** is a real
advantage for a van with no roof fan and no A/C when parked.

## 7. Paperwork

- 12 V changes inside (battery, DC-DC, solar) normally **do not change the registration**. A
  motor caravan in CZ has no extra approval for them — **confirm with the STK station**.
- 230 V work (new charger on the mains side, any inverter wired into the sockets) should go
  through an electrician and a new **elektro revize**. The dealer offers one for free — ask
  whether they would do it **after** the upgrade.

## 8. What it still does not fix

- **The office space.** Energy is solved; the desk is not. The dinette table is the only work
  surface.
- **Heat.** No roof fan when parked. A **12 V roof fan in one of the two hatches** (e.g. a
  MaxxFan-size unit needs a 40 × 40 cm hatch — check the hatch size) would use ≈ 0.1–0.3 kWh a
  day and matters more than any solar in Morocco.
- **Gas.** With the fridge, cooking and hot water on gas, 2 × 5 kg lasts roughly **2–3 weeks**
  in summer (guess). Swapping German bottles abroad is hard; a refillable LPG bottle is the
  usual fix and needs its own gas revize.
