import math


def multiplo_superior(valor: float, paso: int) -> float:
    """
    Replica MULTIPLO.SUPERIOR(valor; paso)
    """
    if paso <= 0:
        return float(valor)
    return math.ceil(valor / paso) * paso


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))