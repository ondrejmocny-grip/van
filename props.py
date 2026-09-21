#!/usr/bin/env python3
"""Low-poly prop meshes for the 3D viewer, generated one appliance at a time.

The viewer draws every appliance as a coloured box. That says where a thing is but not what
it is. This builds an optional layer of real-looking meshes on top, in four stages:

    python props.py preview cassette          # 2D catalogue shots, one per image model
    python props.py sheet cassette            # all of them in one image, to choose from
    python props.py mesh cassette recraft2    # the chosen shot -> meshes, one per 3D model
    python props.py shots cassette            # three views of each mesh, to choose from
    python props.py pick cassette trellis     # adopt one -> props/cassette.glb
    python props.py auto oven hob fridge      # all of the above, best-scoring adopted
    python props.py align                     # turn each prop to match its box
    python props.py face SHOWER -y            # turn its opening toward the aisle

Nothing here is the source of truth. The box in model3d.APPLIANCES stays authoritative: the
viewer scales the mesh to exactly fill its box, so a generated shape can never quietly change
a dimension. The dimension check below is therefore about SHAPE - has the generated thing the
proportions of the real product - not about absolute size, which we impose.

Needs `fal auth login` once, same as impressions.py.
"""
import base64, os, sys

import model3d

OUT = "props"
FACES = 4000            # low poly on purpose - this layer is for reading the layout

# What to draw. The box comes from model3d, so these are only the words.
PROMPTS = {
    "cassette": ("A Thetford C223-CS cassette toilet for a campervan: a compact white plastic "
                 "toilet with a rounded oval seat and closed lid, a grey flush button on the "
                 "upper right, a swivel bowl, standing on the floor as a single free-standing "
                 "unit."),
    # the box is bowl plus tap, 400 x 340 x 450 - the bowl hangs under the counter and the
    # tap stands 300 above it, so the whole thing is a little taller than it is wide
    "sink": ("A rectangular stainless steel inset kitchen sink with its mixer tap: a single "
             "shallow pressed bowl with rounded corners and a narrow flat rim, and a tall "
             "slender chrome mixer tap rising from the rim behind the bowl, its spout curving "
             "forward over the bowl, one lever handle on the tap body, all one assembly in "
             "brushed steel and chrome."),
    # a 15 mm sheet of glass has no geometry to speak of, so the prompt asks for the parts
    # that do stand proud: recessed wells, a raised control strip, knobs
    "hob": ("A two-zone domino induction hob, photographed on its own: a black glass rectangle "
            "twice as long as it is deep, its two cooking zones formed as shallow circular "
            "wells recessed into the glass with raised chrome trim rings around them, a raised "
            "control strip along the front edge carrying two round rotary knobs that stand "
            "proud of the surface, a slim brushed steel frame around the whole plate, and a "
            "shallow body beneath it."),
    "fridge": ("A 70 litre stainless steel campervan drawer fridge unit seen on its own: a "
               "single deep pull-out drawer in a rectangular cabinet, a long horizontal "
               "brushed steel handle across the drawer front, the body slightly wider than it "
               "is deep and a little lower than it is wide, vent slots low on the front."),
    "oven": ("A small 20 litre built-in electric mini oven: a stainless steel box with a glass "
             "front door, a chrome handle across the top of the door, and two round control "
             "knobs on the right."),
    # 600 x 620 x 310: nearly square in plan and only half as tall, which none of the models
    # draw unless the proportions are spelt out in words
    "fresh": ("A wide flat rectangular white food-grade plastic water tank for a campervan: a "
              "low slab of a tank, as wide across as it is deep front to back and only half "
              "that again in height, moulded in one piece with rounded corners and flat top "
              "and bottom faces, a screw filler cap on the top and a threaded outlet fitting "
              "low on one end, lying flat on the ground."),
    "battery": ("A LiFePO4 leisure battery: a black rectangular plastic case with a printed "
                "label panel on the front and two round brass terminals on the top face."),
    "inverter": ("A pure sine wave power inverter: a grey aluminium finned box with a cooling "
                 "fan grille on one end, two mains sockets and an LED display on the front."),
    "calorifier": ("A small marine calorifier hot water cylinder: a white cylindrical insulated "
                   "tank lying horizontally on two moulded feet, with copper pipe stubs at one "
                   "end."),
    "electrics": ("A wall-mounted 12 volt electrical panel: a flat board carrying a blue solar "
                  "charge controller, a black DC-DC charger, a row of red and black busbars and "
                  "a bank of blade fuses."),
    "plumbing": ("A campervan water pump assembly: a small grey diaphragm pump on a bracket "
                 "with a clear inline filter bowl and short lengths of white hose."),
    # furniture. Proportions go into the words - see doc/README.md for why
    # every model read "rounded corners" as a rounded-square tray, so the outline is now
    # spelt out: straight edges, square corners, a true rectangle
    "table": ("A rectangular campervan table top seen on its own: a flat slab of pale birch "
              "plywood whose outline is a true rectangle, four dead straight edges meeting at "
              "sharp square corners, a thin dark edge band running round the perimeter, the "
              "top face perfectly flat, only a finger thick, lying flat."),
    "leg": ("A single campervan table post standing upright on its own: a slim brushed "
            "aluminium tube rising from a small round floor flange, with a matching flat "
            "mounting plate on the top of the tube, the whole post about three times taller "
            "than the flange is wide."),
    "bed": ("One rectangular foam seat cushion on its own: a flat slab of upholstered sage "
            "green fabric with piped seams around the edge and softly rounded corners, wide "
            "and shallow, half again as long as it is deep and fifteen times longer than it "
            "is thick, lying flat."),
    "locker": ("A campervan overhead wall locker: a long shallow rectangular cabinet with two "
               "matte off-white hinged doors side by side, slim brushed brass bar handles, a "
               "birch plywood carcass, much longer than it is tall and shallower than it is "
               "tall, seen from the front and slightly below."),
    "shower": ("A shower head on a riser rail: a round chrome handheld shower head clipped to "
               "a slim vertical wall rail, a flexible hose hanging from it, the whole fitting "
               "tall and narrow, mounted flat against a white wall panel."),
    # v2's fridge is not v1's drawer: Brisa's 65 L unit has a hinged door, and the door is
    # the whole point of the prop - a closed cube reads as a cupboard. Ajar, not wide open:
    # the viewer stretches the mesh to fill the box, so a door swung through ninety degrees
    # would squash the cabinet itself to half its width.
    "fridgedoor": ("A 65 litre campervan compressor refrigerator standing on its own with its "
                   "door AJAR: a boxy stainless steel cabinet as wide as it is deep and only "
                   "a little taller than it is wide, one full-height door hinged on the left "
                   "and open a hand's width, just far enough to show the white moulded "
                   "interior and one wire shelf behind it, a slim vertical bar handle down the "
                   "opening edge of the door, a narrow vent grille along the bottom."),
    # 450 x 600 x 450: a cube a third deeper than it is wide, and no taller than it is wide -
    # every model draws a chair unless the words rule one out
    "SEAT": ("A campervan seat box with storage inside, seen on its own: a low plywood cube, "
             "no taller than it is wide and a third deeper than it is wide, with a thin flat "
             "upholstered sage green cushion lying on its top face, a hinged front door with "
             "a small round recessed finger pull, a birch plywood carcass with visible ply "
             "edges, standing on the floor. No backrest, no legs, no armrests."),
    # 700 x 800 x 1881: two and a half times taller than it is wide, and the open side is the
    # point - a sealed white box tells you nothing about the room it stands in
    # first round came back a pentagonal corner pod - angled panels, chamfered front. In a
    # 700 x 800 rectangular hole that reads as a tent, so the plan shape is now spelt out as
    # hard as the proportions: square corners, right angles, three flat rectangles
    "SHOWER": ("A campervan shower cubicle seen on its own, with NO door and NO curtain: "
               "exactly three flat white rectangular wall panels meeting at SQUARE ninety "
               "degree corners, forming a tall box-shaped enclosure with a strictly "
               "rectangular floor plan, two and a half times taller than it is wide. No "
               "angled panels, no chamfered or cut-off corners, no curved front, no "
               "pentagon. The fourth side stands completely open, floor to ceiling, so the "
               "inside is visible right through. A shallow white rectangular shower tray at "
               "the bottom with a chrome drain grate, a slim chrome riser rail with a "
               "handheld shower head on the back panel, open at the top. An empty "
               "three-walled rectangular shower enclosure, straight edges throughout."),
    # 450 x 600 x 1881: four times taller than it is wide. The lower bay is left EMPTY on
    # purpose - the cassette is its own prop and sits inside this one in the viewer
    "WARDROBE": ("A tall narrow campervan wardrobe cabinet seen on its own: four times taller "
                 "than it is wide and a third deeper than it is wide, birch plywood. The upper "
                 "two thirds is a hanging wardrobe closed by a clear glass door in a slim "
                 "frame, with three shirts on a rail visible through the glass. The lower "
                 "third is a separate empty compartment standing wide open at the front, its "
                 "flat plywood floor and side panels visible, nothing inside it. A horizontal "
                 "plywood shelf divides the two."),
    "grey": ("A flat underslung waste water tank: a wide shallow black plastic box with rounded "
             "corners, moulded mounting lugs and a drain valve on one end."),
}

STYLE = (" Studio product photograph on a plain white seamless background, the whole object "
         "centred and fully in frame, three-quarter view from slightly above, even soft "
         "lighting, sharp focus, matte finish, clean e-commerce catalogue image.")

# Text to image. Args differ per model, so each carries its own extras. recraft's plain
# "realistic_image" style is the one that keeps the background empty; studio_portrait invents
# a coloured backdrop and a pot plant, which would then be baked into the mesh.
IMAGE_MODELS = [
    ("flux",    "fal-ai/flux/dev",      {"image_size": "square_hd", "num_images": 1}),
    ("fluxpro", "fal-ai/flux-pro/v1.1", {"image_size": "square_hd", "num_images": 1}),
    ("recraft", "fal-ai/recraft-v3",    {"image_size": "square_hd", "style": "realistic_image"}),
    ("qwen",    "fal-ai/qwen-image",    {"image_size": "square_hd", "num_images": 1}),
]

# Image to 3D. Same deal - the input field is not spelt the same way twice.
MESH_MODELS = [
    ("trellis", "fal-ai/trellis",            "image_url",       {}),
    ("hunyuan", "fal-ai/hunyuan3d/v2/turbo", "input_image_url", {}),
    ("rodin",   "fal-ai/hyper3d/rodin",      "input_image_urls",
                {"geometry_file_format": "glb", "tier": "Regular"}),
]

# These two accept a job and then never finish it: six attempts across two props, the last two
# with a 40 minute budget, and exactly one delivered a url - which then died on a DNS blip.
# Left here because they may come back, but out of the default set so they cannot hold up a
# run. Name one explicitly and it still goes: `props.py mesh sink flux tripo`.
SLOW = [
    ("triposr", "fal-ai/triposr",                        "image_url", {}),
    ("tripo",   "tripo3d/tripo/v2.5/image-to-3d",        "image_url", {}),
]


def every_box():
    """Every box of every variant. Kinds live in three places - the plan (a shower cubicle is
    a plan box), EXTRA (lockers, tables) and APPLIANCES - and each layout version carries its
    own tables, so a v2-only kind is invisible if you only look at v1."""
    out = []
    for name in model3d.REGISTRY:
        out += model3d.boxes_for(model3d.VARIANTS[name])
    return out


def box_of(kind):
    """The authoritative box for a kind, as (dx, dy, dz) in mm, from model3d. Furniture counts
    too: tables, lockers, bed cushions, the shower cubicle. The viewer draws them all as boxes
    and they get meshes the same way.

    A kind can own several boxes of different sizes - three lockers, two tables. The largest
    is the one to aim at, because the viewer fits each mesh into its own box and a mesh made
    for the big one still reads correctly when shrunk into a small one."""
    boxes = [b for b in every_box() if b[6] == kind]
    if not boxes:
        raise SystemExit("no box for %r - kinds: %s" % (kind, ", ".join(sorted(
            {b[6] for b in every_box()}))))
    b = max(boxes, key=lambda b: (b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4]))
    return (b[1] - b[0], b[3] - b[2], b[5] - b[4])


SUBMIT = __import__("threading").Lock()     # fal caches its token in a file, and parallel
                                            # submits race each other writing it


def run(model, args, tries=2, budget=2400):
    """Submit to fal's queue and poll it ourselves. fal.apps.run() waits on a single HTTP read,
    and the slower image-to-3D endpoints hold the connection until it times out or the far end
    drops it - which is what triposr and tripo did every time before this."""
    import time
    import fal.apps
    for attempt in range(1, tries + 1):
        try:
            with SUBMIT:
                handle = fal.apps.submit(model, args)
            end = time.time() + budget
            while time.time() < end:
                try:
                    if isinstance(handle.status(), fal.apps.Completed):
                        return handle.fetch_result()
                except Exception:
                    pass                            # a dropped poll is not a dropped job
                time.sleep(5)
            raise TimeoutError("%s still running after %d s" % (model, budget))
        except Exception:
            if attempt == tries:
                raise
            time.sleep(3)

def grab(url, path, tries=4):
    """Retry the download. The job itself can take forty minutes, and losing that to one DNS
    blip on a laptop that went to sleep is not acceptable."""
    import time
    import urllib.request
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for attempt in range(1, tries + 1):
        try:
            urllib.request.urlretrieve(url, path)
            return path
        except Exception:
            if attempt == tries:
                raise
            time.sleep(10)


def find_url(obj, exts):
    """First url in a response that looks like one of exts. Every model names it differently."""
    if isinstance(obj, dict):
        for v in obj.values():
            u = find_url(v, exts)
            if u:
                return u
    elif isinstance(obj, list):
        for v in obj:
            u = find_url(v, exts)
            if u:
                return u
    elif isinstance(obj, str) and obj.startswith("http"):
        if any(obj.split("?")[0].lower().endswith(e) for e in exts):
            return obj
    return None


def preview(kind, only=()):
    """One catalogue shot per image model. They disagree about what the product even is, which
    is the whole reason for generating several."""
    import concurrent.futures as cf
    box_of(kind)                                    # fail early if the kind is unknown
    prompt = PROMPTS[kind] + STYLE

    def one(spec):
        tag, model, extra = spec
        try:
            r = run(model, dict(extra, prompt=prompt))
        except Exception as e:
            return "  %-9s FAIL %s %s" % (tag, type(e).__name__, str(e)[:110])
        url = find_url(r, (".png", ".jpg", ".jpeg", ".webp"))
        if not url:
            return "  %-9s no image in response: %s" % (tag, str(r)[:120])
        return "  %-9s %s" % (tag, grab(url, os.path.join(OUT, kind, "preview", tag + ".png")))

    jobs = [m for m in IMAGE_MODELS if not only or m[0] in only]
    with cf.ThreadPoolExecutor(len(jobs)) as pool:
        for line in pool.map(one, jobs):
            print(line, flush=True)


def measure(path, want):
    """Bounding box of a generated mesh, as proportions. Absolute scale is meaningless - all of
    these models normalise to a unit cube - so compare shape only."""
    import trimesh
    m = trimesh.load(path, force="scene")
    e = sorted(m.bounding_box.extents, reverse=True)
    w = sorted(want, reverse=True)
    got = [x / e[0] for x in e]
    exp = [x / w[0] for x in w]
    return got, exp, max(abs(a - b) for a, b in zip(got, exp))


def mesh(kind, chosen, only=()):
    """Every 3D model gets the same picture. They run in parallel - each takes minutes, and one
    slow endpoint should not decide the wall clock for the whole set."""
    import concurrent.futures as cf
    from PIL import Image
    want = box_of(kind)
    src = os.path.join(OUT, kind, "preview", chosen + ".png")
    if not os.path.exists(src):
        raise SystemExit("no preview at " + src)
    # fal hands back jpeg or webp under whatever name we asked for, so sniff the real format -
    # a jpeg labelled image/png is rejected by some of the 3D endpoints
    mime = "image/" + Image.open(src).format.lower()
    durl = ("data:%s;base64," % mime) + base64.b64encode(open(src, "rb").read()).decode()
    print("from %s, target %d x %d x %d mm" % ((src,) + want), flush=True)

    def one(spec):
        tag, model, field, extra = spec
        args = dict(extra)
        args[field] = [durl] if field.endswith("urls") else durl
        try:
            r = run(model, args)
        except Exception as e:
            return "  %-9s FAIL %s %s" % (tag, type(e).__name__, str(e)[:110])
        url = find_url(r, (".glb", ".gltf", ".obj", ".ply"))
        if not url:
            return "  %-9s no mesh in response: %s" % (tag, str(r)[:140])
        path = grab(url, os.path.join(
            OUT, kind, "mesh", tag + os.path.splitext(url.split("?")[0])[1]))
        try:
            got, exp, err = measure(path, want)
            return "  %-9s %s  shape %s  want %s  err %.2f %s" % (
                tag, path, ["%.2f" % g for g in got], ["%.2f" % e for e in exp], err,
                "OK" if err < 0.18 else "OFF")
        except Exception as e:
            return "  %-9s %s  (could not measure: %s)" % (tag, path, e)

    jobs = ([m for m in MESH_MODELS + SLOW if m[0] in only] if only else list(MESH_MODELS))
    with cf.ThreadPoolExecutor(len(jobs)) as pool:
        for line in pool.map(one, jobs):
            print(line, flush=True)


def shot(path, out, want=None, views=((35, 25), (90, 0), (0, 89))):
    """Flat-shaded three-view of a generated mesh. trimesh can only save an image through an
    OpenGL context we do not have here, so this projects the triangles itself and lets
    matplotlib paint them back to front - the same painter's trick model3d uses for boxes."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import trimesh
    from matplotlib.collections import PolyCollection

    m = trimesh.load(path, force="mesh")
    V, F = np.asarray(m.vertices, float), np.asarray(m.faces, int)
    if path.lower().endswith((".glb", ".gltf")):
        V = V[:, [0, 2, 1]]                          # glTF is Y-up, this renderer is Z-up
    V = V - V.mean(axis=0)
    V = V / (np.abs(V).max() or 1)
    fig, axes = plt.subplots(1, len(views), figsize=(3.6 * len(views), 3.9))
    for ax, (az, el) in zip(axes, views):
        a, e = np.radians(az), np.radians(el)
        fwd = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        right = np.cross(fwd, [0, 0, 1.0])
        right = right / (np.linalg.norm(right) or 1)
        P = np.stack([V @ right, V @ np.cross(right, fwd), V @ -fwd], axis=1)
        tri = P[F]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        ln = np.linalg.norm(n, axis=1)
        lit = 0.35 + 0.6 * np.abs(n[:, 2] / np.where(ln == 0, 1, ln))
        order = np.argsort(tri[:, :, 2].mean(axis=1))
        ax.add_collection(PolyCollection(
            tri[order][:, :, :2], facecolors=np.repeat(lit[order][:, None], 3, axis=1),
            edgecolors="none"))
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")
    ext = m.bounding_box.extents
    title = "%s   bbox %.2f x %.2f x %.2f" % ((os.path.basename(path),) + tuple(ext / ext.max()))
    if want:
        w = np.array(sorted(want, reverse=True), float)
        title += "   want %.2f x %.2f x %.2f" % tuple(w / w[0])
    fig.suptitle(title, fontsize=11)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=105, facecolor="white")
    plt.close(fig)
    return out


def shots(kind):
    want = box_of(kind)
    d = os.path.join(OUT, kind, "mesh")
    for f in sorted(os.listdir(d)):
        if f.lower().endswith((".glb", ".gltf", ".obj", ".ply")):
            print("wrote", shot(os.path.join(d, f), os.path.join(
                OUT, kind, "shots", os.path.splitext(f)[0] + ".png"), want))
    sheet(kind, "shots")


def sheet(kind, sub="preview"):
    """One labelled contact sheet of everything generated for a kind, so it can be compared in
    a single image rather than by opening files one at a time."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    d = os.path.join(OUT, kind, sub)
    files = sorted(f for f in os.listdir(d) if f.lower().endswith((".png", ".jpg")))
    if not files:
        raise SystemExit("nothing in " + d)
    tall = sub == "shots"                            # three-views are wide, stack them instead
    fig, axes = (plt.subplots(len(files), 1, figsize=(11, 4.1 * len(files))) if tall
                 else plt.subplots(1, len(files), figsize=(4 * len(files), 4.4)))
    for ax, f in zip([axes] if len(files) == 1 else axes, files):
        ax.imshow(Image.open(os.path.join(d, f)).convert("RGB"))
        if not tall:
            ax.set_title(os.path.splitext(f)[0], fontsize=13)
        ax.axis("off")
    fig.tight_layout()
    out = os.path.join(OUT, kind, sub + "-sheet.png")
    fig.savefig(out, dpi=105, facecolor="white")
    plt.close(fig)
    print("wrote", out)


def pick(kind, tag):
    """Adopt one generated mesh as the prop the viewer loads: drop its texture, decimate it and
    centre it. The viewer scales whatever comes out to fill the box, so only the shape of this
    file matters, never its size."""
    import trimesh
    d = os.path.join(OUT, kind, "mesh")
    hits = [f for f in os.listdir(d) if os.path.splitext(f)[0] == tag]
    if not hits:
        raise SystemExit("no mesh tagged %r for %s" % (tag, kind))
    m = trimesh.load(os.path.join(d, hits[0]), force="mesh")
    m = trimesh.Trimesh(vertices=m.vertices, faces=m.faces)     # texture off - the colour comes
    if len(m.faces) > FACES:                                    # from the layout key instead
        m = m.simplify_quadric_decimation(face_count=FACES)
    m.apply_translation(-m.bounding_box.centroid)
    out = os.path.join(OUT, kind + ".glb")
    open(out, "wb").write(m.export(file_type="glb"))
    print("adopted %s from %s - %d faces, %d kB" % (
        out, hits[0], len(m.faces), os.path.getsize(out) // 1024))
    print("now run `python model3d.py <variant>` to rebuild the viewer with it")


def align(write=True):
    """Turn each prop so its long side runs the same way its box does.

    Run this when a mesh is newly adopted, not on every build: it owns the quarter turn and
    will happily undo a quarter turn asked for by hand. Anything set deliberately should be
    re-set afterwards.

    The viewer stretches a mesh to fill its box, so a mesh lying the wrong way round is not
    merely rotated - it is squashed along one axis and pulled along the other. glTF is Y-up,
    and the viewer maps mesh X to the van's length and mesh Z to its width, so the only
    question is whether the plan footprint wants a quarter turn. Facing - which way the doors
    or the tap point - is a separate judgement and stays whatever is already in yaw.json.
    """
    import json
    import trimesh
    path = os.path.join(OUT, "yaw.json")
    yaw = json.load(open(path)) if os.path.exists(path) else {}
    for name in sorted(os.listdir(OUT)):
        if not name.endswith(".glb"):
            continue
        kind = name[:-4]
        ext = trimesh.load(os.path.join(OUT, name), force="mesh").bounding_box.extents
        bx, by, _ = box_of(kind)
        mesh = ext[0] / (ext[2] or 1)               # mesh X vs mesh Z, both horizontal
        off = lambda r: max(mesh / r, r / mesh)     # how far off the footprint would be
        straight, turned = off(bx / by), off(by / bx)
        # only worth a turn if it actually takes distortion out - a near-square prop can face
        # either way and spinning it just churns the file
        turn = 90 if turned < straight * 0.95 else 0
        was = yaw.get(kind, 0)
        now = (was % 180) // 90 * 90                # the quarter turn already applied
        new = was - now + turn
        if new != was:
            print("  %-10s %d -> %d" % (kind, was, new))
            yaw[kind] = new
    if write:
        json.dump(dict(sorted(yaw.items())), open(path, "w"), indent=2)
        print("wrote", path)


def openness(path, band=0.18):
    """Which way a prop's open side points, in mesh coordinates.

    Surface area near each of the four vertical faces of the bounding box. A wall panel puts
    a lot of area against its own face; the open side has almost none. The answer is the
    outward direction of the emptiest face.

    The obvious measure - centroid against bounding-box centre - is wrong on exactly the
    props this matters for: the shower's tray sticks out through its opening, which drags
    the centroid the wrong way and turned the cubicle to face the wall.
    """
    import numpy as np
    import trimesh
    m = trimesh.load(path, force="mesh")
    lo, hi = m.bounds
    area, mid = m.area_faces, m.triangles_center
    out, best = None, None
    for axis, sign in ((0, 1), (0, -1), (2, 1), (2, -1)):
        span = hi[axis] - lo[axis]
        edge = hi[axis] if sign > 0 else lo[axis]
        near = np.abs(mid[:, axis] - edge) < band * span
        share = area[near].sum() / area.sum()
        if best is None or share < best:
            best = share
            out = (sign if axis == 0 else 0, sign if axis == 2 else 0, share)
    return out


def face(kind, want, write=True):
    """Turn a prop so its OPEN side points where the layout wants it.

        python props.py face WARDROBE -y     # the open front looks across the aisle

    `align` owns the quarter turn that matches the footprint; this owns the facing. They
    disagree whenever a prop's opening is on its long side, and then facing wins: a wardrobe
    30 mm too deep still reads as a wardrobe, one that opens into the wall does not.
    """
    import json
    import numpy as np
    ox, oz, share = openness(os.path.join(OUT, kind + ".glb"))
    targets = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}
    if want not in targets:
        raise SystemExit("face wants one of " + ", ".join(sorted(targets)))
    tx, ty = targets[want]
    best, score = 0, -2.0
    for deg in (0, 90, 180, 270):
        a = np.radians(deg)
        # three.js rotates about Y, and the viewer maps mesh X to the van's length and
        # mesh Z to its width
        vx = ox * np.cos(a) + oz * np.sin(a)
        vy = -ox * np.sin(a) + oz * np.cos(a)
        dot = vx * tx + vy * ty
        if dot > score:
            best, score = deg, dot
    path = os.path.join(OUT, "yaw.json")
    yaw = json.load(open(path)) if os.path.exists(path) else {}
    print("  %-11s open face %+d %+d holds %.0f%% of the area -> yaw %3d"
          % (kind, ox, oz, share * 100, best))
    yaw[kind] = best
    if write:
        json.dump(dict(sorted(yaw.items())), open(path, "w"), indent=2)
    return best


def auto(kinds, workers=12):
    """The whole pipeline for one or more kinds with nobody in the loop, adopting the best.

    Three stages, so the bill stays sane. Meshing every preview on every model would be three
    times the jobs to answer the same question:

        1. every kind on every image model
        2. every preview meshed once, on hunyuan       -> which preview reads as the right shape
        3. that preview on the remaining mesh models   -> which model builds it best

    The shape error picks, not the eye. That is not laziness: four previews of one battery
    produced meshes scoring 0.03 to 0.29, and which photo was right was not visible in the
    photos. Facing is a separate question - run `align`, then set any deliberate turn by hand.
    """
    import concurrent.futures as cf
    from PIL import Image
    first = [m for m in MESH_MODELS if m[0] == "hunyuan"] or MESH_MODELS[:1]
    rest = [m for m in MESH_MODELS if m not in first]

    def one_preview(job):
        kind, (tag, model, extra) = job
        try:
            r = run(model, dict(extra, prompt=PROMPTS[kind] + STYLE))
        except Exception as e:
            return (kind, None, "  %-11s %-8s FAIL %s" % (kind, tag, type(e).__name__))
        url = find_url(r, (".png", ".jpg", ".jpeg", ".webp"))
        if not url:
            return (kind, None, "  %-11s %-8s no image" % (kind, tag))
        grab(url, os.path.join(OUT, kind, "preview", tag + ".png"))
        return (kind, tag, "  %-11s %-8s ok" % (kind, tag))

    def one_mesh(job):
        kind, chosen, (tag, model, field, extra) = job
        src = os.path.join(OUT, kind, "preview", chosen + ".png")
        durl = ("data:image/%s;base64," % Image.open(src).format.lower()) + base64.b64encode(
            open(src, "rb").read()).decode()
        args = dict(extra)
        args[field] = [durl] if field.endswith("urls") else durl
        label = "%s/%s" % (chosen, tag)
        try:
            r = run(model, args)
        except Exception as e:
            return (kind, chosen, tag, None, "  %-11s %-18s FAIL %s" % (
                kind, label, type(e).__name__))
        url = find_url(r, (".glb", ".gltf", ".obj", ".ply"))
        if not url:
            return (kind, chosen, tag, None, "  %-11s %-18s no mesh" % (kind, label))
        # the preview has to be in the name too, or parallel jobs race over one path
        path = grab(url, os.path.join(OUT, kind, "mesh", "%s-%s%s" % (
            chosen, tag, os.path.splitext(url.split("?")[0])[1])))
        try:
            got, exp, err = measure(path, box_of(kind))
        except Exception as e:
            return (kind, chosen, tag, None, "  %-11s %-18s unreadable: %s" % (
                kind, label, str(e)[:40]))
        return (kind, chosen, tag, err, "  %-11s %-18s shape %s want %s err %.2f %s" % (
            kind, label, ["%.2f" % g for g in got], ["%.2f" % e for e in exp], err,
            "OK" if err < 0.18 else "OFF"))

    def fan(fn, jobs):
        out = []
        if not jobs:
            return out
        with cf.ThreadPoolExecutor(min(workers, len(jobs))) as pool:
            for row in pool.map(fn, jobs):
                print(row[-1], flush=True)
                out.append(row)
        return out

    for k in kinds:
        box_of(k)                                   # fail before spending anything
    print("== previews ==", flush=True)
    made = fan(one_preview, [(k, m) for k in kinds for m in IMAGE_MODELS])
    have = {k: [r[1] for r in made if r[0] == k and r[1]] for k in kinds}
    for k in kinds:
        sheet(k)

    print("== one mesh per preview ==", flush=True)
    rows = fan(one_mesh, [(k, c, m) for k in kinds for c in have[k] for m in first])
    best = {}
    for k in kinds:
        scored = [r for r in rows if r[0] == k and r[3] is not None]
        if scored:
            best[k] = min(scored, key=lambda r: r[3])
            print("  -> %s best preview: %s (%.2f)" % (k, best[k][1], best[k][3]), flush=True)

    print("== the winning preview on the other models ==", flush=True)
    rows += fan(one_mesh, [(k, best[k][1], m) for k in kinds if k in best for m in rest])

    print("== adopting ==", flush=True)
    for k in kinds:
        scored = [r for r in rows if r[0] == k and r[3] is not None]
        if not scored:
            print("  %-11s nothing usable" % k, flush=True)
            continue
        win = min(scored, key=lambda r: r[3])
        pick(k, "%s-%s" % (win[1], win[2]))
        shots(k)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "align":
        return align()
    if len(sys.argv) == 4 and sys.argv[1] == "face":
        return face(sys.argv[2], sys.argv[3])
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    cmd, kind, rest = sys.argv[1], sys.argv[2], tuple(sys.argv[3:])
    if cmd == "preview":
        preview(kind, rest)
    elif cmd == "mesh":
        if not rest:
            raise SystemExit("mesh needs the preview to use, e.g. `mesh cassette recraft2`")
        mesh(kind, rest[0], rest[1:])
    elif cmd == "auto":
        auto((kind,) + rest)
    elif cmd == "align":
        align()
    elif cmd == "shots":
        shots(kind)
    elif cmd == "sheet":
        sheet(kind, *rest)
    elif cmd == "pick":
        pick(kind, rest[0])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
