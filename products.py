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
        weight_kg=None, price_eur=(620, 680), shop="dalix.cz / karavan.cz",
        source="https://www.reimo.com/de/bilder/intern/ersatzteile-daten_2012/dometic-seitz/"
               "product-documentation/dateien/S4-Fenster.pdf",
        status="proposed"),
    "s4-500x350": dict(
        name="Dometic S4 hinged window 500 x 350", kind="window",
        cutout=(500, 348), outer=(544, 380), clear=(404, 204), wall=(27, 53),
        glazing="double acrylic", blind=True, flyscreen=True,
        weight_kg=None, price_eur=(260, 400), shop="shop.camperselbstbau.de",
        source="https://www.reimo.com/de/bilder/intern/ersatzteile-daten_2012/dometic-seitz/"
               "product-documentation/dateien/S4-Fenster.pdf",
        status="proposed"),
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
        weight_kg=None, price_eur=(356, 356), shop="nomadem.cz (8,890 CZK)",
        source="https://airxcel.eu/wp-content/uploads/2022/02/airxcel-europe-maxxfan-deluxe.pdf",
        note="Crafter 2017+ roof adapter (PVC, 15 mm): North Devon Campervans, GBP 80-100",
        status="proposed"),
}


def cut(key, side_or_none, a0, b0):
    """A product's cut-out placed at (a0, b0): a window as (side, x0, x1, z0, z1), a roof
    cut-out (side None) as (x0, x1, y0, y1)."""
    w, h = PRODUCTS[key]["cutout"]
    if side_or_none is None:
        return (a0, a0 + w, b0, b0 + h)
    return (side_or_none, a0, a0 + w, b0, b0 + h)
