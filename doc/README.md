# Campervan — project doc

Started: 2026-09-17

## Status

Base vehicle chosen: **VW Crafter L3H3** (see below). Configuration settled.
**[v1](../v1/README.md)** is drawn - plan, elevations and sections.
**[v2](../v2/README.md)** is being drawn on a **Crafter L3H3 with a 3-seat cab** -
schema only so far.
**[v3](../v3/README.md)** turns v2 around: bed at the front on a slide-out platform,
bathroom and a full-height closet at the back. Plan only, no 3D yet.
**[v4](../v4/README.md)** puts the bed back in the middle, fixed and never converted, over a
full-width garage, with a 500 mm bathroom slot behind it and a real office seat at the front.
**[v5](../v5/README.md)** is v4 with the driver seat swivelled as the office chair — the
3-seat cab never blocked that, only the passenger side. Both plan only, no 3D yet.

## Who this is for

[about-us.md](about-us.md) — who we are, how we'll use the van, how we live.
Read it before proposing anything.

## Versions

| Version | What | Status |
|---|---|---|
| [v1](../v1/README.md) | **Crafter L3H3**: swivel-seat front lounge, mid galley, sit-down wet cubicle, rear dinette to bed | Current. Configuration settled, drawings done. |
| [v2](../v2/README.md) | Crafter L3H3 with a 3-seat cab and a partition wall: front-corner shower, hanging wardrobe, split galley, rear U to a 1520 x 1832 bed that sleeps across | **Schema only, iterating.** Brisa's layout ported. No front lounge - open question. |
| [v4](../v4/README.md) | Same van and cab: 500 mm bathroom slot across the whole back, **fixed** 1520 x 1832 crosswise bed over a 1.11 m3 garage that swallows both wheel arches, v2-sized galley, thin larder and a 450 x 400 crosswise office seat with a desk folding off the partition | **Plan only, iterating.** The only version with a work seat and a bed never converted, and it gives up nothing to v2 to get them. Pays for it: the bathroom is behind the bed, so you cross it to get there. |
| [v5](../v5/README.md) | v4 with the **driver seat on a swivel** as the office chair; the bench is deleted and its 450 stays open floor. Driver-side partition opens, passenger side stays closed | **Plan only.** Same geometry as v4, far better chair. Blocked on one fact: lever or electronic parking brake. |
| [v3](../v3/README.md) | Same van and cab as v2, reversed: full-width front bench with a slide-out platform making a 1520 x 1832 bed across, split galley in the middle, rear bathroom 800 x 1000 beside a full-height 800 x 832 closet, both behind sliding panels | **Plan only, iterating.** Most worktop and the biggest bathroom of the three; costs the rear doors and a daily bed conversion. |

## References

| Ref | What | Verdict |
|---|---|---|
| [emandnick-transit-148el](../ref/emandnick-transit-148el/README.md) | 2018 Ford Transit 148" EL, high roof. Wet bath opposite the slider, split galley, rear dinette to bed, front desk. | **We like it.** Layout reconstructed. Basis for v1. |
| [doracamper-brisa-ducato-l2h2](../ref/doracamper-brisa-ducato-l2h2/README.md) | Fiat Ducato L2H2, 5.40 m overall. Front-corner standing shower, split galley, rear salon to a 1350 x 1880 bed. | **Most relevant reference we have.** 330 mm *shorter* than ours and still has a full shower. Layout reconstructed. |
| [scarletseth-promaster-159ext](../ref/scarletseth-promaster-159ext/README.md) | Ram ProMaster 159" EXT. Shower turned sideways against the cab bulkhead, WC in a drawer under the fridge, rear dinette to a near-square bed. | **Two ideas, not a layout.** $104k build on a 4089 mm van. Layout reconstructed. |

## Base vehicle sizing

**Decided 2026-09-20: the Crafter is the base.** v1 was drawn on a Ford Transit L3H3 first
and the Crafter carried alongside as a comparison; the Transit is now dropped. The 48 mm of
extra width lands in the corridor, the tightest spot in the van; the 44 mm of lost length
comes off the bed, which has the most slack. The 64 mm of lost height is the real cost and is
paid in the wet cubicle. The section below is kept as the reasoning behind that swap.


Load compartment, panel van, floor level:

| | Load length | Load height | Width max / between arches |
|---|---|---|---|
| Reference van — US Transit 148" EL, high roof | 4374 mm | 2070 mm | 1784 / 1392 |
| EU Transit **L4H3** (jumbo) | 4217 mm | 2025 mm | 1784 / 1392 |
| EU Transit L3H3 — dropped 2026-09-20 | 3494 mm | 2025 mm | 1784 / 1392 |
| **VW Crafter L3H3 — ours** | **3450 mm** | **1961 mm** | **1832 / 1380** |
| Reference van — Ram ProMaster 159" EXT, high roof | 4089 mm | 1930 mm | 1869 / 1384 |
| Reference van — Fiat Ducato **L2H2** | **3120 mm** | 1932 mm | 1870 / 1422 |

- L4H3 would be the direct equivalent of the reference van — 157 mm shorter, 45 mm lower.
- **L3H3 is 880 mm shorter** than the reference van, 20% of the length. Everything in v1
  follows from having to give that up.
- The **Ducato L2H2** reference goes the other way: **330 mm shorter than ours**, and it
  still carries a full standing shower. It is the best evidence we have that v1 is not
  overreaching.

## How the Crafter was chosen (it was the alternative until 2026-09-20)

Evaluated 2026-09-17. **The layout ports essentially unchanged** — drawings, 3D and
impressions all exist in **[v1/](../v1/README.md)**.

| | Transit L3H3 | Crafter L3H3 | difference |
|---|---|---|---|
| Load length | 3494 | 3450 | −44 mm |
| Load height | 2025 | 1961 | −64 mm |
| Max width | 1784 | **1832** | **+48 mm** |
| Between arches | 1392 | 1380 | −12 mm |

- The 44 mm comes off the bed: 1774 → 1730. Still fine at 171 cm.
- The 48 mm of extra width is best spent on the **corridor past the cubicle, 484 → 532** —
  that corridor is the tightest spot in the van, so this is a real daily gain.
- 64 mm less headroom: ~1881 mm standing instead of 1945. Irrelevant at our heights.

**Points to the Crafter**
- Many 2017+ Crafters have an **electronic parking brake** — no lever fouling the driver seat
  swivel, so no handbrake lowering kit and no releasing the brake to turn the seat. Since the
  front lounge is our main living space, this is worth more than it sounds. Trim-dependent:
  check the specific van.
- Squarer side walls, so the extra width is usable at counter height rather than theoretical.
- Much bigger **European** camper-conversion aftermarket (windows, swivel bases, furniture)
  than the Transit, which is more US-centric for conversions.

**Points to the Transit**
- **The Transit is built in Turkey** by Ford Otosan. With Turkey and Morocco on our list, Ford's
  parts and service network there is far denser than VW's light-commercial network. This is the
  strongest single argument either way.
- Cheaper used, so more of the budget stays with the build.

**Verdict:** dimensionally it does not matter — pick on price, on whether the van has an
electronic parking brake, and on how much the Turkey/Morocco service network is worth to us.
Whichever we buy, the layout is a short edit to `plan.py`.

## Budget

€10-15k target for the build; realistic landing zone **€13.7-17k** with the cuts already
decided (no Cerbo GX, cushions made by us). Starlink stays in, accepted as EU-only.
See [budget.md](budget.md).

## Open questions
- Engine heat exchanger: in the plan, Ondrej to check against the warranty.
- Morocco and Turkey paperwork, and Schengen limits on a Turkish passport.
- Measure the real van's roof once bought; our 3300 x 1570 mm usable figure is derived, not measured.

## Setup

Python 3 plus:

    pip install -r requirements.txt

`matplotlib` draws every plan, elevation and 3D render; `numpy` runs the pinhole projector;
`pillow` reads whatever FAL hands back, which is rarely the format we asked for; `trimesh` and
`fast-simplification` measure and shrink generated meshes; `fal` drives image and image-to-3D
generation. Only `plan.py` and `model3d.py` are needed to draw the layout - `fal` and the mesh
libraries matter only for `impressions.py` and `props.py`. Analysing a video reference
additionally needs `pip install yt-dlp imageio-ffmpeg`.

### FAL credentials

Two ways in, and which one you get depends on where you are:

| | |
|---|---|
| **Locally** | `fal auth login` once. The token lands in `~/.fal/`. |
| **Claude Code on the web, CI, any container** | export `FAL_KEY`. There is no browser to log in with, and nothing persists in `~`. |

`FAL_KEY` wins if both are present, and the `fal` package reads it with no code change - make
a key at [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) and set it in the
environment. A run with neither fails on the first call with a credentials error, not with
anything about the model, so check this before debugging a generation.

### Working on this repo from Claude Code on the web

Everything except image generation runs with no setup: `python plan.py v1` and
`python model3d.py v1` need only the pip install above and redraw the whole layout.

* Set `FAL_KEY` in the environment before running `impressions.py` or `props.py`.
* `props/*/` is **not** in the repo - 700 MB of previews and rejected meshes. The adopted
  `props/<kind>.glb` and `props/yaw.json` are, which is all the viewer build needs. Running
  `props.py auto <kind>` regenerates the intermediates for whatever you are working on.
* The skills this project is worked with are committed under `.claude/skills/`, so the web
  session picks them up the same as the desktop one.
* Nothing in the Python is platform-specific: no absolute paths, no shell-outs, no
  Windows-only calls. It was written on Windows and runs unchanged on Linux.
* `viewer.html` pulls three.js and GLTFLoader from CDNs and Google Fonts for type, so a
  sandbox with no outbound network will render a blank page rather than the model.

## Services and access

- **FAL** — `fal auth login` locally, `FAL_KEY` everywhere else (see Setup). Inference works. **`fal files`, `fal keys` and everything
  serverless are blocked** on both Ondrej's personal and the grip-digital team accounts; that
  is a separate product tier requested at fal.ai/dashboard/serverless-get-started, not an
  admin-role problem. We do not need it: control images go inline as data URIs.
  Note `fal api` on the CLI **cannot take a data URI** (its key=value parser splits on the "="
  padding inside base64), which is why `impressions.py` calls `fal.apps.run()` from Python.
- **Vertex AI** (project `vertex-503913`) — Imagen models are **not enabled**; every
  `imagen-*` endpoint 404s in every region. `gemini-2.5-flash-image` does work. We moved to
  FAL because it gives control-image steering, which Gemini did not.

## Tooling

`plan.py` at the project root draws everything from a list of boxes in millimetres and
writes `.png` + `.svg`.

    python plan.py v1             # plan + elevations + sections -> v1/
    python plan.py v1-roof         # roof layout -> v1/roof.png
    python plan.py v2             # plan -> v2/layout.png
    python plan.py ref             # Em & Nick's Transit 148" EL -> ref/emandnick-transit-148el/
    python plan.py ref-brisa       # Dora Camper "Brisa" Ducato L2H2 -> ref/doracamper-brisa-ducato-l2h2/
    python plan.py ref-scarletseth # Scarlet & Seth ProMaster 159 EXT -> ref/scarletseth-promaster-159ext/

To iterate, edit the variant's `boxes` (plan) and `views` (elevations, sections) and rerun.
Plan coordinates: x = 0 at the front bulkhead growing aft, y = 0 at the passenger wall
growing toward the driver side. In the drawing the nose is at the left, so the driver side
sits at the bottom. View coordinates add z = height above the finished floor.

`model3d.py` extrudes the plan into 3D: greybox renders, edge-only control renders, and an
OBJ for Blender or SketchUp.

    python model3d.py v1          # -> v1/3d/*.png, v1/model.obj, v1/viewer.html
    python model3d.py v2          # -> v2/3d/*.png, v2/model.obj, v2/viewer.html

The model now includes the **vehicle itself**: body panels with real apertures cut for the
sliding door, the rear doors, the windows and the roof fans, plus glazing and the cab with
its two swivel seats, dashboard and windscreen. Walls and roof render back-faces only, so the
body reads as an enclosure from inside and never blocks the view from outside.

It also carries the **big kit at real catalogue sizes** — oven, hob, sink, cassette, both
water tanks, calorifier, batteries, inverter, electrics board — in `APPLIANCES`. Before it
renders anything, `check()` asserts every appliance sits inside the van, inside a cabinet,
and clear of its neighbours, so changing a size to a real product fails loudly instead of
quietly overlapping.

**Each layout version carries its own 3D tables.** `REGISTRY` in model3d.py maps a variant to
its `HEIGHTS`, `EXTRA`, `APPLIANCES`, `CONTAINERS`, window and fan positions, hatches, the
partition and the cab seats — v1 and v2 furnish completely different rooms, and nothing about
one survives being shifted onto the other. A variant with no entry (the reference vans)
borrows v1's and gets them through `remap()`, which moves anything on the driver side or aft
of the rear-bench line onto that vehicle's walls. `check()` accepts kit housed in a **run of
carcasses that meet**, not only a single box, because v2's U is one continuous carcass and
its fresh tank crosses the joint on purpose.

In the viewer, **Sizes** labels every block with its name and width × depth × height in mm,
and **Appliances** toggles the kit *and* ghosts the carcasses listed in `CONTAINERS`, so the
oven, tanks and batteries are visible inside the galley, the cubicle and the benches. Ghosting
beats cutting openings here: real door and drawer splits are not designed yet, and a face
panel would hide the kit from most angles anyway. Sizes is off by default — thirty labels at
once is unreadable, and tags declutter front-to-back, so switch off the layers you are not
measuring first.

**Schema overlay** lays the plan drawing itself on the floor of the 3D model, and the
**Plan** view looks straight down at it from the plan's own viewpoint — nose left, driver
side at the bottom, and it switches the overlay on when you pick it. `plan.overlay_png()`
renders the same drawing cropped to exactly the load box, so it is the real layout image and
it lands 1:1 on the floor; model3d embeds it as a data URI. The overlay deliberately ignores
the depth buffer: on the floor, under the furniture, the one angle where a plan is worth
reading would show nothing but the bed.

**Panning**: right-drag, middle-drag, shift-drag or two fingers move what the camera looks
at. Orbiting alone always points at the middle of the van, so a corner can never be centred.
Picking a view puts the camera back where that view says, panning included.

**Furniture is checked against a seated person.** `SITTER_V2` is trunk, thighs and shins on
the office seat, and `check()` fails the build if anything but the seat itself runs through
them. The office table was mounted on the partition twice, and both times the swing arm went
straight through the sitter's chest - a clash no box list shows and every render does.

**A mirrored placement turns its prop with it.** `FACING_V2` records which wall each mesh was
modelled facing away from; a box against the other wall gets a half turn on top of the kind's
own `yaw.json` entry, so the galley on v2's passenger side does not open into the wall.

A variant can also send its own **Show** buttons — v2 groups shower, wardrobe and office
table differently from v1 — in `LAYERS_V2`. Without one, the viewer uses the list in the
template.

`viewer_template.html` is the viewer's markup; model3d.py injects the geometry into it.
Published viewers: **[v1 Crafter](https://claude.ai/artifact/LwGHoarYhEiNDaQSUbvz5s)** ·
**[v2 Crafter](https://claude.ai/artifact/4zfKdrCzAheAzWhmKarVFe)** -
republish it after any change with the Artifact tool, passing that URL so it updates in place
rather than making a second one. It is private to Ondrej's account; sharing is done from the
page's own Share menu, not from here.

`impressions.py` turns a shaded render into photoreal interior views via FAL
(depth-conditioned FLUX, strength 0.75). Needs `fal auth login` once.

    python impressions.py v1          # all four shots -> v1/impressions/*.jpg
    python impressions.py v1 01 02    # just those shots, when you are tuning one

Each run also writes the control it used to `<variant>/3d/control/<shot>.png`, plus a line
version `<shot>-lines.png` that is easier to read the layout from.
**Prompts must never contain a negation** - "no tall cupboards" reliably produces a tall
cupboard. Say what is there instead.

Impressions are **mood images, not drawings**. Build from `plan.py` output.

`props.py` replaces the coloured boxes with generated low-poly meshes, one appliance at a
time, through FAL. Four stages, each one showing its work so a human picks:

    python props.py preview cassette          # one catalogue photo per image model
    python props.py sheet cassette            # all of them side by side, to choose from
    python props.py mesh cassette recraft2    # the chosen photo -> one mesh per 3D model
    python props.py shots cassette            # three views of each mesh, to choose from
    python props.py pick cassette trellis     # adopt one -> props/cassette.glb

`pick` strips the texture, decimates to 4000 faces and centres the mesh; `model3d.py` embeds
every `props/*.glb` into viewer.html as base64, so the viewer stays one file you can mail.
The **Detailed props** layer swaps each box for its mesh.

The box in `APPLIANCES` stays the authority: the viewer scales a mesh to exactly fill its
box, so a generated shape can never quietly change a dimension. What the mesh stage checks is
**shape**, not size — the bounding box proportions against the real product's, since every one
of these models normalises its output to a unit cube. If a mesh comes back the wrong way
round, put its correction in `props/yaw.json` as `{"cassette": 90}`; degrees about the
vertical.

**What we learnt building it, 2026-09-19.** Each of these cost a full round, so check them
before blaming a model.

* **The box has to contain the whole prop.** The sink box was the bowl alone, 150 mm tall, so
  the tap had nowhere to go; it is now 750-1200. Decide what the prop *includes* before
  writing its prompt.
* **A decimated mesh carries no normals and three.js lights it pure black.** The viewer calls
  `computeVertexNormals()` when the attribute is missing.
* **`fal.apps.run()` waits on a single HTTP read**, and the slow image-to-3D endpoints drop the
  connection long before they finish. `run()` here submits to the queue and polls it instead.
* **Parallel submits race on fal's token cache file** (Windows error 32). A lock around
  `submit()` fixes it; the polling stays parallel.
* **Only shape can be checked, never size** - every one of these models normalises its output
  to a unit cube.

Model notes: `fal-ai/imagen4/preview` and `fal-ai/hunyuan3d/v21` both 404. Tripo belongs to
`tripo3d`, not `fal-ai`. triposr and tripo are both far slower than the rest. recraft-v3 needs
`style: realistic_image` - `realistic_image/studio_portrait` invents a coloured backdrop and a
pot plant, and image-to-3D bakes both into the mesh.

**Say the shape, not just the object.** Single-view image-to-3D pulls everything toward
average proportions, so a long slim battery came back squat and a stubby cylinder came back
long - on every model at once, which is the tell that the prompt is at fault and not the
model. Writing the proportions into words fixed all three: "twice as long as it is wide",
"only about a third longer than it is wide", "as wide across as it is deep and only half that
again in height". The battery went from 0.29-0.36 to 0.04, the calorifier from 0.28 to 0.06.

**Let the check pick the preview, not the eye.** The same battery prompt through four image
models gave meshes scoring 0.03 to 0.29. Which photo reads as the right shape is not
something you can see - generate the mesh from each and read the numbers.

All eleven adopted, 2026-09-20:

| | | | | |
|---|---|---|---|---|
| cassette trellis 0.04 | sink rodin 0.04 | inverter rodin 0.03 | battery hunyuan 0.04 | grey hunyuan 0.04 |
| calorifier hunyuan 0.06 | oven hunyuan 0.10 | hob hunyuan 0.09 | electrics trellis 0.14 | fresh rodin 0.16 |

Furniture followed on 2026-09-20 - table, table post, bed cushion, overhead locker, shower
head - generated and adopted with no human in the loop, the shape error picking rather than
the eye. Errors 0.01 to 0.11. Two of them needed new geometry first: `leg` (260 x 260 x 700,
one under each table) and `shower` (80 x 180 x 400 on the cubicle wall), both in EXTRA rather
than APPLIANCES because they are furniture, not kit inside a cabinet. `box_of()` reads EXTRA
too, and where a kind owns several boxes it aims at the largest - the viewer fits the mesh
into each box separately, so one locker mesh serves all three lockers.

The **Detailed props** layer is on by default. plumbing sits at 0.21 and cannot do better: its box is a 340 x 350 x 360 cube, which is a
space reservation for a pump, a filter and a trap, not a product anyone makes. Kept anyway -
with uniform fit the mesh sits inside its reserved volume undistorted.

The viewer **fits a mesh inside its box without distorting it**. Stretching each axis to fill
the box lies about the product's shape whenever the two disagree, and plumbing disagrees by a
lot. The box still owns the reserved volume, and the Sizes layer still reports it.

### Four props for v2, 2026-09-21 — and where the score lies to you

`fridgedoor` (65 L, hinged door — a different product from v1's drawer fridge, so a different
kind), `SEAT`, `SHOWER` and `WARDROBE`. Adopted: fridgedoor rodin 0.39, SEAT rodin 0.14,
SHOWER **trellis 0.50**, WARDROBE rodin 0.06.

Two things this round taught:

- **The shape error only ranks candidates that modelled the same object.** rodin scored best
  on SHOWER at 0.17 and had modelled the shower head on its rail — not the cubicle at all. A
  tall thin thing matched a tall thin box perfectly. Read the shots sheet first and throw out
  anything that is the wrong object; only then trust the number.
- **An opening costs score and is worth it.** Every fridgedoor mesh scored OFF because the
  open door widens the bounding box, and a cubicle you can see into is squatter than the slot
  it fills. Both were the point of the prop.

**SHOWER: a room is not a product, and generating one was the wrong idea.** Round one came
back a pentagonal corner pod, because the flux preview had angled panels — **the preview
decides the plan shape, and the plan shape is exactly what the shape error cannot see**: a
hexagon and a rectangle of the same proportions score the same. Round two, re-meshed from
the rectangular qwen shot, came back rectangular (rodin 0.17) and was still wrong in the
viewer: its one open side faced the wall, and three separate ways of measuring which way it
pointed — centroid offset, area near each face, coverage of each face — all agreed with each
other and disagreed with what the browser drew.

So the cubicle is **built, not generated**: three wall panels, a tray, and a glass screen
across the side that opens onto the lobby, all in `EXTRA_V2`. A single mesh scaled to fill a
700 x 800 x 1881 hole can only read as a solid block or turn its one opening to a wall, and
which way a generated mesh faces is a coin toss the box list should not be losing. Products
get meshes; rooms get panels. `props/SHOWER.glb` is gone and `SHOWER` is a void in
`HEIGHTS_V2`.

**Three more for the sink, 2026-09-21:** `bowl` (hunyuan 0.07), `filtertap` (rodin) and
`filter` (trellis 0.03). The tap scored 0.37 against its box and the mesh was not the
problem - **the box was**: a gooseneck reaches sideways about two thirds of its height, and
the box had been drawn as a 50 x 50 stick. Widening it to the tap's real footprint,
50 x 170 x 250, took the error to 0.11 without touching the mesh. When one prop scores badly
and all three models agree on the shape, suspect the box before the generator.

A prop with no opening has no "face" to measure, so the direction is read from where its
mass sits: the top fifth of the tap mesh leans toward mesh +Z, which the viewer sends to
van +y - the back of the cabinet - so it carries a deliberate 180 in yaw.json.

`props.py face <kind> <+x|-x|+y|-y>` sets which way a prop looks. It measures surface area
near each of the four vertical faces of the bounding box: a wall panel puts a lot of area
against its own face, an opening has almost none. The first version compared the centroid
with the centre of the bounding box, and was wrong on the very prop it was written for —
the shower tray sticks out through the opening and drags the centroid toward it. `align` still owns the quarter turn that matches the footprint; when the two
disagree, facing wins. A wardrobe 150 mm too shallow still reads as a wardrobe; one that
opens into the wall does not.

Each viewer now embeds **only the props its own variant uses**, so v1 does not carry v2's
shower cubicle and wardrobe.

### Finding a pipeline that keeps the layout — the ladder, 2026-09-18

Canny-on-a-line-drawing kept inventing furniture, so we climbed from the geometry toward
realism one rung at a time, checking the layout at each. Samples in
`v1/impressions/ladder/`.

| Rung | Result |
|---|---|
| Line render (`model3d.line_render`) | matches the plan, verified |
| Shaded render (`model3d.shaded_render`) — real body panels, apertures, flat material colour | matches the plan, verified |
| img2img on the shaded render, strength 0.40 | layout perfect, no realism added |
| img2img, 0.75 | layout perfect, cabinet detail appears, still flat |
| img2img, 0.85 | **layout destroyed** — became a bedroom |
| canny control + shaded init | layout perfect, almost no realism |
| **shaded render → `fal-ai/flux-control-lora-depth`, strength 0.75** | **photoreal and the layout holds** |
| true depth map (`model3d.depth_render`) → same model | worse: the bright near walls read as a doorway |
| shaded → depth, 0.85 and 0.95 | frames the whole van inside a false doorway |

**The recipe that works: a flat shaded colour render as the control image for a
depth-conditioned model, at strength 0.75.** Depth carries the volume of the room rather than
just its edges, so the model can light and texture freely without moving anything; and the flat
*colour* beats a true depth map because the material cues stop it reading a bright near wall as
a door. Realism and layout stop fighting each other, which they always did with canny.

**Always look at a control render in `<variant>/3d/control/` after changing a camera.**
Cameras are an eye and a target in millimetres, in plan coordinates; `line_render` does its own
pinhole projection with near-plane clipping and painter-sorted solid faces, because
matplotlib's 3D axes always parks its camera a fixed distance from the centre of the data and
so put every one of ours *outside* the van. Prompts must also agree with the camera about which
side is which — the plan is drawn nose-left, so its top edge is the driver side, and looking
aft flips left and right again. Written up in
[v1/README.md](../v1/README.md#3d-and-impressions).
