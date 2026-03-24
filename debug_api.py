import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.pricing.engine import quote

try:
    res = quote("PLANA_TROQUEL", "CAMBREL_70", {
        "ancho_cm": 35, "alto_cm": 40, "fuelle_cm": 0, "manija1_cm": 60, "manija2_cm": 60, 
        "ancho_manijas_cm": 5, "dobles_cm": 3, "caras": 1, "tintas": 1, "cantidad": 500
    })
    print("MATERIAL COST REVEAL:")
    print(res["breakdown"].get("material_costo_por_m2", "MISSING!"))
    print("C19_tela REVEAL:")
    print(res["breakdown"].get("C19_tela", "MISSING!"))
except Exception as e:
    print(e)
