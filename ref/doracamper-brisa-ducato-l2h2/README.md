# Reference: "Brisa" — Dora Camper Studio, Fiat Ducato L2H2

**Status:** analysed, layout reconstructed. **The most relevant reference we have** — it is the
only one built on a van *shorter* than ours, and it still fits a full standing shower.

## Source

- Van tour (8:08, Spanish): https://www.youtube.com/watch?v=RrNkzK-014A
- Builder: Dora Camper Studio (Debora + Garrido), Spain. https://www.doracamperstudio.com/
- They **sell the full plans** — measurements, wiring and plumbing schematics, material links:
  https://www.doracamperstudio.com/product-page/planos-y-guia-tecnica-brisa
  If we ever seriously consider this layout, buying that is cheaper than re-deriving it.
- `transcript-es.txt` — the creators' own Spanish captions, with timestamps.
- `frames/` — 12 stills used to work out the geometry.

## Base vehicle

| | |
|---|---|
| Model | **Fiat Ducato L2H2** |
| Overall length | **5413 mm** — they advertise it as "solo 5,40 m" |
| Load box | **3120 × 1870 × 1932 mm**, 1422 between the wheel arches |
| vs our Crafter L3H3 | **330 mm shorter**, 38 mm wider, 29 mm lower |

That last line is the point of this reference. They lost more than a third of a metre against
what we have and still got a standing shower, a split galley and a four-seat salon into it.

## Layout

See `layout.png` / `layout.svg`. Front at left, driver side at the bottom.

Front to rear:

1. **Bulkhead.** A **sliding partition door to the cab** (driver half) — quick access, better
   insulation, and it separates living from driving. On the passenger half, a shallow
   **oak display shelf unit** you see as you step in; every object is **velcroed down** so
   nothing moves on the road.
2. **Driver side, front corner: the shower.** Full height, arched opening, **real tile**,
   teak slatted floor, recessed niche with a gold rail, gold mixer with hot and cold, a
   **curtain**, a **window** (they say it is what stops it feeling like a box), and a
   **heater outlet inside the cubicle** to dry towels and wetsuits.
3. **Passenger side: the sliding door is the entry.**
4. **Split galley across the aisle**, both runs **900 × 600**:
   - passenger side — **2-burner gas hob** with automatic ignition (chosen specifically so
     cooking does not drain the battery), porcelain worktop, **65 L fridge with freezer**
     below, cutlery drawer, hidden socket with USB, and a **window beside the hob** so you
     can cook with it open.
   - driver side — porcelain worktop, stainless sink, **gold pull-out tap** hot and cold,
     tiled splashback, hidden socket with USB, and a **Nespresso machine on a pop-up lift**
     that disappears into the counter at the press of a button.

   **Measured off the hob close-up** (2026-09-20, Ondrej's still). Confidence ±80 mm on the
   hob, ±100 mm on the board:

   | | mm | How it was read |
   |---|---|---|
   | Gas hob, glass panel | **480 × 340** | standard 2-burner camper unit — two unequal burners, two knobs at the front-left, flush glass |
   | Clear board beside it | **~420 long** | ≈ 0.9 × the hob width after perspective correction; also ≈ the run from the fridge's aft edge to the counter end |
   | Whole run | **~900 × 600** | hob 480 + board 420 |
   | Fridge | **~500 W × ~520 D**, 65 L | **a normal hinged door, not a drawer** — door gasket and handle edge are visible, there are no drawer runners |

   The 900 mm run is **360 mm longer than this file first claimed**. It does not fit
   3120 mm alongside a 700 mm shower and an 1880 mm bed, so the bed has to reach
   **360 mm forward between the two counters** — which is exactly the step you can see at
   the head of the made-up bed at 06:24. The plan is redrawn that way.

5. **Rear: the salon.** Benches down both sides, a table on a **height-adjustable pillar that
   also slides sideways**, seating **4 to eat**. Heater control, USB and USB-C on both sides.
   Drop the table, add one infill piece → a bed **1880 mm fore-aft × 1350 mm across** — you
   sleep along the van, head forward, feet to the rear doors. 1880 could not run across a
   1870 mm-wide body anyway, and the narration says it: *"1,35 de ancho por 1,88 de largo"*.
   - Under the driver-side bench: the **whole electrical installation**.
   - Under the passenger-side bench: the **90 L fresh water tank**.
   - **The rear doors still open into the living space** — they call this out explicitly as
     the thing a fixed bed costs you.
6. **Storage:** overhead lockers for crockery, **3 large upper cabinets** for clothes, a small
   arched door at the front into a wide shallow bedding/towel locker, and **2 drawers under
   the salon platform, one opening inward and one opening outward through the body**.

## Systems

- **Power:** **400 W** panel — a **domestic house panel, not a camper panel**, which is why it
  is so much cheaper per watt. Nearly all **Victron**, everything Bluetooth-monitored,
  **3000 W inverter** (sized so the Nespresso runs), three charge paths (solar, vehicle, shore).
  A **rotary selector** switches the sockets between inverter and shore.
- **Water:** 90 L fresh. Hot and cold to both the sink and the shower.
- **Heat:** diesel/stationary heater, outlets in the salon *and* in the shower.
- **Roof:** **70 × 50 cm** openable rooflight with blackout and flyscreen, walk-on roof deck
  with a rear ladder, reverse camera.
- **Interior:** natural wood slat ceiling in a pale lasur, **concealed LED strips** (invisible
  when off), and a **projector** with a drop-down screen hidden in a ceiling shelf.

## What to steal / what to question

Worth stealing:
- **Rear salon instead of a fixed bed, on a short van.** We already chose this in v1; Brisa is
  the proof it survives on 3120 mm when ours has 3450 mm.
- **Keeping the rear doors usable.** Same reasoning as ours, said out loud by someone living it.
- **Heater outlet inside the shower cubicle.** Cheap, and it turns the wet cubicle into the
  drying room — which is exactly what a minimal-water build needs.
- **A window in the shower.** Ours is 700 mm wide; this is the difference between a cubicle
  and a coffin.
- **Domestic solar panel instead of camper panels.** 400 W for the price of far less. Worth
  checking against our 3300 × 1570 mm roof and against weight.
- **Sliding partition door to the cab** rather than a curtain — and it is the honest answer to
  "we are not using swivel seats".
- **Velcro on everything on an open shelf.** Trivially cheap, and it is the only way an open
  display shelf survives a Moroccan road.

Worth questioning for us:
- **Gas.** They use 2-ring gas so cooking does not touch the battery; v1 chose induction plus
  an oven. Their argument is real, but gas means a bottle locker and a solenoid, and refilling
  across Turkey and Morocco is its own problem. Our alternator-heavy energy plan is the
  counter-argument.
- **Bed 1350 × 1880.** 1880 is fine at 171 cm. **1350 wide is narrow for two** — v1's is 1132
  at the cubicle and 1832 at the rear, so we are not obviously worse off, but check it.
- **No fixed desk anywhere.** Brisa is a holiday van, not an office. The salon table is
  height-adjustable and slides, which is the nearest thing — but Ondrej works 5 days a week,
  so a table that has to be cleared for dinner is a question, not an answer.
- **90 L fresh on a full shower.** Matches our "very economical with water" line; worth noting
  they run a full rainfall shower on less water than most builds with none.
- **The plans are for sale.** €-for-hour, buying them may be the cheapest way to check every
  number in this file.
