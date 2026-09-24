#!/usr/bin/env python3
"""Draw campervan floor plans, elevations and sections.

Edit a variant in VARIANTS, rerun, get .png + .svg.

Plan coordinates are millimetres of real van interior:
  x = 0 at the front bulkhead line (back of the cab), growing toward the rear.
  y = 0 at the PASSENGER-side wall, growing toward the DRIVER side.
Plan view puts the nose at the left, which places the driver side at the bottom.

Plan boxes are (x0, x1, y0, y1, label, sub, fill); fill=None draws open floor (dashed).
View boxes are (a0, a1, z0, z1, label, sub, fill); z is height above the finished floor.
For elevations a = x (front at left). For sections a runs driver-wall to passenger-wall.

Run: python plan.py <variant>
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

WARM, GALLEY, SOFT, WET, COLD = "#efe7d8", "#dce7e4", "#e7e0ec", "#d9e6f0", "#e2efdf"

VARIANTS = {}

# --------------------------------------------------------------------------
# The reference van we liked: US Ford Transit 148" EL, high roof.
# --------------------------------------------------------------------------
VARIANTS["ref"] = dict(
    out="ref/emandnick-transit-148el/layout",
    length=4370, width=1780, well=(2600, 3500, 195), slider=(350, 1650),
    title='Em & Nick - 2018 Ford Transit 148" EL, high roof',
    note="Reconstructed from video stills. Dimensions estimated, +/-100 mm.",
    boxes=[
        (   0,  400,    0, 1780, "DESK / OFFICE", '32" monitor on swivel arm · cab pass-through under', WARM),
        ( 400, 1280,  980, 1780, "WET BATH", "shower + dry-flush WC · curtain door", WET),
        (1280, 1900, 1180, 1780, "FRIDGE", "12 V 130 L · door faces aft", COLD),
        (1900, 2500, 1160, 1780, "SINK", "farmhouse sink + filter tap", GALLEY),
        (1650, 2270,    0,  620, "STOVE + OVEN", "3-burner propane", GALLEY),
        (2270, 2500,    0,  620, "DRAWERS", "", GALLEY),
        (2500, 4370,    0,  600, "BENCH", "storage under", SOFT),
        (2500, 4370, 1180, 1780, "BENCH", "", SOFT),
        (2500, 4370,  600, 1180, "TABLE -> BED", "Lagun table drops to a 1870 x 1780 bed", SOFT),
    ],
)

# --------------------------------------------------------------------------
# Reference: "Brisa" by Dora Camper Studio - Fiat Ducato L2H2, only 5.40 m.
# Shortest van here by a long way: 3120 mm of load length and it still has a
# full standing shower, a split galley and a 4-seat salon.
# --------------------------------------------------------------------------
VARIANTS["ref-brisa"] = dict(
    out="ref/doracamper-brisa-ducato-l2h2/layout",
    length=3120, width=1870, well=(1600, 2500, 224), slider=(280, 1530),
    title='Dora Camper Studio "Brisa" - Fiat Ducato L2H2 (5.40 m overall)',
    note=("Reconstructed from video stills plus the narration. Dimensions estimated, +/-100 mm; "
      "the bed size is theirs. Counters re-cut to 900 from a close-up of the hob - which forces "
      "the bed to reach 360 mm forward between them, and explains the step at its head."),
    boxes=[
        (   0,  700, 1070, 1870, "SHOWER", "700 x 800 - tile - teak grate - window", WET),
        (   0,  200,    0, 1070, "SHELVES", "", WARM),
        ( 200,  700,    0, 1070, "ENTRY", "500 x 1070 - cab door forward", None),
        ( 700, 1600, 1270, 1870, "SINK", "900 x 600 - gold tap - Nespresso lift", GALLEY),
        ( 700, 1600,    0,  600, "HOB", "900 x 600 - gas 2-ring - fridge under", GALLEY),
        (1240, 1600,  600, 1270, "BED", "360 x 670", SOFT),
        (1600, 3120, 1350, 1870, "BENCH", "1520 x 520 - Victron + inverter", SOFT),
        (1600, 3120,    0,  520, "BENCH", "1520 x 520 - 90 L fresh", SOFT),
        (1600, 3120,  520, 1350, "TABLE -> BED", "bed 1880 fore-aft x 1350 across", SOFT),
    ],
)

# --------------------------------------------------------------------------
# Reference: Scarlet & Seth - Ram ProMaster 159" EXT, high roof, black.
# Shower turned sideways and parked against the cab bulkhead, which frees the
# whole middle of the van. Galley split across the aisle - sink and prep one
# side, a hob that slides forward out of the counter opposite. Rear dinette is
# a U reaching the same line on both sides, opening into a near-square bed.
# --------------------------------------------------------------------------
VARIANTS["ref-scarletseth"] = dict(
    out="ref/scarletseth-promaster-159ext/layout",
    length=4089, width=1869, well=(2450, 3350, 242), slider=(400, 1660),
    title='Scarlet & Seth - Ram ProMaster 159" EXT, high roof',
    note="Reconstructed from a 30-second tour plus their build blog. Dimensions estimated, +/-150 mm.",
    boxes=[
        (   0,  760,  560, 1869, "SHOWER", "Roman clay - boat-hatch skylight - roll door", WET),
        (   0,  760,    0,  560, "LOBBY", "shower door - pocket door to the cab", None),
        ( 760, 1260, 1269, 1869, "FRIDGE", "toilet drawer under", COLD),
        (1260, 2200, 1269, 1869, "SINK + PREP", "sink - oven - food store - bins", GALLEY),
        ( 760, 1060,  969, 1269, "BIN", "quarter-round seat", WARM),
        ( 760, 1660,    0, 1269, "ENTRY", "sliding door - floor kept clear", None),
        (1660, 2200,    0,  600, "STOVE", "pull-out hob", GALLEY),
        (2200, 4089,    0,  560, "BENCH", "litter box at the forward end", SOFT),
        (2200, 4089, 1309, 1869, "BENCH", "", SOFT),
        (2200, 4089,  560, 1309, "TABLE -> BED", "bed ~1890 fore-aft x 1870 across", SOFT),
    ],
)

# --------------------------------------------------------------------------
# v1 - Ford Transit L3H3, AWD. Configuration settled in the grilling session.
# --------------------------------------------------------------------------
VARIANTS["v1"] = dict(
    out="v1/layout",
    length=3450, width=1832, height=1781, well=(1863, 2763, 195), slider=(300, 1600),
    cab=800,                                   # cab depth drawn forward of x=0
    seats=[(-430, 460, 285), (-430, 1380, 285)],
    title="v1 - VW Crafter L3H3 · swivel seats, wet cubicle, rear dinette",
    viewer_title="Crafter L3H3 Interior",
    stats=["bed 1730 long", "galley aisle 1232", "corridor past cubicle 532",
           "worktop 900", "seat 520", "standing 1781"],
    note="Load box 3450 x 1832 x 1781 mm finished - the 4MOTION van, 100 lower than FWD. Furniture depths include the wall build. Estimated +/-50 mm.",
    boxes=[
        (-150,  550,  620, 1220, "TABLE", "Lagun swing arm", None),
        (   0,  620,    0, 1832, "FRONT LOUNGE", "swivel seats · office + seat", None),
        ( 620, 1600,    0, 1232, "ENTRY", "step-in · standing space", None),
        ( 620, 1720, 1232, 1832, "GALLEY", "sink + induction + oven under", GALLEY),
        (1600, 2350,    0,  700, "WET CUBICLE", "sit-down shower + WC · floor +360", WET),
        (1720, 2270, 1232, 1832, "FRIDGE", "70 L, over the arch", COLD),
        (2270, 3000, 1232, 1832, "BENCH", "battery + inverter", SOFT),
        (2350, 3000,    0,  700, "BENCH", "108 L fresh tank", SOFT),
        (3000, 3450,    0, 1832, "REAR BENCH", "garage - calorifier + electrics", SOFT),
        (1720, 3000,  700, 1232, "TABLE -> BED", "infill drops to a 1730 mm bed", SOFT),
    ],
    views=[
        dict(kind="elev", title="Driver side elevation", span=3450, left="FRONT", right="REAR",
             datum=(520, "bed / seat top 520"),
             boxes=[
                 (   0,  620,    0, 1781, "FRONT LOUNGE", "swivel seat + Lagun table", None),
                 ( 620, 1720,    0,  900, "GALLEY", "sink · induction · oven · one drawer stack", GALLEY),
                 ( 620, 1720, 1400, 1700, "overhead locker", "", WARM),
                 ( 900, 1550, 1000, 1350, "awning window", "", None),
                 (1720, 2270,    0,  900, "FRIDGE", "70 L, over the arch", COLD),
                 (2270, 3000,    0,  450, "BENCH", "battery + inverter under", SOFT),
                 (3000, 3450,    0,  450, "REAR BENCH", "", SOFT),
                 (2270, 3000, 1400, 1700, "overhead locker", "", WARM),
                 (2350, 3000,  620,  960, "awning window", "", None),
             ]),
        dict(kind="elev", title="Passenger side elevation (kerb side)", span=3450, left="FRONT", right="REAR",
             datum=(520, "bed / seat top 520"),
             boxes=[
                 (   0,  300,    0, 1781, "LOUNGE", "", None),
                 ( 300, 1600,    0, 1550, "SLIDING DOOR", "entry", None),
                 (1600, 2350,    0, 1781, "WET CUBICLE", "sit-down shower · floor +360", WET),
                 (1750, 2100,  410,  810, "cassette hatch", "", None),
                 (2350, 3000,    0,  450, "BENCH", "108 L fresh tank under", SOFT),
                 (3000, 3450,    0,  450, "REAR BENCH", "", SOFT),
                 (2350, 3000, 1400, 1700, "overhead locker", "", WARM),
                 (2400, 3000,  620,  960, "awning window", "", None),
             ]),
        dict(kind="sect", title="Section A-A · through the galley, looking forward", span=1832,
             left="DRIVER", right="PASSENGER",
             boxes=[
                 (   0,  600,    0,  900, "GALLEY", "600 deep", GALLEY),
                 (   0,  320, 1400, 1700, "locker", "", WARM),
             ],
             notes=[(1216, 1150, "entry / aisle 1232 wide"), (1650, 500, "sliding door")]),
        dict(kind="sect", title="Section B-B · through the wet cubicle, looking forward", span=1832,
             left="DRIVER", right="PASSENGER", datum=(520, "bed 1132 wide here"),
             boxes=[
                 (   0,  600,    0,  900, "FRIDGE", "70 L over the arch", COLD),
                 (   0,  320, 1400, 1700, "locker", "", WARM),
                 (1132, 1832,    0, 1781, "WET CUBICLE", "700 wide · floor +360", WET),
                 (1132, 1832,    0,  360, "step", "", WARM),
             ],
             notes=[(866, 1150, "corridor 532")]),
        dict(kind="sect", title="Section C-C · through the dinette, looking forward", span=1832,
             left="DRIVER", right="PASSENGER", datum=(520, "bed 1832 wide here"),
             boxes=[
                 (   0,  600,    0,  450, "BENCH", "battery + inverter under", SOFT),
                 (1132, 1832,    0,  450, "BENCH", "fresh tank", SOFT),
                 ( 600, 1132,  700,  760, "TABLE", "", WARM),
                 (   0,  320, 1400, 1700, "locker", "", WARM),
                 (1512, 1832, 1400, 1700, "locker", "", WARM),
             ],
             notes=[(916, 1150, "headroom 1781")]),
    ],
)


VARIANTS["v1-roof"] = dict(
    out="v1/roof",
    length=3300, width=1570,
    title="v1 roof - 400 W solar, two fans, Starlink flat mount",
    note=("Usable flat roof estimated at 3300 x 1570 mm for an L3H3 - measure the actual van. "
          "Panels mount on rails, never straight onto the roof ribs."),
    top_label="PASSENGER SIDE (kerb side) - service strip",
    boxes=[
        (  60, 1640,  762, 1570, "SOLAR 200 W", "1580 x 808", "#c9d4e4"),
        (1680, 3260,  762, 1570, "SOLAR 200 W", "1580 x 808", "#c9d4e4"),
        ( 860, 1340,  140,  620, "FAN", "over the galley", "#dce7e4"),
        (1700, 2300,  180,  580, "STARLINK", "flat mount", "#e7e0ec"),
        (2460, 2940,  140,  620, "FAN", "over the bed", "#dce7e4"),
    ],
)


# --------------------------------------------------------------------------
# v2 - VW Crafter L3H3 with a 3-seat cab and a partition wall behind it.
# Brisa's layout ported: shower in the front driver corner, galley split
# across the aisle, rear U-dinette. No swivel seats - the 3-seat bench makes
# them pointless, and the partition is what pays for the shower position.
# --------------------------------------------------------------------------
VARIANTS["v2"] = dict(
    out="v2/layout",
    length=3450, width=1832, height=1781, well=(1863, 2763, 226), slider=(300, 1600),
    cab=800,
    title="v2 - VW Crafter L3H3 - front shower + wardrobe, split galley, rear U",
    viewer_title="Crafter L3H3 v2 Interior",
    stats=["bed 1520 x 1832 at 630", "table 900 x 600 at 900", "shower opening 450",
           "garage 600 x 1832 x 570", "crawl-through 500 x 930", "galley aisle 632",
           "rear floor +220", "standing 1781"],
    note=("Load box 3450 x 1832 x 1781 mm finished - the 4MOTION van, 100 lower than FWD. Partition wall behind a 3-seat cab at x=0, "
          "with a hatch over the shoe locker instead of a walk-through - the bench backs onto "
          "the partition, so there was never a way past it. The rear is a U again, but the "
          "whole of it is "
          "lifted: you step up 220 into the footwell, the benches are 570 high, and the bed "
          "makes up at 630 across the van - 1832 gross, ~1760 after the wall build. That lift "
          "is the storage: 570 of garage under the rear bench, and a shallow drawer under the "
          "footwell floor. The table is 900 x 600 on a post at 900, the galley worktop height, "
          "and drops onto cleats to become the middle of the bed. WC stows under the wardrobe "
          "and slides forward into the shower, cassette out through the driver-side panel. The "
          "U is one carcass, so the fresh tank runs the side-to-rear corner, inboard of the "
          "wheel arch. Estimated +/-50 mm."),
    shapes={"SHOWER": [(0, 1032), (700, 1232), (700, 1832), (0, 1832)]},
    boxes=[
        ( 400, 1090,  660, 1032, "ENTRY", "690 wide at the side door - the lobby", None),
        (   0,  700, 1032, 1832, "SHOWER", "700 x 800>600 - diagonal face - 450 opening aft", WET),
        ( 700, 1150, 1232, 1832, "WARDROBE", "450 x 600 - WC under", WARM),
        (   0,  450,    0,  400, "LOCKER", "450 x 400 - shoes - step to the hatch", SOFT),
        (-190,  210,  580,  980, "CAT", "400 x 400 - slides behind the bench - flap aft", WARM),
        ( 460,  800,   60,  440, "SIDE TABLE", "340 x 380 at 720 - L bracket off the locker", GALLEY),
        ( 750, 1150,    0,  600, "WORKTOP", "400 x 600 - fold-down leaf", GALLEY),
        (1150, 1930, 1232, 1832, "SINK", "780 x 600 - 440 single bowl, 340 prep aft", GALLEY),
        (1150, 1930,    0,  600, "HOB", "780 x 600 - hob forward, 480 prep aft", GALLEY),
        (1150, 1930,  600, 1232, "AISLE", "780 x 632", None),
        (1930, 2850, 1232, 1832, "BENCH", "920 x 600 - battery + inverter", SOFT),
        (1930, 2850,    0,  600, "BENCH", "920 x 600 - 118 L tank inboard of arch", SOFT),
        (1930, 2850,  600, 1232, "FOOTWELL -> BED", "632 wide - floor +220, drawer under", SOFT),
        (2850, 3450,    0, 1832, "REAR BENCH", "600 x 1832 - garage 570 clear under", SOFT),
    ],
)


# --------------------------------------------------------------------------
# v3 - VW Crafter L3H3. Same van and same 3-seat cab as v2, turned around:
# the bed moves to the FRONT as an L-sofa that converts, and the whole rear
# becomes a bathroom on the driver side with a full-height garage closet
# beside it. The bed now sleeps FORE-AFT, which is what buys the length.
# --------------------------------------------------------------------------
VARIANTS["v3"] = dict(
    out="v3/layout",
    length=3450, width=1832, height=1781, well=(1863, 2763, 226), slider=(300, 1600),
    cab=800,
    title="v3 - VW Crafter L3H3 - L-galley, dinette that works as the office, rear bathroom",
    viewer_title="Crafter L3H3 v3 Interior",
    stats=["bed 1520 x 1832 across", "galley 1.15 m2", "bathroom 600 x 1232",
           "entry 730", "corridor 632", "garage 600 wide full height"],
    note=("Load box 3450 x 1832 x 1781 mm finished - the 4MOTION van. The galley is a proper L round the corner "
          "behind the driver: 600 x 1382 across the bulkhead and a 530 return down the driver "
          "wall, then the larder. No separate office seat - two people work at the dinette, "
          "facing each other across the 632 corridor with the table at 745. The bed is TWO "
          "parallel benches; the corridor between them runs to the bathroom door, and a wall "
          "closes the bed off from the bathroom and the garage. Estimated +/-50 mm."),
    boxes=[
        (   0,  600,  450, 1832, "GALLEY", "600 x 1382 - hob at the door, sink in the corner", GALLEY),
        ( 600, 1130, 1232, 1832, "GALLEY", "530 x 600 - return - oven under", GALLEY),
        (   0,  600,    0,  450, "LOCKER", "shoes - step - leaf over it", SOFT),
        (1130, 1330, 1232, 1832, "LARDER", "200 x 600 - pull-out", WARM),
        ( 600, 1330,    0,  600, "ENTRY", "730 clear at the door - aisle 632", None),
        (1330, 2850, 1232, 1832, "BENCH -> BED", "1520 x 600 - batteries + calorifier under", SOFT),
        (1330, 2850,    0,  600, "BENCH -> BED", "1520 x 600 - 118 L fresh tank inboard of the arch", SOFT),
        (1330, 2850,  600, 1232, "CORRIDOR -> BED", "632 wide - to the bathroom", None),
        (1640, 2540,  636, 1196, "TABLE", "900 x 560 - 745 to work, 700 to eat, 450 as bed", None),
        (2850, 3450,  600, 1832, "BATHROOM", "1232 wide - pocket door", WET),
        (2850, 3450,    0,  600, "GARAGE", "600 wide - loads from the back", WARM),
    ],
)


# --------------------------------------------------------------------------
# v4 - VW Crafter L3H3. Bathroom squeezed thin and run the full width at the
# very back; fixed crosswise bed in front of it over a full-width garage, and
# the WC slides aft out of that garage. Everything else - galley, a front
# office seat behind the driver, a thin larder - shares the front 1550.


# --------------------------------------------------------------------------
# v5 - v4 with the driver seat on a swivel base. The double passenger bench
# cannot turn and never could; the driver seat is on the other side of the
# cab and nothing about a 3-seat front stops it. So the office bench is
# deleted and its 450 becomes open floor - same geometry, a far better chair.


# Every variant carries its own key, so model3d.py can look up the 3D fit-out that belongs
# to it instead of guessing from the geometry.
for _name, _variant in VARIANTS.items():
    _variant["name"] = _name


def draw(ax, v):
    """Plan view."""
    LEN, WID = v["length"], v["width"]

    if v.get("cab"):
        ax.add_patch(Rectangle((-v["cab"], 0), v["cab"], WID, fc="#f2f0eb", ec="#bbb",
                               lw=1, ls=(0, (5, 4)), zorder=1))
        ax.text(-v["cab"] / 2, WID + 60, "cab", ha="center", va="top", fontsize=6, color="#aaa")
    for cx, cy, r in v.get("seats", []):
        ax.add_patch(Circle((cx, cy), r, fc="none", ec="#999", lw=1.2, ls=(0, (4, 3)), zorder=4))
    if v.get("seats"):
        ax.text(v["seats"][0][0], WID / 2, "seats swivel", ha="center", va="center",
                fontsize=5.5, color="#999", zorder=5)

    ax.add_patch(Rectangle((0, 0), LEN, WID, fc="white", ec="#222", lw=3, zorder=2))

    # A box can be drawn as a polygon instead, when the thing it stands for is not square in
    # plan - v2's shower has a diagonal face. The box stays: it is the label position and
    # the bounding size the rest of the tooling reads.
    shapes = v.get("shapes", {})
    for x0, x1, y0, y1, lab, sub, fc in v["boxes"]:
        open_floor = fc is None
        style = dict(fc="none" if open_floor else fc, ec="#b5b5b5" if open_floor else "#8a8a8a",
                     lw=1.2, ls=(0, (4, 3)) if open_floor else "-", zorder=3)
        if lab in shapes:
            ax.add_patch(Polygon(shapes[lab], closed=True, **style))
        else:
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **style))
        cx = (x0 + x1) / 2
        # open zones label at their top edge, so furniture drawn inside them stays readable
        cy = y0 + 130 if open_floor else (y0 + y1) / 2
        rot = 0 if open_floor else (90 if (x1 - x0) < 620 else 0)
        col = "#999" if open_floor else "#222"
        ax.text(cx - (40 if (rot and sub) else 0), cy - (40 if (not rot and sub and not open_floor) else 0),
                lab, ha="center", va="center", rotation=rot, fontsize=8.5, weight="bold",
                color=col, zorder=5)
        if sub:
            ax.text(cx + (105 if rot else 0), cy + (0 if rot else 105), sub, ha="center", va="center",
                    rotation=rot, fontsize=6, color="#888" if open_floor else "#666", zorder=5)

    if v.get("well"):
      w0, w1, wd = v["well"]
      for y in (0, WID - wd):
        ax.add_patch(Rectangle((w0, y), w1 - w0, wd, fc="none", ec="#b03a3a", lw=1.2,
                               ls=(0, (4, 3)), zorder=6))
      ax.text((w0 + w1) / 2, wd / 2, "wheel well", ha="center", va="center", fontsize=5.5,
              color="#b03a3a", zorder=7)

    if v.get("slider"):
        d0, d1 = v["slider"]
        ax.plot([d0, d1], [0, 0], color="#0f9d78", lw=5, solid_capstyle="butt", zorder=8)
        ax.text((d0 + d1) / 2, -70, "SLIDING DOOR  ~%d mm" % (d1 - d0), ha="center", va="bottom",
                fontsize=7.5, weight="bold", color="#0f9d78")

    ax.text(LEN / 2, -230, v.get("top_label", "PASSENGER SIDE (kerb side)"),
            ha="center", fontsize=7, color="#999")
    ax.text(LEN / 2, WID + 130, "DRIVER SIDE", ha="center", va="top", fontsize=7.5,
            weight="bold", color="#555")
    ax.text(LEN + 90, WID / 2, "REAR", ha="center", va="center", rotation=270, fontsize=8,
            weight="bold", color="#555")
    ax.text(LEN / 2, WID + 300, v["note"], ha="center", va="top", fontsize=6, color="#aaa",
            style="italic")

    ax.set_xlim(-(v.get("cab", 0) + 220), LEN + 320)
    ax.set_ylim(WID + 560, -400)          # inverted: driver side at the bottom
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(v["title"], fontsize=11, weight="bold", color="#111", pad=14)


def draw_view(ax, view, height):
    """Elevation or cross-section."""
    span = view["span"]
    ax.add_patch(Rectangle((0, 0), span, height, fc="white", ec="#222", lw=2.5, zorder=1))

    for a0, a1, z0, z1, lab, sub, fc in view["boxes"]:
        open_box = fc is None
        ax.add_patch(Rectangle((a0, z0), a1 - a0, z1 - z0, fc="none" if open_box else fc,
                               ec="#b5b5b5" if open_box else "#8a8a8a", lw=1.1,
                               ls=(0, (4, 3)) if open_box else "-", zorder=2))
        if not lab:
            continue
        big = (a1 - a0) >= 600 and (z1 - z0) >= 300
        col = "#999" if open_box else "#222"
        ca, cz = (a0 + a1) / 2, (z0 + z1) / 2
        ax.text(ca, cz + (55 if (sub and big) else 0), lab, ha="center", va="center",
                fontsize=8 if big else 5.5, weight="bold", color=col, zorder=4)
        if sub and big:
            ax.text(ca, cz - 75, sub, ha="center", va="center", fontsize=5.5,
                    color="#888" if open_box else "#666", zorder=4)

    if view.get("datum"):
        z, lab = view["datum"]
        ax.plot([0, span], [z, z], color="#0f9d78", lw=1.1, ls=(0, (6, 4)), zorder=5)
        ax.text(span - 40, z + 55, lab, ha="right", va="bottom", fontsize=5.5, color="#0f9d78")

    for a, z, txt in view.get("notes", []):
        ax.text(a, z, txt, ha="center", va="center", fontsize=5.5, color="#999", zorder=4)

    ax.text(-70, height / 2, view["left"], ha="center", va="center", rotation=90,
            fontsize=6.5, weight="bold", color="#777")
    ax.text(span + 70, height / 2, view["right"], ha="center", va="center", rotation=270,
            fontsize=6.5, weight="bold", color="#777")
    ax.text(span / 2, -110, "%d mm wide x %d mm clear" % (span, height), ha="center", va="top",
            fontsize=5.5, color="#aaa")

    ax.set_xlim(-190, span + 190)
    ax.set_ylim(-260, height + 120)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(view["title"], fontsize=8.5, weight="bold", color="#111", pad=8)


def overlay_png(v, path, inch_per_m=3.2, dpi=200):
    """The plan cropped to exactly the load box, for the 3D viewer's schema overlay.

    Same drawing code as the layout, so the viewer shows the real plan rather than a redrawn
    copy of it - only the cab, the title and the margins are outside the crop. The axes fill
    the figure and the figure has the van's own aspect ratio, so one pixel is one fixed number
    of millimetres and the image lies on the floor of the 3D model 1:1. That is also why the
    aspect goes back to "auto": "equal" lets matplotlib shrink the axes inside the figure,
    which would slide the drawing off the floor it is supposed to match.
    """
    L, W = v["length"], v["width"]
    fig = plt.figure(figsize=(L / 1000.0 * inch_per_m, W / 1000.0 * inch_per_m), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    draw(ax, v)
    ax.set_title("")
    ax.set_aspect("auto")
    ax.set_xlim(0, L)
    ax.set_ylim(W, 0)
    ax.axis("off")
    fig.savefig(path, facecolor="white", dpi=dpi)
    plt.close(fig)
    print("wrote", path)
    return path


def render_views(v):
    views, height = v["views"], v["height"]
    elevs = [x for x in views if x["kind"] == "elev"]
    sects = [x for x in views if x["kind"] == "sect"]
    fig = plt.figure(figsize=(14, 18.5), dpi=110)
    fig.patch.set_facecolor("#fbfaf7")
    gs = fig.add_gridspec(len(elevs) + 1, max(len(sects), 1),
                          height_ratios=[7.4] * len(elevs) + [4.9], hspace=0.10, wspace=0.10)
    for i, view in enumerate(elevs):
        draw_view(fig.add_subplot(gs[i, :]), view, height)
    for j, view in enumerate(sects):
        draw_view(fig.add_subplot(gs[len(elevs), j]), view, height)
    fig.suptitle(v["title"] + "  ·  elevations and sections", fontsize=12, weight="bold", y=0.975)
    stem = v["out"].rsplit("/", 1)[0] + "/views" if "/" in v["out"] else "views"
    for ext in ("png", "svg"):
        fig.savefig("%s.%s" % (stem, ext), facecolor=fig.get_facecolor(), bbox_inches="tight")
        print("wrote", "%s.%s" % (stem, ext))


def main(name):
    v = VARIANTS[name]
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=160)
    fig.patch.set_facecolor("#fbfaf7")
    draw(ax, v)
    for ext in ("png", "svg"):
        fig.savefig("%s.%s" % (v["out"], ext), facecolor=fig.get_facecolor(), bbox_inches="tight")
        print("wrote", "%s.%s" % (v["out"], ext))
    if v.get("views"):
        render_views(v)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v1")
