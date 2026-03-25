import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.pricing.engine import quote

try:
    res = quote("PLANA_MANIJA", "CAMBREL_70", {
        "ancho_cm": 34, "alto_cm": 40, "fuelle_cm": 0, "manija1_cm": 60, "manija2_cm": 60, 
        "ancho_manijas_cm": 5, "dobles_cm": 3, "caras": 1, "tintas": 1
    })
    print("SUCCESS")
    print("Precios sin IVA:", [v["precio_unitario_sin_iva"] for v in res["prices_by_band_before_iva"].values()])
except Exception as e:
    import traceback
    traceback.print_exc()
