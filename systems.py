#!/usr/bin/env python3
"""Wiring, gas and water for v2-real: every run as a route through the van, so the cable and
pipe lengths, the cable sizes and the fuses come from the model, not from a guess.

    python systems.py           # -> v2-real/systems.png and v2-real/systems.md

The end points are the boxes in model3d.py (APPLIANCES_V2R and friends), so moving an
appliance there moves its cable here. Routes are waypoints (x, y, z) in the model's mm; the
length is the path along them plus 15 % for bends, loops at the ends and mistakes, rounded up
to half a metre. Cable size: the thicker of (a) 3 % voltage drop there and back, and (b) what
the fuse protecting it needs. Check every size against the product manuals before buying.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from plan import VARIANTS, wall_inset
from model3d import APPLIANCES_V2R, EXTRA_V2R, FANS_V2R, HATCHES_V2R, ROOF_V2R

HERE = os.path.dirname(os.path.abspath(__file__))
V = VARIANTS["v2-real"]
SLACK = 1.15
RHO = 0.0175                     # copper, ohm mm2 / m
DROP = 0.03 * 12.0               # 3 % of 12 V
# What a cable may carry, bundled in a warm van (conservative, PVC 70 C) - the fuse must not
# be bigger than this. mm2 -> A.
AMPACITY = {1.5: 14, 2.5: 20, 4: 27, 6: 35, 10: 50, 16: 70, 25: 95, 35: 120, 50: 150,
            70: 190, 95: 230, 120: 270}
FUSES = (3, 5, 7.5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 250)
KG_PER_M = {s: s * 0.0089 * 1.25 for s in AMPACITY}      # copper + ~25 % insulation


def box(kind, n=0):
    return [b for b in APPLIANCES_V2R if b[6] == kind][n]


def centre(b, z=None):
    return ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2 if z is None else z)


# --- the nodes ----------------------------------------------------------------------------
H = V["height"]
DIST = centre(box("electrics", 0))          # bench: main fuse, shunt, busbars, DC-DC, fuse block
BOARD = centre(box("board"))         # garage: MPPT, 230 V box
INV = centre(box("inverter"))
BAT = centre(box("battery", 0))
BAT2 = centre(box("battery", 1))
FRIDGE = (box("fridgedoor")[1] - 30, (box("fridgedoor")[2] + box("fridgedoor")[3]) / 2, 120)
PUMP = centre(box("plumbing"), 150)
OVEN = centre(box("oven"))
HOB = centre(box("hob"), 845)
B10 = centre(box("calorifier"))
BOTTLE = centre(box("gasbottle"))
FRESH, GREY = box("fresh"), box("grey")
TAP = centre(box("tap"), 925)
FTAP = centre(box("filtertap"), 925)
FILTER = centre(box("filter"))
FAN1, FAN2 = [((f[0] + f[1]) / 2, (f[2] + f[3]) / 2, H) for f in FANS_V2R]
STARLINK = [((b[0] + b[1]) / 2, (b[2] + b[3]) / 2, H) for b in ROOF_V2R if b[6] == "starlink"][0]
PANELS_END = [(b[1], b[3] - 60, H) for b in ROOF_V2R if b[6] == "solar"][-1]
INLET = [((h[1] + h[2]) / 2, 1782, 440) for h in HATCHES_V2R if h[0] == "d"][0]
FILLER = [((h[1] + h[2]) / 2, 43, 440) for h in HATCHES_V2R if h[0] == "p" and h[1] < 3000][0]
SHOWER_MIX = (80, 1550, 1100)                # on the partition, in the shower riser
SHOWER_DRAIN = (350, 1350, 20)
GULPER = (600, 1420, 80)                     # under the tray's lobby edge, reachable
# The Crafter's starter battery sits in the cab floor, driver side (position to confirm on
# the van; VW's converter guidelines name the take-off point).
STARTER = (-800, 1450, -150)
CH = 20                                      # cable channel in the floor build, z
AISLE_Y = 916                                # the floor channel runs up the centre line


# --- the runs -----------------------------------------------------------------------------
# (group, name, amps, route, note). amps None = 230 V or a pipe: no DC sizing.
def via_floor(a, b, x_cross=None):
    """From a down into the floor channel, along it, and up to b."""
    xc = b[0] if x_cross is None else x_cross
    return [a, (a[0], a[1], CH), (a[0], AISLE_Y, CH), (xc, AISLE_Y, CH), (xc, b[1], CH), b]


def via_ceiling(a, b, wall_y=1640):
    """Up the driver wall behind the lockers, along the ceiling, down to b."""
    top = H - 30
    return [a, (a[0], wall_y, a[2]), (a[0], wall_y, top), (a[0], AISLE_Y, top),
            (b[0], AISLE_Y, top), b]


DC = [
    # main
    ("12 V main", "Battery 1 -> own fuse -> busbar (via the shunt)", 90,
     [BAT, (BAT[0], BAT[1], 230), (DIST[0], DIST[1], 230), DIST],
     "each battery carries half of ~180 A (inverter ~148 + DC loads ~30); equal cable lengths"),
    ("12 V main", "Battery 2 -> own fuse -> busbar (via the shunt)", 90,
     [BAT2, (BAT2[0], BAT2[1], 230), (DIST[0], DIST[1], 230), DIST], "same length as battery 1"),
    ("12 V main", "Busbars -> MultiPlus C 12/2000 (1600 W)", 148,
     [DIST, (DIST[0], DIST[1], 300), (INV[0], INV[1], 300), INV],
     "1600 W / 12 V / 0.9; follow Victron's manual table if it asks for more"),
    ("12 V charge", "Starter battery -> Orion XS 50 A (input)", 53,
     via_floor(STARTER, DIST, x_cross=DIST[0]),
     "fuse at the starter battery end; + a thin ignition / D+ wire alongside it"),
    ("12 V charge", "Orion XS -> busbars (output)", 50, [DIST, DIST], "a short link in the same box"),
    ("12 V charge", "MPPT 100/30 -> busbars", 30,
     [BOARD, (BOARD[0], 1700, 250), (2850, 1650, 250), (DIST[0], DIST[1], 200), DIST],
     "past the wheel arch, above it"),
    ("12 V solar", "Solar: panels in series -> DC isolator -> MPPT", 10,
     [(PANELS_END[0] - 1485, PANELS_END[1], H + 40), (PANELS_END[0], PANELS_END[1], H + 40),
      (PANELS_END[0] + 60, 1500, H), (3000, 1650, H - 60), (3000, 1720, 1300), BOARD],
     "on the roof: panel link + one cable to a gland aft of the panels; 4-6 mm2 solar cable"),
    # loads, from the fuse block in the distribution box
    ("12 V loads", "Fridge Vitrifrigo C95L", 7, via_floor(DIST, FRIDGE, x_cross=1930) ,
     "compressor fridges cut out on low voltage: keep this one thick"),
    ("12 V loads", "Water pump Shurflo Trail King 7", 4.5,
     [DIST, (DIST[0], 1330, 150), (1930, 1330, 150), (1520, 1580, 150), PUMP], ""),
    ("12 V loads", "Shower drain pump Whale Gulper 220", 4,
     [DIST, (1930, 1330, 150), (1150, 1420, 150), (700, 1420, 100), GULPER],
     "on a switch at the shower; through the WC base, not the tray"),
    ("12 V loads", "Rear fan MaxxFan", 3, via_ceiling(DIST, FAN2), ""),
    ("12 V loads", "Front fan MaxxFan", 3, via_ceiling(DIST, FAN1), ""),
    ("12 V loads", "Starlink Mini (12 V in)", 5, via_ceiling(DIST, STARLINK), "gland at the roof front"),
    ("12 V loads", "Lights, front circuit", 3, via_ceiling(DIST, (100, AISLE_Y, H - 30)), "LED strips"),
    ("12 V loads", "Lights, rear circuit", 3, via_ceiling(DIST, (3350, AISLE_Y, H - 30)), ""),
    ("12 V loads", "USB-C / 12 V sockets, galley", 10,
     [DIST, (1930, 1330, 150), (1250, 1650, 150), (1250, 1690, 1000)], "worktop back wall"),
    ("12 V loads", "USB-C / 12 V sockets, dinette + bed", 10,
     [DIST, (2300, 1700, 300), (2300, 1720, 700), (2300, AISLE_Y, CH), (2300, 80, 700)],
     "one each side, at the backrest"),
    ("12 V loads", "Truma B10 (control) + gas / CO detector", 1.5,
     [DIST, (DIST[0], AISLE_Y, CH), (3100, AISLE_Y, CH), (3100, B10[1], CH), B10],
     "the detector sits low by the gas locker"),
    ("12 V loads", "Hob ignition + tank level displays", 1,
     via_floor(DIST, HOB, x_cross=1930), "tiny currents - size set by the fuse"),
]

AC = [
    ("230 V", "CEE inlet -> shore box (2-pole RCBO 16 A)", [INLET, (INLET[0], 1727, 400), BOARD], ""),
    ("230 V", "Shore box -> MultiPlus AC-in",
     [BOARD, (BOARD[0], 1700, 400), (2850, 1650, 400), (INV[0], INV[1], 400), INV], ""),
    ("230 V", "MultiPlus AC-out -> box B (2-pole RCD + 2 MCB)",
     [INV, (2600, 1450, 420)], "box B beside the MultiPlus, under the bench lid"),
    ("230 V", "Circuit 1 (16 A): galley socket + oven",
     [(2600, 1450, 420), (1930, 1450, 420), OVEN, (1250, 1700, 1000)], ""),
    ("230 V", "Circuit 2 (10 A): dinette sockets",
     [(2600, 1450, 420), (2200, 1720, 700), (2200, AISLE_Y, CH), (2200, 80, 700)], ""),
]

VALVES = (3100, 560, 400)                    # gas valve block, in the garage by the locker
GAS = [
    ("Gas", "Bottle -> 30 mbar regulator -> hose into the locker's bulkhead",
     [BOTTLE, (BOTTLE[0], 870, 450)], "hose, max ~400-450 long; regulator with a crash sensor"),
    ("Gas", "Locker -> valve block", [(BOTTLE[0], 870, 450), (3100, 870, 400), VALVES], "8 mm copper"),
    ("Gas", "Valve block -> Truma B10", [VALVES, (3100, B10[1], 300), B10], "8 mm copper"),
    ("Gas", "Valve block -> Thetford hob",
     [VALVES, (3100, 90, 100), (1300, 90, 100), (1300, 110, 830), HOB],
     "8 mm copper low along the passenger wall, behind the fridge; clipped every 50 cm"),
]

W_IN = (FRESH[0] + 20, (FRESH[2] + FRESH[3]) / 2, 40)       # tank outlet, forward low end
W_T = (PUMP[0] + 150, PUMP[1], 200)                          # after pump + accumulator
WATER = [
    ("Fresh", "Filler -> tank (38 mm hose)", "38 mm hose", [FILLER, (FILLER[0], 300, 340)], ""),
    ("Fresh", "Tank vent / overflow -> floor (16 mm)", "16 mm",
     [(FILLER[0] + 40, 500, 340), (FILLER[0] + 40, 520, 600), (FILLER[0] + 40, 560, 0)],
     "loops up above the filler first"),
    ("Fresh", "Tank -> strainer -> pump (12 mm)", "12 mm", via_floor(W_IN, PUMP, x_cross=1930),
     "crosses the aisle in the floor build at x 1930, the galley's aft end"),
    ("Cold", "Pump -> filter -> mixer + drinking tap", "12 mm",
     [PUMP, W_T, FILTER, (TAP[0], TAP[1], 900), TAP, FTAP], ""),
    ("Cold", "Pump -> Truma B10", "12 mm",
     [W_T, (1930, 1330, CH), (1930, 150, CH), (3000, 150, 100), B10],
     "water crosses to the PASSENGER side - away from the batteries"),
    ("Hot", "Truma B10 -> galley mixer", "12 mm, insulated",
     [B10, (3000, 170, 100), (1930, 170, CH), (1930, 1330, CH), (TAP[0], 1600, 300), TAP], ""),
    ("Cold", "Pump -> shower mixer", "12 mm", [W_T, (1150, 1450, 150), (700, 1450, 150), (160, 1550, 150),
                                      SHOWER_MIX], ""),
    ("Hot", "Galley T -> shower mixer", "12 mm, insulated", [(TAP[0], 1600, 300), (1150, 1470, 150), (700, 1470, 150),
                                         (160, 1570, 150), SHOWER_MIX], "tee off the galley hot line"),
    ("Fresh", "Drains: tank valve + B10 FrostControl -> floor", "12 mm",
     [W_IN, (W_IN[0], W_IN[1], 0)], "+ ~0.3 m from the B10 in the garage"),
    ("Grey", "Sink -> trap -> tank (32 mm, falling)", "32 mm",
     [(TAP[0] - 250, 1480, 715), (TAP[0] - 250, 1480, 400), (1930, 1250, 250),
      (GREY[0] + 30, 1100, GREY[5])], "falls ~500 over ~1 m - gravity is plenty"),
    ("Grey", "Shower tray -> Gulper -> tank (19 mm)", "19 mm",
     [SHOWER_DRAIN, GULPER, (1150, 1400, 150), (1930, 1250, 150), (GREY[0] + 30, 1150, GREY[5])], ""),
    ("Grey", "Tank -> ball valve -> through the floor", "25 mm",
     [((GREY[0] + GREY[1]) / 2, (GREY[2] + GREY[3]) / 2, 10), ((GREY[0] + GREY[1]) / 2, 916, -150)],
     "valve reachable from the footwell lid; outlet >= 3/4 inch"),
]


def length(route):
    raw = sum(math.dist(a, b) for a, b in zip(route, route[1:])) / 1000
    return max(0.5, math.ceil(raw * SLACK * 2) / 2)


def size(amps, metres):
    fuse = next(f for f in FUSES if f >= amps * 1.25)
    by_drop = 2 * metres * amps * RHO / DROP
    mm2 = next(s for s in sorted(AMPACITY) if s >= by_drop and AMPACITY[s] >= fuse)
    return fuse, mm2


def report():
    out = ["# v2-real — wiring, gas and water", "",
           "Generated by `python systems.py` — do not edit by hand. Drawing: "
           "[systems.png](systems.png). Every run is a route between the model's boxes, "
           "+15 % for bends and ends, rounded up to 0.5 m.", "",
           "**Before buying, check each cable size against the product's manual** (Victron "
           "gives its own tables) and let the certified installers sign off the gas and 230 V.", "",
           "## 12 V", "",
           "Cable size = the thicker of: 3 % voltage drop there and back, and what the fuse "
           "needs. The fuse sits at the **source** end (battery, busbar or fuse block). The "
           "length is one way; you buy it twice (red + black).", "",
           "| Group | Run | A | m | Fuse A | Cable mm² |", "|---|---|---|---|---|---|"]
    per_size, kg = {}, 0.0
    for g, name, amps, route, note in DC:
        m = length(route)
        fuse, mm2 = size(amps, m)
        per_size[mm2] = per_size.get(mm2, 0) + 2 * m
        kg += 2 * m * KG_PER_M[mm2]
        out.append("| %s | %s%s | %g | %.1f | %g | **%g** |" %
                   (g, name, " — " + note if note else "", amps, m, fuse, mm2))
    out += ["", "**To buy, 12 V cable (red + black):** " +
            ", ".join("%g mm² %g m" % (s, per_size[s]) for s in sorted(per_size, reverse=True)) +
            " — about **%.0f kg** of cable." % kg, "",
            "## 230 V", "",
            "3-core flexible cable (H07RN-F or H05VV-F) 2.5 mm². Two boxes: **A** by the inlet "
            "(2-pole RCBO 16 A, before the MultiPlus) and **B** after it (2-pole RCD + two MCBs) — "
            "the MultiPlus output needs its own RCD. Earth bonded to the van body.", "",
            "| Run | m | Note |", "|---|---|---|"]
    ac_m = 0
    for g, name, route, note in AC:
        m = length(route)
        ac_m += m
        out.append("| %s | %.1f | %s |" % (name, m, note))
    out += ["", "**To buy:** 3 x 2.5 mm² flexible, **%.0f m**." % ac_m, "",
            "## Gas — for the certified installer", "",
            "Design basis only: EN 1949 and the Czech inspection decide. 30 mbar regulator on "
            "the locker wall, one isolating valve per appliance in a valve block, 8 mm copper "
            "clipped every ~50 cm, no joints hidden behind panels, the locker sealed from the "
            "living space and vented at its floor. Gas + CO detector, low.", "",
            "| Run | m | Note |", "|---|---|---|"]
    gas_m = 0
    for g, name, route, note in GAS:
        m = length(route)
        gas_m += m if "copper" in note else 0
        out.append("| %s | %.1f | %s |" % (name, m, note))
    out += ["", "**To buy:** 8 mm copper gas pipe **%.0f m**, a 2-way valve block, "
            "a 30 mbar regulator + hose, bulkhead fittings." % gas_m, "",
            "## Water", "",
            "12 mm push-fit pipe (PEX or John Guest) for fresh, cold and hot; 32 mm and 19 mm "
            "for grey. **Water stays on the passenger side and in the floor** — the batteries "
            "and the distribution box are on the driver side.", "",
            "| Line | Run | Pipe | m | Note |", "|---|---|---|---|---|"]
    pipe = {}
    for g, name, k, route, note in WATER:
        m = length(route)
        pipe[k] = pipe.get(k, 0) + m
        out.append("| %s | %s | %s | %.1f | %s |" % (g, name, k, m, note))
    out += ["", "**To buy:** " + "; ".join("%s: %g m" % (k, pipe[k]) for k in sorted(pipe)) +
            ". Plus: a strainer before the pump, a small accumulator, a non-return valve "
            "and FrostControl at the B10, drain valves on both tanks, a sink trap.", "",
            "## Things this found", "",
            "- **The hot water runs are long.** The B10 is in the garage, the taps are 1.5–3 m "
            "away: ~%.0f m of hot pipe. Insulate it; ~0.1 L runs cold before hot arrives per "
            "metre of 12 mm pipe." % sum(length(r) for g, n, _k, r, _ in WATER if g == "Hot"),
            "- **The shower is the far end of everything:** the drain pump, both water lines and "
            "a light all go through the WC base. Plan that base with a service panel.",
            "- **The starter battery cable is the longest heavy run** (~%.1f m, one way). Fuse "
            "it at the starter battery." % length(DC[3][3]),
            "- **Nothing wet near the batteries:** all water crosses to the passenger side in "
            "the floor at x 1930, the galley's aft end."]
    path = os.path.join(HERE, "v2-real", "systems.md")
    open(path, "w").write("\n".join(out) + "\n")
    print("wrote", path, "- 12 V cable %.0f kg" % kg)
    return kg


STYLE = {"12 V main": ("#c0392b", "-", 3.0), "12 V charge": ("#e67e22", "-", 2.0),
         "12 V loads": ("#c0392b", "-", 1.0), "12 V solar": ("#e67e22", ":", 1.6), "230 V": ("#7d3c98", "-", 1.6),
         "Gas": ("#d4ac0d", "-", 2.2), "Fresh": ("#2e86c1", "-", 1.6),
         "Cold": ("#2e86c1", "-", 1.2), "Hot": ("#e74c3c", "--", 1.4),
         "Grey": ("#6e5a44", "-", 2.2)}


def background(ax, title):
    L, W = V["length"], V["width"]
    ins = wall_inset(V, 300)
    ax.add_patch(Rectangle((0, ins), L, W - 2 * ins, fc="#faf8f4", ec="#222", lw=1.5))
    items = [b for b in APPLIANCES_V2R] + [b for b in EXTRA_V2R if b[6] in ("bed", "overhead")]
    for x0, x1, y0, y1, z0, z1, k in items:
        if k in ("bed", "overhead"):
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="#ddd", lw=0.6))
            continue
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#e9e6df", ec="#aaa", lw=0.6))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, k, fontsize=4.5, color="#777", ha="center", va="center")
    ax.set_xlim(-950, L + 80); ax.set_ylim(W + 80, -80); ax.set_aspect("equal")
    ax.set_title(title, fontsize=8); ax.tick_params(labelsize=5)
    ax.text(-900, 1500, "cab", fontsize=6, color="#999")


def draw_runs(ax, runs):
    seen = set()
    for g, name, route in runs:
        c, ls, lw = STYLE[g]
        xs, ys = [p[0] for p in route], [p[1] for p in route]
        ax.plot(xs, ys, color=c, ls=ls, lw=lw, alpha=0.85, label=None if g in seen else g,
                solid_capstyle="round")
        seen.add(g)
        ax.plot(xs[-1], ys[-1], "o", color=c, ms=2.5)
    ax.legend(fontsize=6, loc="upper left", bbox_to_anchor=(1.0, 1.0), framealpha=0.9)


def drawing():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 10), dpi=150)
    background(a1, "v2-real electrics, from above - nose left, driver side down. "
                   "Lines show routes, not wire counts; dotted = on the roof")
    draw_runs(a1, [(g, n, r) for g, n, a, r, _ in DC] + [(g, n, r) for g, n, r, _ in AC])
    for p, t in ((DIST, "distribution\n(bench)"), (BOARD, "MPPT +\nshore box"), (INLET, "230 V inlet"),
                 (STARTER, "starter\nbattery")):
        a1.annotate(t, (p[0], p[1]), fontsize=5.5, xytext=(0, -14), textcoords="offset points",
                    ha="center", color="#333")
    background(a2, "v2-real gas and water, from above")
    draw_runs(a2, [(g, n, r) for g, n, r, _ in GAS] + [(g, n, r) for g, n, _k, r, _ in WATER])
    for p, t in ((VALVES, "gas valves"), (FILLER, "filler"), (SHOWER_MIX, "shower mixer"),
                 (B10, "Truma B10")):
        a2.annotate(t, (p[0], p[1]), fontsize=5.5, xytext=(0, 10), textcoords="offset points",
                    ha="center", color="#333")
    fig.tight_layout()
    path = os.path.join(HERE, "v2-real", "systems.png")
    fig.savefig(path, facecolor="white", bbox_inches="tight"); plt.close(fig)
    print("wrote", path)


# For the viewer: each run as a tube of a kind (model3d.KIND colours it) and a radius in mm,
# drawn thicker than life so a 1.5 mm2 wire can still be seen.
TUBE = {"12 V main": ("cable12", 16), "12 V charge": ("cable12", 11), "12 V loads": ("cable12", 7),
        "12 V solar": ("cablepv", 8), "230 V": ("cable230", 8), "Gas": ("gaspipe", 9),
        "Fresh": ("coldpipe", 11), "Cold": ("coldpipe", 9), "Hot": ("hotpipe", 9),
        "Grey": ("greypipe", 16)}


def runs():
    out = []
    for group, *rest in DC + AC + GAS + WATER:
        route = rest[-2]
        k, r = TUBE[group]
        out.append({"k": k, "r": r, "pts": [[round(c, 1) for c in p] for p in route]})
    return out


if __name__ == "__main__":
    report()
    drawing()
