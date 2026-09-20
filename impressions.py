#!/usr/bin/env python3
"""Photoreal interior impressions, generated from our own 3D geometry.

Pipeline: model3d draws a flat shaded view from a camera placed by hand inside the van - real
body panels with their apertures cut, one colour per material - and that goes to FAL's
DEPTH-conditioned FLUX as the control image. Strength 0.75.

This replaced canny-on-a-line-drawing, which could not do both jobs at once: loose enough to
look photographic and it furnished the empty entry with sofas, tight enough to keep the layout
and it looked like a CAD render. Depth carries the volume of the room rather than just its
edges, so there is nothing left for the model to guess about what a blank area means. A true
depth map is worse than the shaded colour render - the bright near walls read as a doorway and
it frames the whole van inside one. The ladder of everything tried is in doc/README.md.

Cameras are eye and target points in millimetres, in plan coordinates. Two rules, both learnt
the hard way:

  * The eye has to be somewhere a person could actually stand or sit. Every camera used to be
    outside the van without anyone noticing, because matplotlib's 3D axes always parks its
    camera a fixed distance from the centre of the data. model3d.line_render now projects the
    geometry itself, so the eye goes exactly where we put it.
  * The prompt's left and right have to match what the control image shows. Work them out
    from the camera, not from the plan drawing - the plan is drawn nose-left, so its "top"
    is the driver side, and looking aft flips left and right again.

Needs `fal auth login` once. Uses fal.apps.run rather than the `fal api` CLI because the
CLI's key=value parser splits on the "=" padding inside a data URI.

    python impressions.py v1
"""
import base64, os, sys, time, urllib.request

import model3d
from plan import VARIANTS

MODEL = "fal-ai/flux-control-lora-depth"
STRENGTH = 0.75

STYLE = ("Real photograph shot on a full-frame camera with a wide lens, photorealistic, daylight "
         "through the side windows, soft real shadows. Warm minimal Scandinavian campervan interior: "
         "birch plywood walls, matte off-white cabinet doors, sage green fabric cushions, brushed "
         "brass handles, pale oak floor, white tiled shower cubicle. Real materials and real "
         "textures, magazine interior photography, unoccupied.")

# name, eye, target (both in mm, as functions of the van), horizontal FOV, show the cab,
# kinds to hide, and what the camera is looking at. Screen right is noted per shot - it is
# what the prompt's left and right must agree with.
SHOTS = [
    ("01-from-the-bed-looking-forward",
     lambda L, W, H: (L - 120, W * 0.50, 1120), lambda L, W, H: (0, W * 0.50, 800),
     80, True, (),
     # screen right = PASSENGER side. The sliding door is not in this shot and must not be
     # described: the wet cubicle stands between the bed and the door opening.
     "Interior of a campervan seen from the rear bed looking forward down its length. In the "
     "foreground the made-up bed, a mattress with folded bedding on it. On the left a galley "
     "counter with a sink and an induction hob under an overhead locker, a window above the "
     "counter. On the right the tall birch panel of a compact shower cubicle. Ahead the front "
     "lounge, the cab seats swivelled round to face a small table, windscreen beyond."),
    ("02-from-the-front-looking-aft",
     lambda L, W, H: (-850, W * 0.55, 1450), lambda L, W, H: (L * 0.9, W * 0.32, 600),
     94, False, ("table",),
     # screen right = DRIVER side. Standing height and a wide lens, aimed a little toward the
     # kerb: from a seated, centred eye the sliding door fell outside the frame and the model
     # filled the empty left foreground with a sofa. Tables are hidden here - the front Lagun
     # table sits right under this camera and the model grows a whole dinette around it.
     "Interior of a campervan looking toward the rear. On the right a galley counter with a "
     "sink and an induction hob, a window above it and an overhead locker. On the left an "
     "open sliding door with daylight pouring in across clear empty floor. Just beyond the "
     "doorway a compact white tiled shower cubicle. At the far end two low benches facing "
     "each other under a window, rear doors behind them."),
    ("03-through-the-sliding-door",
     lambda L, W, H: (950, -500, 1400), lambda L, W, H: (1150, W * 0.65, 700),
     92, False, (),
     # screen right = toward the NOSE
     "Looking into a campervan through its wide open sliding side door. Directly across from "
     "you, the galley counter with a sink and an induction hob, a window and an overhead "
     "locker above it. To the right the front lounge with a small swing-arm table and the "
     "swivelled cab seats. To the left the compact white shower cubicle, with the rear seating "
     "area beyond it."),
    ("04-over-the-dinette",
     lambda L, W, H: (L - 200, W * 0.85, 1600), lambda L, W, H: (2100, W * 0.35, 450),
     88, False, ("bed",),
     # three-quarter from the rear driver corner, looking down; bed not made up
     "Interior of a campervan, a three-quarter view down onto the rear dinette: benches with "
     "sage green cushions down both sides, a wooden table between them, an overhead locker "
     "and a window above one bench, the galley counter beyond it on the left and a compact "
     "white shower cubicle on the right."),
]

# Plan coordinates are left-handed, so mirroring the whole control image is a one-character
# mistake that is easy to miss and ruins every prompt's left and right. Assert the sides.
SIDE_CHECKS = [
    ("01-from-the-bed-looking-forward", "galley", lambda L, W, H: (1170, W * 0.84, 450), "left"),
    ("01-from-the-bed-looking-forward", "wet cubicle", lambda L, W, H: (1975, W * 0.19, 900), "right"),
    ("02-from-the-front-looking-aft", "galley", lambda L, W, H: (1170, W * 0.84, 450), "right"),
    ("02-from-the-front-looking-aft", "wet cubicle", lambda L, W, H: (1975, W * 0.19, 900), "left"),
]


def check_sides(v):
    L, W, H = v["length"], v["width"], v["height"]
    cams = {s[0]: (s[1], s[2]) for s in SHOTS}
    for shot, what, where, want in SIDE_CHECKS:
        eye, target = cams[shot]
        xy = model3d.screen_xy(eye(L, W, H), target(L, W, H), where(L, W, H))
        assert xy, "%s: %s is behind the camera" % (shot, what)
        got = "left" if xy[0] < 0 else "right"
        assert got == want, "%s: %s comes out on the %s, the prompt says %s" % (
            shot, what, got, want)
    print("sides ok - %d checks" % len(SIDE_CHECKS))


def run(args, tries=4):
    """fal's queue poll times out now and then; retry rather than lose the whole set."""
    import fal.apps
    for attempt in range(1, tries + 1):
        try:
            return fal.apps.run(MODEL, args)
        except Exception as e:
            if attempt == tries:
                raise
            print("   retry %d (%s)" % (attempt, type(e).__name__))
            time.sleep(3)


def main(name, only=()):
    v = VARIANTS[name]
    out = v["out"].rsplit("/", 1)[0] if "/" in v["out"] else "."
    img_dir = os.path.join(out, "impressions")
    ctl_dir = os.path.join(out, "3d", "control")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(ctl_dir, exist_ok=True)

    check_sides(v)
    L, W, H = v["length"], v["width"], v["height"]
    for shot, eye, target, hfov, cab, hide, subject in SHOTS:
        if only and not any(shot.startswith(o) for o in only):
            continue
        e, t = eye(L, W, H), target(L, W, H)
        drop = tuple(hide) + ((), ("seat", "dash", "cab"))[not cab]
        # the shaded render is the control; the line version is only for reading the layout
        ctl = model3d.shaded_render(v, e, t, os.path.join(ctl_dir, shot + ".png"),
                                    hfov=hfov, hide=drop)
        model3d.line_render(v, e, t, os.path.join(ctl_dir, shot + "-lines.png"),
                            hfov=hfov, cab=cab, hide=hide)
        durl = "data:image/png;base64," + base64.b64encode(open(ctl, "rb").read()).decode()
        try:
            r = run({"prompt": subject + " " + STYLE,
                     "control_lora_image_url": durl,
                     "control_lora_strength": STRENGTH,
                     "image_size": "landscape_4_3",
                     "num_images": 1})
        except Exception as e:
            print("FAIL", shot, type(e).__name__, str(e)[:160])
            continue
        path = os.path.join(img_dir, shot + ".jpg")
        urllib.request.urlretrieve(r["images"][0]["url"], path)
        print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v1", tuple(sys.argv[2:]))
