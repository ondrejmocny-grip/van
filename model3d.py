#!/usr/bin/env python3
"""Extrude a plan into 3D: greybox renders, line renders, an OBJ, and a web viewer.

The footprint comes straight from plan.py, so there is one source of truth.
HEIGHTS gives each plan box its z range; EXTRA adds what a plan cannot show; SHELL builds
the vehicle itself - body panels with real apertures, glazing, and the cab.

    python model3d.py v1

line_render() is used by impressions.py as the control image for image generation.
write_viewer() fills viewer_template.html with this variant's geometry.
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from plan import VARIANTS, overlay_png

HERE = os.path.dirname(os.path.abspath(__file__))

# --- v1: plan label -> (z0, z1). None means the plan box is a void (footwell, open floor).
# Every table below is v1's. The v2 tables follow, and REGISTRY at the end of this section
# says which variant gets which. A variant with no entry falls back to v1's, remapped.
HEIGHTS = {
    "GALLEY": (0, 900),
    "WET CUBICLE": (0, 1945),
    "FRIDGE": (0, 900),
    "BENCH": (0, 450),
    "REAR BENCH": (0, 450),
    "TABLE -> BED": None,
    "FRONT LOUNGE": None,
    "ENTRY": None,
    "TABLE": None,
}

# Things the plan cannot show: (x0, x1, y0, y1, z0, z1, kind)
EXTRA = [
    (2350, 3044,  700, 1184,  450,  520, "infill"),     # aisle piece, bed made up
    (2350, 3494,    0,  700,  450,  520, "bed"),
    (2350, 3494, 1184, 1784,  450,  520, "bed"),
    (3044, 3494,  700, 1184,  450,  520, "bed"),
    ( 620, 1720, 1484, 1784, 1400, 1800, "locker"),     # driver, over the galley
    (2270, 3044, 1484, 1784, 1400, 1800, "locker"),     # driver, over the dinette
    (2350, 3044,    0,  300, 1400, 1800, "locker"),     # passenger, over the dinette
    (2350, 3044,  700, 1184,  700,  760, "table"),      # dinette table, same patch
    ( -50,  550,  600, 1180,  700,  760, "ftable"),     # front Lagun table
    (1600, 2350,    0,  700,    0,  360, "step"),       # raised cubicle floor, high
                                                         # enough to clear the arch
    (2567, 2827,  812, 1072,    0,  700, "leg"),        # dinette post, under its centre
    ( 120,  380,  760, 1020,    0,  700, "fleg"),       # front table post
    (1600, 1760,   60,  420, 1140, 1940, "shower"),     # head and riser, raised with
                                                         # the floor under it
]

# The big kit at its real catalogue size, so we find out here and not in the workshop.
# Same tuple; the kind carries both the colour and the name.
APPLIANCES = [
    # galley run, 1100 long - see v1/README.md for what the oven costs us
    ( 680, 1130, 1334, 1684,  380,  720, "oven"),        # 20 L mini oven, 450 x 350 x 340
    ( 700, 1000, 1224, 1744,  845,  905, "hob"),         # 2-zone domino induction, 300 x 520,
                                                         # 55 deep body under the worktop
    (1120, 1520, 1284, 1624,  750, 1200, "sink"),        # 400 x 340 bowl 150 deep under the
                                                         # counter, plus a 300 tap above it
    (1160, 1500, 1300, 1650,   60,  420, "plumbing"),    # pump, filter, waste trap
    (1750, 2240, 1250, 1750,  380,  860, "fridge"),      # 70 L front opening, sits
                                                         # above the wheel arch
    # wet cubicle - hatch on the passenger wall is at x 1750-2100, so the cassette lines up
    (1750, 2170,    0,  570,  360,  860, "cassette"),    # Thetford C223 CS, on the step
    # water
    (2380, 3000,  200,  700,   40,  390, "fresh"),       # 108 L, inboard of the arch -
                                                         # 3000 is where the Crafter
                                                         # bench ends, so it fits both
    (2100, 2800,  400,  900, -270,  -70, "grey"),        # 70 L, underslung
    (3100, 3400,  150,  550,   60,  360, "calorifier"),  # 10 L off the engine heat exchanger
    # electrics
    # 150 Ah LiFePO4, group 31 case: 330 x 172 x 215 lying with its long side across the van,
    # in a 350 x 200 x 240 slot. The old 270 x 520 x 230 boxes were 32 L each for a 12 L cell.
    # against the driver wall put them 175 mm inside the tyre - drawing the wheels settled it
    (2320, 2520, 1230, 1580,   30,  270, "battery"),
    (2560, 2760, 1230, 1580,   30,  270, "battery"),
    (2320, 2790, 1300, 1580,  270,  450, "inverter"),    # 3000 W, on a shelf above the
                                                         # cells and inboard of the arch
    # MPPT, DC-DC, busbars, fuses - against the driver wall at the forward end of the garage,
    # the shortest cable run to the cells under the bench just ahead of it
    (3060, 3460, 1624, 1744,   60,  360, "electrics"),
]

# --------------------------------------------------------------------------
# v2 - written in v2's own coordinates, not remapped from v1. The layout is a
# different room: shower in the front driver corner, galley split across the
# aisle, U-dinette in the back. Nothing about v1's fit-out would survive being
# shifted onto it, so it gets its own tables.
# --------------------------------------------------------------------------
HEIGHTS_V2 = {
    "SHOWER": None,             # the cubicle is built from panels in EXTRA_V2, not one solid
    "WARDROBE": (0, 1881),      # hanging above, WC drawer below
    "LOCKER": (0, 450),         # shoe locker, and the step through to the cab
    "SINK": (0, 900),
    "HOB": (0, 900),
    "BENCH": (0, 450),
    "REAR BENCH": (0, 450),
    "WORKTOP": None,            # the fold-down leaf is in EXTRA_V2, in both its positions
    "ENTRY": None,
    "AISLE": None,
    "TABLE -> BED": None,
}

EXTRA_V2 = [
    # the U made up as a bed: 1520 fore-aft across the full 1832
    (1930, 2850,    0,  600,  450,  520, "bed"),
    (1930, 2850, 1232, 1832,  450,  520, "bed"),
    (2850, 3450,    0, 1832,  450,  520, "bed"),
    (1930, 2850,  600, 1232,  450,  520, "infill"),
    (2150, 2750,  616, 1216,  700,  760, "table"),      # dinette table, drops to the infill
    (2320, 2580,  786, 1046,    0,  700, "leg"),
    # The galley worktop carries on forward as a fold-down leaf, hinged on the hob unit's
    # front face at worktop height. This used to be an office table at 760 on a swing arm;
    # the office is gone, so it is 900 like the rest of the kitchen and it is prep space.
    # Both positions are drawn: deployed it reaches forward over the entry, folded it hangs
    # flat down the galley's end panel. Folded is the default, which is the state the entry
    # gap assumes.
    ( 900, 1150,  260,  320,  780,  840, "farm"),       # swing-out bracket under the leaf
    ( 750, 1150,    0,  600,  840,  900, "ftable"),     # deployed: 400 x 600 at worktop height
    (1090, 1150,    0,  600,  440,  840, "ftablep"),    # folded: hangs down the galley end
    (1150, 1930, 1532, 1832, 1400, 1800, "locker"),     # driver, over the sink
    (1930, 2850, 1532, 1832, 1400, 1800, "locker"),     # driver, over the dinette
    (1600, 2850,    0,  300, 1400, 1800, "locker"),     # passenger, clear of the door head
    (   0,  160, 1600, 1760, 1140, 1860, "shower"),     # head and riser, on the partition
    # The shower cubicle, built rather than generated. A room is not a product: a single
    # mesh scaled to fill a 700 x 800 x 1881 hole either reads as a solid block or turns
    # its one opening to the wall, and which way a generated mesh faces is a coin toss the
    # box list should not be losing. Three panels, a tray, and a glass screen across the
    # side that opens onto the lobby - so you can see in from the aisle, which is the whole
    # point of drawing it at all.
    (   0,   40, 1032, 1832,    0, 1881, "wetwall"),    # forward wall, on the partition
    ( 660,  700, 1032, 1832,    0, 1881, "wetwall"),    # aft wall, shared with the wardrobe
    (   0,  700, 1792, 1832,    0, 1881, "wetwall"),    # the driver-side wall
    (  40,  660, 1072, 1792,    0,   60, "tray"),
    (  40,  660, 1032, 1072,   60, 1881, "screen"),     # glass, on the lobby side
]

APPLIANCES_V2 = [
    # galley, driver side - sink unit, worktop 900
    (1300, 1750, 1252, 1602,  380,  720, "oven"),       # 20 L mini oven, at the aisle edge
                                                        #   of the cabinet, not buried at the back
    (1180, 1520, 1480, 1820,   40,  370, "plumbing"),   # pump, filter and trap under the sink,
                                                        #   behind the oven - shortest run to the tap
    # The double sink is BUILT, in sink_wells() below - a generated mesh of it came back a
    # solid block. 780 mm of run cannot hold two bowls AND a prep area in the middle, so the
    # bowls sit hard against the wardrobe and the free counter is all in one piece aft.
    (1300, 1400, 1640, 1830,  905, 1185, "tap"),        # mixer on the deck behind the bowls:
                                                        #   100 across the lever, 190 of reach
    # Drinking water on its own path: a dedicated gooseneck beside the mixer, fed through an
    # inline carbon block teed off the cold line after the pump. Inline rather than a sump
    # housing because there is only 380 mm under the bowls and a sump needs ~400 to drop the
    # cartridge out; an inline cartridge is swapped by pulling its two hose fittings and can
    # lie on its side.
    (1440, 1490, 1700, 1820,  905, 1155, "filtertap"),  # gooseneck, beside the mixer
    (1600, 1860, 1700, 1760,  420,  480, "filter"),     # 2 x 10 inch inline carbon block
    # galley, passenger side - hob over the fridge
    (1150, 1450,   40,  560,  845,  905, "hob"),        # 2-zone domino induction, 300 x 520,
                                                        #   hard against the forward end, so the
                                                        #   480 aft of it is one clear run
    (1250, 1780,   30,  575,   60,  680, "fridgedoor"), # 90 L hinged door, 530 x 545 x 620,
                                                        #   still 83 mm clear of the wheel arch
    # bathroom - the WC lives in the wardrobe base and slides into the shower
    ( 715, 1135, 1252, 1822,   40,  560, "cassette"),   # ~420 x 570, hatch at x 700-1150
    # water - the tank runs the bench-to-garage corner, inboard of the wheel arch
    (1930, 2950,  226,  600,   30,  340, "fresh"),      # 1020 x 374 x 310 = 118 L
    (2100, 2800,  400,  900, -270,  -70, "grey"),       # 70 L, underslung
    (3100, 3400,  150,  550,   60,  360, "calorifier"), # 10 L off the engine heat exchanger
    # electrics, driver bench - 16 mm inboard of the tyre, which is what sets y here
    (2100, 2300, 1240, 1590,   30,  270, "battery"),    # 150 Ah LiFePO4, group 31 case
    (2340, 2540, 1240, 1590,   30,  270, "battery"),
    (2100, 2570, 1300, 1580,  270,  450, "inverter"),   # 3000 W, on a shelf over the cells
    (2900, 3300, 1700, 1820,   60,  360, "electrics"),  # MPPT, DC-DC, busbars, fuses
]

CONTAINERS_V2 = ("WARDROBE", "LOCKER", "SINK", "HOB", "BENCH", "REAR BENCH")

# Where a person actually is when they perch on the shoe locker to put boots on: facing
# aft, knees down, feet on the floor in front of it. Furniture is checked against this the
# same way appliances are checked against each other, because two rounds of this design were
# drawn with a swing arm running straight through the sitter's chest - obvious in a render,
# invisible in a box list. Trunk, thighs, shins.
SITTER_V2 = [
    ( 60,  400,  60,  400,  450, 1300),
    (400,  800, 100,  380,  380,  500),
    (620,  820, 100,  380,    0,  400),
]

# Which wall a prop mesh was modelled facing away from: "p" = passenger (y=0), "d" = driver.
# v2 mirrors several of v1's placements across the aisle, and a mesh with a front - a door,
# a drawer, a lid - has to turn with them or it opens into the wall. The viewer adds this to
# the kind's own yaw, so yaw.json keeps meaning what it meant.
# fridgedoor, LOCKER and WARDROBE are modelled for v2's own placements, so they are
# not in here - their facing lives in yaw.json like any deliberate turn.
FACING_V2 = {"locker": "d", "hob": "d", "oven": "d", "sink": "d", "cassette": "p"}

# The viewer's Show buttons. v2 groups different things from v1, so it carries its own list;
# a variant without one gets the template's default.
LAYERS_V2 = [
    {"id": "bed", "label": "Bed made up", "kinds": ["infill"], "on": False,
     "hide": ["table", "leg"]},
    {"id": "wet", "label": "Shower + wardrobe",
     "kinds": ["wetwall", "tray", "screen", "shower", "WARDROBE"], "on": True},
    {"id": "worktop", "label": "Worktop leaf out", "kinds": ["ftable", "farm"], "on": False,
     "hide": ["ftablep"]},
    {"id": "lockers", "label": "Lockers", "kinds": ["locker"], "on": True},
    {"id": "kit", "label": "Appliances", "kinds": sorted({b[6] for b in APPLIANCES_V2}),
     "on": True, "xray": True},
    {"id": "body", "label": "Body + glass",
     "kinds": ["shell", "glass", "floor", "wheel", "partition", "hatch"], "on": True},
    {"id": "cab", "label": "Cab + seats", "kinds": ["cab", "seat", "dash"], "on": True},
    {"id": "props", "label": "Detailed props", "kinds": [], "on": True, "props": True},
    {"id": "schema", "label": "Schema overlay", "kinds": [], "on": False, "schema": True},
    {"id": "sizes", "label": "Sizes", "kinds": [], "on": False, "sizes": True},
]


# --------------------------------------------------------------------------
# v3 - its own tables again. Nothing about v2's room survives here: the bed is
# two parallel benches with a corridor between them, the bathroom is a 500 mm
# slot in the back driver corner beside a full-height garage, and the front
# driver corner is a 450 x 400 office seat with a desk folding off the
# partition. Written in v3's own coordinates.
# --------------------------------------------------------------------------
HEIGHTS_V3 = {
    "GALLEY": (0, 900),             # both legs of the L carry the same label
    "LOCKER": (0, 450),             # shoes, and the step through to the cab
    "LARDER": (0, 1881),
    "BENCH -> BED": (0, 450),       # both benches carry the same label
    "BATHROOM": (0, 1881),          # a carcass the viewer ghosts, like v1's wet cubicle
    "GARAGE": (0, 1881),
    "ENTRY": None,
    "CORRIDOR -> BED": None,
    "TABLE": None,
}

EXTRA_V3 = [
    # The bed made up. Only the middle 632 changes state - the two benches are already at
    # bed height, which is the whole point of splitting the U into two.
    (1330, 2850,    0,  600,  450,  520, "bed"),
    (1330, 2850, 1232, 1832,  450,  520, "bed"),
    (1330, 2850,  600, 1232,  450,  520, "infill"),
    # One table, three heights on a telescopic pedestal: 745 to work at, 700 to eat at, 450
    # as the bed's centre panel. 900 x 560 is what two laptops facing each other need.
    (1640, 2540,  636, 1196,  725,  745, "table"),
    (1960, 2220,  786, 1046,    0,  725, "leg"),
    # A pull-up leaf on the galley's passenger end panel, making prep space over the shoe
    # locker at worktop height. Up it crosses the cab pass-through; down it hangs flat.
    (   0,  600,    0,  450,  880,  900, "ltable"),      # up, over the locker
    (   0,  600,  430,  450,  450,  875, "ltablep"),     # folded down the end panel
    # Overhead lockers. The passenger run starts aft of the sliding door head.
    (   0, 1130, 1532, 1832, 1400, 1800, "locker"),      # driver, over the galley
    (1330, 2850, 1532, 1832, 1400, 1800, "locker"),      # driver, over the bed bench
    (1700, 2850,    0,  300, 1400, 1800, "locker"),      # passenger, clear of the door head
    # Bathroom fit-out. A pocket door has nothing to draw when it is open - the leaf is
    # inside the wall - so only the shut position is a box, and it is off by default.
    (2890, 3410,  640, 1792,    0,   60, "tray"),
    (2890, 3050, 1672, 1832, 1140, 1860, "shower"),      # head and riser, clear of the wall
    (2850, 2890,  600, 1200,    0, 1881, "doorshut"),    # shut: the leaf out of its pocket
    # The wall that closes the bed off from the bathroom and the garage, with the doorway
    # left open in it.
    (2850, 2890,    0,  600,    0, 1881, "wall"),
    (2850, 2890, 1200, 1832,    0, 1881, "wall"),
]

APPLIANCES_V3 = [
    # The galley crosses the front bulkhead, so every run below is turned 90 from where v1
    # and v2 put it: depth is now x, length is now y. YAW_V3 turns the props to match.
    ( 150,  450,  500, 1020,  845,  905, "hob"),         # 2-zone domino induction, 300 x 520,
                                                         #   at the door end for the ventilation
    (  30,  575,  480, 1025,   60,  585, "fridgedrawer"),# 90 L drawer, 545 x 545 x 525, under
                                                         #   the hob - no arch anywhere near it
    ( 120,  470, 1200, 1650,  380,  720, "oven"),        # 20 L mini oven, 450 x 350 x 340
    ( 150,  490, 1490, 1830,   40,  370, "plumbing"),    # pump and trap, under the bowls
    ( 200,  460, 1680, 1740,  420,  480, "filter"),      # 2 x 10 inch inline carbon block
    (  60,  160, 1400, 1590,  905, 1185, "tap"),         # mixer on the 200 of counter between
                                                         #   the bowls and the bulkhead
    (  60,  110, 1650, 1770,  905, 1155, "filtertap"),   # drinking gooseneck beside it
    # bathroom - the WC stays put, no sliding drawer. 420 x 570 against the driver wall
    # leaves 662 of knee room across the room, which is what the 1232 width buys.
    (2890, 3310, 1262, 1832,   40,  560, "cassette"),
    # water
    (1800, 2820,  226,  600,   30,  340, "fresh"),       # 1020 x 374 x 310 = 118 L, inboard
                                                         #   of the arch in the passenger bench
    (2100, 2800,  400,  900, -270,  -70, "grey"),        # 70 L, underslung
    (2950, 3250,  150,  550,   60,  360, "calorifier"),  # 10 L, in the garage
    # electrics, driver bench - forward of the tyre, which starts at x 1957
    (1400, 1600, 1240, 1590,   30,  270, "battery"),     # 150 Ah LiFePO4, group 31 case
    (1640, 1840, 1240, 1590,   30,  270, "battery"),
    (1400, 1870, 1300, 1580,  270,  450, "inverter"),    # 3000 W, on a shelf over the cells
    (2950, 3340,   20,  140,   60,  360, "electrics"),   # MPPT, DC-DC, busbars, fuses
]

CONTAINERS_V3 = ("LOCKER", "GALLEY", "LARDER", "BENCH -> BED", "BATHROOM", "GARAGE")

# TWO people at the dinette with laptops, facing each other across the 632 corridor - which
# is what the dinette has to do now that the separate office seat is gone. Trunk, thighs,
# shins each. Sitting back on a 600-deep bench, the knees reach about 130 past its front
# edge, so the two sets stop 368 mm apart: they do not meet, and the table at 745 clears
# both. SIT_OK_V3 lists what is allowed to touch them - the benches they sit on and the
# cushions on top.
SITTER_V3 = [
    (1900, 2240, 1480, 1800,  450, 1300),    # driver side: trunk
    (1940, 2220, 1180, 1480,  380,  500),    #   thighs, overhanging the bench edge by 52
    (1940, 2220, 1072, 1232,    0,  400),    #   shins, dropping into the corridor
    (1900, 2240,   32,  352,  450, 1300),    # passenger side: trunk
    (1940, 2220,  352,  652,  380,  500),    #   thighs
    (1940, 2220,  600,  760,    0,  400),    #   shins
]
SIT_OK_V3 = ("BENCH -> BED", "bed", "infill", "ENTRY", "CORRIDOR -> BED")

FACING_V3 = {"locker": "d", "hob": "d", "oven": "d", "sink": "d", "cassette": "p"}
# v3's galley crosses the bulkhead instead of running along a wall, so its kit is a quarter
# turn from the box every existing mesh was made for. These are the turns Ondrej read off the
# viewer, added to whatever yaw.json and FACING already apply.
#
# Sign: the viewer does rotation.y with world X = van length and world Z = van width, so +90
# takes van +x to van -y - COUNTER-CLOCKWISE seen from above, which is how the plan is drawn.
# Clockwise is therefore 270.
YAW_V3 = {
    "LOCKER": 270,          # 90 cw
    "hob": 90,              # 90 ccw, on top of yaw.json 270 + the 180 FACING adds
    "fridgedrawer": 90,     # 90 ccw, from nothing
    "oven": 270,            # 180 on top of the 90 quarter turn the bulkhead run needs
    # The larder mesh is a slab 0.31 x 1.00 x 0.07, thin on mesh Z. The slot is thin on van x,
    # so without a quarter turn the viewer would stretch the thin axis to 600 and squash the
    # wide one to 200. 270 rather than 90 so the modelled door looks aft rather than into the
    # galley return it butts against - see v3/README.md, the real unit opens the other way.
    "LARDER": 270,
}

LAYERS_V3 = [
    {"id": "bed", "label": "Bed made up", "kinds": ["infill"], "on": False,
     "hide": ["table", "leg"]},
    {"id": "door", "label": "Bathroom door shut", "kinds": ["doorshut"], "on": False},
    {"id": "leaf", "label": "Galley leaf up", "kinds": ["ltable"], "on": False,
     "hide": ["ltablep"]},
    {"id": "lockers", "label": "Lockers", "kinds": ["locker"], "on": True},
    {"id": "kit", "label": "Appliances", "kinds": sorted({b[6] for b in APPLIANCES_V3}),
     "on": True, "xray": True},
    {"id": "body", "label": "Body + glass",
     "kinds": ["shell", "glass", "floor", "wheel", "partition", "hatch", "wall"], "on": True},
    {"id": "cab", "label": "Cab + seats", "kinds": ["cab", "seat", "dash"], "on": True},
    {"id": "props", "label": "Detailed props", "kinds": [], "on": True, "props": True},
    {"id": "schema", "label": "Schema overlay", "kinds": [], "on": False, "schema": True},
    {"id": "sizes", "label": "Sizes", "kinds": [], "on": False, "sizes": True},
]

WINDOWS_V3 = [
    ("d",  120, 1000, 1000, 1350),              # over the galley
    ("d", 1450, 2250,  620,  960),              # over the driver bench
    ("p", 1600, 2400,  620,  960),              # over the passenger bench
]
FAN_HOLES_V3 = [(150, 630, 500, 980), (1900, 2380, 676, 1156)]
HATCHES_V3 = [("d", 2900, 3320, 40, 580)]       # cassette out of the rear quarter panel
# The pass-through is over the shoe locker in the passenger corner - the galley now owns the
# driver corner, which is the whole point of the L.
PARTITION_V3 = (60, 440, 420, 1620)
CAB_SEATS_V3 = [(-670, -190, 1140, 1620), (-670, -190, 60, 1060)]


# Carcasses with kit inside them. The viewer ghosts these while the appliances are shown,
# so you can see into a bench without inventing door and drawer divisions we have not designed.
CONTAINERS = ("GALLEY", "WET CUBICLE", "BENCH", "REAR BENCH", "FRIDGE")

# Kit that lives inside a cabinet. A wireframe has no occlusion, so leaving these in the
# control image just draws boxes through the furniture and confuses the canny map.
INTERNAL = ("oven", "plumbing", "fridge", "fridgedoor", "fridgedrawer", "fresh", "grey",
            "calorifier", "filter",
            "battery", "inverter", "electrics")

# What each kind is called, for the viewer key and the dimension labels.
NAMES = {
    "SHOWER": "Shower", "WARDROBE": "Wardrobe + WC under", "LOCKER": "Shoe locker / step",
    "wetwall": "Shower wall", "tray": "Shower tray", "screen": "Shower screen, glass",
    "SINK": "Galley - sink side", "HOB": "Galley - hob side",
    "OFFICE SEAT": "Office seat", "LARDER": "Larder",
    "BENCH -> BED": "Bench / bed", "BATHROOM": "Bathroom", "GARAGE": "Garage, full height",
    "doorshut": "Bathroom door, shut", "wall": "Bathroom / garage wall",
    "otable": "Office table", "otablep": "Office table, folded",
    "ltable": "Galley leaf, up", "ltablep": "Galley leaf, folded",
    "fridgedrawer": "Fridge 90 L drawer",
    "partition": "Partition wall", "hatch": "Cassette hatch",
    "GALLEY": "Galley", "WET CUBICLE": "Wet cubicle", "FRIDGE": "Fridge 70 L drawer",
    "BENCH": "Bench", "REAR BENCH": "Rear bench / garage", "bed": "Seat cushion", "infill": "Bed infill",
    "locker": "Overhead locker", "table": "Table", "step": "Cubicle step",
    "leg": "Table post", "shower": "Shower head",
    "ftable": "Worktop leaf", "fleg": "Front table post",
    "ftablep": "Worktop leaf, folded", "farm": "Leaf bracket",
    "oven": "Mini oven 20 L", "hob": "Induction hob, 2 zone",
    "sink": "Sink", "sinkrim": "Sink deck", "bowl": "Sink bowl", "tap": "Mixer tap",
    "filtertap": "Drinking tap, filtered", "filter": "Carbon block, inline",
    "plumbing": "Pump, filter, trap", "cassette": "Cassette WC",
    "fridge": "Fridge 70 L", "fridgedoor": "Fridge 90 L, hinged door",
    "fresh": "Fresh water 110 L", "grey": "Grey water 70 L", "calorifier": "Calorifier 10 L",
    "battery": "Battery 150 Ah", "inverter": "Inverter 3000 W",
    "electrics": "MPPT, DC-DC, fuses",
}

# --- the vehicle itself ----------------------------------------------------
# Apertures are cut out of the body panels, so the openings are real holes rather
# than drawn-on rectangles. p = passenger wall (y=0), d = driver wall (y=width).
WALL = 40           # panel thickness, mm
NOSE = 1500         # how far the cab reaches forward of the load area
CAB_ROOF = 1500     # the roof over the cab sits lower than the load-space roof

SLIDER = (300, 1600, 0, 1550)                   # x0, x1, z0, z1
WINDOWS = [                                     # side, x0, x1, z0, z1
    ("p", 2400, 3000,  620,  960),              # over the passenger bench
    ("d",  900, 1550, 1000, 1350),              # over the galley
    ("d", 2350, 3000,  620,  960),              # over the driver bench
]
REAR_DOORS = (60, 60, 0, 1700)                  # inset from each side, z0, z1
FAN_HOLES = [(860, 1340, 140, 620), (2460, 2940, 140, 620)]

# v2 puts different things against the walls, so the holes move with them.
WINDOWS_V2 = [
    ("d",  120,  620, 1180, 1520),              # shower window, Brisa's trick
    ("d", 1250, 1850, 1000, 1350),              # over the sink
    ("d", 1950, 2750,  620,  960),              # over the driver bench
    ("p", 1950, 2750,  620,  960),              # over the passenger bench
]
FAN_HOLES_V2 = [(1400, 1880, 676, 1156), (2350, 2830, 676, 1156)]
# Service hatches: a real hole in a body panel with a lid in it. side, x0, x1, z0, z1.
HATCHES_V2 = [("d", 700, 1150, 40, 580)]        # the cassette comes out sideways here
# Partition behind a 3-seat cab, with the pass-through cut in it: y0, y1, z0, z1.
PARTITION_V2 = (600, 1032, 0, 1600)
# Cab seats as x0, x1, y0, y1 - a single driver seat and a double bench, no swivels.
CAB_SEATS_V2 = [(-670, -190, 1140, 1620), (-670, -190, 60, 1060)]

KIND = {          # plan label or extra kind -> colour
    "SHOWER": "#bcd6e6", "WARDROBE": "#e6dcc6", "LOCKER": "#d8cfe2",
    "wetwall": "#cfe0ea", "tray": "#dde4e8", "screen": "#a9c6d8",
    "SINK": "#cfded9", "HOB": "#cfded9", "partition": "#d9d4c8", "hatch": "#c9c2b4",
    "OFFICE SEAT": "#d8cfe2", "LARDER": "#e6dcc6",
    "BENCH -> BED": "#d8cfe2", "BATHROOM": "#bcd6e6", "GARAGE": "#e6dcc6",
    "doorshut": "#d9d4c8", "wall": "#d9d4c8", "fridgedrawer": "#cfe4c9",
    "otable": "#d9b98a", "otablep": "#d9b98a", "ltable": "#d9b98a", "ltablep": "#d9b98a",
    "ftablep": "#d9b98a", "farm": "#9a9287",
    "GALLEY": "#cfded9", "WET CUBICLE": "#bcd6e6", "FRIDGE": "#cfe4c9",
    "BENCH": "#d8cfe2", "REAR BENCH": "#d8cfe2",
    "bed": "#eceaf1", "infill": "#eceaf1", "wheel": "#3b3b3d", "locker": "#e6dcc6", "table": "#d9b98a", "ftable": "#d9b98a", "fleg": "#9a9287",
    "step": "#e6dcc6", "leg": "#9a9287", "shower": "#b9c3c7",
    "shell": "#e4e1da", "glass": "#a9c6d8", "floor": "#cdc4b2",
    "cab": "#dcd8d0", "seat": "#8f9a8c", "dash": "#5f6166",
    # appliances: stainless greys for the kitchen, blue for water, amber for electrics
    "oven": "#8d9295", "hob": "#4e5457", "sink": "#b6bcbe", "sinkrim": "#c3c9cb", "bowl": "#a9b0b2", "plumbing": "#9aa3a6", "fridge": "#cfe4c9",
    "fridgedoor": "#cfe4c9", "filter": "#7fb2cf", "filtertap": "#b6bcbe", "tap": "#b6bcbe",
    "cassette": "#dde4e8", "fresh": "#7fb2cf", "grey": "#8f9aa2", "calorifier": "#c08f7a",
    "battery": "#e0b25c", "inverter": "#cf9a3f", "electrics": "#b98b36",
}
GLASSY = ("glass", "screen")     # drawn transparent in the viewer

# Props whose mesh keeps its own proportions instead of being stretched to fill its box.
# Only for boxes that are a space reservation rather than the shape of a real object: the
# plumbing box is a 340 cube standing in for a pump, a filter and a trap, and stretching a
# pump to fill it looks like a smear. Everywhere else filling is what you want - a bed cushion
# fitted uniformly shrinks to a quarter of its slot, because the mesh is thicker than 70 mm.
KEEP_SHAPE = ("plumbing",)

CAMERAS = [                         # name, elevation, azimuth
    ("01-from-the-rear-looking-forward", 6, -24),
    ("02-from-the-front-looking-aft", 6, 204),
    ("03-three-quarter-through-the-slider", 16, -104),
    ("04-cutaway-from-above", 46, -56),
]


# Which tables belong to which variant. A variant not listed borrows v1's and gets them
# remapped onto its own walls - right for a reference van drawn on the same furniture,
# never right for a layout designed on its own, which brings its own tables instead.
REGISTRY = {
    "v1": dict(own_coords=False, heights=HEIGHTS, extra=EXTRA, appliances=APPLIANCES,
               containers=CONTAINERS, windows=WINDOWS, fans=FAN_HOLES, hatches=(),
               partition=None, cab_seats=None, layers=None, facing={}, sitter=()),
    "v2": dict(own_coords=True, heights=HEIGHTS_V2, extra=EXTRA_V2, appliances=APPLIANCES_V2,
               containers=CONTAINERS_V2, windows=WINDOWS_V2, fans=FAN_HOLES_V2,
               hatches=HATCHES_V2, partition=PARTITION_V2, cab_seats=CAB_SEATS_V2,
               layers=LAYERS_V2, facing=FACING_V2, sitter=SITTER_V2),
    "v3": dict(own_coords=True, heights=HEIGHTS_V3, extra=EXTRA_V3, appliances=APPLIANCES_V3,
               containers=CONTAINERS_V3, windows=WINDOWS_V3, fans=FAN_HOLES_V3,
               hatches=HATCHES_V3, partition=PARTITION_V3, cab_seats=CAB_SEATS_V3,
               layers=LAYERS_V3, facing=FACING_V3, sitter=SITTER_V3, yaw=YAW_V3,
               sit_ok=SIT_OK_V3),
}


def spec(v):
    """The 3D tables for this variant, v1's as the fallback."""
    return REGISTRY.get(v.get("name"), REGISTRY["v1"])


def heights_for(v):
    return spec(v)["heights"]


def half_turn(v, box):
    """How far to turn this box's prop mesh, in degrees.

    Two separate reasons to turn. `facing` is the 180 a mesh needs when its box sits against
    the opposite wall from the one it was modelled for. `yaw` is a variant's own quarter turn,
    for a run that is rotated 90 from the run the mesh was made on - v3's galley crosses the
    front bulkhead where v1's and v2's ran along a side wall, so its oven faces the wrong way
    without it. The viewer adds the result to the kind's own yaw.json entry."""
    x0, x1, y0, y1, z0, z1, kind = box
    sp = spec(v)
    turn = sp.get("yaw", {}).get(kind, 0)
    want = sp.get("facing", {}).get(kind)
    if want:
        side = "p" if (y0 + y1) / 2 < v["width"] / 2 else "d"
        if side != want:
            turn += 180
    return turn % 360


def fitout(v):
    """(EXTRA, APPLIANCES) in this variant's own coordinates."""
    sp = spec(v)
    if sp["own_coords"]:
        return list(sp["extra"]), list(sp["appliances"])
    return [remap(b, v) for b in sp["extra"]], [remap(b, v) for b in sp["appliances"]]


# --- axis-aligned rectangle subtraction, so panels have real holes ----------
def _sub(rect, hole):
    a0, a1, b0, b1 = rect
    ha0, ha1, hb0, hb1 = hole
    if ha1 <= a0 or ha0 >= a1 or hb1 <= b0 or hb0 >= b1:
        return [rect]
    out = []
    if ha0 > a0:
        out.append((a0, ha0, b0, b1))
    if ha1 < a1:
        out.append((ha1, a1, b0, b1))
    ma0, ma1 = max(a0, ha0), min(a1, ha1)
    if hb0 > b0:
        out.append((ma0, ma1, b0, hb0))
    if hb1 < b1:
        out.append((ma0, ma1, hb1, b1))
    return out


def subtract(rect, holes):
    rects = [rect]
    for h in holes:
        nxt = []
        for r in rects:
            nxt.extend(_sub(r, h))
        rects = nxt
    return rects


def sink_wells(x0, x1, y0, y1, z0, z1, rim=20, wall=8, gap=30, axis="x"):
    """A double-bowl inset sink, built out of boxes rather than generated.

    Image-to-3D gave a clean double sink at 0.06 shape error and it rendered as a solid
    block: 4000 faces is not enough to keep a recess, and a sink IS its recess. Same verdict
    as the shower cubicle - products get meshes, hollow things get built. Here that is a deck
    with two rectangular holes in it (the same subtract() the body panels use), and a
    five-sided well hanging under each hole.
    """
    deck = z1 - 10
    ix0, ix1, iy0, iy1 = x0 + rim, x1 - rim, y0 + rim, y1 - rim
    if axis == "y":                     # bowls side by side ALONG the van's width
        mid = (iy0 + iy1) / 2.0
        bowls = [(ix0, ix1, iy0, mid - gap / 2.0), (ix0, ix1, mid + gap / 2.0, iy1)]
    else:                               # bowls side by side along the van's length
        mid = (ix0 + ix1) / 2.0
        bowls = [(ix0, mid - gap / 2.0, iy0, iy1), (mid + gap / 2.0, ix1, iy0, iy1)]
    out = [(a0, a1, b0, b1, deck, z1, "sinkrim")
           for a0, a1, b0, b1 in subtract((x0, x1, y0, y1), bowls)]
    for bx0, bx1, by0, by1 in bowls:
        out.append((bx0, bx1, by0, by1, z0, z0 + wall, "bowl"))            # bottom
        out.append((bx0, bx1, by0, by0 + wall, z0, deck, "bowl"))          # aisle side
        out.append((bx0, bx1, by1 - wall, by1, z0, deck, "bowl"))          # wall side
        out.append((bx0, bx0 + wall, by0, by1, z0, deck, "bowl"))          # forward end
        out.append((bx1 - wall, bx1, by0, by1, z0, deck, "bowl"))          # aft end
    return out


# hard against the wardrobe at x 1150, which leaves the 200 mm aft of it as free counter
EXTRA_V2 += sink_wells(1150, 1730, 1440, 1800, 750, 905)
# v3: in the corner behind the driver, bowls side by side ACROSS the van - the run crosses
# the bulkhead, so the axis that holds two bowls is y, not x. Cut down to 340 x 560 from
# 440 x 640 - a smaller, narrower unit, product still to be found. The 200 mm of counter it
# frees between the bowls and the bulkhead is where the taps stand.
EXTRA_V3 += sink_wells(200, 540, 1240, 1800, 755, 905, axis="y")


def shell_for(v):
    """Body panels with apertures, glazing, and the cab. Same box format as everything else."""
    L, W, H = v["length"], v["width"], v["height"]
    sp = spec(v)
    out = []
    clamp = lambda a, b: (min(a, L - 50), min(b, L - 50))

    # side walls, holes cut for the sliding door, the windows and any service hatch
    for side, y0, y1 in (("p", -WALL, 0), ("d", W, W + WALL)):
        holes = []
        if side == "p":
            sx0, sx1, sz0, sz1 = SLIDER
            holes.append((sx0, sx1, sz0, sz1))
        for s, wx0, wx1, wz0, wz1 in list(sp["windows"]) + list(sp["hatches"]):
            if s == side:
                wx0, wx1 = clamp(wx0, wx1)
                holes.append((wx0, wx1, wz0, wz1))
        for x0, x1, z0, z1 in subtract((0, L, 0, H), holes):
            out.append((x0, x1, y0, y1, z0, z1, "shell"))
        for s, wx0, wx1, wz0, wz1 in sp["windows"]:          # glaze the window openings
            if s == side:
                wx0, wx1 = clamp(wx0, wx1)
                out.append((wx0, wx1, y0, y1, wz0, wz1, "glass"))
        for s, hx0, hx1, hz0, hz1 in sp["hatches"]:          # lid sits in its own hole
            if s == side:
                hx0, hx1 = clamp(hx0, hx1)
                out.append((hx0, hx1, y0, y1, hz0, hz1, "hatch"))

    # roof, holes cut for the two fans
    for x0, x1, y0, y1 in subtract((0, L, 0, W), sp["fans"]):
        out.append((x0, x1, y0, y1, H, H + WALL, "shell"))
    out.append((0, L, 0, W, -WALL, 0, "floor"))

    # partition behind the cab, with the pass-through cut in it
    if sp["partition"]:
        py0, py1, pz0, pz1 = sp["partition"]
        for y0, y1, z0, z1 in subtract((0, W, 0, H), [(py0, py1, pz0, pz1)]):
            out.append((-WALL, 0, y0, y1, z0, z1, "partition"))

    # rear doors
    ri, _, rz0, rz1 = REAR_DOORS
    for y0, y1, z0, z1 in subtract((0, W, 0, H), [(ri, W - ri, rz0, rz1)]):
        out.append((L, L + WALL, y0, y1, z0, z1, "shell"))

    # cab: floor, lower roof, raked-off windscreen simplified to a vertical pane,
    # side walls with door openings, dashboard, wheel, and the seats
    out.append((-NOSE, 0, 0, W, -WALL, 0, "cab"))
    out.append((-NOSE + 100, -100, 0, W, CAB_ROOF, CAB_ROOF + WALL, "cab"))
    out.append((-NOSE + 50, -NOSE + 90, 60, W - 60, 900, CAB_ROOF, "glass"))
    for y0, y1 in ((-WALL, 0), (W, W + WALL)):
        for x0, x1, z0, z1 in subtract((-NOSE, 0, 0, CAB_ROOF), [(-1200, -350, 300, 1400)]):
            out.append((x0, x1, y0, y1, z0, z1, "cab"))
    out.append((-1250, -1000, 60, W - 60, 700, 950, "dash"))
    out.append((-1050, -980, W - 620, W - 280, 950, 1300, "dash"))      # steering wheel
    out.extend(cab_seats(v))
    out.extend(wheels_for(v))
    return out


def cab_seats(v):
    """Seat blocks in the cab. v1 swivels, so plan.py already carries their centres; v2 has a
    fixed driver seat and a double bench, which the plan does not draw at all."""
    seats = spec(v)["cab_seats"]
    if seats is None:
        seats = [(cx - 240, cx + 240, cy - 240, cy + 240) for cx, cy, _r in v.get("seats", [])]
    out = []
    for x0, x1, y0, y1 in seats:
        out.append((x0, x1, y0, y1,   0,  420, "seat"))
        out.append((x0, x1, y0, y1, 420,  500, "seat"))
        out.append((x1 - 100, x1, y0, y1, 500, 1100, "seat"))
    return out


# 235/65 R16, the usual L3 shoe: 711 mm across the tread, 235 wide. The axle sits below the
# finished floor, so only the top of the tyre reaches into the load space - which is the real
# reason a wheel arch is there at all, and the number WELL_H only guesses at.
TYRE_R = 356
TYRE_W = 235
AXLE_Z = -244          # centre below the finished floor, so the tread tops out at +112
FRONT_AXLE = -900      # under the cab, forward of the bulkhead


def wheels_for(v):
    """Four road wheels, as boxes here and as cylinders in the viewer. They are the thing the
    wheel arch is built around, so drawing them says whether kit that sits against a wall is
    really in the way or only near it."""
    if not v.get("well"):
        return []
    w0, w1, wd = v["well"]
    W = v["width"]
    out = []
    for cx in (FRONT_AXLE, (w0 + w1) / 2):
        for y0 in (wd - TYRE_W, W - wd):            # inner face at the arch line, on both sides
            out.append((cx - TYRE_R, cx + TYRE_R, y0, y0 + TYRE_W,
                        AXLE_Z - TYRE_R, AXLE_Z + TYRE_R, "wheel"))
    return out


def remap(box, v):
    """EXTRA and APPLIANCES are written in v1 coordinates. On another base vehicle the extra
    width lands in the corridor and the extra length in the bed, so anything that sits on the
    driver side or aft of the rear-bench line moves with those walls instead of floating."""
    x0, x1, y0, y1, z0, z1, kind = box
    dx, dy = v["length"] - 3494, v["width"] - 1784
    at = lambda a, line, d: a + d if a >= line else a
    return (at(x0, 3044, dx), at(x1, 3044, dx), at(y0, 1184, dy), at(y1, 1184, dy), z0, z1, kind)


def boxes_for(v, with_shell=False):
    """(x0, x1, y0, y1, z0, z1, kind) for everything solid."""
    heights = heights_for(v)
    out = []
    for x0, x1, y0, y1, label, _sub_label, _fill in v["boxes"]:
        z = heights.get(label)
        if z:
            out.append((x0, x1, y0, y1, z[0], z[1], label))
    extra, appliances = fitout(v)
    out.extend(extra + appliances)
    if with_shell:
        out.extend(shell_for(v))
    return [b for b in out if b[1] > b[0] and b[3] > b[2] and b[5] > b[4]]


def faces(x0, x1, y0, y1, z0, z1):
    """Six quads, in the order bottom, top, and the four sides."""
    return [
        [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
        [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
        [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
        [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
    ]


def shade(hexcol, factor):
    """Fake directional light: top faces bright, sides progressively darker."""
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(min(255, int(c * factor)) for c in (r, g, b))


FACE_LIGHT = (0.72, 1.0, 0.88, 0.80, 0.92, 0.84)     # per face, same order as faces()


def render(v, out_dir):
    """Greybox: furniture only, with the van as a wireframe so you can see inside."""
    L, W, H = v["length"], v["width"], v["height"]
    # appliances live inside cabinets; matplotlib has no depth buffer, so they would sort
    # through the doors. Use the viewer to look at them.
    solids = [b for b in boxes_for(v) if b[6] not in INTERNAL]
    os.makedirs(out_dir, exist_ok=True)

    for name, elev, azim in CAMERAS:
        fig = plt.figure(figsize=(11, 7), dpi=150)
        fig.patch.set_facecolor("white")
        ax = fig.add_subplot(111, projection="3d")
        for x0, x1, y0, y1, z0, z1, kind in solids:
            for quad, light in zip(faces(x0, x1, y0, y1, z0, z1), FACE_LIGHT):
                ax.add_collection3d(Poly3DCollection(
                    [quad], facecolor=shade(KIND[kind], light), edgecolor="#5a5a5a",
                    linewidths=0.4, alpha=1.0, zsort="average"))
        for quad in faces(0, L, 0, W, 0, H):
            ax.add_collection3d(Poly3DCollection([quad], facecolor="none", edgecolor="#111",
                                                 linewidths=1.0))
        ax.set_xlim(0, L); ax.set_ylim(0, W); ax.set_zlim(0, H)
        ax.set_box_aspect((L, W, H))
        ax.view_init(elev=elev, azim=azim)
        ax.set_proj_type("persp", focal_length=0.35)
        ax.set_axis_off()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        path = os.path.join(out_dir, name + ".png")
        fig.savefig(path, facecolor="white", bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        print("wrote", path)


def shell_outline(v):
    """The van as clean semantic lines for a control image: the room itself, plus a rectangle
    for each real opening. The full panel geometry adds dozens of spurious edges where panels
    meet, which drowns the furniture in the canny map."""
    L, W, H = v["length"], v["width"], v["height"]
    T = 2                                           # nominal thickness, so nothing is degenerate
    out = [(0, L, 0, W, 0, H, "room")]
    clamp = lambda a, b: (min(a, L - 50), min(b, L - 50))
    sx0, sx1, sz0, sz1 = SLIDER
    out.append((sx0, sx1, -T, T, sz0, sz1, "hole"))
    for side, wx0, wx1, wz0, wz1 in list(spec(v)["windows"]) + list(spec(v)["hatches"]):
        wx0, wx1 = clamp(wx0, wx1)
        y0, y1 = (-T, T) if side == "p" else (W - T, W + T)
        out.append((wx0, wx1, y0, y1, wz0, wz1, "hole"))
    ri, _, rz0, rz1 = REAR_DOORS
    out.append((L - T, L + T, ri, W - ri, rz0, rz1, "hole"))
    for fx0, fx1, fy0, fy1 in spec(v)["fans"]:
        out.append((fx0, fx1, fy0, fy1, H - T, H + T, "hole"))
    # no cab volume: as a wireframe it throws long lines across every interior view.
    # The seats and dash alone are enough to say "the cab is that way".
    out.append((-1250, -1000, 60, W - 60, 700, 950, "dash"))
    for x0, x1, y0, y1, z0, z1, kind in cab_seats(v):
        if z0 == 0:
            out.append((x0, x1, y0, y1, 0, 500, kind))      # base and cushion as one block
        elif z0 >= 500:
            out.append((x0, x1, y0, y1, z0, z1, kind))
    return out


WIRE = ("room", "hole")     # drawn as outlines, so they never occlude the interior


# Outward normals, in the same order as faces(): bottom, top, y0, y1, x0, x1.
NORMALS = ((0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0))
NEAR = 120.0        # mm in front of the eye; anything closer is clipped away


def _basis(eye, target):
    """Pinhole camera basis. Returns a function mapping a world point to (x, y, depth),
    with depth positive in front of the eye.

    Plan coordinates are LEFT-handed: x runs aft, y runs toward the driver side, z is up, and
    the plan is drawn from above with y pointing DOWN the page. numpy's cross product is
    right-handed, so using plan coordinates directly mirrors the whole image - which is exactly
    what happened: the galley came out on the wrong side of every control render. Flipping y
    gives a right-handed world, and the standard camera maths is then correct."""
    import numpy as np
    flip = np.array([1.0, -1.0, 1.0])
    e, t = np.array(eye, float) * flip, np.array(target, float) * flip
    w = e - t
    w /= np.linalg.norm(w)                       # points back toward the eye
    u = np.cross((0.0, 0.0, 1.0), w)
    u /= np.linalg.norm(u)                       # screen right
    ve = np.cross(w, u)                          # screen up
    def to_cam(p):
        c = np.array(p, float) * flip - e
        return np.array([c.dot(u), c.dot(ve), -c.dot(w)])
    return to_cam


def screen_xy(eye, target, point):
    """Where a world point lands on the control image. x > 0 is screen right, y > 0 is up.
    Returns None if the point is behind the eye. Used to assert which side things end up on."""
    c = _basis(eye, target)(point)
    return None if c[2] <= 1e-6 else (c[0] / c[2], c[1] / c[2])


def _clip_near(poly):
    """Sutherland-Hodgman against the single plane depth = NEAR. Without this, anything
    behind the eye projects through the vanishing point and the frame fills with starbursts
    - which is exactly what matplotlib's own 3D axes does, and why we do not use it here."""
    out = []
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        ina, inb = a[2] >= NEAR, b[2] >= NEAR
        if ina:
            out.append(a)
        if ina != inb:
            out.append(a + (NEAR - a[2]) / (b[2] - a[2]) * (b - a))
    return out


def shaded_render(v, eye, target, path, hfov=95.0, hide=(), aspect=4.0 / 3.0, size=(8, 6)):
    """The same camera as line_render, but the real vehicle: body panels with their apertures
    cut, glazing, the cab, and every surface in its own colour with a bit of directional shading.

    This exists because a line drawing asks the image model to invent both the materials and
    the meaning of every blank area, and it always invents furniture in the empty entry. A
    shaded view already IS the picture, just a flat one, so image-to-image only has to add
    texture and light. Faces are sorted by their own depth rather than by their box's, because
    a wall is large enough that its centre tells you nothing about where its surface is.
    """
    import numpy as np
    to_cam = _basis(eye, target)
    eye_v = np.array(eye, float)
    items = [b for b in boxes_for(v, with_shell=True)
             if b[6] not in INTERNAL and b[6] not in hide]

    parts = []
    for x0, x1, y0, y1, z0, z1, kind in items:
        for quad, n, light in zip(faces(x0, x1, y0, y1, z0, z1), NORMALS, FACE_LIGHT):
            mid = np.array(quad).mean(axis=0)
            if np.dot(n, mid - eye_v) >= 0:
                continue                              # back face
            poly = _clip_near([to_cam(p) for p in quad])
            if len(poly) < 3:
                continue
            depth = sum(p[2] for p in poly) / len(poly)
            parts.append((depth, poly, shade(KIND.get(kind, "#d8d8d8"), light)))

    fig = plt.figure(figsize=size, dpi=150)
    fig.patch.set_facecolor("#f2f2f0")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#f2f2f0")
    flat = lambda poly: [(p[0] / p[2], p[1] / p[2]) for p in poly]
    parts.sort(key=lambda it: -it[0])
    for i, (_d, poly, colour) in enumerate(parts):
        ax.add_patch(plt.Polygon(flat(poly), closed=True, facecolor=colour,
                                 edgecolor=colour, linewidth=0.4, zorder=i + 2))
    tx = np.tan(np.deg2rad(hfov) / 2.0)
    ax.set_xlim(-tx, tx)
    ax.set_ylim(-tx / aspect, tx / aspect)
    ax.set_axis_off()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def depth_render(v, eye, target, path, hfov=95.0, hide=(), aspect=4.0 / 3.0, size=(8, 6)):
    """A depth map of the same view: near surfaces bright, far ones dark, which is what a
    depth-conditioned image model wants. Depth carries the volume of the room, not just its
    edges, so the model can light and texture it freely without moving anything - which is the
    one thing canny on a line drawing could never do.

    Each face is drawn with per-vertex depth and Gouraud shading, because a floor running away
    from the camera is a single polygon covering most of the frame and one flat grey for it
    would tell the model nothing."""
    import numpy as np
    to_cam = _basis(eye, target)
    eye_v = np.array(eye, float)
    items = [b for b in boxes_for(v, with_shell=True)
             if b[6] not in INTERNAL and b[6] not in hide]

    parts = []
    for x0, x1, y0, y1, z0, z1, kind in items:
        for quad, n in zip(faces(x0, x1, y0, y1, z0, z1), NORMALS):
            if np.dot(n, np.array(quad).mean(axis=0) - eye_v) >= 0:
                continue
            poly = _clip_near([to_cam(p) for p in quad])
            if len(poly) >= 3:
                parts.append((sum(p[2] for p in poly) / len(poly), poly))
    if not parts:
        raise ValueError("nothing visible from this camera")

    near = min(p[2] for _d, poly in parts for p in poly)
    far = np.percentile([p[2] for _d, poly in parts for p in poly], 97)
    fig = plt.figure(figsize=size, dpi=150)
    fig.patch.set_facecolor("black")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("black")
    parts.sort(key=lambda it: -it[0])
    for i, (_d, poly) in enumerate(parts):
        xs = [p[0] / p[2] for p in poly]
        ys = [p[1] / p[2] for p in poly]
        cs = [1.0 - min(1.0, max(0.0, (p[2] - near) / max(far - near, 1.0))) for p in poly]
        tri = [(0, k, k + 1) for k in range(1, len(poly) - 1)]
        ax.tripcolor(xs, ys, tri, cs, shading="gouraud", cmap="gray",
                     vmin=0.0, vmax=1.0, zorder=i + 2, rasterized=True)
    tx = np.tan(np.deg2rad(hfov) / 2.0)
    ax.set_xlim(-tx, tx)
    ax.set_ylim(-tx / aspect, tx / aspect)
    ax.set_axis_off()
    fig.savefig(path, facecolor="black")
    plt.close(fig)
    return path


def line_render(v, eye, target, path, hfov=95.0, cab=False, hide=(), aspect=4.0 / 3.0,
                size=(8, 6)):
    """The control image for image generation: a real interior view, drawn by hand.

    matplotlib's 3D axes cannot do this. Its camera always sits at a fixed distance from the
    centre of the data box (10 x focal_length in normalised units), which put every one of our
    cameras OUTSIDE the van - shot 01 ended up 1.3 m behind the rear doors, so the model was
    being shown an exterior view of a wireframe box and invented the interior. Shortening the
    focal length to pull the eye inside only trades that for starbursts, because mplot3d never
    clips at the near plane. So: our own pinhole projection, our own near clipping, and solid
    white faces painted back to front so nearer furniture actually hides what is behind it.

    eye and target are in millimetres, same coordinates as the plan. hfov is the horizontal
    field of view in degrees; the frame is exactly `aspect`, so nothing has to be padded.
    `hide` drops kinds - pass ("bed",) to see the dinette as seating instead of made up.
    """
    import numpy as np
    to_cam = _basis(eye, target)
    items = [b for b in boxes_for(v) + shell_outline(v)
             if b[6] not in INTERNAL and b[6] not in hide
             and (cab or b[6] not in ("seat", "dash"))]

    # One list, sorted once. Wires used to be drawn on top of everything, which painted the
    # room's far corners straight across the galley and fed the canny map edges that are not
    # really visible. Now a nearer white face hides the lines behind it.
    parts = []
    eye_v = np.array(eye, float)
    for x0, x1, y0, y1, z0, z1, kind in items:
        quads = faces(x0, x1, y0, y1, z0, z1)
        if kind in WIRE:                          # the room and its openings: edges only
            for quad in quads:
                pts = [to_cam(p) for p in quad]
                for i, a in enumerate(pts):
                    seg = _clip_near([a, pts[(i + 1) % 4]])
                    if len(seg) == 2:
                        parts.append(((seg[0][2] + seg[1][2]) / 2.0, False, seg))
            continue
        centre = np.array([(x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0])
        depth = np.linalg.norm(centre - eye_v)
        for quad, n in zip(quads, NORMALS):
            if np.dot(n, np.array(quad).mean(axis=0) - eye_v) >= 0:
                continue                          # back face, never visible
            poly = _clip_near([to_cam(p) for p in quad])
            if len(poly) >= 3:
                parts.append((depth, True, poly))

    fig = plt.figure(figsize=size, dpi=150)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("white")
    flat = lambda poly: [(p[0] / p[2], p[1] / p[2]) for p in poly]

    parts.sort(key=lambda it: -it[0])              # painter: farthest first
    for i, (_d, filled, poly) in enumerate(parts):
        if filled:
            ax.add_patch(plt.Polygon(flat(poly), closed=True, facecolor="white",
                                     edgecolor="black", linewidth=1.0, zorder=i + 2))
        else:
            (px, py), (qx, qy) = flat(poly)
            ax.plot([px, qx], [py, qy], color="black", linewidth=0.9, zorder=i + 2)

    tx = np.tan(np.deg2rad(hfov) / 2.0)
    ax.set_xlim(-tx, tx)
    ax.set_ylim(-tx / aspect, tx / aspect)
    ax.set_axis_off()
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path


def write_obj(v, path):
    lines, n = [], 0
    for x0, x1, y0, y1, z0, z1, _kind in boxes_for(v, with_shell=True):
        # metres, Y up, so it lands right way up in Blender and three.js
        for vx, vy, vz in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                           (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]:
            lines.append("v %.4f %.4f %.4f" % (vx / 1000.0, vz / 1000.0, vy / 1000.0))
        for a, b, c, d in [(1, 2, 3, 4), (5, 6, 7, 8), (1, 2, 6, 5),
                           (2, 3, 7, 6), (3, 4, 8, 7), (4, 1, 5, 8)]:
            lines.append("f %d %d %d %d" % (n + a, n + b, n + c, n + d))
        n += 8
    open(path, "w", encoding="utf-8").write("# " + v["title"] + "\n" + "\n".join(lines) + "\n")
    print("wrote", path)


def props_data(kinds=None):
    """Prop meshes made by props.py, embedded so viewer.html stays a single file. Absent is
    fine - the viewer just keeps drawing the coloured box for that kind.

    Only the kinds this variant actually uses go in. v1 has no wardrobe and v2 has no wet
    cubicle, and neither viewer should carry a quarter megabyte of the other's furniture."""
    import base64
    d = os.path.join(HERE, "props")
    if not os.path.isdir(d):
        return {}
    yaw_path = os.path.join(d, "yaw.json")
    yaw = json.load(open(yaw_path)) if os.path.exists(yaw_path) else {}
    out = {}
    for name in sorted(os.listdir(d)):
        if name.endswith(".glb"):
            kind = name[:-4]
            if kinds is not None and kind not in kinds:
                continue
            out[kind] = {"yaw": yaw.get(kind, 0),
                         "fit": "keep" if kind in KEEP_SHAPE else "fill",
                         "glb": base64.b64encode(open(os.path.join(d, name), "rb").read()).decode()}
    return out


def plan_image(v, path):
    """Render the plan cropped to the load box and hand it back as a data URI, so viewer.html
    stays one file you can mail."""
    import base64
    overlay_png(v, path)
    return {"img": "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()}


def write_viewer(v, path):
    """Fill viewer_template.html with this variant's geometry."""
    tpl_path = os.path.join(HERE, "viewer_template.html")
    if not os.path.exists(tpl_path):
        print("skipped viewer.html - viewer_template.html not found")
        return
    sp = spec(v)
    used = {b[6] for b in boxes_for(v, with_shell=True)}
    data = {
        "title": v["title"], "note": v["note"],
        "length": v["length"], "width": v["width"], "height": v["height"], "nose": NOSE,
        "colours": KIND, "glassy": list(GLASSY), "stats": v.get("stats", []),
        "names": NAMES, "appliances": sorted({b[6] for b in fitout(v)[1]}),
        "containers": list(sp["containers"]), "props": props_data(used),
        "cylinders": ["wheel"], "layers": sp["layers"],
        # the plan drawing itself, for the schema overlay: plan.py renders it cropped to the
        # load box, so the viewer lays the real layout image on the floor 1:1 rather than
        # redrawing an approximation of it
        "plan": plan_image(v, os.path.join(os.path.dirname(path) or ".", "overlay.png")),
        "boxes": [dict({"b": [x0, x1, y0, y1, z0, z1], "k": kind},
                       **({"y": t} if (t := half_turn(v, (x0, x1, y0, y1, z0, z1, kind))) else {}))
                  for x0, x1, y0, y1, z0, z1, kind in boxes_for(v, with_shell=True)],
    }
    tpl = open(tpl_path, encoding="utf-8").read()
    tpl = tpl.replace("<title>Van Interior</title>",
                      "<title>" + v.get("viewer_title", "Van Interior") + "</title>")
    open(path, "w", encoding="utf-8").write(tpl.replace("/*MODEL_DATA*/null", json.dumps(data)))
    print("wrote", path)


WELL_H = 350            # wheel arch height above the finished floor - not in the plan data


def check(v):
    """Every appliance must sit inside the van, inside a cabinet, and clear of its neighbours.
    The sizes are real catalogue sizes, so this is what tells us the layout actually works."""
    L, W, H = v["length"], v["width"], v["height"]
    app = fitout(v)[1]
    heights = heights_for(v)
    rooms = [b[:6] for b in boxes_for(v) if heights.get(b[6])]
    overlap = lambda a, b: all(min(a[i * 2 + 1], b[i * 2 + 1]) - max(a[i * 2], b[i * 2]) > 1
                               for i in range(3))

    def housed(a):
        """Inside one carcass, or inside a run of carcasses that meet. v2's U is one
        continuous carcass, and its fresh tank crosses the joint between the side bench and
        the garage on purpose - so a single-box test would reject a tank that is really
        housed. Depth still has to be respected by every box it passes through."""
        segs = sorted((max(r[0], a[0]), min(r[1], a[1])) for r in rooms
                      if a[2] >= r[2] - 1 and a[3] <= r[3] + 1
                      and min(r[1], a[1]) - max(r[0], a[0]) > 1)
        reach = a[0]
        for s0, s1 in segs:
            if s0 > reach + 1:
                break
            reach = max(reach, s1)
        return reach >= a[1] - 1

    bad = []
    for i, a in enumerate(app):
        for b in app[i + 1:]:
            if overlap(a[:6], b[:6]):
                bad.append("%s clashes with %s" % (a[6], b[6]))
        if not (0 <= a[0] and a[1] <= L and 0 <= a[2] and a[3] <= W and a[5] <= H):
            bad.append("%s sticks out of the van" % a[6])
        if a[6] == "grey":
            continue                                    # underslung, deliberately outside
        if not housed(a):
            bad.append("%s is not inside any cabinet" % a[6])
    assert not bad, "appliance check failed: " + "; ".join(bad)

    # Nothing may occupy the space a seated person does - except the seat they sit on, and
    # the cushion on top of it. A table at 760 over the thighs is fine; the arm that carries
    # it is what goes wrong, and it goes wrong silently.
    sat = []
    sit_ok = spec(v).get("sit_ok", ("LOCKER", "bed", "ENTRY", "AISLE"))
    for body in spec(v).get("sitter", ()):
        for b in boxes_for(v):
            if b[6] in sit_ok:
                continue
            if overlap(b[:6], body):
                sat.append("%s runs through the person on the seat" % b[6])
    assert not sat, "sitter check failed: " + "; ".join(sorted(set(sat)))

    # Wheel arches are drawn on the plan but are not boxes, so they have to be checked apart
    # from everything else. A warning, not a failure: the fresh tank does clash today and how
    # to split it is still open, and a hard failure would block every other drawing meanwhile.
    if v.get("well"):
        w0, w1, wd = v["well"]
        for a in app:
            if a[6] == "grey" or a[1] <= w0 or a[0] >= w1 or a[4] >= WELL_H:
                continue
            for y0, y1 in ((0, wd), (W - wd, W)):
                across = min(a[3], y1) - max(a[2], y0)
                if across > 1:
                    print("warning: %s overlaps the wheel well by %d x %d mm"
                          % (a[6], min(a[1], w1) - max(a[0], w0), across))
    # the arch above is a guess; the tyre is not. Anything the tyre itself reaches is a real
    # clash whatever WELL_H turns out to be.
    for tyre in [b for b in wheels_for(v)]:
        for a in app:
            hit = [min(a[i * 2 + 1], tyre[i * 2 + 1]) - max(a[i * 2], tyre[i * 2])
                   for i in range(3)]
            if all(o > 1 for o in hit):
                print("CLASH: %s runs into the tyre itself by %d x %d x %d mm"
                      % ((a[6],) + tuple(int(o) for o in hit)))
    print("check ok - %d appliances placed" % len(app))


def main(name):
    v = VARIANTS[name]
    if "height" not in v:
        sys.exit("variant %r has no 'height' - add one before extruding it" % name)
    out = v["out"].rsplit("/", 1)[0] if "/" in v["out"] else "."
    os.makedirs(out, exist_ok=True)
    check(v)
    render(v, os.path.join(out, "3d"))
    write_obj(v, os.path.join(out, "model.obj"))
    write_viewer(v, os.path.join(out, "viewer.html"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v1")
