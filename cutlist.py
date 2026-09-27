#!/usr/bin/env python3
"""First cut list for v2-real: every furniture panel at real board thickness, the doors and
drawers, the sheets to buy, and the weight.

    python cutlist.py           # -> v2-real/cutlist.md, and a summary on the screen

The pieces come from the model's boxes, so the list follows the layout. It is a FIRST draft:
the door and drawer layout below is a proposal, and every size is to be re-measured on the
real van before a board is cut (the walls lean and are not straight). Panels that meet the
leaning wall are drawn to the box, which is their widest point - trim on site.

Weights use the board densities in BOARD (kg per m2); payload.py takes the furniture weight
from here instead of estimating it from the boxes.
"""
import math
import os

import model3d
from plan import VARIANTS

HERE = os.path.dirname(os.path.abspath(__file__))
V = VARIANTS["v2-real"]
SHEET = (2520, 1220)                  # Dřevobis poplar sheets
YIELD = 0.75                          # usable share of a sheet after the cuts and offcuts

# kg per m2, from the shops' sheet weights (researched 2026-09-25): Dřevobis poplar 15 mm
# 5.3, 12 mm 4.2, 6 mm 2.1 (~350 kg/m3). MAPH lists the same kind of poplar at 450 kg/m3 -
# WEIGH ONE SHEET before trusting the total. 9 mm and the worktop are estimates.
BOARD = {
    "poplar 15": 5.3, "poplar 12": 4.2, "poplar 9": 3.2, "poplar 6": 2.1,
    "worktop 19 (poplar 18 + HPL)": 7.6, "wet lining 3 (ACM)": 3.8,
}
BIRCH = {"poplar 15": 9.6, "poplar 12": 7.7, "poplar 9": 5.8, "poplar 6": 3.9,
         "worktop 19 (poplar 18 + HPL)": 12.5, "wet lining 3 (ACM)": 3.8}
# CZK per sheet (Dřevobis, incl. VAT); None = not priced yet
PRICE = {"poplar 15": 2299, "poplar 12": 1936, "poplar 9": None, "poplar 6": 1476,
         "worktop 19 (poplar 18 + HPL)": None, "wet lining 3 (ACM)": None}


# --- the shell layers: walls, roof, rear doors, floor --------------------------------------
def areas():
    """m2 from the model: side walls along the real profile (net of the openings), the
    ceiling, the rear doors, the floor, and how much wall hides behind furniture."""
    from plan import wall_inset
    sp = model3d.spec(V)
    L, W, H = V["length"], V["width"], V["height"]
    zs = sorted({0, H} | {z for z, _ in V["body"]["profile"] if 0 < z < H})
    run = sum(math.hypot(zb - za, wall_inset(V, zb) - wall_inset(V, za)) for za, zb in zip(zs, zs[1:]))
    holes = (V["slider"][1] - V["slider"][0]) * V["body"]["slider_h"]
    holes += sum((x1 - x0) * (z1 - z0) for _s, x0, x1, z0, z1 in list(sp["windows"]) + list(sp["hatches"]))
    walls = (2 * run * L - holes) / 1e6
    hidden = 0
    for b in model3d.boxes_for(V):
        if b[6] in ("SINK", "HOB", "BENCH", "WARDROBE", "LOCKER", "overhead"):
            hidden += (b[1] - b[0]) * (b[5] - b[4])
        elif b[6] == "REAR BENCH":
            hidden += 2 * (b[1] - b[0]) * (b[5] - b[4])
    return dict(walls=walls, walls_gross=2 * run * L / 1e6, hidden=hidden / 1e6,
                ceiling=L * (W - 2 * wall_inset(V, H)) / 1e6,
                doors=(W - 2 * model3d.REAR_DOORS[0]) * V["body"]["rear_h"] / 1e6,
                floor=L * (W - 2 * wall_inset(V, 0)) / 1e6)


# (layer, m2, product, kg/m2, CZK per m2 or None, note). Picks of 2026-09-25, see
# doc/products.md. FLOOR is option A (the cheap one); B is in the notes.
DEADEN_SHARE = 0.20                   # butyl on ~20 % of the bare panels: the big flat ones
FOAM_LAYERS = 1.3                     # 20 mm foam, a second layer where a cavity allows it


def shell_layers():
    a = areas()
    panels = a["walls_gross"] + a["ceiling"] + a["doors"]
    insul = (a["walls"] + a["ceiling"] + a["doors"]) * FOAM_LAYERS
    clad = a["walls"] - a["hidden"] + a["ceiling"] + a["doors"]
    return [
        ("Sound deadening", panels * DEADEN_SHARE, "Comfortmat Cobra 2.3 mm (butyl + alu)", 2.71,
         279 / 0.35, "on ~20 % of the bare panels, the big flat ones and the roof"),
        ("Insulation, walls + roof + rear doors", insul, "K-Flex 20 mm self-adhesive (closed cell)",
         1.23, 459, "fills the rib cavities; ~1.3 layers on average. Closed cell: no vapour "
                    "barrier needed. Glue the roof with K-414 too (the self-adhesive gives up at ~80 C)"),
        ("Glue for the foam", insul, "K-Flex K-414 contact adhesive", 0.15, 1190 / 2.6 / 3,
         "~150 g/m2 on each side, ~3 x 2.6 l; weight = dry film"),
        ("Floor: XPS", a["floor"], "Styrodur 2800 C 20 mm", 0.6, 149, "between battens"),
        ("Floor: board", a["floor"], "poplar plywood 12 mm (Dřevobis)", 4.2, 1936 / 3.07,
         "screwed through to the battens; furniture fixes to it"),
        ("Floor: covering", a["floor"], "Gerflor Texline vinyl 2.9 mm", 2.0, 571,
         "20 + 12 + 2.9 = 34.9 mm - inside the 35 of the model"),
        ("Floor: battens + glue", a["floor"], "20 mm battens on the ribs, Sikaflex-252", 0.8, 180, "est."),
        ("Cladding, walls + ceiling + rear doors", clad, "poplar plywood 6 mm (Dřevobis)", 2.1,
         1476 / 3.07 / YIELD, "not behind furniture (%.1f m2 hidden)" % a["hidden"]),
        ("Carpet on the curved parts", 3.0, "Carbest X-Trem stretch carpet 4.6 mm", 0.39, 249,
         "window surrounds and the tight curve at the roof edge; glued with 3M 90"),
    ]


def boxes(kind):
    return [b for b in model3d.boxes_for(V) if b[6] == kind]


# --- the proposal for doors and drawers ----------------------------------------------------
# (piece, x0, x1, z0, z1) on the carcass's front face, in van x and height; what it is for.
FRONTS = {
    "SINK": [   # driver galley, face at y 1197; oven 1285-1747 x 380-668, sink bowl above
        ("fixed panel", 1150, 1285, 40, 890, "beside the oven, over the pump box"),
        ("oven opening", 1285, 1747, 380, 668, "the Tefal slides in from the aisle"),
        ("door", 1285, 1747, 40, 370, "under the oven: pump box, trap, pots"),
        ("drawer", 1600, 1930, 700, 890, "cutlery, under the prep counter"),
        ("pull-out", 1747, 1930, 40, 690, "bottles and oils, 180 wide"),
        ("fixed panel", 1285, 1600, 668, 890, "the sink bowl is behind it"),
    ],
    "HOB": [    # passenger galley, face at y 635; the fridge 1250-1735 has its own door
        ("fixed panel", 1150, 1250, 40, 890, "beside the fridge"),
        ("fridge opening", 1250, 1735, 30, 822, "the C95L's own door"),
        ("pull-out", 1735, 1930, 40, 890, "pantry, 195 wide, full height"),
    ],
    "WARDROBE": [  # driver, aisle face at y 1232
        ("door", 700, 1150, 40, 560, "the WC: the waste tank comes out here"),
        ("drawer", 700, 1150, 560, 775, "towels, toiletries"),
        ("door", 700, 925, 775, 1811, "hanging space, left"),
        ("door", 925, 1150, 775, 1811, "hanging space, right"),
    ],
    "LOCKER": [("door", 0, 450, 40, 430, "shoes, from the lobby")],
    "BENCH-d": [("door", 2540, 2850, 80, 500, "electrics service hatch (distribution box)")],
}
# Lids on top of the seats (piece count, what is under them)
LIDS = {"BENCH-p": (2, "fresh tank, filler"), "BENCH-d": (2, "batteries, MultiPlus"),
        "REAR BENCH": (3, "garage: gas locker, Truma B10, gear"),
        "FOOTWELL -> BED": (1, "grey tank valve and the table post")}


def carcass(name, box, face_along_x=True, top=True, bottom=False, shelves=0, t="poplar 15",
            back=False):
    """Top, optional bottom, two ends, the front face (doors are cut from it), shelves."""
    x0, x1, y0, y1, z0, z1, _ = box
    L, D, H = (x1 - x0, y1 - y0, z1 - z0) if face_along_x else (y1 - y0, x1 - x0, z1 - z0)
    out = []
    if top:
        out.append((name, "top / lids", L, D, t, 1))
    if bottom:
        out.append((name, "bottom", L, D, t, 1))
    out.append((name, "end", D, H, t, 2))
    out.append((name, "front face (doors cut from it)", L, H, t, 1))
    if back:
        out.append((name, "back", L, H, "poplar 9", 1))
    if shelves:
        out.append((name, "shelf", L - 30, D - 15, "poplar 12", shelves))
    return out


def drawer(name, w, h, d):
    """A drawer box in 12 mm behind its front."""
    return [(name, "drawer side", d - 50, h - 40, "poplar 12", 2),
            (name, "drawer front+back", w - 30, h - 40, "poplar 12", 2),
            (name, "drawer bottom", w - 30, d - 50, "poplar 9", 1)]


def pieces():
    out = []
    sink, = boxes("SINK")
    hob, = boxes("HOB")
    for b, n in ((sink, "Galley, sink side"), (hob, "Galley, hob side")):
        out += carcass(n, b, top=False, shelves=1)
        out.append((n, "worktop", b[1] - b[0], b[3] - b[2] + 20, "worktop 19 (poplar 18 + HPL)", 1))
    out += drawer("Galley, sink side", 330, 190, 520)
    out += drawer("Galley, sink side", 180, 650, 520)          # the bottle pull-out
    out += drawer("Galley, hob side", 195, 850, 520)           # the pantry pull-out
    bench = sorted(boxes("BENCH"), key=lambda b: b[2])
    out += carcass("Bench, passenger (fresh tank)", bench[0], shelves=0)
    out += carcass("Bench, driver (batteries)", bench[1], shelves=0)
    out.append(("Bench, driver (batteries)", "divider at the batteries", bench[1][3] - bench[1][2],
                bench[1][5] - bench[1][4], "poplar 12", 1))
    rear, = boxes("REAR BENCH")
    out += carcass("Rear bench / garage", rear, face_along_x=False)
    out += [("Rear bench / garage", "gas locker (sealed box)", 300, 560, "poplar 12", 4),
            ("Rear bench / garage", "gas locker lid + floor", 300, 300, "poplar 12", 2)]
    fw, = boxes("FOOTWELL -> BED")
    out += [("Footwell", "top (lid over the grey tank)", fw[1] - fw[0], fw[3] - fw[2], "poplar 15", 1),
            ("Footwell", "front riser", fw[3] - fw[2], fw[5] - fw[4], "poplar 15", 1),
            ("Footwell", "bearers", fw[1] - fw[0], 80, "poplar 15", 3)]
    locker, = boxes("LOCKER")
    out += carcass("Shoe locker (seat)", locker, shelves=1)
    wr = sorted(boxes("WARDROBE"), key=lambda b: b[4])
    base = wr[0]
    out += carcass("Wardrobe + WC base", base, top=True, shelves=0)
    up_h = sum(b[5] - b[4] for b in wr[1:])
    up_d = sum((b[3] - b[2]) * (b[5] - b[4]) for b in wr[1:]) / up_h   # mean depth up the lean
    out += [("Wardrobe + WC base", "upper end (follows the lean)", up_d, up_h, "poplar 15", 2),
            ("Wardrobe + WC base", "upper front (2 doors)", base[1] - base[0], up_h, "poplar 15", 1),
            ("Wardrobe + WC base", "top", base[1] - base[0], wr[-1][3] - wr[-1][2], "poplar 15", 1),
            ("Wardrobe + WC base", "shelf over the hanging rail", base[1] - base[0] - 30,
             wr[-1][3] - wr[-1][2] - 15, "poplar 12", 1)]
    out += drawer("Wardrobe + WC base", 450, 215, 500)
    for i, b in enumerate(sorted(boxes("overhead"), key=lambda b: (b[4], b[0]))):
        out += carcass("Overhead lockers", b, bottom=True, t="poplar 12")
    out += [("Tables", "dinette table 900 x 600", 900, 600, "poplar 15", 1),
            ("Tables", "galley leaf", 400, 562, "poplar 15", 1),
            ("Tables", "side table by the lobby", 340, 380, "poplar 15", 1)]
    # the shower: fore and aft walls in ply with a wet lining; the driver side lining only
    # the shower: the aft wall in ply (the fore wall is our partition), a wet lining on all
    # three walls (fore, aft, and over the driver-side cladding), the carved face to the lobby
    out += [("Shower", "aft wall (ply)", 760, 1811, "poplar 12", 1),
            ("Shower", "wet lining, fore + aft", 760, 1811, "wet lining 3 (ACM)", 2),
            ("Shower", "wet lining, driver wall", 700, 1811, "wet lining 3 (ACM)", 1),
            ("Shower", "carved lobby face", 700, 1740, "poplar 12", 1)]
    # our own partition behind the cab, with the crawl-through
    part = [b for b in model3d.boxes_for(V, with_shell=True) if b[6] == "partition"]
    area = sum((b[3] - b[2]) * (b[5] - b[4]) for b in part)
    out.append(("Partition", "partition, net of the crawl-through", 1000, area / 1000, "poplar 15", 1))
    return out


def shell_groups():
    """(item, kg, x) for payload.py."""
    return [(n + " - " + prod, m2 * kg, 1700) for n, m2, prod, kg, _c, _note in shell_layers()]


def weight(rows, table):
    return sum(a * b / 1e6 * q * table[t] for _g, _n, a, b, t, q in rows)


def groups(birch=False):
    """(group, kg poplar, kg birch, x) for payload.py - the same shape as its old estimate."""
    xs = {"Galley, sink side": 1540, "Galley, hob side": 1540, "Bench, passenger (fresh tank)": 2390,
          "Bench, driver (batteries)": 2390, "Rear bench / garage": 3120, "Footwell": 2390,
          "Shoe locker (seat)": 225, "Wardrobe + WC base": 925, "Overhead lockers": 1900,
          "Tables": 2000, "Shower": 350, "Partition": 0}
    rows = pieces()
    out = []
    for g in dict.fromkeys(r[0] for r in rows):
        rs = [r for r in rows if r[0] == g]
        out.append((g, weight(rs, BOARD), weight(rs, BIRCH), xs.get(g, 1700)))
    return out


def report():
    rows = pieces()
    out = ["# v2-real — first cut list", "",
           "Generated by `python cutlist.py` — do not edit by hand. **A first draft:** sizes come "
           "from the model's boxes (a panel against the leaning wall is given at its widest - "
           "trim on site), and **every size is to be re-measured on the real van** before cutting.",
           "", "## Doors and drawers — the proposal", "",
           "| Carcass | Front | Along the van | Height | For |", "|---|---|---|---|---|"]
    for k, fr in FRONTS.items():
        for piece, x0, x1, z0, z1, what in fr:
            out.append("| %s | %s | %d–%d (%d) | %d–%d | %s |" % (k, piece, x0, x1, x1 - x0, z0, z1, what))
    for k, (n, what) in LIDS.items():
        out.append("| %s | %d lid%s on top | | | %s |" % (k, n, "s" if n > 1 else "", what))
    out += ["", "Every door and drawer gets a **push latch** and **rounded corners** (the approval "
            "asks for both, [approval.md](approval.md)).", "",
            "## Panels", "", "| Group | Panel | a x b mm | Board | Qty | m² |", "|---|---|---|---|---|---|"]
    for g, n, a, b, t, q in rows:
        out.append("| %s | %s | %.0f x %.0f | %s | %d | %.2f |" % (g, n, a, b, t, q, a * b / 1e6 * q))
    out += ["", "## Boards to buy (sheets %d x %d, %d %% usable)" % (SHEET[0], SHEET[1], YIELD * 100), "",
            "| Board | m² net | Sheets | kg (poplar) | kg (if birch) |", "|---|---|---|---|---|"]
    tot_p = tot_b = 0
    for t in dict.fromkeys(r[4] for r in rows):
        rs = [r for r in rows if r[4] == t]
        m2 = sum(a * b / 1e6 * q for _g, _n, a, b, _t, q in rs)
        sheets = math.ceil(m2 / (SHEET[0] * SHEET[1] / 1e6 * YIELD))
        wp, wb = weight(rs, BOARD), weight(rs, BIRCH)
        tot_p, tot_b = tot_p + wp, tot_b + wb
        out.append("| %s | %.1f | %d | %.0f | %.0f |" % (t, m2, sheets, wp, wb))
    out.append("| **Total** | | | **%.0f** | **%.0f** |" % (tot_p, tot_b))
    out += ["", "## By group — into the payload check", "", "| Group | kg poplar | kg birch |",
            "|---|---|---|"]
    for g, p, b, _x in groups():
        out.append("| %s | %.1f | %.1f |" % (g, p, b))
    cost = sum(math.ceil(sum(a * b / 1e6 * q for _g, _n, a, b, tt, q in rows if tt == t)
                         / (SHEET[0] * SHEET[1] / 1e6 * YIELD)) * PRICE[t]
               for t in dict.fromkeys(r[4] for r in rows) if PRICE.get(t))
    out += ["", "**Board cost (priced boards only):** ~%s CZK." % format(round(cost, -2), ",.0f"), ""]
    a = areas()
    out += ["## Walls, roof, floor — layers and shopping list", "",
            "Areas from the model: side walls %.1f m² net of the openings (%.1f gross), ceiling "
            "%.1f, rear doors %.1f, floor %.1f; %.1f m² of wall is behind furniture (insulated, "
            "not clad)." % (a["walls"], a["walls_gross"], a["ceiling"], a["doors"], a["floor"],
                            a["hidden"]), "",
            "| Layer | m² | Product | kg | CZK | Note |", "|---|---|---|---|---|---|"]
    tk = tc = 0
    for n, m2, prod, kg, czk, note in shell_layers():
        k, c = m2 * kg, (m2 * czk if czk else None)
        tk, tc = tk + k, tc + (c or 0)
        out.append("| %s | %.1f | %s | %.1f | %s | %s |" % (n, m2, prod, k,
                   format(round(c, -1), ",.0f") if c else "—", note))
    out.append("| **Total** | | | **%.0f** | **~%s** | |" % (tk, format(round(tc, -2), ",.0f")))
    out += ["", "**Floor option B** (lighter, dearer): Bo-dapter XPS kit for the Crafter L3 "
            "(21,390 CZK, <5 kg) + 6 mm poplar + Texline = ~29 mm, ~7 kg lighter and ~20,000 CZK "
            "more than A. Worth it only if the weight gets tight."]
    path = os.path.join(HERE, "v2-real", "cutlist.md")
    open(path, "w").write("\n".join(out) + "\n")
    print("wrote", path, "- furniture %.0f kg poplar / %.0f kg birch" % (tot_p, tot_b))


if __name__ == "__main__":
    report()
