#!/usr/bin/env python3
"""Energy check: what the van uses in a day, what it can put back, and whether 300 Ah holds
over a typical week - for a few set-ups (panels, DC-DC size, Starlink model).

    python energy.py            # -> v2-real/energy.md, and a summary on the screen

Numbers are from datasheets where we have them (source given) and marked "est." otherwise.
Solar yields are rough (flat panel, typical sun for the season and place) - the point is the
comparison between set-ups, not the second decimal.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

BATTERY_KWH = 300 * 12.8 / 1000          # 2 x 150 Ah LiFePO4 = 3.84 kWh
USABLE = 0.90                            # keep 10 % in reserve
INVERTER_EFF = 0.92                      # AC loads cost ~8 % more at the battery (est.)

# Loads: (name, watts while on, hours on per day-type, AC?, source). Hours per day-type:
# work_parked, work_drive, free_drive, free_parked.
LOADS = [
    ("Fridge, Isotherm Cruise 85", None, None, False,
     "Indel Cruise 85: 0.386 kWh/24 h at 25 C; x1.5 on hot days (est.)"),
    ("Induction cooking (hob capped at 2000 W)", 2000, (0.5, 0.5, 0.5, 0.6), True,
     "est. - 30 min at full power a day, incl. kettle"),
    ("Oven, Tefal Optimo 1380 W (3 times a week, 25 min, ~70 % duty)", 1380, (0.18,) * 4, True,
     "est."),
    ("Hot water, calorifier 10 L on 230 V (engine heats it when driving)", 660, (0.7, 0, 0, 0.7), True,
     "Elgena 660 W element; ~0.45 kWh a day incl. losses (est.)"),
    ("Starlink", None, (10, 10, 5, 4), True, "Standard: average 75-100 W (Starlink spec); Mini: see set-ups"),
    ("Laptop + monitor (Ondrej's working day)", 60, (9, 8, 1, 1), True, "est."),
    ("Phones, tablet, second laptop", 25, (6,) * 4, False, "est."),
    ("Lights, 12 V LED", 20, (4,) * 4, False, "est."),
    ("2 x MaxxFan, average", 20, (12,) * 4, False, "0.2-2.3 A each (Maxxair); est. average"),
    ("Water pump", 60, (0.3,) * 4, False, "Shurflo Trail King 7, est. use"),
    ("Inverter idle, in AES mode, off at night", 25, (14,) * 4, False,
     "MultiPlus 12/3000: 30 W idle, 25 W AES, 10 W search (Victron datasheet)"),
]

DAY_TYPES = ("work_parked", "work_drive", "free_drive", "free_parked")
DRIVE_HOURS = {"work_parked": 0, "work_drive": 2, "free_drive": 4, "free_parked": 0}
# A typical week: Ondrej works Monday to Friday from the van; we move on Wednesday evening
# and on Saturday. No shore power all week.
WEEK = ("work_parked", "work_parked", "work_drive", "work_parked", "work_parked",
        "free_drive", "free_parked")
DAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# Solar yield per 200 W panel, kWh/day (est.: flat panel, ~0.75 system factor).
SUN = {"Morocco, winter": 0.60, "Turkey, spring / autumn": 0.70, "EU, summer": 0.85}
HOT = {"Morocco, winter": False, "Turkey, spring / autumn": False, "EU, summer": True}

# "Lean" use: Starlink Mini (25-40 W), the inverter in search mode (10 W), and hot water only
# from the engine or at a campsite - the three biggest cuts that do not touch cooking or work.
# "Shore": a campsite with a hook-up on Tuesday and Friday nights (the MultiPlus charges
# 120 A - full in ~3 h), so the battery starts the next day full.
SETUPS = [
    # name, panels, DC-DC amps, lean, shore days, gas cooking
    ("v2 plan: 1 panel, 30 A DC-DC", 1, 30, False, (), False),
    ("2 panels, 50 A DC-DC", 2, 50, False, (), False),
    ("3 panels (~600 W), 50 A, lean, induction - no campsite", 3, 50, True, (), False),
    ("3 panels, 50 A, lean, induction + campsite twice a week", 3, 50, True, ("Tue", "Fri"), False),
    ("3 panels, 50 A, lean, gas - no campsite", 3, 50, True, (), True),
    ("4 panels (~800 W), 50 A, lean - no campsite", 4, 50, True, (), False),
    ("**Chosen 2026-09-25: full gas (cooking + hot water), 2 panels, 50 A, lean** - no campsite", 2, 50, True, (), True),
    ("Full gas, 1 panel, 50 A, lean - no campsite", 1, 50, True, (), True),
]


def day_use(day, hot, lean=False, shore=False, gas=False):
    """kWh taken from the battery on one day, and the list of (load, kWh)."""
    i = DAY_TYPES.index(day)
    rows = []
    for name, watts, hours, ac, _src in LOADS:
        if name.startswith("Induction") and gas:
            rows.append((name, 0.0))            # cooked on gas
            continue
        if name.startswith("Fridge"):
            kwh = 0.386 * (1.5 if hot else 1.0)
        elif name == "Starlink":
            kwh = (32 if lean else 85) * hours[i] / 1000
        elif name.startswith("Hot water") and (lean or shore):
            kwh = 0.0                            # engine, or the campsite's power
        elif name.startswith("Inverter idle") and lean:
            kwh = 10 * hours[i] / 1000           # search mode
        else:
            kwh = watts * hours[i] / 1000
        if ac:
            kwh /= INVERTER_EFF
        rows.append((name, kwh))
    return sum(k for _, k in rows), rows


def week(panels, amps, place, lean=False, shore=(), gas=False):
    """Run the week from a full battery. Returns (lowest charge %, kWh short, per-day log)."""
    usable = BATTERY_KWH * USABLE
    charge, short, low, log = usable, 0.0, 100.0, []
    for d, name in zip(WEEK, DAY_NAMES):
        use, _ = day_use(d, HOT[place], lean, name in shore, gas)
        gain = panels * SUN[place] + DRIVE_HOURS[d] * amps * 13.4 / 1000
        charge = charge - use + gain
        if charge < 0:
            short += -charge
            charge = 0.0
        charge = min(charge, usable)
        low = min(low, 100 * charge / usable)   # the evening, before any hook-up
        if name in shore:
            charge = usable                      # hooked up for the night
        log.append((name, d, use, gain, 100 * charge / usable))
    return low, short, log


def report():
    out = ["# v2-real — energy check", "",
           "Generated by `python energy.py` — do not edit by hand. The numbers and their sources "
           "are in `energy.py`.", "",
           "**Battery:** 2 x 150 Ah LiFePO4 = %.2f kWh, **%.2f kWh usable** (90 %%). **Driving:** "
           "a DC-DC charger gives %.2f kWh per hour at 30 A, %.2f at 50 A (the Crafter's "
           "alternator is 140-230 A). **Solar:** ~0.6-0.85 kWh a day per 200 W panel." %
           (BATTERY_KWH, BATTERY_KWH * USABLE, 30 * 13.4 / 1000, 50 * 13.4 / 1000), "",
           "## What a day uses (Starlink Standard, mild weather)", "",
           "| Load | Work day, parked | Work day, 2 h drive | Free day, 4 h drive | Free day, parked | Source |",
           "|---|---|---|---|---|---|"]
    per = {d: day_use(d, False)[1] for d in DAY_TYPES}
    lean = {d: sum(k for _, k in day_use(d, False, lean=True)[1]) for d in DAY_TYPES}
    for k, (name, *_rest) in enumerate(LOADS):
        src = LOADS[k][4]
        out.append("| %s | %s | %s |" % (name, " | ".join("%.2f" % per[d][k][1] for d in DAY_TYPES), src))
    out.append("| **Total, kWh** | %s | |" % " | ".join("**%.2f**" % sum(v for _, v in per[d]) for d in DAY_TYPES))
    out.append("| *Lean: Starlink Mini, inverter search mode, hot water from engine / campsite* | %s | |"
               % " | ".join("*%.2f*" % lean[d] for d in DAY_TYPES))
    out += ["", "A parked working day uses **more than the whole usable battery** — so the question "
            "is how often it is filled again.", "",
            "## A typical week without shore power", "",
            "Work Monday to Friday from the van, move 2 h on Wednesday and 4 h on Saturday, rest "
            "on Sunday. Starting full. **Lowest charge** during the week, and the energy that "
            "**was missing** (the battery hit empty):", "",
            "| Set-up | %s |" % " | ".join(SUN), "|---|%s" % ("---|" * len(SUN))]
    summary = []
    for name, panels, amps, lean_use, shore, gas in SETUPS:
        cells = []
        for place in SUN:
            low, short, _ = week(panels, amps, place, lean_use, shore, gas)
            cells.append("%d %% · %s" % (low, "**%.1f kWh short**" % short if short > 0.05 else "ok"))
        out.append("| %s | %s |" % (name, " | ".join(cells)))
        summary.append((name, cells))
    out += ["", "## The week, day by day (chosen: full gas, 2 panels, Morocco in winter, no campsite)", "",
            "| Day | Type | Used kWh | Charged kWh | Charge at night |", "|---|---|---|---|---|"]
    for n, d, use, gain, pct in week(2, 50, "Morocco, winter", lean=True, gas=True)[2]:
        out.append("| %s | %s | %.2f | %.2f | %d %% |" % (n, d.replace("_", ", "), use, gain, pct))
    path = os.path.join(HERE, "v2-real", "energy.md")
    open(path, "w").write("\n".join(out) + "\n")
    print("wrote", path)
    for name, cells in summary:
        print(name, "|", " | ".join(cells))


if __name__ == "__main__":
    report()
