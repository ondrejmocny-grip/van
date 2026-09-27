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

    def quad(self, pts, colour, out=None):
        """A flat four-corner face, any orientation. `out` is a direction the face should look
        toward (its normal is flipped to agree), else the corners' own winding decides."""
        q = [np.array(c, float) for c in pts]
        n = np.cross(q[1] - q[0], q[2] - q[0])
        if out is not None and np.dot(n, out) < 0:
            q, n = q[::-1], -n
        n = n / (np.linalg.norm(n) or 1)
        self._add(colour, q, [n] * 4, [0, 1, 2, 0, 2, 3])

    def polygon(self, pts2, axis, at, colour, out):
        """A flat polygon (ear-clipped, may be concave) in the plane axis = at. pts2 are the
        two other coordinates in order (for axis 'z': x, y-up)."""
        tris = earclip(pts2)
        def lift(p):
            a, b = p
            return {"z": (a, b, at), "x": (at, b, a), "y": (a, at, b)}[axis]
        for i, j, k in tris:
            q = [np.array(lift(pts2[t]), float) for t in (i, j, k)]
            n = np.cross(q[1] - q[0], q[2] - q[0])
            if np.dot(n, out) < 0:
                q, n = q[::-1], -n
            n = n / (np.linalg.norm(n) or 1)
            self._add(colour, q, [n] * 3, [0, 1, 2])

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
            hx = colour[1:] if len(colour) in (7, 9) else "".join(ch * 2 for ch in colour[1:])
            rgba = [int(hx[k:k + 2], 16) / 255 for k in (0, 2, 4)]
            alpha = int(hx[6:8], 16) / 255 if len(hx) == 8 else 1.0      # "#rrggbbaa": see-through
            mat = {"pbrMetallicRoughness": {"baseColorFactor": rgba + [alpha],
                                            "metallicFactor": 0, "roughnessFactor": 0.8}}
            if alpha < 1:
                mat["alphaMode"] = "BLEND"
            mats.append(mat)
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


def earclip(pts):
    """Triangles (index triples) of a simple polygon given in order."""
    P = [tuple(p) for p in pts]
    area = sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1]
               for i in range(len(P)))
    idx = list(range(len(P))) if area > 0 else list(range(len(P)))[::-1]
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    def inside(p, a, b, c):
        return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0
    out, guard = [], 0
    while len(idx) > 3 and guard < 10000:
        guard += 1
        for n in range(len(idx)):
            i, j, k = idx[n - 1], idx[n], idx[(n + 1) % len(idx)]
            a, b, c = P[i], P[j], P[k]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(inside(P[m], a, b, c) for m in idx if m not in (i, j, k)):
                continue
            out.append((i, j, k))
            idx.pop(n)
            break
        else:
            break
    if len(idx) == 3:
        out.append(tuple(idx))
    return out


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


def fronts(key, box, L, H, mirrored):
    """The doors, drawers and openings the cut list proposes (cutlist.FRONTS) for this box,
    in its own frame: x from the box's start (mirrored for a piece built turned), z from its
    foot, cut to its height - so a wardrobe door runs on through the bands it spans."""
    import cutlist
    x0b, z0b = box[0], box[4]
    doors, openings = [], []
    for piece, a0, a1, b0, b1, _what in cutlist.FRONTS.get(key, []):
        za, zb = max(b0 - z0b, 0), min(b1 - z0b, H)
        if zb <= za or piece == "fixed panel":
            continue
        xa, xb = a0 - x0b, a1 - x0b
        if mirrored:
            xa, xb = L - xb, L - xa
        if "opening" in piece:
            openings.append((xa, xb, za, zb))
        else:
            top_here = b1 - z0b <= H                      # the latch goes near its top edge
            doors.append((xa, xb, za, zb, ((xa + xb) / 2, zb - 40) if top_here else None))
    return doors, openings


def furniture_piece(kind, L, W, H, front_plus_z, n, box=None):
    """One furniture box. L along x, W across (z), H up. Front at z = 0, turned if +z."""
    if kind in ("SINK", "HOB"):
        # the galley: 30 worktop, and the doors, drawers and openings of the cut list
        doors, openings = fronts(kind, box, L, H, front_plus_z)
        m = carcass(L, W, H, 30, doors=doors, openings=openings)
    elif kind in ("BENCH", "LOCKER"):
        key = kind if kind == "LOCKER" else ("BENCH-p" if front_plus_z else "BENCH-d")
        doors, _ = fronts(key, box, L, H, front_plus_z)
        m = carcass(L, W, H, doors=doors,
                    lids=[(0, L / 2), (L / 2, L)] if kind == "BENCH" else [(0, L)])
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
        doors, _ = fronts("WARDROBE", box, L, H, front_plus_z)
        m = carcass(L, W, H, doors=doors)
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
    elif kind == "seat":
        m = Mesh()
        seat_dark, cloth = "#2f3135", "#474a50"
        if H > 300:                    # the base, or the backrest (the tall thin one)
            if L < 150:                # backrest with headrests: aft face at x = L
                m.box(0, L, 0, H - 200, 20, W - 20, cloth)
                heads = 2 if W > 700 else 1
                for i in range(heads):
                    c = W * (i + 0.5) / heads
                    m.box(20, L - 20, H - 190, H, c - 130, c + 130, cloth)
                    m.box(40, L - 40, H - 220, H - 190, c - 60, c - 45, "#9aa0a6")
                    m.box(40, L - 40, H - 220, H - 190, c + 45, c + 60, "#9aa0a6")
            else:
                m.box(40, L - 40, 0, 60, 40, W - 40, "#6d6f72")          # rails
                m.box(60, L - 60, 60, H, 60, W - 60, seat_dark)          # pedestal
        else:
            m = cushion(L, W, H, colour=cloth)
        return m
    elif kind == "dash":
        m = Mesh()
        if n == 0:                     # the dashboard: sloping top toward the windscreen
            m.hexa([(0, 0, 0), (0, 0, W), (L, 0, W), (L, 0, 0),
                    (0, H - 60, 0), (0, H - 60, W), (L, H, W), (L, H, 0)], "#2e3033")
            for c in (W * 0.2, W * 0.5, W * 0.8):
                m.box(L - 2, L, H - 110, H - 60, c - 60, c + 60, "#1c1c1c")     # vents
        else:                          # the steering wheel on its column
            c, r = (W / 2, H / 2), min(W, H) / 2 - 10
            for k in range(28):
                a0, a1 = 2 * math.pi * k / 28, 2 * math.pi * (k + 1) / 28
                za, ya = c[1] + r * math.sin(a0), c[0] + r * math.cos(a0)
                zb, yb = c[1] + r * math.sin(a1), c[0] + r * math.cos(a1)
                m.box(L - 30, L - 5, min(za, zb) - 12, max(za, zb) + 12,
                      min(ya, yb) - 12, max(ya, yb) + 12, "#1c1c1c")
            m.box(L - 30, L - 5, c[1] - 12, c[1] + 12, c[0] - r, c[0] + r, "#1c1c1c")
            m.cylinder(c[1], c[0], 0, L - 30, 25, colour="#2e3033", axis="x")    # column
        return m
    elif kind in ("litter", "litterlid"):
        return slab(L, W, H, colour="#8fa3b0" if kind == "litter" else "#c9d3da")
    elif kind == "wheel":
        m = Mesh()
        cz, r = H / 2, min(L, H) / 2
        m.cylinder(L / 2, cz, 0, W, r, colour="#232325", axis="z", seg=48)       # tyre
        rim_z = (0, 25) if front_plus_z else (W - 25, W)
        m.cylinder(L / 2, cz, rim_z[0] - 1, rim_z[1] + 1, r * 0.6, colour="#b9bcc0", axis="z", seg=40)
        m.cylinder(L / 2, cz, rim_z[0] - 3, rim_z[1] + 3, r * 0.17, colour="#6d6f72", axis="z")
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
        out[key] = furniture_piece(kind, x1 - x0, y1 - y0, z1 - z0, (y0 + y1) / 2 < v["width"] / 2, n, b)
    return out


# --- the van body (v2-real): real positions, in millimetres -------------------------------
# glTF is y-up, so a model point (x, y, z) is written (x, z, y) - the viewer's own mapping.
def G(x, y, z):
    return (x, z, y)


SKIN_IN, SKIN_OUT, ARCH = "#e4e1da", "#f4f4f2", "#d9d5cc"
SILL = -250                       # the body's lower edge below the finished floor
CAVITY = 100                      # rib face to outer skin (model3d.BODY_CAVITY)
TYRE_CUT = 420                    # wheel-arch cut-out radius in the outer skin


def body_shell(variant="v2-real"):
    """Both side walls following the real lean (finished face inside, the skin CAVITY outside
    the ribs), their openings (slider, windows, hatches) with reveals, the wheel-arch cut-outs
    in the skin, the rounded wheel arches inside, and the rear frame round the open doors."""
    import model3d
    from plan import VARIANTS, wall_inset
    v = VARIANTS[variant]
    sp, body = model3d.spec(v), v["body"]
    L, W, H, WALL = v["length"], v["width"], v["height"], model3d.WALL
    fin = lambda z: wall_inset(v, max(0, min(z, H)))
    bare = lambda z: wall_inset(v, max(0, min(z, H)), bare=True)
    clamp = lambda a: min(a, L - 50)
    w0, w1, wd = v["well"]
    wheel_x = (w0 + w1) / 2
    m = Mesh()
    zs_prof = [z for z, _ in body["profile"] if 0 < z < H]
    for side in ("p", "d"):
        sgn = 1 if side == "p" else -1                        # +1: the inside is +y
        yin = lambda z: fin(z) if side == "p" else W - fin(z)
        yout = lambda z: (bare(z) - CAVITY) if side == "p" else W - bare(z) + CAVITY
        holes = [(sp_x0, clamp(sp_x1), 0, body["slider_h"]) for sp_x0, sp_x1 in [v["slider"]]] \
            if side == "p" else []
        holes += [(clamp(x0), clamp(x1), z0, z1)
                  for s_, x0, x1, z0, z1 in list(sp["windows"]) + list(sp["hatches"]) if s_ == side]
        top = H + WALL
        rows = [(SILL + 25 * k, SILL + 25 * (k + 1)) for k in range(-SILL // 25)]
        zz = sorted({0, top} | set(zs_prof) | {z for h in holes for z in h[2:] if 0 < z < top})
        rows += list(zip(zz, zz[1:]))
        for za, zb in rows:
            zm = (za + zb) / 2
            xs = {0, L}
            cut = None
            if zb <= 0 and abs(zm + 244) < TYRE_CUT:          # the rear wheel's cut-out
                dx = (TYRE_CUT ** 2 - (zm + 244) ** 2) ** 0.5
                cut = (wheel_x - dx, wheel_x + dx)
                xs |= set(cut)
            live = [h for h in holes if h[2] <= za and zb <= h[3]]
            for h in live:
                xs |= {h[0], h[1]}
            xs = sorted(xs)
            for xa, xb in zip(xs, xs[1:]):
                xm = (xa + xb) / 2
                if cut and cut[0] < xm < cut[1]:
                    continue
                if any(h[0] < xm < h[1] for h in live):
                    continue
                if zb > 0:                                    # the inner, finished face
                    m.quad([G(xa, yin(za), za), G(xb, yin(za), za), G(xb, yin(zb), zb),
                            G(xa, yin(zb), zb)], SKIN_IN, out=G(0, sgn, 0))
                m.quad([G(xa, yout(za), za), G(xb, yout(za), za), G(xb, yout(zb), zb),
                        G(xa, yout(zb), zb)], SKIN_OUT, out=G(0, -sgn, 0))
        # reveals round each opening: the wall's thickness, skin to finished face
        for x0, x1, z0, z1 in holes:
            for z in (z0, z1):
                if z > 0:
                    m.quad([G(x0, yin(z), z), G(x1, yin(z), z), G(x1, yout(z), z),
                            G(x0, yout(z), z)], SKIN_OUT, out=G(0, 0, 1 if z == z0 else -1))
            for x in (x0, x1):
                for za, zb in zip(zz, zz[1:]):
                    if z0 <= za and zb <= z1:
                        m.quad([G(x, yin(za), za), G(x, yout(za), za), G(x, yout(zb), zb),
                                G(x, yin(zb), zb)], SKIN_OUT, out=G(1 if x == x0 else -1, 0, 0))
        # the wall's lower edge and the top edge under the roof
        m.quad([G(0, yin(0), SILL), G(L, yin(0), SILL), G(L, yout(0), SILL), G(0, yout(0), SILL)],
               SKIN_OUT, out=G(0, 0, -1))
        # the wheel arch inside: flat top, rounded ends (a squared ellipse), up to arch_h
        ya, yb = (fin(0), wd) if side == "p" else (W - wd, W - fin(0))
        face = wd if side == "p" else W - wd
        n, half, h = 32, (w1 - w0) / 2, body["arch_h"]
        prof = []
        for k in range(n + 1):
            x = w0 + (w1 - w0) * k / n
            u = min(1.0, abs(x - (w0 + half)) / half)
            prof.append((x, h * (1 - u ** 4) ** 0.25))
        for (xa, za), (xb, zb) in zip(prof, prof[1:]):
            m.quad([G(xa, ya, za), G(xb, ya, zb), G(xb, yb, zb), G(xa, yb, za)], ARCH, out=G(0, 0, 1))
        m.polygon([(w0, 0)] + prof[1:-1] + [(w1, 0)], "z", face, ARCH, out=G(0, sgn, 0))
    # the rear frame round the open doors, and the bumper and lights
    ri, rh = model3d.REAR_DOORS[0], body["rear_h"]
    zz = sorted({SILL, 0, rh, H + WALL} | set(zs_prof))
    for za, zb in zip(zz, zz[1:]):
        ia, ib = max(fin(za), 0), max(fin(zb), 0)
        oa, ob = bare(za) - CAVITY, bare(zb) - CAVITY
        if zb <= rh:
            strips = [((oa, ob), (ri, ri)), ((W - ri, W - ri), (W - oa, W - ob))]
        else:
            strips = [((oa, ob), (W - oa, W - ob))]
        for (y0a, y0b), (y1a, y1b) in strips:
            for x, out in ((L + WALL, 1), (L, -1)):
                m.quad([G(x, y0a, za), G(x, y1a, za), G(x, y1b, zb), G(x, y0b, zb)],
                       SKIN_OUT if out > 0 else SKIN_IN, out=G(out, 0, 0))
    x0, x1 = L, L + 226
    m.box(x0, x1, -380, -150, -60, W + 60, "#3a3a3a")          # rear bumper (glTF: y is up)
    for y0 in (bare(900) - CAVITY + 5, W - bare(900) + CAVITY - 75):
        m.box(L + WALL, L + WALL + 6, 700, 1250, y0, y0 + 70, "#b3262e")   # tall rear lights
    return m


def body_roof(variant="v2-real"):
    """The roof panel, with the two fan cut-outs, from skin to skin across the top."""
    import model3d
    from plan import VARIANTS, wall_inset
    v = VARIANTS[variant]
    sp = model3d.spec(v)
    L, W, H, WALL = v["length"], v["width"], v["height"], model3d.WALL
    y0, y1 = wall_inset(v, H, bare=True) - CAVITY, W - wall_inset(v, H, bare=True) + CAVITY
    fans = sp["fans"]
    xs = sorted({0, L + WALL} | {f[0] for f in fans} | {f[1] for f in fans})
    ys = sorted({y0, y1} | {f[2] for f in fans} | {f[3] for f in fans})
    m = Mesh()
    for xa, xb in zip(xs, xs[1:]):
        for ya, yb in zip(ys, ys[1:]):
            xm, ym = (xa + xb) / 2, (ya + yb) / 2
            if any(f[0] < xm < f[1] and f[2] < ym < f[3] for f in fans):
                continue
            m.quad([G(xa, ya, H + WALL), G(xb, ya, H + WALL), G(xb, yb, H + WALL),
                    G(xa, yb, H + WALL)], SKIN_OUT, out=G(0, 0, 1))
            m.quad([G(xa, ya, H), G(xb, ya, H), G(xb, yb, H), G(xa, yb, H)], SKIN_IN,
                   out=G(0, 0, -1))
    for f in fans:                                              # the cut-out's reveal
        for (xa, ya), (xb, yb) in (((f[0], f[2]), (f[1], f[2])), ((f[1], f[2]), (f[1], f[3])),
                                   ((f[1], f[3]), (f[0], f[3])), ((f[0], f[3]), (f[0], f[2]))):
            m.quad([G(xa, ya, H), G(xb, yb, H), G(xb, yb, H + WALL), G(xa, ya, H + WALL)], SKIN_OUT)
    return m


def body_cab(variant="v2-real"):
    """The Crafter's nose, from the partition to the bumper: its side profile (roof over the
    cab, windscreen, bonnet, grille, bumper, the front wheel's arch) extruded across the van,
    open door windows, a see-through windscreen, lights, grille, mirrors."""
    import model3d
    from plan import VARIANTS
    v = VARIANTS[variant]
    sp = model3d.spec(v)
    W, H, WALL = v["width"], v["height"], model3d.WALL
    nose, fa = sp["nose"], sp["front_axle"]
    top = H + WALL
    wy0, wy1 = -80, W + 80                                      # the cab's outer skin
    ws_top, ws_base = (-1080, 1420), (-1600, 880)
    front = [(0, top), (-850, top), (-1000, top - 100), ws_top, ws_base,
             (-2230, 700), (-2330, 600), (-nose, 350), (-nose, -380)]
    arch = []
    for k in range(25):                                         # the front wheel's arch
        a = math.pi * k / 24
        arch.append((fa - TYRE_CUT * math.cos(a), -244 + TYRE_CUT * math.sin(a)))
    arch = [(x, max(z, SILL)) for x, z in arch]
    lower = front + [(fa - TYRE_CUT - 30, -380)] + arch + [(0, SILL)]
    m = Mesh()
    belt = 1000
    below = [(x, min(z, belt)) for x, z in lower]
    ws_at_belt = ws_base[0] + (belt - ws_base[1]) * (ws_top[0] - ws_base[0]) / (ws_top[1] - ws_base[1])
    lower_pts = [(0, belt), (ws_at_belt, belt), ws_base, (-2230, 700), (-2330, 600), (-nose, 350),
                 (-nose, -380), (fa - TYRE_CUT - 30, -380)] + arch + [(0, SILL)]
    for y, out in ((wy0, -1), (wy1, 1)):
        m.polygon(lower_pts, "z", y, SKIN_OUT, out=G(0, out, 0))
        # above the belt: B-pillar, the roof edge, the A-pillar along the windscreen
        m.polygon([(0, belt), (0, top), (-150, top), (-150, belt)], "z", y, SKIN_OUT, out=G(0, out, 0))
        m.polygon([(-150, 1380), (-150, top), (-850, top), (-1000, top - 100), ws_top,
                   (-1000, 1380)], "z", y, SKIN_OUT, out=G(0, out, 0))
        m.polygon([ws_top, (ws_at_belt, belt), (ws_at_belt + 110, belt), (ws_top[0] + 90, ws_top[1] - 30)],
                  "z", y, SKIN_OUT, out=G(0, out, 0))
        # door handle and mirror
        m.box(-420, -300, 820, 845, y - 6 if out < 0 else y, y if out < 0 else y + 6, "#2b2b2b")
        my = (y - 260, y) if out < 0 else (y, y + 260)
        m.box(-1320, -1240, 1030, 1300, my[0], my[1], "#2b2b2b")
    # across the front: roof front, windscreen (glass), bonnet, grille face, bumper face
    for (xa, za), (xb, zb) in zip(front, front[1:]):
        col = "#8fb3c766" if (xa, za) == ws_top else SKIN_OUT
        m.quad([G(xa, wy0, za), G(xb, wy0, zb), G(xb, wy1, zb), G(xa, wy1, za)], col,
               out=G(-1, 0, 1))
    m.box(-nose - 20, -2200, -380, -150, wy0 + 20, wy1 - 20, "#3a3a3a")          # bumper
    m.box(-nose - 4, -nose, 380, 560, 420, W - 420, "#2b2b2b")                  # grille
    for y0 in (40, W - 360):                                                    # headlights
        m.box(-2336, -2300, 440, 560, y0, y0 + 320, "#e8eef2")
    return m


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
    for part, make in (("shell", body_shell), ("roof", body_roof), ("cab", body_cab)):
        path = os.path.join(OUT, "v2-real-body-%s.glb" % part)
        make().glb(path)
        print("wrote", path, "%.1f kB" % (os.path.getsize(path) / 1000))


if __name__ == "__main__":
    main()
