"""The product register: one entry per real product the build uses or is weighing up.

Sizes here are the manufacturer's, and the model takes them from here - so a product change
is one edit, and model3d.check() then says whether it still fits. Prices in EUR incl. VAT
from the source named (CZK at 25 per EUR). None means not found yet, never a guess.

status: "proposed" (recommended, not agreed), "chosen" (agreed with Ondrej), "option".
"""

PRODUCTS = {
    # --- side windows ----------------------------------------------------------------------
    # Universal framed, top-hinged. Double acrylic, blackout blind and flyscreen built in.
    # cutout / outer / clear are width x height, from Dometic-Seitz's S4 size table.
    "s4-900x450": dict(
        name="Dometic S4 hinged window 900 x 450", kind="window",
        cutout=(902, 448), outer=(948, 481), clear=(804, 304), wall=(27, 53),
        glazing="double acrylic", blind=True, flyscreen=True,
        weight_kg=8.0, price_eur=(620, 680), shop="dalix.cz / karavan.cz",
        source="https://www.reimo.com/de/bilder/intern/ersatzteile-daten_2012/dometic-seitz/"
               "product-documentation/dateien/S4-Fenster.pdf",
        status="chosen"),
    "s4-500x350": dict(
        name="Dometic S4 hinged window 500 x 350", kind="window",
        cutout=(500, 348), outer=(544, 380), clear=(404, 204), wall=(27, 53),
        glazing="double acrylic", blind=True, flyscreen=True,
        weight_kg=4.7, price_eur=(260, 400), shop="shop.camperselbstbau.de",
        source="https://www.reimo.com/de/bilder/intern/ersatzteile-daten_2012/dometic-seitz/"
               "product-documentation/dateien/S4-Fenster.pdf",
        status="chosen"),
    # Made for the Crafter 2017+: fills a whole stamped field. Single tinted safety glass,
    # no blind or flyscreen. Kept as the alternative.
    "carbest-crafter-front": dict(
        name="Carbest sliding window VW Crafter 2017+, front (31710 R / 31711 L)", kind="window",
        cutout=(1492, 713), outer=(1492, 713), clear=None, wall=None,
        glazing="single tinted ESG", blind=False, flyscreen=False,
        weight_kg=None, price_eur=(329, 329), shop="camping-factory.com",
        source="https://www.camping-factory.com/carbest-schiebefenster-vw-crafter-ab-bj.-2017-vorne-rechts",
        status="option"),
    "globus-crafter-side": dict(
        name="Globus Camper hinged window VW Crafter 2017+, side (vent 800 x 350)", kind="window",
        cutout=(1489, 709), outer=(1489, 709), clear=(800, 350), wall=None,
        glazing="single ESG", blind=False, flyscreen=True,
        weight_kg=None, price_eur=(490, 490), shop="globus-camper.com (fitting from 220)",
        source="https://globus-camper.com/product/ausstellfenster/ausstellfenster-vw-crafter/",
        status="option"),
    # --- roof fans -------------------------------------------------------------------------
    "maxxfan-deluxe": dict(
        name="Maxxair MaxxFan Deluxe 00-07500KI40 (EU)", kind="fan",
        cutout=(400, 400), outer=(585, 417), above_roof=(127, 237), roof=(25, 90),
        current_a=(0.2, 2.3), features="10 speeds, in and out, rain cover, thermostat, remote",
        weight_kg=7.7, price_eur=(356, 356), shop="nomadem.cz (8,890 CZK)",
        source="https://airxcel.eu/wp-content/uploads/2022/02/airxcel-europe-maxxfan-deluxe.pdf",
        note="Crafter 2017+ roof adapter (PVC, 15 mm): North Devon Campervans, GBP 80-100",
        status="chosen"),
    # --- sliding door fly screen (no window in the door: agreed 2026-09-24) -------------------
    "horrex-plissee-crafter": dict(
        name="Horrex pleated fly screen door, VW Crafter / MAN TGE 2017+ (art. 052176, maker 134998)",
        kind="flyscreen", outer=(1267, 1884), depth_mm=None,
        weight_kg=3.5, price_eur=(414, 668), shop="campingplus.de 414 / campingwuerdig.de 667.50",
        source="https://www.campingplus.de/caravaning-technik/fenster-u.-tuer/insektenschutz/"
               "horrex-plissee-fliegenschutztuer-vw-crafter-man-ab-2017",
        note="Mounts IN the door opening: floor profile screwed down at the threshold, top profile "
             "clipped on the opening's metal flange under the door seal, pleat cassette standing "
             "at one end. 1884 tall is made for the FWD high-roof opening (1822, VW H508); our "
             "4MOTION high floor gives 1722 - ask Horrex for a 4MOTION version before buying. "
             "Cassette depth not published: check against the shoe locker (x 0-450, y from 41).",
        status="option"),
    "vanquito-crafter": dict(
        name="VanQuito magnetic mosquito net, right sliding door, VW Crafter / MAN TGE 2017+, "
             "fine mesh, H2 + H3 (art. 1734-mag-fine-mesh)", kind="flyscreen",
        outer=None, depth_mm=0,
        weight_kg=0.75, price_eur=(195, 195), shop="lila-bus-shop.de (RRP 229.90)",
        source="https://www.lila-bus-shop.de/Insektenschutzgitter/VW-Crafter/Insektenschutzgitter-VW-Crafter-4424.html",
        note="Soft net held by sewn-in magnets around the opening, magnetic zip to walk through; "
             "mesh 0.94 x 0.94 mm. The maker says it can stay on with the door closed - but off "
             "in rain and while driving. Made for the passenger-side door and H2/H3 vans "
             "(2590-2640 high), so it does not depend on the 4MOTION floor.",
        status="chosen"),
    # --- WC ------------------------------------------------------------------------------------
    # Emptied INSIDE (2026-09-24): no hatch in the side panel. A portable unit is the natural
    # fit for a WC that slides out of the wardrobe: it has its own flush tank and no plumbing.
    "porta-potti-565e": dict(
        name="Thetford Porta Potti 565E (Curve)", kind="wc",
        outer=(386, 450, 447), waste_l=21, flush_l=15,
        weight_kg=6.1, price_eur=None, shop=None,
        source="https://www.campingworld.com/thetford-porta-potti-565e-curve-portable-rvmarine-toilet-58980.html",
        note="386 W x 450 D x 447 H - inside the 420 x 520 slot, which the shower's diagonal "
             "face limits to 520 deep",
        status="option"),
}


def cut(key, side_or_none, a0, b0):
    """A product's cut-out placed at (a0, b0): a window as (side, x0, x1, z0, z1), a roof
    cut-out (side None) as (x0, x1, y0, y1)."""
    w, h = PRODUCTS[key]["cutout"]
    if side_or_none is None:
        return (a0, a0 + w, b0, b0 + h)
    return (side_or_none, a0, a0 + w, b0, b0 + h)
