from dataclasses import dataclass


@dataclass(frozen=True)
class PricingBand:
    code: str
    label: str
    margen_base_pct: float   # 30,29,28...
    redondeo: int            # 50,10,10,10,10,5