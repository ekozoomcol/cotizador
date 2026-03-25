from dataclasses import dataclass
from typing import Dict, List

from app.pricing.materials import MaterialCatalog, Material
from app.pricing.bands import PricingBand

@dataclass(frozen=True)
class FixedCosts:
    maquila_bolsas: float = 25
    luz: float = 50
    agua: float = 10.0
    arriendo: float = 75.0

    @property
    def total(self) -> float:
        return self.maquila_bolsas + self.luz + self.agua + self.arriendo

@dataclass
class GlobalConfig:
    fixed_costs: FixedCosts
    materials: MaterialCatalog
    bands: List[PricingBand]
    cola_produccion_global: float = 5000.0
    nomina_diaria: float = 1500000.0
    extra_global_discount_pct: float = 0.0

def default_config() -> GlobalConfig:
    import json
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ref_file = os.path.join(base_dir, "data", "precios_referencia.json")
    
    cola_produccion_global = 5000.0
    nomina_diaria = 1500000.0
    material_costs = {
        "CAMBREL_70": 1100.0,
        "CAMBREL_80": 1200.0,
        "CAMBREL_90": 1300.0,
    }
    f_costs = {
        "maquila_bolsas": 25.0,
        "luz": 50.0,
        "agua": 10.0,
        "arriendo": 75.0
    }

    if os.path.exists(ref_file):
        try:
            with open(ref_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "material_costs_per_m2" in data:
                material_costs.update(data["material_costs_per_m2"])
            if "fixed_costs" in data:
                f_costs.update(data["fixed_costs"])
            if "cola_produccion_global" in data:
                cola_produccion_global = float(data["cola_produccion_global"])
            if "nomina_diaria" in data:
                nomina_diaria = float(data["nomina_diaria"])
        except Exception as e:
            print("Error loading precios_referencia.json:", e)
            
    # Always write back to ensure newly introduced keys (like nomina_diaria) are visible to the user
    try:
        with open(ref_file, "w", encoding="utf-8") as f:
            json.dump({
                "cola_produccion_global": cola_produccion_global,
                "nomina_diaria": nomina_diaria,
                "material_costs_per_m2": material_costs,
                "fixed_costs": f_costs
            }, f, indent=2)
    except Exception as e:
        print("Error saving precios_referencia.json:", e)

    fixed = FixedCosts(
        maquila_bolsas=float(f_costs.get("maquila_bolsas", 25.0)),
        luz=float(f_costs.get("luz", 50.0)),
        agua=float(f_costs.get("agua", 10.0)),
        arriendo=float(f_costs.get("arriendo", 75.0))
    )

    materials = MaterialCatalog(
        by_code={
            "CAMBREL_70": Material(code="CAMBREL_70", name="Cambrel 70gr", costo_por_m2=float(material_costs.get("CAMBREL_70", 1100.0))),
            "CAMBREL_80": Material(code="CAMBREL_80", name="Cambrel 80gr", costo_por_m2=float(material_costs.get("CAMBREL_80", 1200.0))),
            "CAMBREL_90": Material(code="CAMBREL_90", name="Cambrel 90gr", costo_por_m2=float(material_costs.get("CAMBREL_90", 1300.0))),
        }
    )

    bands = [
        PricingBand(code="B50000P",      label="50000+",     margen_base_pct=25, redondeo=5, is_public=False),
        PricingBand(code="B30000_49999", label="30000-49999",margen_base_pct=26, redondeo=5, is_public=False),
        PricingBand(code="B11000_29999", label="11000-29999",margen_base_pct=27, redondeo=5, is_public=False),
        PricingBand(code="B5500_10999",  label="5500-10999", margen_base_pct=28, redondeo=5, is_public=True),
        PricingBand(code="B1500_5499",   label="1500-5499",  margen_base_pct=33, redondeo=10, is_public=True),
        PricingBand(code="B500_1499",    label="500-1499",   margen_base_pct=38, redondeo=10, is_public=True),
        PricingBand(code="B300_499",     label="300-499",    margen_base_pct=43, redondeo=20, is_public=True),
        PricingBand(code="B200_299",     label="200-299",    margen_base_pct=48, redondeo=20, is_public=True),
    ]

    return GlobalConfig(
        fixed_costs=fixed,
        materials=materials,
        bands=bands,
        cola_produccion_global=cola_produccion_global,
        nomina_diaria=nomina_diaria,
        extra_global_discount_pct=0.0
    )