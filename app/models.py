from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


BagType = Literal["PLANA_MANIJA", "PLANA_TROQUEL"]


class QuoteInputs(BaseModel):
    ancho_cm: float = Field(..., gt=0, le=2000)
    alto_cm: float = Field(..., gt=0, le=2000)
    fuelle_cm: float = Field(0, ge=0, le=1000)

    # Solo aplican a PLANA_MANIJA; para PLANA_TROQUEL se ignoran
    manija1_cm: float = Field(0, ge=0, le=500)
    manija2_cm: float = Field(0, ge=0, le=500)
    ancho_manijas_cm: float = Field(0, ge=0, le=100)

    dobles_cm: float = Field(0, ge=0, le=500)

    caras: int = Field(0, ge=0, le=2)
    tintas: int = Field(0, ge=0, le=10) # Para compatibilidad, seguirá representyando la cantidad de colores (max)
    tintas_c1: int = Field(0, ge=0, le=10)
    tintas_c2: int = Field(0, ge=0, le=10)
    cola_produccion: float = Field(999999, ge=0)

    print_type: str = Field("SERIGRAFIA", max_length=20) # SERIGRAFIA o DTF
    dtf_ancho_cm: float = Field(10, ge=0)
    dtf_alto_cm: float = Field(10, ge=0)

    material_code: str = Field("CAMBREL_70", max_length=100)

    # Parámetros opcionales para afinar “espejo” sin tocar código:
    # (equivalentes a celdas que no estén claras aún)
    fijo_F11: Optional[float] = None
    umbral_E8: Optional[float] = None


class QuoteRequest(BaseModel):
    bag_type: BagType
    inputs: QuoteInputs


class QuoteResponse(BaseModel):
    bag_type: BagType
    material_code: str
    breakdown: Dict[str, Any]
    costs_by_band: Dict[str, Any]
    prices_by_band_before_iva: Dict[str, Any]
    prices_by_band_with_iva: Dict[str, Any]
    svg_preview: Optional[str] = None