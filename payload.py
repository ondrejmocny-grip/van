#!/usr/bin/env python3
"""Payload check: the van, the build and what we carry, against 3500 kg and the two axles.

Every item has a weight and a position along the van, so the same list gives the total and
the load on each axle (lever rule between the axles). Weights come from products.py where a
product is chosen, from the maker or shop pages (source given), or are marked "est." - an
estimate to replace when the product is picked. The furniture is estimated from the model's
own boxes, so it follows the layout.

    python payload.py            # -> v2-real/payload.md, and a summary on the screen

x is ours: from the partition, growing aft. The rear axle is at x 2270 (centre of VW's wheel
arch); the front axle is one wheelbase (3640) forward of it.
"""
import os
import model3d as m

HERE = os.path.dirname(os.path.abspath(__file__))
V = m.VARIANTS["v2-real"]

GROSS = 3500                  # licence B, and the van's registration
AXLE_MAX = (1800, 2100)       # front, rear - VW, Crafter 35 4MOTION
SEATS = 3                     # the 3-seat cab
LENGTH_M = 6.0                # overall length, 5986
ROOF_MAX = 150               # VW converter guidelines p. 74, high roof H3
FRONT_MIN_SHARE = 0.33        # VW converter guidelines p. 54: loaded, the front axle >= 33 %
REAR_AXLE = 2270
FRONT_AXLE = REAR_AXLE - 3640

# The van as sold: 2440 kg from the aaaauto listing, which by VW's definition (EU 1230/2012)
# includes a 75 kg driver, all fluids and 90 % fuel. To confirm on the ORV / COC and by weighing.
# How it splits over the axles is NOT known - 53 / 47 is an assumption until we weigh it.
KERB = 2440
KERB_FRONT_SHARE = 0.53

# Plywood for the furniture, kg per m2 (WISA birch 680 kg/m3; Italian poplar sheet weights).
PLY = {"poplar 15": 6.1, "birch 15": 10.2}
FOAM = 40                     # kg per m3 of cushion, foam + cover, est.


def at(kind):
    """x centre of the first model box of this kind - where an item sits along the van."""
    for b in m.boxes_for(V):
        if b[6] == kind:
            return (b[0] + b[1]) / 2
    raise KeyError(kind)


def prod(key):
    return m.PRODUCTS[key]["weight_kg"]


# (group, item, kg, x, source). kg None = not known yet: counted as 0 and listed as a gap.
ITEMS = [
    # --- electrics
    ("Electrics", "2 x 150 Ah LiFePO4 (Ective LC 150 LT 15.5 kg each)", 31.0, at("battery"), "ective.de"),
    ("Electrics", "Victron MultiPlus 12/3000/120", 18.0, at("inverter"), "Victron datasheet"),
    ("Electrics", "SmartSolar MPPT 100/50 + Orion-Tr 12/12-30", 3.1, at("electrics"), "Victron datasheets"),
    ("Electrics", "Busbars, fuses, consumer unit, shore inlet", 5.0, at("electrics"), "est."),
    ("Electrics", "70 mm2 cable ~8 m (0.78 kg/m) + other wiring", 16.0, 1500, "cable 0.78 kg/m; wiring est."),
    ("Electrics", "2 solar panels ~200 W (2 x 11 kg) + rails - full gas, 2026-09-25", 29.0, 2400, "Victron 185 W 11 kg; rails est."),
    ("Electrics", "Starlink Mini + mount and cable", 1.6, 2900, "Mini 1.10 kg (Starlink spec); mount est."),
    ("Electrics", "12 V lighting, switches, USB", 4.0, 1500, "est."),
    # --- water and bathroom
    ("Water system", "Fresh tank 118 L, empty", 8.0, at("fresh"), "PE tanks 6-8.5 kg"),
    ("Water system", "Grey tank 95 L, empty", 8.5, at("grey"), "Fusion 100 L 8.5 kg"),
    ("Water system", "Truma Boiler B10 gas water heater 10 L, empty, + flue", 7.5, at("calorifier"), "Truma 6.7 kg; flue est."),
    ("Gas system", "Gas locker (sealed, floor vent), regulator, hose, pipes, gas + CO detector", 6.0, at("gasbottle"), "est."),
    ("Water system", "Pump (Shurflo Trail King 7), filter, pipes, fittings", 10.0, at("plumbing"), "pump 2.3 kg; rest est."),
    ("Water system", "Thetford Porta Potti 565E, dry", 6.1, at("cassette"), "sylvansport.com"),
    ("Water system", "Shower tray, wet lining, curtain, mixer + head", 15.0, 350, "est."),
    # --- kitchen: estimates until the kitchen products are picked
    ("Kitchen", "Vitrifrigo C95L fridge, 95 L", prod("vitrifrigo-c95l"), at("fridgedoor"), "products.py"),
    ("Kitchen", "2-burner gas hob, 30 cm (model to pick)", 4.0, at("hob"), "est. - Can Hoodiny 3.9 kg"),
    ("Kitchen", "Tefal Optimo OF4448 oven", prod("tefal-of4448"), at("oven"), "products.py"),
    ("Kitchen", "Quadron Anthony 50 sink + colander, 2 taps, carbon filter", 10.0, at("sinkrim"), "est. - sink weight not published"),
    # --- shell: insulation, floor, cladding, openings
    ("Shell", "3 x Dometic S4 (2 x 900x450 8.0 kg, 1 x 500x350 4.7 kg)", 20.7, 2000, "Dometic S4 chart"),
    ("Shell", "2 x MaxxFan Deluxe + 2 Crafter adapters", 17.4, 1400, "fan ~7.7 kg (shops vary); adapter est."),
    ("Shell", "Insulation: Armaflex 19 mm on ~17.5 m2 + cavity fill", 27.0, 1700, "Armaflex 1.17 kg/m2; fill est."),
    ("Shell", "Sound deadening ~6 m2", 9.0, 1700, "est. 1.5 kg/m2"),
    ("Shell", "Floor 6 m2: 20 XPS + 12 ply + 2 vinyl + battens", 58.0, 1700, "XPS 0.6, poplar 12 4.9, vinyl ~3 kg/m2; battens est."),
    ("Shell", "Wall + ceiling cladding, 6 mm ply ~11 m2 (not behind furniture)", 28.0, 1700, "poplar 6 mm ~2.5 kg/m2"),
    ("Shell", "Our partition, 15 mm ply + frame + crawl-through door", 22.0, 0, "est."),
    ("Shell", "VanQuito door fly screen", prod("vanquito-crafter"), 960, "products.py"),
    ("Shell", "Tarp 3 x 2.4 m on a keder rail (yourGEAR) + rail", prod("yourgear-tarp-3x24") + 1.0, 1650, "tarp 2.9 kg; rail est. 1"),
    ("Shell", "Screws, rivnuts, glue, sealant", 10.0, 1700, "est."),
    # --- vehicle upgrades, tier 1 + 2
    ("Upgrades", "Front engine guard, 6 mm aluminium (GTV)", 17.7, -1400, "gtv-van.com"),
    ("Upgrades", "Rear diff / AWD coupling guard", 7.0, 2150, "est."),
    ("Upgrades", "VB-SemiAir rear air springs + compressor", 22.0, 2270, "motorfit.de"),
    ("Upgrades", "Seikel +30 lift (springs and dampers swapped)", 5.0, 450, "est. - weight change not published"),
    ("Upgrades", "A/T tyres x 5 vs stock", 0.0, 450, "KO2 LT 16.3 kg = stock 16.3 kg"),
    ("Upgrades", "Breather extensions", 1.0, -1000, "est."),
]


def furniture():
    """The furniture estimated from the model: every carcass as its top, its front and two
    ends (the back is the wall, the bottom the floor) plus 30 % for shelves and dividers;
    thin panels by their big face; cushions by volume. Returns (item, kg poplar, kg birch, x)."""
    carcass = ("LOCKER", "SINK", "HOB", "BENCH", "REAR BENCH", "WARDROBE", "FOOTWELL -> BED",
               "overhead")
    panels = ("wetwall", "wetface", "table", "ftable", "ftablep", "ptable", "ptablep", "litter")
    soft = ("bed", "infill", "pillow", "backrest")
    rows = {}
    for x0, x1, y0, y1, z0, z1, k in m.boxes_for(V):
        dx, dy, dz = (x1 - x0) / 1000, (y1 - y0) / 1000, (z1 - z0) / 1000
        if k in carcass:
            area, kind = (dx * dy + dx * dz + 2 * dy * dz) * 1.3, "ply"
        elif k in panels:
            area, kind = max(dx * dy, dx * dz, dy * dz), "ply"
        elif k in soft:
            area, kind = dx * dy * dz * FOAM, "soft"
        else:
            continue
        name = {"FOOTWELL -> BED": "Footwell floor + frame", "overhead": "Overhead lockers",
                "wetwall": "Shower walls", "wetface": "Shower face", "bed": "Cushions",
                "infill": "Cushions", "pillow": "Cushions", "backrest": "Cushions",
                "table": "Tables and leaves", "ftable": "Tables and leaves",
                "ftablep": "Tables and leaves", "ptable": "Tables and leaves",
                "ptablep": "Tables and leaves", "litter": "Cat box"}.get(k, k.title())
        r = rows.setdefault(name, [0.0, 0.0, 0.0, 0.0])      # poplar, birch, moment, mass
        if kind == "soft":
            r[0] += area
            r[1] += area
        else:
            r[0] += area * PLY["poplar 15"]
            r[1] += area * PLY["birch 15"]
        r[2] += (x0 + x1) / 2 * (area if kind == "soft" else area * PLY["poplar 15"])
        r[3] += area if kind == "soft" else area * PLY["poplar 15"]
    out = [(n, r[0], r[1], r[2] / r[3] if r[3] else 0) for n, r in sorted(rows.items())]
    out.append(("Hinges, runners, catches, struts, table post", 12.0, 12.0, 1700))
    return out


# What we carry - the driver is already in the kerb weight.
LOAD = [
    ("People", "Passenger (Ondrej's wife)", 65.0, -600, "est. - to confirm"),
    ("People", "Child + child seat", 25.0, -600, "est. - to confirm"),
    ("People", "Cat + litter", 10.0, 0, "est."),
    ("Water", "Fresh water, full 118 L", 118.0, at("fresh"), "1 kg/L"),
    ("Water", "Water heater full + WC flush water", 25.0, 900, "10 + 15 L"),
    ("Gas", "6 kg refillable gas bottle, full", 14.3, at("gasbottle"), "tare ~8.3 typical + 6 kg gas"),
    ("Water", "Grey water - empty when driving", 0.0, at("grey"), "empty it before driving"),
    ("Gear", "Belongings, 140 L for two + the child's", 60.0, 3120, "about-us: 70 L each; est."),
    ("Gear", "Food, drinks, kitchen things", 30.0, 1500, "est."),
    ("Gear", "Bedding, towels", 12.0, 2600, "est."),
    ("Gear", "Laptops, monitor, work kit", 8.0, 2400, "est."),
    ("Gear", "Recovery boards, shovel, compressor, tools", 25.0, 3120, "est."),
    # Bikes: left out for now (2026-09-24) - 60 kg with a rack, all behind the rear axle.
]


def axle(kg, x):
    """Split a weight at x over the two axles: (front, rear)."""
    rear = kg * (x - FRONT_AXLE) / (REAR_AXLE - FRONT_AXLE)
    return kg - rear, rear


def run(ply="poplar 15"):
    idx = 1 if ply == "poplar 15" else 2
    lines, gaps = [], []
    total, front, rear = KERB, KERB * KERB_FRONT_SHARE, KERB * (1 - KERB_FRONT_SHARE)
    groups = {}
    rows = [(g, n, kg, x, s) for g, n, kg, x, s in ITEMS]
    rows += [("Furniture", n, (p, b)[idx - 1], x, "model boxes, %s ply" % ply)
             for n, p, b, x in furniture()]
    rows += LOAD
    for g, n, kg, x, s in rows:
        if kg is None:
            gaps.append(n)
            kg = 0.0
        f, r = axle(kg, x)
        total, front, rear = total + kg, front + f, rear + r
        groups.setdefault(g, [0.0, 0.0, 0.0])
        groups[g][0] += kg
        groups[g][1] += f
        groups[g][2] += r
        lines.append((g, n, kg, x, s))
    return dict(total=total, front=front, rear=rear, groups=groups, lines=lines, gaps=gaps)


def report():
    p, b = run("poplar 15"), run("birch 15")
    build = lambda r: sum(v[0] for g, v in r["groups"].items() if g not in ("People", "Water", "Gear", "Gas"))
    load = lambda r: sum(v[0] for g, v in r["groups"].items() if g in ("People", "Water", "Gear", "Gas"))
    out = ["# v2-real — payload check", "",
           "Generated by `python payload.py` — do not edit by hand. Weights and sources are in "
           "`payload.py`; chosen products come from `products.py`.", "",
           "**Limits:** %d kg total (licence B), axles %d front / %d rear, front at least %d %% "
           "loaded. **Van as sold: %d kg** incl. a 75 kg driver and 90 %% fuel (listing - confirm "
           "on the COC and by weighing). Axle split of the empty van **assumed** %d / %d %%." %
           (GROSS, AXLE_MAX[0], AXLE_MAX[1], FRONT_MIN_SHARE * 100, KERB,
            KERB_FRONT_SHARE * 100, 100 - KERB_FRONT_SHARE * 100), "",
           "## Result", "",
           "| | Poplar furniture | Birch furniture |", "|---|---|---|",
           "| Van as sold | %d | %d |" % (KERB, KERB),
           "| Build (conversion + upgrades) | %d | %d |" % (build(p), build(b)),
           "| Load (people, water, gear) | %d | %d |" % (load(p), load(b)),
           "| **Total** | **%d** | **%d** |" % (p["total"], b["total"]),
           "| **Margin to %d** | **%+d** | **%+d** |" % (GROSS, GROSS - p["total"], GROSS - b["total"]),
           "| Front axle (max %d) | %d | %d |" % (AXLE_MAX[0], p["front"], b["front"]),
           "| Rear axle (max %d) | %d | %d |" % (AXLE_MAX[1], p["rear"], b["rear"]),
           "| Front share (min %d %%) | %d %% | %d %% |" % (FRONT_MIN_SHARE * 100,
                                                        100 * p["front"] / p["total"],
                                                        100 * b["front"] / b["total"]), ""]
    opt = [(n, kg) for g, n, kg, x, s in p["lines"] if "optional" in n]
    if opt:
        out += ["**Optional, first to cut:** %s — without them the total is **%d kg**." %
                ("; ".join("%s (%.0f kg)" % (n.split(" (optional")[0], k) for n, k in opt),
                 p["total"] - sum(k for _, k in opt)), ""]
    # Registration as a motor caravan: the converted van, empty, plus 75 kg for each seat
    # beyond the driver and a luggage allowance of 10 x (seats + length in m) - EU 1230/2012,
    # as we read it; the STK confirms. The driver is already in the kerb weight.
    empty = KERB + build(p)
    need = empty + 75 * (SEATS - 1) + 10 * (SEATS + LENGTH_M)
    out += ["**Registration test (motor caravan, EU 1230/2012 as we read it):** converted van "
            "empty %d kg + %d kg for %d more seats + %d kg luggage allowance = **%d kg** — "
            "%s 3500 by %d." % (empty, 75 * (SEATS - 1), SEATS - 1, 10 * (SEATS + LENGTH_M),
                                need, "under" if need <= GROSS else "OVER", abs(GROSS - need)), ""]
    # Stricter reading: "mass in running order" of a motor caravan may include the fresh
    # water tank at 90 % and the gas bottle full - the STK decides which applies.
    extra = 0.9 * 118 + 14.3
    out += ["Stricter reading (fresh water 90 %% + a full gas bottle counted as well): **%d kg** — "
            "%s 3500 by %d." % (need + extra, "under" if need + extra <= GROSS else "OVER",
                                abs(GROSS - need - extra)), ""]
    roof = [(n, kg) for g, n, kg, x, s in p["lines"]
            if any(w in n for w in ("solar", "Starlink", "MaxxFan", "awning", "Tarp"))]
    out += ["**Roof load (VW max %d kg):** %d kg — %s." % (ROOF_MAX, sum(k for _, k in roof),
            ", ".join("%s %.0f" % (n.split(",")[0].split("(")[0].strip(), k) for n, k in roof)), ""]
    if p["gaps"]:
        out += ["**Not counted yet (weight unknown):** " + "; ".join(p["gaps"]) + ".", ""]
    out += ["## By group (poplar)", "", "| Group | kg | front | rear |", "|---|---|---|---|"]
    for g, (kg, f, r) in p["groups"].items():
        out.append("| %s | %d | %d | %d |" % (g, kg, f, r))
    out += ["", "## Every line (poplar)", "", "| Group | Item | kg | x | Source |", "|---|---|---|---|---|"]
    for g, n, kg, x, s in p["lines"]:
        out.append("| %s | %s | %.1f | %d | %s |" % (g, n, kg, x, s))
    path = os.path.join(HERE, "v2-real", "payload.md")
    open(path, "w").write("\n".join(out) + "\n")
    print("wrote", path)
    for name, r in (("poplar", p), ("birch", b)):
        print("%-6s total %d kg, margin %+d, front %d / rear %d" %
              (name, r["total"], GROSS - r["total"], r["front"], r["rear"]))


if __name__ == "__main__":
    report()
