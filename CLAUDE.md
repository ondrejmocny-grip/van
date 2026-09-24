# Campervan Project

Ondrej and his wife are building a campervan. This repo holds the planning work:
layout schemas, possibly 3D visualizations of them.

## Folders

- `ref/` — collected references (photos, links, specs, PDFs, inspiration).
- `doc/` — ongoing project documentation. Keep it updated as the project moves.

## Rules

- New reference material goes in `ref/`.
- When something is decided or changes, update the relevant file in `doc/`.
- **No pull requests here.** Work on a branch, then merge it straight into `main` and push.

## Drawing layouts

Everything is generated from one list of boxes in millimetres, so the plan, the elevations,
the 3D model and the renders can never disagree. `plan.py` holds that list per variant;
`model3d.py` extrudes it and adds the vehicle body and the big appliances at real catalogue
sizes; `impressions.py` turns it into photoreal views. `model3d.check()` asserts every
appliance still fits before anything renders, so changing a size to a real product fails
loudly rather than quietly overlapping.

**Coordinates.** x = 0 at the front bulkhead, growing aft. y = 0 at the passenger wall,
growing toward the driver side. z = height above the finished floor. Drawn with the nose at
the left, which puts the driver side at the bottom.

Commands and setup are in [doc/README.md](doc/README.md#tooling). Change dimensions there,
never by hand-editing a `.png` or `.svg` — they are build output.

## Who this is for

See [doc/about-us.md](doc/about-us.md) — who we are, how we'll use the van, how we live.
Read it before proposing anything; it explains why this build is minimal on storage and
water but heavy on daily working comfort.

## Layout versions

Each design version lives in its own folder (`v1/`, `v2/`, ...) with its own README and
drawings. `plan.py` generates them all: `python plan.py <variant>`.

**v2-real** (2026-09-24) is v2 being turned into a buildable plan - on the real VW body, with
the agreed wall build-up. It has its own tables and a `body=` in `plan.py`; its body check is
strict. **v2 is frozen**: edit v2-real, never v2.

**v1, v2 and v3 are all a VW Crafter L3H3.** v1 was drawn on a Ford Transit first; the Transit
was dropped on 2026-09-20 and its folder no longer exists.

Each version also brings its own 3D tables — `REGISTRY` in `model3d.py` says which variant
gets which fit-out. A variant not listed there borrows v1's, remapped.

One published 3D viewer holds every version with a switch between them: `python model3d.py
viewer` writes it to the top-level `viewer.html`. Republish that one; the per-version
`vN/viewer.html` files are local copies.

## Prop meshes

`props.py` replaces the viewer's coloured boxes with generated low-poly meshes through FAL.
The box in `model3d.py` stays the authority — the viewer scales a mesh to fill its box, so a
generated shape can never quietly change a dimension.

Two things that cost a whole generation round each when we got them wrong:

- **The prompt must state the SHAPE, not only the object.** Single-view image-to-3D pulls
  everything toward average proportions. If *every* model misses the same prop, the prompt is
  at fault, not the models — put the proportions into words ("twice as long as it is wide").
- **Let the shape error pick the preview, not the eye.** Four previews of one battery gave
  meshes scoring 0.03 to 0.29, and which photo was right was not visible in the photos.

The rest of the traps are in [doc/README.md](doc/README.md#tooling).

## Working with Ondrej on this

- **He cannot see images rendered in a reply — always give a file path.** Build a contact
  sheet so it is one file to open rather than five (`props.py sheet` / `shots` do this).
- When generating props he chooses at each stage: several 2D previews, then several meshes.
  Recommend one with reasons, then wait. `props.py auto` is for when he says to skip that.
- Plain English, structured over prose. He is not a native speaker.

## Setup

`pip install -r requirements.txt`. Image generation needs FAL credentials: `fal auth login`
locally, or `FAL_KEY` in the environment on the web and in containers. Details in
[doc/README.md](doc/README.md#setup).

`props/*/` is gitignored — 700 MB of previews and rejected meshes, all regenerable. The
adopted `props/<kind>.glb` files and `props/yaw.json` are committed, and are all the viewer
build needs.
