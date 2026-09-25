#!/usr/bin/env python3
"""Exact prop meshes for products that are simple shapes, built from their datasheet sizes.

    python solids.py            # -> props/<name>.glb for every mesh below

props.py asks an image-to-3D model for things whose shape is hard to put into words - a hob,
a toilet. A solar panel, a gas bottle or a battery is a few boxes and cylinders, and drawing
those in code is exact, free and repeatable. The viewer treats both the same way: it scales
the mesh to fill the model's box, so the box stays the authority on size. These keep their
own colours (model3d.OWN_COLOURS), because a panel is not one colour.

Frame: glTF, so X = along the van, Y = up, Z = across the van, all in mm; the viewer rescales.
"""
import json
import math
import os
import struct

import numpy as np

from products import PRODUCTS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "props")


class Mesh:
    """Triangles grouped by colour - one glTF primitive per colour."""

    def __init__(self):
        self.parts = {}

    def _add(self, colour, pos, nrm, idx):
        p = self.parts.setdefault(colour, [[], [], []])
        base = sum(len(a) for a in p[0])
        p[0].append(np.asarray(pos, "f4"))
        p[1].append(np.asarray(nrm, "f4"))
        p[2].append(np.asarray(idx, "u4") + base)

    def box(self, x0, x1, y0, y1, z0, z1, colour):
        """An axis-aligned box: x along, y up, z across."""
        faces = [  # normal, four corners counter-clockwise seen from outside
            ((1, 0, 0), [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]),
            ((-1, 0, 0), [(x0, y0, z1), (x0, y1, z1), (x0, y1, z0), (x0, y0, z0)]),
            ((0, 1, 0), [(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)]),
            ((0, -1, 0), [(x0, y0, z1), (x0, y0, z0), (x1, y0, z0), (x1, y0, z1)]),
            ((0, 0, 1), [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]),
            ((0, 0, -1), [(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)]),
        ]
        for n, quad in faces:
            self._add(colour, quad, [n] * 4, [0, 1, 2, 0, 2, 3])

    def hexa(self, corners, colour):
        """Any six-sided solid from its 8 corners: bottom 4 then top 4, each counter-clockwise
        from above. Flat-shaded - used for the fan's sloped hood."""
        b, t = corners[:4], corners[4:]
        quads = [b[::-1], t] + [[b[i], b[(i + 1) % 4], t[(i + 1) % 4], t[i]] for i in range(4)]
        for q in quads:
            q = [np.array(c, float) for c in q]
            n = np.cross(q[1] - q[0], q[2] - q[0])
            n = n / (np.linalg.norm(n) or 1)
            self._add(colour, q, [n] * 4, [0, 1, 2, 0, 2, 3])

    def cylinder(self, cx, cz, y0, y1, r0, r1=None, colour="#888", seg=32, caps=True, axis="y"):
        """Upright (along y) cylinder or cone frustum, radius r0 at y0 and r1 at y1. With
        axis="z" it lies across the van instead: cx, cz are then its x and height, y0..y1 its
        run across - for knobs on a front face."""
        if axis in ("z", "x"):
            # axis="x": lying along the van; cx, cz are then its height and across position
            order = [0, 2, 1] if axis == "z" else [1, 0, 2]
            tmp = Mesh()
            tmp.cylinder(cx, cz, y0, y1, r0, r1, colour, seg, caps)
            for col, (ps, ns, ix) in tmp.parts.items():
                for pp, nn, ii in zip(ps, ns, ix):
                    # swapping two axes is a mirror, so the triangles turn round too
                    self._add(col, pp[:, order], nn[:, order], ii.reshape(-1, 3)[:, ::-1].ravel()
                              - ii.min())
            return
        r1 = r0 if r1 is None else r1
        pos, nrm, idx = [], [], []
        slope = (r0 - r1) / ((y1 - y0) or 1)
        for i in range(seg + 1):
            a = 2 * math.pi * i / seg
            c, s = math.cos(a), math.sin(a)
            n = np.array([c, slope, s]); n /= np.linalg.norm(n)
            pos += [(cx + r0 * c, y0, cz + r0 * s), (cx + r1 * c, y1, cz + r1 * s)]
            nrm += [n, n]
        for i in range(seg):
            a, b, c2, d = 2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3
            idx += [a, b, d, a, d, c2]
        self._add(colour, pos, nrm, idx)
        if caps:
            for y, r, up in ((y0, r0, -1), (y1, r1, 1)):
                if r <= 0:
                    continue
                ring = [(cx + r * math.cos(2 * math.pi * i / seg), y,
                         cz + r * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
                pts = [(cx, y, cz)] + ring
                tri = []
                for i in range(seg):
                    j = 1 + (i + 1) % seg
                    tri += [0, j, 1 + i] if up > 0 else [0, 1 + i, j]
                self._add(colour, pts, [(0, up, 0)] * len(pts), tri)

    def glb(self, path):
        """Write a minimal binary glTF: one mesh, a primitive and a material per colour."""
        blob, views, accs, prims, mats = b"", [], [], [], []
        for colour, (ps, ns, ix) in self.parts.items():
            p, n, i = np.concatenate(ps), np.concatenate(ns), np.concatenate(ix)
            ids = []
            for arr, target, kind in ((p, 34962, "VEC3"), (n, 34962, "VEC3"), (i, 34963, "SCALAR")):
                data = arr.tobytes()
                views.append({"buffer": 0, "byteOffset": len(blob), "byteLength": len(data),
                              "target": target})
                acc = {"bufferView": len(views) - 1, "count": len(arr),
                       "componentType": 5126 if arr.dtype == np.float32 else 5125, "type": kind}
                if arr is p:
                    acc["min"], acc["max"] = p.min(0).tolist(), p.max(0).tolist()
                accs.append(acc)
                ids.append(len(accs) - 1)
                blob += data + b"\0" * (-len(data) % 4)
            hx = colour[1:] if len(colour) == 7 else "".join(ch * 2 for ch in colour[1:])
            rgb = [int(hx[k:k + 2], 16) / 255 for k in (0, 2, 4)]
            mats.append({"pbrMetallicRoughness": {"baseColorFactor": rgb + [1],
                                                  "metallicFactor": 0, "roughnessFactor": 0.8}})
            prims.append({"attributes": {"POSITION": ids[0], "NORMAL": ids[1]}, "indices": ids[2],
                          "material": len(mats) - 1})
        doc = {"asset": {"version": "2.0", "generator": "van/solids.py"}, "scene": 0,
               "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0}], "meshes": [{"primitives": prims}],
               "materials": mats, "accessors": accs, "bufferViews": views,
               "buffers": [{"byteLength": len(blob)}]}
        js = json.dumps(doc, separators=(",", ":")).encode()
        js += b" " * (-len(js) % 4)
        with open(path, "wb") as f:
            f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(blob)))
            f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
            f.write(struct.pack("<II", len(blob), 0x004E4942) + blob)


# --- the products ------------------------------------------------------------------------
def solar():
    """Victron BlueSolar 185 W: aluminium frame, 4 x 9 cells, a junction box underneath."""
    L, W, _ = PRODUCTS["victron-185w"]["outer"]
    H, f = 35, 28
    m = Mesh()
    m.box(0, L, 0, H, 0, f, "#c9cdd2"); m.box(0, L, 0, H, W - f, W, "#c9cdd2")
    m.box(0, f, 0, H, f, W - f, "#c9cdd2"); m.box(L - f, L, 0, H, f, W - f, "#c9cdd2")
    m.box(f, L - f, H - 8, H - 3, f, W - f, "#1b2a4a")                   # the glass over the cells
    nx, nz = 9, 4
    for k in range(1, nx):
        x = f + (L - 2 * f) * k / nx
        m.box(x - 2, x + 2, H - 3, H - 2.5, f, W - f, "#7f8fae")
    for k in range(1, nz):
        z = f + (W - 2 * f) * k / nz
        m.box(f, L - f, H - 3, H - 2.5, z - 2, z + 2, "#7f8fae")
    m.box(L * 0.45, L * 0.55, 0, 20, W * 0.35, W * 0.65, "#222")         # junction box
    return m


def maxxfan():
    """MaxxFan Deluxe with its rain hood closed: a white flange, and a hood that slopes up from
    the front to its opening at the back."""
    L, W = PRODUCTS["maxxfan-deluxe"]["outer"]
    H = PRODUCTS["maxxfan-deluxe"]["above_roof"][0]
    m = Mesh()
    m.box(0, L, 0, 14, 0, W, "#e9e8e3")
    i = 22
    lo, hi = 45, H
    m.hexa([(i, 14, i), (i, 14, W - i), (L - i, 14, W - i), (L - i, 14, i),
            (i, lo, i), (i, lo, W - i), (L - i, hi, W - i), (L - i, hi, i)], "#f2f1ec")
    m.box(L - i, L - i + 3, 20, hi - 12, i + 10, W - i - 10, "#3a3d42")   # the dark opening
    return m


def gas_bottle():
    """6 kg steel LPG bottle: foot ring, body, shoulders, the protective collar and valve."""
    D, _, H = PRODUCTS["gas-bottle-6kg"]["outer"]
    r, c = D / 2, D / 2
    m = Mesh()
    body = "#c9563c"
    m.cylinder(c, c, 0, 30, r * 0.92, colour="#6d6f72")                  # foot ring
    m.cylinder(c, c, 30, H * 0.70, r, colour=body)
    m.cylinder(c, c, H * 0.70, H * 0.80, r, r * 0.55, colour=body, caps=False)
    m.cylinder(c, c, H * 0.80, H * 0.83, r * 0.55, r * 0.40, colour=body)
    m.cylinder(c, c, H * 0.83, H, r * 0.62, colour="#b54b33", caps=False)  # collar, open ring
    m.cylinder(c, c, H * 0.83, H * 0.95, r * 0.14, colour="#b08d57")     # valve
    m.cylinder(c, c, H * 0.95, H * 0.97, r * 0.22, colour="#222")        # handwheel
    return m


def battery():
    """Ective LC 150 LT: black case, a grey lid, two terminals. Built across the van, as it
    stands in the bench (175 along, 353 across)."""
    Lx, Wz, H = 175, 353, 190
    m = Mesh()
    m.box(0, Lx, 0, H - 12, 0, Wz, "#262626")
    m.box(4, Lx - 4, H - 12, H, 4, Wz - 4, "#4a4d52")
    m.box(Lx - 1, Lx + 0.5, 50, 120, 60, Wz - 60, "#c8102e")             # label band
    for z, col in ((50, "#c8102e"), (Wz - 50, "#111")):
        m.cylinder(Lx * 0.5, z, H, H + 18, 10, colour=col)
    return m


def multiplus_c():
    """Victron MultiPlus C 12/2000: the blue case, black end covers, a small display panel."""
    L, W, H = PRODUCTS["multiplus-c-12-2000"]["outer"]    # 520 x 255 x 125, lying flat
    m = Mesh()
    m.box(40, L - 40, 0, H, 0, W, "#1f5fa8")
    m.box(0, 40, 0, H, 0, W, "#1d1d1d"); m.box(L - 40, L, 0, H, 0, W, "#1d1d1d")
    m.box(L * 0.4, L * 0.6, H, H + 2, W * 0.3, W * 0.7, "#e8e8e8")      # label
    return m


def starlink_mini():
    """Starlink Mini: a white slab with its kickstand folded, on a low mount."""
    L, W, H = PRODUCTS["starlink-mini"]["outer"]
    m = Mesh()
    m.box(0, L, 12, 12 + H * 0.8, 0, W, "#f4f4f2")
    m.box(L * 0.2, L * 0.8, 0, 12, W * 0.2, W * 0.8, "#6b6f75")          # mount
    return m


def hob():
    """Thetford Topline 922: a stainless top with two burners one behind the other, black pan
    supports, two knobs at the aisle edge; the body hangs under the worktop. 305 along the van,
    500 across, the aisle at +z."""
    L, W, _ = PRODUCTS["thetford-topline-922"]["outer"]
    H, top = 80, 70
    m = Mesh()
    m.box(10, L - 10, 0, top - 2, 10, W - 10, "#3a3a3a")                 # body under the worktop
    m.box(0, L, top - 2, top + 2, 0, W, "#c9cdd2")                       # stainless top
    for zc, r in ((150, 45), (330, 38)):
        m.cylinder(L / 2, zc, top + 2, top + 9, r, colour="#2b2b2b")     # burner
        m.cylinder(L / 2, zc, top + 9, top + 12, r * 0.55, colour="#111")      # cap
        for a in range(4):                                               # pan support arms
            if a % 2:
                m.box(L / 2 - 4, L / 2 + 4, top + 2, H, zc - r - 25, zc - r + 5, "#111")
                m.box(L / 2 - 4, L / 2 + 4, top + 2, H, zc + r - 5, zc + r + 25, "#111")
            else:
                m.box(L / 2 - r - 25, L / 2 - r + 5, top + 2, H, zc - 4, zc + 4, "#111")
                m.box(L / 2 + r - 5, L / 2 + r + 25, top + 2, H, zc - 4, zc + 4, "#111")
    for xc in (L * 0.3, L * 0.7):
        m.cylinder(xc, W - 45, top + 2, top + 22, 17, colour="#1a1a1a")  # knobs
    return m


def fridge_c95l():
    """Vitrifrigo C95L: black cabinet, a flush door on the aisle side (+z) with a long handle,
    the control panel along the top, a vent grille at the bottom."""
    L, D, H = PRODUCTS["vitrifrigo-c95l"]["outer"]
    m = Mesh()
    m.box(0, L, 0, H, 0, D - 20, "#1f1f1f")
    m.box(10, L - 10, 60, H - 70, D - 20, D, "#2c2d30")                  # door
    m.box(0, L, H - 70, H, D - 20, D - 4, "#151515")                     # control strip
    m.box(L * 0.4, L * 0.6, H - 45, H - 25, D - 4, D - 2, "#5ab4e6")     # display
    m.box(L - 45, L - 25, 200, H - 150, D, D + 12, "#b9bcc0")            # handle
    for k in range(6):                                                   # grille
        m.box(40, L - 40, 12 + 8 * k, 16 + 8 * k, D - 20, D - 16, "#555")
    return m


def truma_b10():
    """Truma Boiler B10: a light grey casing, the flue out through the passenger wall (-z),
    blue and red water connections on top."""
    L, D, H = PRODUCTS["truma-b10"]["outer"]
    m = Mesh()
    m.box(0, L, 0, H, 20, D, "#dfe1e0")
    m.box(L * 0.3, L * 0.7, H * 0.3, H * 0.75, 3, 20, "#9a9c9e")          # flue to the wall
    m.box(L * 0.25, L * 0.75, H * 0.2, H * 0.85, 0, 3, "#6d6f72")         # wall cowl, inside face
    m.cylinder(L * 0.35, D * 0.6, H, H + 25, 9, colour="#2e86c1")
    m.cylinder(L * 0.65, D * 0.6, H, H + 25, 9, colour="#e74c3c")
    m.box(L * 0.1, L * 0.3, H * 0.5, H * 0.65, D, D + 4, "#3a3d42")       # control / label
    return m


def porta_potti():
    """Thetford Porta Potti 565E at its REAL size (386 x 450 x 447), which is smaller than its
    slot - the viewer places it at 1:1 on the slot's floor (model3d.REAL_SIZE). Grey waste
    tank below, white flush unit with seat and lid above, facing the aisle (-z)."""
    W, D, H = PRODUCTS["porta-potti-565e"]["outer"]
    m = Mesh()
    low = H * 0.42
    m.box(0, W, 0, low, 0, D, "#8d9399")                                 # waste tank
    m.box(0, W, low, H - 40, 0, D, "#f3f3f1")                            # flush unit
    m.box(20, W - 20, H - 40, H - 25, 0, D - 60, "#e6e6e3")              # seat
    m.box(20, W - 20, H - 25, H, 10, D - 60, "#fafaf8")                  # lid, closed
    m.box(W - 90, W - 30, H - 40, H - 20, D - 55, D - 10, "#9aa0a6")     # flush button
    m.box(W * 0.3, W * 0.7, low - 30, low - 10, -4, 0, "#5b6066")        # release handle
    return m


def oven_tefal():
    """Tefal Optimo OF4448: silver-grey body, a dark glass door on the aisle side (-z) with a
    handle, three knobs down the right of the front."""
    L, D, H = PRODUCTS["tefal-of4448"]["outer"]
    m = Mesh()
    m.box(0, L, 0, H, 3, D, "#b9bcc0")
    # the knobs are on the right of the front seen from the aisle - the forward end (x = 0)
    m.box(120, L - 15, 30, H - 30, 0, 3, "#262a2e")                      # door glass
    m.box(145, L - 40, H - 55, H - 42, -18, 0, "#8d9399")                # handle
    for k in range(3):
        m.cylinder(60, H * (0.25 + 0.25 * k), -16, 0, 15, colour="#1a1a1a", axis="z")
    return m


def tank(L, D, H, lid_x, fittings):
    """A tank made to size: natural PE, a cleaning lid, round fittings on top."""
    m = Mesh()
    m.box(0, L, 0, H, 0, D, "#e8e4d8")
    m.cylinder(lid_x, D / 2, H, H + 12, min(80, D / 2 - 20), colour="#3a3d42")
    for x, z, r, col in fittings:
        m.cylinder(x, z, H, H + 30, r, colour=col)
    return m


def fresh_tank():
    """Fresh tank, 1020 x 374 x 310: cleaning lid, filler, vent, level sensor, blue outlet."""
    return tank(1020, 374, 310, 520,
                [(930, 187, 22, "#d6d8da"), (980, 300, 9, "#d6d8da"), (300, 187, 14, "#555"),
                 (40, 187, 10, "#2e86c1")])


def grey_tank():
    """Grey tank, 880 x 600 x 180: cleaning lid, sink and shower inlets, level sensor."""
    return tank(880, 600, 180, 440,
                [(40, 480, 18, "#6e5a44"), (40, 540, 11, "#6e5a44"), (780, 300, 14, "#555")])


def tap_grohe():
    """Grohe Eurosmart Cosmopolitan 31170000: a round body at the aft end on its base, a
    lever on top, and the spout reaching 226 forward (toward x = 0) over the bowl."""
    L, W, H = 256, 60, 202                      # the box: reach + body, 202 tall
    bx, bz = L - 30, W / 2
    chrome = "#c9ced3"
    m = Mesh()
    m.cylinder(bx, bz, 0, 12, 28, colour="#aab0b6")                      # base
    m.cylinder(bx, bz, 12, H - 40, 22, colour=chrome)                    # body
    m.box(bx - 60, bx + 10, H - 40, H - 30, bz - 8, bz + 8, chrome)      # lever
    m.cylinder(H - 55, bz, 0, bx, 11, colour=chrome, axis="x")           # spout, forward
    m.cylinder(20, bz, H - 90, H - 55, 9, colour=chrome)                 # its nose, pointing down
    return m


def tap_franke():
    """Franke Lina Semi Pro: a chrome column on its base, an arm at the top reaching 205
    forward (toward x = 0) that holds the spray head, and the black spring hose rising from
    the base to the head."""
    L, W, H = 235, 60, 410
    bx, c = L - 30, W / 2
    chrome, black = "#c9ced3", "#1d1d1d"
    m = Mesh()
    m.cylinder(bx, c, 0, 15, 28, colour="#aab0b6")                       # base
    m.cylinder(bx, c, 15, 120, 22, colour=chrome)                        # body with the lever
    m.box(bx - 55, bx + 5, 105, 115, c - 7, c + 7, chrome)               # lever
    m.cylinder(bx + 12, c, 120, H - 20, 8, colour=chrome)                # the column
    m.cylinder(H - 20, c, 30, bx + 12, 8, colour=chrome, axis="x")       # arm, forward
    for k in range(14):                                                  # the spring, rising
        z = 125 + k * 17
        m.cylinder(bx - 10, c, z, z + 9, 17, colour=black)
    m.cylinder(bx - 10, c, 120, H - 40, 7, colour="#3a3a3a")             # the hose inside it
    m.cylinder(H - 40, c, 40, bx - 10, 7, colour="#3a3a3a", axis="x")    # hose to the head
    m.cylinder(40, c, H - 120, H - 20, 20, colour=chrome)                # spray head in its holder
    return m


def filtertap_its():
    """A slim drinking-water tap standing aft of the bowl: base, a thin column, and a neck
    reaching forward (toward x = 0) so it pours into the bowl, a small lever."""
    L, W, H = 210, 50, 280
    bx, c = L - 25, W / 2
    m = Mesh()
    m.cylinder(bx, c, 0, 10, 20, colour="#aab0b6")
    m.cylinder(bx, c, 10, H - 12, 9, colour="#c9ced3")
    m.cylinder(H - 12, c, 15, bx, 7, colour="#c9ced3", axis="x")        # the neck, forward
    m.cylinder(15, c, H - 50, H - 12, 6, colour="#c9ced3")               # nose, pointing down
    m.box(bx - 4, bx + 4, H - 80, H - 70, c - 4, W, "#8d9399")           # lever
    return m


def filter_alb():
    """Alb Filter Nano: a white housing Ø69 x 120 lying along the van, quick couplings and
    hoses at both ends, on a small wall bracket."""
    L, W, H = 260, 75, 75
    c = W / 2
    m = Mesh()
    m.cylinder(c, c, 70, 190, 34, colour="#f1f1ef", axis="x")            # housing
    m.cylinder(c, c, 190, 200, 36, colour="#1f5fa8", axis="x")           # cap
    m.cylinder(c, c, 0, 70, 6, colour="#2e86c1", axis="x")               # hose in
    m.cylinder(c, c, 200, L, 6, colour="#2e86c1", axis="x")              # hose out
    m.box(110, 150, 0, 4, 10, W - 10, "#8d9399")                         # bracket
    return m


VBLUE, COPPER = "#1f5fa8", "#b87333"


def distribution():
    """The distribution box in the driver bench, 220 along x 160 across x 200 high: a board on
    the wall side (+z) carrying the Orion XS, the SmartShunt, two copper busbars, a MEGA fuse
    per battery and the blade fuse block - all at their datasheet sizes."""
    L, W, H = 220, 160, 200
    m = Mesh()
    m.box(0, L, 0, H, W - 12, W, "#d8cfbf")                              # plywood backboard
    ob = PRODUCTS["orion-xs-50"]["outer"]                                # 137 x 123 x 40
    m.box(8, 8 + ob[0], 70, 70 + ob[1], W - 12 - ob[2], W - 12, VBLUE)   # Orion XS
    sh = PRODUCTS["smartshunt-500"]["outer"]                             # 46 x 120 x 54
    m.box(8, 8 + sh[1], 12, 12 + sh[0], W - 12 - sh[2], W - 12, VBLUE)   # SmartShunt, lying
    m.box(150, 212, 150, 162, W - 40, W - 12, COPPER)                    # + busbar
    m.box(150, 212, 128, 140, W - 40, W - 12, "#333")                    # - busbar
    for k, x in enumerate((152, 184)):                                   # MEGA fuse per battery
        m.box(x, x + 26, 60, 118, W - 42, W - 12, "#c8102e")
    m.box(140, 212, 8, 50, W - 45, W - 12, "#222")                       # blade fuse block
    for k in range(6):
        m.box(146 + 11 * k, 152 + 11 * k, 50, 58, W - 30, W - 20,
              ("#f2c200", "#c8102e", "#2e86c1", "#2e8b57", "#f2c200", "#c8102e")[k])
    return m


def garage_board():
    """The garage board on the driver wall, 400 along x 110 deep x 300 high: SmartSolar MPPT
    100/30, the PV isolator, and the 230 V box A (2-pole RCBO) under the CEE inlet."""
    L, W, H = 400, 110, 300
    m = Mesh()
    m.box(0, L, 0, H, W - 12, W, "#d8cfbf")                              # backboard
    mp = PRODUCTS["smartsolar-100-30"]["outer"]                          # 130 x 186 x 70
    m.box(20, 20 + mp[0], 90, 90 + mp[1], W - 12 - mp[2], W - 12, VBLUE)
    m.box(40, 130, 150, 190, W - 12 - mp[2] - 2, W - 12 - mp[2], "#15407a")  # heat sink look
    sb = PRODUCTS["shore-230v"]["outer"]                                 # 150 x 100 x 100
    m.box(230, 230 + sb[0], 150, 150 + sb[1], W - 12 - sb[2] + 10, W - 12, "#9aa0a6")
    m.box(270, 340, 170, 230, W - 12 - sb[2] + 6, W - 12 - sb[2] + 10, "#dfe6ea")  # window
    m.box(230, 290, 40, 100, W - 50, W - 12, "#e8e8e8")                  # PV isolator
    m.cylinder(260, W - 50, 60, 80, 14, colour="#c8102e", axis="z")      # its red knob
    return m


def plumbing():
    """The pump box under the sink, 340 x 340 x 330: the Shurflo Trail King 7 on its plate,
    a strainer before it, a small accumulator after it, and the sink trap coming down."""
    L, W, H = 340, 340, 330
    m = Mesh()
    pl, pw, ph = PRODUCTS["shurflo-trailking-7"]["outer"]                # 197 x 127 x 113
    m.box(20, 240, 0, 8, 20, 180, "#555")                                # mounting plate
    m.box(30, 30 + pl * 0.55, 8, 8 + ph, 40, 40 + pw, "#2b2b2b")         # motor
    m.box(30 + pl * 0.55, 30 + pl, 8, 8 + ph, 40, 40 + pw, "#8d9399")    # pump head
    m.cylinder(8 + ph / 2, 100, 230, 300, 30, colour="#e9e9e9", axis="x")  # strainer, in
    m.cylinder(290, 250, 0, 200, 45, colour="#2e86c1")                   # accumulator
    m.cylinder(120, 280, 180, H, 20, colour="#cfcfcf")                   # trap, down from the sink
    m.cylinder(120, 280, 140, 180, 32, colour="#cfcfcf")                 # its bottle
    return m


# --- furniture (v2-real): one mesh per box, built at that box's own size -----------------
PLY, EDGE, TOP = "#e8dcc2", "#c9b187", "#c2a07a"          # poplar ply, its edge band, worktop
FABRIC, PIPING, ALU = "#9aa98f", "#7c8b73", "#c9cdd2"


def turned(m, L, W):
    """The same mesh turned 180 degrees about the vertical: for a piece whose front faces +z."""
    out = Mesh()
    for col, (ps, ns, ix) in m.parts.items():
        for pp, nn, ii in zip(ps, ns, ix):
            q, r = pp.copy(), nn.copy()
            q[:, 0], q[:, 2] = L - pp[:, 0], W - pp[:, 2]
            r[:, 0], r[:, 2] = -nn[:, 0], -nn[:, 2]
            out._add(col, q, r, ii - ii.min())
    return out


def panel(m, x0, x1, y0, y1, colour=PLY, latch=None):
    """A door or lid front on the z = 0 face, 3 mm gaps, a round push latch at `latch`."""
    m.box(x0 + 2, x1 - 2, y0 + 2, y1 - 2, 0, 2, colour)
    if latch:
        m.cylinder(latch[0], latch[1], -3, 0, 9, colour="#3a3a3a", axis="z")


def carcass(L, W, H, worktop=0, doors=(), openings=(), lids=()):
    """Front at z = 0. Body in poplar ply with edge bands round the front, an optional worktop,
    door panels (x0, x1, y0, y1, latch), dark openings where an appliance shows, lids on top."""
    m = Mesh()
    m.box(0, L, 0, H - worktop, 2, W, PLY)
    if worktop:
        m.box(0, L, H - worktop, H, 0, W, TOP)
    e = 18
    for x0, x1, y0, y1 in ((0, e, 0, H - worktop), (L - e, L, 0, H - worktop),
                           (0, L, H - worktop - e, H - worktop), (0, L, 0, e)):
        m.box(x0, x1, y0, y1, 0.5, 2, EDGE)
    for x0, x1, y0, y1, latch in doors:
        panel(m, x0, x1, y0, y1, latch=latch)
    for x0, x1, y0, y1 in openings:
        m.box(x0, x1, y0, y1, 0, 2.5, "#2a2a2a")
    for x0, x1 in lids:                                    # lid gaps on the top
        m.box(x0, x0 + 3, H, H + 0.5, 2, W, EDGE)
        m.box(x1 - 3, x1, H, H + 0.5, 2, W, EDGE)
    return m


def cushion(L, W, H, colour=FABRIC):
    """Foam in fabric, a piped edge round the top."""
    m = Mesh()
    m.box(6, L - 6, 0, H - 6, 6, W - 6, colour)
    m.box(12, L - 12, H - 6, H, 12, W - 12, colour)
    for x0, x1, z0, z1 in ((0, L, 0, 8), (0, L, W - 8, W), (0, 8, 8, W - 8), (L - 8, L, 8, W - 8)):
        m.box(x0, x1, H - 16, H - 6, z0, z1, PIPING)
    return m


def slab(L, W, H, colour=TOP):
    m = Mesh()
    m.box(0, L, 0, H, 0, W, colour)
    return m


def furniture_piece(kind, L, W, H, front_plus_z, n):
    """One furniture box. L along x, W across (z), H up. Front at z = 0, turned if +z."""
    if kind in ("SINK", "HOB"):
        # the galley: 30 worktop, the built-in appliance's opening, a cupboard door beside it
        if kind == "SINK":        # oven opening at x 135-597, z 380-668; cupboard aft of it
            m = carcass(L, W, H, 30, doors=[(597, L, 40, H - 30, (L - 40, H - 80))],
                        openings=[(135, 597, 380, 668)])
        else:                      # passenger side, so built mirrored and turned: the fridge
            # door at van x 100-585 is 195-680 here, the cupboard aft of it 0-195
            m = carcass(L, W, H, 30, doors=[(0, 195, 40, H - 30, (40, H - 80))],
                        openings=[(195, 680, 30, 822)])
    elif kind in ("BENCH", "LOCKER"):
        m = carcass(L, W, H, lids=[(0, L / 2), (L / 2, L)] if kind == "BENCH" else [(0, L)])
    elif kind == "REAR BENCH":
        # front faces forward (-x): built with its length across, then turned a quarter
        m = carcass(W, L, H, lids=[(0, W / 3), (W / 3, 2 * W / 3), (2 * W / 3, W)])
        out = Mesh()
        for col, (ps, ns, ix) in m.parts.items():
            for pp, nn, ii in zip(ps, ns, ix):
                q, r = pp.copy(), nn.copy()
                q[:, 0], q[:, 2] = pp[:, 2], W - pp[:, 0]
                r[:, 0], r[:, 2] = nn[:, 2], -nn[:, 0]
                out._add(col, q, r, ii - ii.min())
        return out
    elif kind == "FOOTWELL -> BED":
        m = carcass(L, W, H, lids=[(0, L)])
        m.cylinder(L / 2, W / 2, H, H + 3, 60, colour=ALU)             # the post socket
        return m                                                        # no front to turn
    elif kind == "WARDROBE":
        latch = (L / 2 - 20, H - 60) if n in (0, 3) else None
        m = carcass(L, W, H)
        panel(m, 20, L / 2 - 1, 20, H, latch=latch and (L / 2 - 30, latch[1]))
        panel(m, L / 2 + 1, L - 20, 20, H, latch=latch and (L / 2 + 30, latch[1]))
    elif kind == "overhead":
        m = carcass(L, W, H)
        k = max(1, round(L / 420))                                      # doors ~400 wide
        for i in range(k):
            x0, x1 = 20 + (L - 40) * i / k, 20 + (L - 40) * (i + 1) / k
            panel(m, x0, x1, 20, H - 20, latch=((x0 + x1) / 2, 40))
    elif kind in ("bed", "infill", "backrest"):
        m = cushion(L, W, H)
    elif kind == "pillow":
        m = cushion(L, W, H, colour="#f1eee8")
    elif kind in ("table", "ftable"):
        m = Mesh()
        m.box(0, L, H - 25, H, 0, W, TOP)
        for x0, x1, z0, z1 in ((0, L, 0, 3), (0, L, W - 3, W), (0, 3, 0, W), (L - 3, L, 0, W)):
            m.box(x0, x1, H - 25, H, z0, z1, EDGE)
        if kind == "table":
            m.cylinder(L / 2, W / 2, 0, H - 25, 55, colour=ALU)         # the socket on the post
        else:
            m.box(L * 0.6, L * 0.9, 0, H - 25, W * 0.4, W * 0.5, ALU)   # its bracket
        return m                                                        # symmetric enough
    elif kind in ("ftablep", "ptablep", "ptable"):
        return slab(L, W, H)
    elif kind in ("farm", "parm"):
        return slab(L, W, H, colour=ALU)
    elif kind == "leg":
        m = Mesh()
        m.cylinder(L / 2, W / 2, 0, 8, L / 2, colour=ALU)
        m.cylinder(L / 2, W / 2, 8, H - 8, 30, colour=ALU)
        m.cylinder(L / 2, W / 2, H - 8, H, L / 2 - 10, colour=ALU)
        return m
    elif kind == "shower":
        m = Mesh()
        m.cylinder(L / 2, W - 20, 0, H, 12, colour=ALU)                 # riser rail on the wall
        m.cylinder(L / 2, W - 60, H - 90, H - 60, 55, colour=ALU)       # the head
        m.cylinder(L / 2, W - 40, 0, 300, 8, colour="#8d9399")          # hose
        m.box(L / 2 - 30, L / 2 + 30, 600 - 30 if H > 600 else H / 2, 600 if H > 600 else H / 2 + 30,
              W - 40, W - 20, "#e8e8e8")                                # mixer body
        return m
    else:
        return slab(L, W, H, colour=PLY)
    return turned(m, L, W) if front_plus_z else m


def furniture(variant="v2-real"):
    """{key: Mesh} for every furniture box of the variant, keyed as the viewer asks for them."""
    import model3d
    from plan import VARIANTS
    v = VARIANTS[variant]
    boxes = model3d.boxes_for(v, with_shell=True)
    out = {}
    for b, key in zip(boxes, model3d.furniture_keys(v, boxes)):
        if not key:
            continue
        x0, x1, y0, y1, z0, z1, kind = b
        n = int(key.rsplit("-", 1)[1])
        out[key] = furniture_piece(kind, x1 - x0, y1 - y0, z1 - z0, (y0 + y1) / 2 < v["width"] / 2, n)
    return out


SOLIDS = {"solar": solar, "fan": maxxfan, "gasbottle": gas_bottle,
          "battery-ective": battery, "inverter-multiplusc": multiplus_c, "starlink": starlink_mini,
          "hob-thetford": hob, "fridge-c95l": fridge_c95l, "b10": truma_b10,
          "portapotti": porta_potti, "oven-tefal": oven_tefal,
          "fresh-v2r": fresh_tank, "grey-v2r": grey_tank,
          "tap-grohe": tap_grohe, "tap-franke": tap_franke,
          "dist-v2r": distribution, "board-v2r": garage_board, "plumbing-v2r": plumbing, "filtertap-its": filtertap_its, "filter-alb": filter_alb}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, make in SOLIDS.items():
        path = os.path.join(OUT, name + ".glb")
        make().glb(path)
        print("wrote", path, "%.1f kB" % (os.path.getsize(path) / 1000))
    for old in os.listdir(OUT):                      # furniture keys can change with the plan
        if old.startswith("v2-real-") and old.endswith(".glb"):
            os.remove(os.path.join(OUT, old))
    pieces = furniture()
    for name, m in pieces.items():
        m.glb(os.path.join(OUT, name + ".glb"))
    print("wrote %d furniture meshes" % len(pieces))


if __name__ == "__main__":
    main()
