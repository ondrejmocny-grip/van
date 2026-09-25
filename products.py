"""The product register: one entry per real product the build uses or is weighing up.

Sizes here are the manufacturer's, and the model takes them from here - so a product change
is one edit, and model3d.check() then says whether it still fits. Prices in EUR incl. VAT
from the source named (CZK at 25 per EUR). None means not found yet, never a guess.

status: "proposed" (recommended, not agreed), "chosen" (agreed with Ondrej), "option",
"optional" (nice to have - first to cut if weight or money runs short).
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
    # --- kitchen (researched 2026-09-24) ----------------------------------------------------
    # outer is W x D x H. The fridge stands under the hob run; above it there is room up to
    # ~835 (the Bosch hob wants 65 free under the worktop), so 620 was never the real limit.
    "isotherm-cruise-85": dict(
        name="Isotherm (Webasto) Cruise 85 Elegance, compressor, hinged door", kind="fridge",
        outer=(475, 505, 627), volume_l=85, kwh_day=None, weight_kg=22.0,
        price_eur=(1040, 1040), shop="koesling.de",
        source="https://www.webasto.com/en-int/cooling/fridges-freezers/cruise-elegance.html",
        note="shallow (505) - leaves ~75 behind it for air in our 565 carcass; freezer size and "
             "daily use not on the maker page",
        status="option"),
    "indel-cruise-85": dict(
        name="Indel B Cruise 85 OFF, compressor, hinged door", kind="fridge",
        outer=(475, 545, 635), volume_l=85, kwh_day=0.386, weight_kg=21.5,
        price_eur=(774, 774), shop="prokes-auto.com",
        source="https://www.prokes-auto.com/indel-b-cruise-85-off-built-in-compressor-refrigerator-12-24v-85l/",
        note="cheaper, but 545 deep: little room behind it for air", status="option"),
    "vitrifrigo-c75l": dict(
        name="Vitrifrigo C75L, compressor, hinged door", kind="fridge",
        outer=(470, 462, 622), volume_l=75, kwh_day=None, weight_kg=18.6,
        price_eur=(815, 815), shop="svetkaravanu.cz (20,360 CZK)",
        source="https://www.svetkaravanu.cz/vestavna-autochladnicka-vitrifrigo-c75l-chr-51-l-cerna_z102502/",
        note="smallest and lightest; 10 L less", status="option"),
    "bosch-pib375fb1e": dict(
        name="Bosch PIB375FB1E Serie 6, domino induction 30 cm, 2 zones", kind="hob",
        outer=(306, 527, 51), cutout=(270, 490), power_w=3700, power_limit_w=(1000, 3000),
        weight_kg=6.8, price_eur=(400, 472), shop="ab-com.cz (10,041 CZK) / kueche24.com",
        source="https://media3.bsh-group.com/Documents/9001763570_C.pdf",
        note="total power can be LIMITED in the settings, 1000-3000 W: set 2000 on our inverter",
        status="option"),
    "quadron-anthony-50": dict(
        name="Quadron Anthony 50 = 'Paul' MF4444BS_I, stainless inset sink", kind="sink",
        outer=(440, 440, 190), bowl=(400, 400, 190), cutout=(420, 420), drain='3 1/2"',
        weight_kg=6.4, price_eur=(179, 190), shop="absulo.sk 189.57 / SIKO.cz ~4,472 CZK (search MF4444BS_I)",
        source="https://absulo.sk/p/quadron-paul-nerezovy-drez-44x44-cm-mf4444bs-i",
        note="1 mm steel, R10 corners, space-saving siphon included. NO workstation ledge - board, "
             "mat and colander rest on the rim; no sink with a real ledge fits 440 x 440 x 190. "
             "Cut-out: shops say 420 or 400 - use the template in the box. Backup: Blanco Andano "
             "400-IF, same size, 7,641 CZK. 6.4 kg is with packaging",
        status="proposed"),
    # --- taps and drinking water (researched 2026-09-25) ------------------------------------
    # NOT a German "Niederdruck" tap: those are for open boilers; the Truma B10 is pressurised.
    "grohe-31170000": dict(
        name="Grohe Eurosmart Cosmopolitan 31170000, window mixer (lifts out)", kind="tap",
        outer=(226, 60, 202), reach=226, hole=35, flow_l_min=13, weight_kg=None,
        price_eur=(224, 228), shop="sanitino.cz 5,709 CZK (~21 days) / armixx.com 224",
        source="https://www.sanitino.cz/grohe-eurostyle-cosmopolitan-pakova-drezova-baterie-chrom-31170000",
        note="202 tall, reaches 226 - to the middle of the bowl from beside it. The tap lifts off "
             "its base for driving (a 30 mm stub stays). 3/8 inch hoses: 12 mm push-fit adapters. "
             "Minimum pressure not published. Cheaper: Reich Linnea L (200 tall, reach 160 - "
             "short), 109; Comet London folds flat, 18, reach 145",
        status="proposed"),
    "alb-nano": dict(
        name="Alb Filter Nano under-sink set, 0.1 micron hollow fibre", kind="filter",
        outer=(120, 69, 69), micron=0.1, weight_kg=0.5, price_eur=(170, 170),
        shop="alb-filter.com", source="https://alb-filter.com/products/alb-filter-nano-untertisch-komplett-set",
        note="certified ASTM F838-15A, 99.999 % of bacteria. Cartridge 5,000-7,000 L or 6 months, "
             "59.90. Needs ~75 x 75 x 260 with its couplings. No carbon - add the Active stage "
             "(Fusion, ~320 long) for taste. Flow at 1.4 bar not published: ask or test. On the "
             "cold line to the drinking tap only",
        status="proposed"),
    "its-fil-1weg-kurz": dict(
        name="its-wasser.de 'Fil 1-Weg 1/4 kurz', drinking-water tap", kind="filtertap",
        outer=(50, 120, 250), hole=12, weight_kg=None, price_eur=(109, 109), shop="its-wasser.de",
        source="https://www.its-wasser.de/wasserhaehne-wasserhaehne-61-61.html",
        note="item Fil-1Weg 1/4 Edel kurz, swivel spout, 1/4 inch hose. The page says nicht fur "
        "Arbeitsplatte geeignet - ask. Spout outlet ~228 above the worktop; check the "
        "total height (limit 250) and the reach (needs >= ~180 to pour into the bowl) before buying", status="proposed"),
    "tefal-of4448": dict(
        name="Tefal Optimo OF4448 mini oven 19 L, hot air", kind="oven",
        outer=(462, 318, 288), power_w=1380, volume_l=19, weight_kg=4.8,
        price_eur=(100, 100), shop="zbozi.cz (from 2,497 CZK)",
        source="https://www.mironet.cz/tefal-of444834-elektricka-trouba-prikon-1380-w-objem-19-l+dp754085/",
        note="a countertop oven built in: leave air space round it", status="proposed"),
    "electrolux-emz421mmw": dict(
        name="Electrolux EMZ421MMW, 20 L microwave + grill", kind="oven",
        outer=(442, 345, 262), power_w=1270, volume_l=20, weight_kg=11.5,
        price_eur=(138, 138), shop="borovec-elektro.cz (3,460 CZK)",
        source="https://www.borovec-elektro.cz/p/electrolux-emz421mmw",
        note="fits the old 450 x 350 slot; a microwave with grill, no hot air", status="option"),
    # --- awning (added 2026-09-24) ---------------------------------------------------------
    "thule-omnistor-6300-325": dict(
        name="Thule Omnistor 6300 roof awning 3.25 x 2.50", kind="awning",
        outer=(3250, 250, None), weight_kg=25.1, price_eur=None,
        shop="thule.com; Crafter H3 2017+ adapter Thule 301768 (camping-factory.com)",
        source="https://www.thule.com/de-de/awnings/manual-awnings/thule-omnistor-6300-325x250-_-302230",
        note="on the passenger side, over the sliding door; counts toward the 150 kg roof load",
        status="option"),
    "fiamma-f80s-320": dict(
        name="Fiamma F80S 320 roof awning, 3.2 m, projection 2.5 m", kind="awning",
        outer=(3200, 250, None), weight_kg=29.0, price_eur=None,
        shop="Crafter 2017+ bracket kit 98655Z058 (justkampers.com)",
        source="https://www.offroadaccessoires.ch/de/markise/1004-1012-fiamma-f80s-320-cm-dachmarkise-fuer-vans-und-wohnmobile.html",
        note="4 kg heavier than the Thule", status="option"),
    # --- power (chosen 2026-09-25: 3 panels, 50 A DC-DC, lean use) ------------------------
    "starlink-mini": dict(
        name="Starlink Mini", kind="internet", outer=(299, 259, 39), power_w=(25, 40),
        weight_kg=1.10, price_eur=None, shop="starlink.com",
        source="https://starlink.com/public-files/specification_sheet_mini.pdf",
        note="replaces the Standard (75-100 W, 2.9 kg): -0.6 kWh on a working day", status="chosen"),
    "orion-xs-50": dict(
        name="Victron Orion XS 12/12-50A DC-DC charger", kind="dcdc", current_a=50,
        outer=(137, 123, 40), efficiency=0.985, weight_kg=0.33, price_eur=(233, 233),
        shop="geizhals.de (from)",
        source="https://www.victronenergy.com/upload/documents/Orion_XS_12-12-50A_DC-DC_battery_charger/124067-Orion_XS_DC-DC_battery_charger-pdf-en.pdf",
        note="0.67 kWh per hour of driving; the Crafter's alternator is 140-230 A (VW). A Euro 6 "
             "smart alternator can drop to ~12.6 V while driving and the Orion then thinks the "
             "engine is off - wire an ignition / D+ engine-running signal to it from the start",
        status="proposed"),
    # --- electrics, researched 2026-09-25 ---------------------------------------------------
    "ective-lc150-lt": dict(
        name="Ective LC 150 LT, 12 V 150 Ah LiFePO4 (heated, Bluetooth BMS)", kind="battery",
        outer=(353, 175, 190), current_a=150, weight_kg=15.5, price_eur=(1109, 1199),
        shop="ective.de 1,109 (sold out) / vandalierer.com 1,199",
        source="https://www.ective.de/mediafiles/Datenblatt/ective/LC-BT-LT/Ective-LC-150-BT%2BLT-EN.pdf",
        note="LT = heating plates, charges down to -30 C. Two of them (300 Ah). One LC 300L LT "
             "(520 x 268 x 228, 37.5 kg, ~1,485) is cheaper but 6.5 kg heavier and does not fit",
        status="proposed"),
    "multiplus-c-12-2000": dict(
        name="Victron MultiPlus C 12/2000/80-30 inverter / charger", kind="inverter",
        outer=(520, 255, 125), power_w=(1600, 1400), idle_w=(9, 7, 3), charger_a=80,
        weight_kg=12.0, price_eur=(975, 1145), shop="bau-tech.shop 975 / heureka.cz ~28,612 CZK",
        source="https://www.victronenergy.com/upload/documents/Datasheet-MultiPlus-inverter-charger-800VA-5kVA-EN.pdf",
        note="1600 W at 25 C, 1400 at 40 C - the smallest that runs the 1380 W oven (the 12/1600 "
             "gives 1300). Idle 9 / AES 7 / search 3 W. Size: datasheet 520 x 255 x 125, shops "
             "375 x 214 x 110 - check before building; the model uses the larger",
        status="proposed"),
    "multiplus-12-3000": dict(
        name="Victron MultiPlus 12/3000/120-16", kind="inverter", outer=(364, 295, 221),
        power_w=(2400, 2200), idle_w=(20, 15, 8), charger_a=120, weight_kg=18.0,
        price_eur=(1094, 1094), shop="bau-tech.shop",
        source="https://www.victronenergy.com/upload/documents/Datasheet-MultiPlus-inverter-charger-800VA-5kVA-EN.pdf",
        note="the v2 choice, sized for induction cooking - not needed on full gas", status="option"),
    "smartsolar-100-30": dict(
        name="Victron SmartSolar MPPT 100/30", kind="mppt", outer=(130, 186, 70), current_a=30,
        weight_kg=1.3, price_eur=(86, 120), shop="geizhals.de (from)",
        source="https://www.victronenergy.com/upload/documents/Datasheet-SmartSolar-charge-controller-MPPT-100-30-&-100-50-EN.pdf",
        note="440 W at 12 V - enough for 2 x 185 W. Panels in series (Voc ~48 V, ~56 V in cold)",
        status="proposed"),
    "victron-185w": dict(
        name="Victron BlueSolar 185 W-12 V mono panel (SPM041851200)", kind="solar",
        outer=(1485, 668, 30), vmp=19.68, voc=24.11, isc=9.91, weight_kg=11.0,
        price_eur=None, shop=None,
        source="https://www.victronenergy.com/upload/documents/Datasheet-BlueSolar-Monocrystalline-Panels-EN.pdf",
        status="proposed"),
    "smartshunt-500": dict(
        name="Victron SmartShunt 500A battery monitor", kind="monitor", outer=(46, 120, 54),
        weight_kg=0.2, price_eur=(71, 82), shop="geizhals.de (from)",
        source="https://www.victronenergy.com/upload/documents/Datasheet-SmartShunt-EN.pdf",
        note="no Cerbo GX for now (from ~161): we lose one screen for all, VRM remote history and "
             "DVCC. The app still reads each device over Bluetooth. Can be added later",
        status="proposed"),
    "shore-230v": dict(
        name="CEE 16 A caravan inlet with lid + IP65 box, 2-pole RCD + 2 MCB", kind="shore",
        outer=(150, 100, 100), weight_kg=0.95, price_eur=(120, 220),
        shop="anhaenger-ersatzteile24.de 12.90 (inlet) / tigerexped.de 78-203 (box)",
        source="https://www.tigerexped.de/1pn-2pn-small-distribution",
        note="2-pole: on campsites you cannot trust which wire is live", status="proposed"),
    # --- water, researched 2026-09-25 -------------------------------------------------------
    "fresh-tank-custom": dict(
        name="Fresh water tank made to size, food-safe PE", kind="tank",
        outer=(1020, 374, 310), litres=108, weight_kg=8.0, price_eur=(200, 500),
        shop="vanready.de (to drawing) / leto.de (from 500) / DL Kunststofftechnik (~200 net, forum)",
        source="https://www.vanready.de/frischwasser-abwassertank-fuer-camper-und-wohnmobil-massanfertigung-nach-zeichnung",
        note="no catalogue tank fits 374 wide at ~100 L (Reimo 100 L is 480 wide, Varile 120 L "
             "1150 x 400). Fittings: filler 1 1/2, vent 1/2 led above the filler, pump outlet and "
             "drain valve at the low end, sensor port, cleaning lid 120-160",
        status="proposed"),
    "grey-tank-custom": dict(
        name="Grey water tank made to size, PE, flat", kind="tank",
        outer=(880, 600, 180), litres=85, weight_kg=8.0, price_eur=(200, 500),
        shop="same makers as the fresh tank",
        source="https://leto.de/grauwassertank-wohnmobil/",
        note="closest catalogue tank: Varile NEO 80 L, 800 x 600 x 200, 7.2 kg, ~90 - 20 too "
             "tall (would lift the footwell 20). Outlet >= 3/4 at the low point, ball valve, "
             "pipe down through the floor",
        status="proposed"),
    "shurflo-trailking-7": dict(
        name="Shurflo Trail King 7 (2095-204-412), 12 V diaphragm pump", kind="pump",
        outer=(197, 127, 113), flow_l_min=6.8, bar=1.4, current_a=3.3, weight_kg=2.3,
        price_eur=(151, 151), shop="e-flow.cz 3,781 CZK",
        source="https://www.e-flow.cz/shurflo-2095-204-412-membranove-cerpadlo-6-8-l-min-1-4-bar-12-v-dc-pp-sp-epdm-ps-p3765/",
        note="quiet, proven. For a stronger shower: Seaflo 42 series 11.3 l/min, 3.8 bar, 7 A",
        status="proposed"),
    "whale-gulper-220": dict(
        name="Whale Gulper 220 (BP1552) shower drain pump", kind="pump",
        outer=(273, 133, 114), flow_l_min=14, current_a=4.0, weight_kg=1.5,
        price_eur=(218, 218), shop="comptoirnautique.com",
        source="https://en.comptoirnautique.com/waste-water-pump/37795-whale-gulper-220-electric-grey-water-pump-12v-14-l-min.html",
        note="shower tray -> grey tank, on a switch; runs dry, takes hair and soap", status="proposed"),
    "votronic-levels": dict(
        name="Votronic tank electrodes 15-50 K (5545, fresh) + 12-24 K (5543, grey) + displays",
        kind="sensor", weight_kg=0.4, price_eur=(180, 200), shop="schnell-und-sicher-handelskontor.de",
        source="https://www.votronic.de/en/tank-sensor-fl/",
        note="the FL sender needs a 300+ tank - too tall for grey. Both use a PG29 fitting",
        status="proposed"),
    # --- bigger fridge options (asked 2026-09-25) --------------------------------------------
    # Up to ~835 is free above the fridge base (the hob wants 65 under the worktop), so a
    # taller fridge fits if it stands low.
    "vitrifrigo-c95l": dict(
        name="Vitrifrigo C95L, compressor, hinged door", kind="fridge",
        outer=(485, 473, 792), volume_l=95, freezer_l=12.8, weight_kg=22.3,
        price_eur=None, shop="prokes-auto.com",
        source="https://www.vitrifrigo.com/en_en/fridge-freezer-c95l-chr-black",
        note="+10 L and a real 12.8 L freezer; 792 tall - its base must sit at ~40 to stay "
             "under 835: 3 mm to spare, check on the real carcass", status="chosen"),
    "isotherm-cruise-100": dict(
        name="Isotherm Cruise 100 Elegance, compressor, hinged door", kind="fridge",
        outer=(487, 455, 746), volume_l=100, freezer_l=5, weight_kg=26.0,
        price_eur=None, shop=None,
        source="https://www.indelwebastomarine.com/int/products/product/show/cruise-100/",
        note="+15 L, same family as the Cruise 85; +4 kg; plenty of height margin", status="option"),
    # --- gas, if cooking and hot water switch (asked 2026-09-25) ------------------------------
    "truma-b10": dict(
        name="Truma Boiler B10, gas water heater 10 L", kind="water heater",
        outer=(350, 350, 260), power_w=1500, gas_g_h=120, weight_kg=6.7, price_eur=None,
        shop=None, source="https://www.truma.com/products/water-systems/boiler-gas-electro/boiler-gas-boiler-gas-elektro/",
        note="needs a wall flue (one more hole) and the gas installation; replaces the calorifier",
        status="chosen"),
    # --- tarp instead of an awning (asked 2026-09-25) ----------------------------------------
    "yourgear-tarp-3x24": dict(
        name="yourGEAR caravan tarp 3 x 2.4 m, keder 7 / 5 mm, 3 poles", kind="awning",
        outer=(3000, 2400, None), weight_kg=2.9, price_eur=None, shop="your-gear.de",
        source="https://your-gear.de/your-gear-wohnwagen-sonnensegel-caravan-tarp-3-x-2-4-m-sonnendach-inkl.-aufstellstangen-5000-mm",
        note="slides into a keder rail along the roof edge; 5000 mm water column, UV 50+; "
             "poles, guy lines and pegs included. 4 x 2.4 m: 3.4 kg",
        status="chosen"),
    # --- full gas (chosen 2026-09-25) -------------------------------------------------------
    "thetford-topline-922": dict(
        name="Thetford Topline 922 (SHB92290Z), 2-burner gas hob for vehicles", kind="hob",
        outer=(305, 500, 95), cutout=(285, 485), power_kw=(1.5, 1.5), gas_g_h=216,
        weight_kg=5.5, price_eur=(359, 508), shop="stavbakaravanu.cz 12,690 CZK / reimo.com 359",
        source="https://www.thetford.com/au/products-and-support/topline-hob-922-gas-only/",
        note="LPG 30 mbar from the factory; flame failure on both burners; 12 V ignition (no "
             "inverter needed); no lid. Frankana lists it discontinued - buy soon. Depth under "
             "the worktop not published: check before cutting",
        status="chosen"),
    "bosch-prb3a6b70": dict(
        name="Bosch PRB3A6B70 Serie 8, domino gas hob 30 cm", kind="hob",
        outer=(306, 527, 47), cutout=(270, 490), power_kw=(1.9, 2.8), weight_kg=7.0,
        price_eur=(465, 465), shop="elektroshock.cz 11,628 CZK",
        source="https://media3.bosch-home.com/Documents/specsheet/en-GB/PRB3A6B70.pdf",
        note="a home appliance: set for natural gas, LPG jets included (Bosch service changes "
             "them); 230 V ignition; only 47 high. Check the CZ gas inspection accepts it",
        status="option"),
    "gas-bottle-6kg": dict(
        name="6 kg refillable LPG bottle", kind="gas", outer=(256, 256, 495),
        weight_kg=14.3, price_eur=None, shop=None,
        source="https://www.elgas.com.au/elgas-knowledge-hub/residential-lpg/lpg-gas-bottle-sizes-gas-bottle-dimension-measurements/",
        note="full: ~8.3 kg tare (typical steel) + 6 kg gas; composite ones are lighter. An 11 kg "
             "bottle is ~580 tall and does not fit under the 570 garage. ~210 g a day -> ~4 weeks",
        status="chosen"),
    "water-filler": dict(
        name="Lockable fresh water filler, marked WATER, ~60 mm", kind="filler",
        weight_kg=0.3, price_eur=(30, 60), shop=None, source=None,
        note="passenger side behind the arch, above the tank; the tank also needs a vent / "
             "overflow hose through the floor", status="chosen"),
}


def cut(key, side_or_none, a0, b0):
    """A product's cut-out placed at (a0, b0): a window as (side, x0, x1, z0, z1), a roof
    cut-out (side None) as (x0, x1, y0, y1)."""
    w, h = PRODUCTS[key]["cutout"]
    if side_or_none is None:
        return (a0, a0 + w, b0, b0 + h)
    return (side_or_none, a0, a0 + w, b0, b0 + h)
