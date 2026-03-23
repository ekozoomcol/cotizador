from dataclasses import dataclass
from typing import Dict, List

from app.pricing.materials import MaterialCatalog, Material
from app.pricing.bands import PricingBand


@dataclass(frozen=True)
class FixedCosts:
    """
    Costos fijos globales (no repetirlos por tipo de bolsa).
    Equivalente a C20..C23 en tu hoja.
    """
    maquila_bolsas: float = 25
    luz: float = 50
    agua: float = 5
    arriendo: float = 100

    @property
    def total(self) -> float:
        return self.maquila_bolsas + self.luz + self.agua + self.arriendo


@dataclass
class GlobalConfig:
    """
    Config global para todo el cotizador.
    Aquí defines materiales, bandas (tramos), y fijos.
    """
    fixed_costs: FixedCosts
    materials: MaterialCatalog
    bands: List[PricingBand]

    # Ajuste global que en tu Excel se resta en los márgenes: 30 - $L$49 etc.
    # Ojo: en tu Excel L49 se calcula como MAX(H49:K49). Aquí se calcula igual,
    # pero si quieres forzar algo adicional, puedes sumar aquí.
    extra_global_discount_pct: float = 0.0


def default_config() -> GlobalConfig:
    fixed = FixedCosts()

    # Material Cambrel 70gr: el pantallazo muestra C2 = 1100 (por m2).
    # Cambrel 80gr: +100 por m2 (según tu instrucción).
    materials = MaterialCatalog(
        by_code={
            "CAMBREL_70": Material(code="CAMBREL_70", name="Cambrel 70gr", costo_por_m2=1100),
            "CAMBREL_80": Material(code="CAMBREL_80", name="Cambrel 80gr", costo_por_m2=1200),
        }
    )

    bands = [
        PricingBand(code="B100_200",   label="100-200",    margen_base_pct=30, redondeo=50),
        PricingBand(code="B300_450",   label="300-450",    margen_base_pct=29, redondeo=10),
        PricingBand(code="B500_1000",  label="500-1000",   margen_base_pct=28, redondeo=10),
        PricingBand(code="B1100_5000", label="1100-5000",  margen_base_pct=27, redondeo=10),
        PricingBand(code="B5500_10000",label="5500-10000", margen_base_pct=26, redondeo=10),
        PricingBand(code="B11000P",    label="11000+",     margen_base_pct=25, redondeo=5),
    ]

    return GlobalConfig(
        fixed_costs=fixed,
        materials=materials,
        bands=bands,
        extra_global_discount_pct=0.0
    )