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

    def cylinder(self, cx, cz, y0, y1, r0, r1=None, colour="#888", seg=32, caps=True):
        """Upright (along y) cylinder or cone frustum, radius r0 at y0 and r1 at y1."""
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


SOLIDS = {"solar": solar, "fan": maxxfan, "gasbottle": gas_bottle,
          "battery-ective": battery, "inverter-multiplusc": multiplus_c, "starlink": starlink_mini}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, make in SOLIDS.items():
        path = os.path.join(OUT, name + ".glb")
        make().glb(path)
        print("wrote", path, "%.1f kB" % (os.path.getsize(path) / 1000))


if __name__ == "__main__":
    main()
