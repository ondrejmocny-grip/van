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

from plan import VARIANTS

HERE = os.path.dirname(os.path.abspath(__file__))

# plan label -> (z0, z1). None means the plan box is a void (footwell, open floor).
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

# Carcasses with kit inside them. The viewer ghosts these while the appliances are shown,
# so you can see into a bench without inventing door and drawer divisions we have not designed.
CONTAINERS = ("GALLEY", "WET CUBICLE", "BENCH", "REAR BENCH", "FRIDGE")

# Kit that lives inside a cabinet. A wireframe has no occlusion, so leaving these in the
# control image just draws boxes through the furniture and confuses the canny map.
INTERNAL = ("oven", "plumbing", "fridge", "fresh", "grey", "calorifier",
            "battery", "inverter", "electrics")

# What each kind is called, for the viewer key and the dimension labels.
NAMES = {
    "GALLEY": "Galley", "WET CUBICLE": "Wet cubicle", "FRIDGE": "Fridge 70 L drawer",
    "BENCH": "Bench", "REAR BENCH": "Rear bench / garage", "bed": "Seat cushion", "infill": "Bed infill",
    "locker": "Overhead locker", "table": "Table", "step": "Cubicle step",
    "leg": "Table post", "shower": "Shower head",
    "ftable": "Front table", "fleg": "Front table post",
    "oven": "Mini oven 20 L", "hob": "Induction hob, 2 zone", "sink": "Sink",
    "plumbing": "Pump, filter, trap", "cassette": "Cassette WC",
    "fridge": "Fridge 70 L",
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

KIND = {          # plan label or extra kind -> colour
    "GALLEY": "#cfded9", "WET CUBICLE": "#bcd6e6", "FRIDGE": "#cfe4c9",
    "BENCH": "#d8cfe2", "REAR BENCH": "#d8cfe2",
    "bed": "#eceaf1", "infill": "#eceaf1", "wheel": "#3b3b3d", "locker": "#e6dcc6", "table": "#d9b98a", "ftable": "#d9b98a", "fleg": "#9a9287",
    "step": "#e6dcc6", "leg": "#9a9287", "shower": "#b9c3c7",
    "shell": "#e4e1da", "glass": "#a9c6d8", "floor": "#cdc4b2",
    "cab": "#dcd8d0", "seat": "#8f9a8c", "dash": "#5f6166",
    # appliances: stainless greys for the kitchen, blue for water, amber for electrics
    "oven": "#8d9295", "hob": "#4e5457", "sink": "#b6bcbe", "plumbing": "#9aa3a6", "fridge": "#cfe4c9",
    "cassette": "#dde4e8", "fresh": "#7fb2cf", "grey": "#8f9aa2", "calorifier": "#c08f7a",
    "battery": "#e0b25c", "inverter": "#cf9a3f", "electrics": "#b98b36",
}
GLASSY = ("glass",)     # drawn transparent in the viewer

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


def shell_for(v):
    """Body panels with apertures, glazing, and the cab. Same box format as everything else."""
    L, W, H = v["length"], v["width"], v["height"]
    out = []
    clamp = lambda a, b: (min(a, L - 50), min(b, L - 50))

    # side walls, holes cut for the sliding door and the windows
    for side, y0, y1 in (("p", -WALL, 0), ("d", W, W + WALL)):
        holes = []
        if side == "p":
            sx0, sx1, sz0, sz1 = SLIDER
            holes.append((sx0, sx1, sz0, sz1))
        for s, wx0, wx1, wz0, wz1 in WINDOWS:
            if s == side:
                wx0, wx1 = clamp(wx0, wx1)
                holes.append((wx0, wx1, wz0, wz1))
        for x0, x1, z0, z1 in subtract((0, L, 0, H), holes):
            out.append((x0, x1, y0, y1, z0, z1, "shell"))
        for s, wx0, wx1, wz0, wz1 in WINDOWS:          # glaze the window openings
            if s == side:
                wx0, wx1 = clamp(wx0, wx1)
                out.append((wx0, wx1, y0, y1, wz0, wz1, "glass"))

    # roof, holes cut for the two fans
    for x0, x1, y0, y1 in subtract((0, L, 0, W), FAN_HOLES):
        out.append((x0, x1, y0, y1, H, H + WALL, "shell"))
    out.append((0, L, 0, W, -WALL, 0, "floor"))

    # rear doors
    ri, _, rz0, rz1 = REAR_DOORS
    for y0, y1, z0, z1 in subtract((0, W, 0, H), [(ri, W - ri, rz0, rz1)]):
        out.append((L, L + WALL, y0, y1, z0, z1, "shell"))

    # cab: floor, lower roof, raked-off windscreen simplified to a vertical pane,
    # side walls with door openings, dashboard, wheel, and the two swivel seats
    out.append((-NOSE, 0, 0, W, -WALL, 0, "cab"))
    out.append((-NOSE + 100, -100, 0, W, CAB_ROOF, CAB_ROOF + WALL, "cab"))
    out.append((-NOSE + 50, -NOSE + 90, 60, W - 60, 900, CAB_ROOF, "glass"))
    for y0, y1 in ((-WALL, 0), (W, W + WALL)):
        for x0, x1, z0, z1 in subtract((-NOSE, 0, 0, CAB_ROOF), [(-1200, -350, 300, 1400)]):
            out.append((x0, x1, y0, y1, z0, z1, "cab"))
    out.append((-1250, -1000, 60, W - 60, 700, 950, "dash"))
    out.append((-1050, -980, W - 620, W - 280, 950, 1300, "dash"))      # steering wheel
    for cx, cy, _r in v.get("seats", []):
        out.append((cx - 240, cx + 240, cy - 240, cy + 240,   0,  420, "seat"))
        out.append((cx - 240, cx + 240, cy - 240, cy + 240, 420,  500, "seat"))
        out.append((cx + 140, cx + 240, cy - 240, cy + 240, 500, 1100, "seat"))
    out.extend(wheels_for(v))
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
    out = []
    for x0, x1, y0, y1, label, _sub_label, _fill in v["boxes"]:
        z = HEIGHTS.get(label)
        if z:
            out.append((x0, x1, y0, y1, z[0], z[1], label))
    out.extend(remap(b, v) for b in EXTRA + APPLIANCES)
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
    for side, wx0, wx1, wz0, wz1 in WINDOWS:
        wx0, wx1 = clamp(wx0, wx1)
        y0, y1 = (-T, T) if side == "p" else (W - T, W + T)
        out.append((wx0, wx1, y0, y1, wz0, wz1, "hole"))
    ri, _, rz0, rz1 = REAR_DOORS
    out.append((L - T, L + T, ri, W - ri, rz0, rz1, "hole"))
    for fx0, fx1, fy0, fy1 in FAN_HOLES:
        out.append((fx0, fx1, fy0, fy1, H - T, H + T, "hole"))
    # no cab volume: as a wireframe it throws long lines across every interior view.
    # The seats and dash alone are enough to say "the cab is that way".
    out.append((-1250, -1000, 60, W - 60, 700, 950, "dash"))
    for cx, cy, _r in v.get("seats", []):
        out.append((cx - 240, cx + 240, cy - 240, cy + 240, 0, 500, "seat"))
        out.append((cx + 140, cx + 240, cy - 240, cy + 240, 500, 1100, "seat"))
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
    open(path, "w").write("# " + v["title"] + "\n" + "\n".join(lines) + "\n")
    print("wrote", path)


def props_data():
    """Prop meshes made by props.py, embedded so viewer.html stays a single file. Absent is
    fine - the viewer just keeps drawing the coloured box for that kind."""
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
            out[kind] = {"yaw": yaw.get(kind, 0),
                         "fit": "keep" if kind in KEEP_SHAPE else "fill",
                         "glb": base64.b64encode(open(os.path.join(d, name), "rb").read()).decode()}
    return out


def write_viewer(v, path):
    """Fill viewer_template.html with this variant's geometry."""
    tpl_path = os.path.join(HERE, "viewer_template.html")
    if not os.path.exists(tpl_path):
        print("skipped viewer.html - viewer_template.html not found")
        return
    data = {
        "title": v["title"], "note": v["note"],
        "length": v["length"], "width": v["width"], "height": v["height"], "nose": NOSE,
        "colours": KIND, "glassy": list(GLASSY), "stats": v.get("stats", []),
        "names": NAMES, "appliances": sorted({b[6] for b in APPLIANCES}),
        "containers": list(CONTAINERS), "props": props_data(),
        "cylinders": ["wheel"],
        "boxes": [{"b": [x0, x1, y0, y1, z0, z1], "k": kind}
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
    app = [remap(b, v) for b in APPLIANCES]
    rooms = {b[:6]: b[6] for b in boxes_for(v) if HEIGHTS.get(b[6])}
    overlap = lambda a, b: all(min(a[i * 2 + 1], b[i * 2 + 1]) - max(a[i * 2], b[i * 2]) > 1
                               for i in range(3))
    bad = []
    for i, a in enumerate(app):
        for b in app[i + 1:]:
            if overlap(a[:6], b[:6]):
                bad.append("%s clashes with %s" % (a[6], b[6]))
        if not (0 <= a[0] and a[1] <= L and 0 <= a[2] and a[3] <= W and a[5] <= H):
            bad.append("%s sticks out of the van" % a[6])
        if a[6] == "grey":
            continue                                    # underslung, deliberately outside
        if not [k for r, k in rooms.items()
                if a[0] >= r[0] - 1 and a[1] <= r[1] + 1 and a[2] >= r[2] - 1 and a[3] <= r[3] + 1]:
            bad.append("%s is not inside any cabinet" % a[6])
    assert not bad, "appliance check failed: " + "; ".join(bad)

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
