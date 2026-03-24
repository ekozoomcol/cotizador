from app.bags.registry import get_bag
from app.config import default_config
from app.models import QuoteInputs
from app.pricing.discounts import DiscountsConfig


def quote(bag_type: str, material_code: str, inputs: dict):
    """
    Unifica la respuesta del backend con el formato esperado por el frontend:
    - breakdown
    - costs_by_band
    - prices_by_band_before_iva
    - prices_by_band_with_iva
    - svg_preview
    """
    cfg = default_config()
    bag = get_bag(bag_type)
    material = cfg.materials.by_code.get(material_code)
    if material is None:
        raise ValueError(f"Material no existe: {material_code}")

    normalized_inputs = dict(inputs or {})
    # El frontend puede no mandar cantidad; para cálculo visual usamos 1.
    cantidad = float(normalized_inputs.get("cantidad", 1) or 1)
    normalized_inputs["cantidad"] = cantidad

    quote_inputs = QuoteInputs(**normalized_inputs)
    raw = bag.compute(quote_inputs, config=cfg, material=material)

    breakdown = dict(raw.get("excel", {}))
    costs_by_band = raw.get("costs_by_band", {})
    svg_preview = raw.get("svg_preview")

    discounts = DiscountsConfig()
    E5 = float(breakdown.get("E5_alto_rollo_cm", 0) or 0)
    F5 = float(breakdown.get("F5_saldo_rollo_cm", 0) or 0)
    P2 = float(cfg.cola_produccion_global)
    dto_l49 = float(discounts.dto_final_L49(E5, F5, P2))
    breakdown["L49_dto_final_pct"] = dto_l49

    prices_before = {}
    prices_with_iva = {}
    for band in cfg.bands:
        cost_row = costs_by_band.get(band.code, {})
        # Usar exactamente el precio_final y rentabilidad_pct computados desde la lógica de Excel
        # Si por alguna razón cost_row no lo tiene, regresamos 0.
        unit_before = float(cost_row.get("precio_final", 0))
        rentabilidad = float(cost_row.get("rentabilidad_pct", 30))
        
        unit_with_iva = round(unit_before * 1.19)

        prices_before[band.code] = {
            "label": band.label,
            "margen_base_pct": rentabilidad,
            "dto_L49_pct": dto_l49, # ya no se usa L49 pero el front lo espera
            "margen_real_pct": rentabilidad,
            "precio_unitario_sin_iva": int(round(unit_before)),
            "is_public": band.is_public
        }
        prices_with_iva[band.code] = {
            "label": band.label,
            "precio_unitario_con_iva": int(unit_with_iva),
            "is_public": band.is_public
        }

    # Determinar chosen_band_code
    chosen_band_code = cfg.bands[0].code # Default
    for band in cfg.bands:
        # Simplistic parsing of min_qty from label (like "500-1000")
        import re
        match = re.search(r'\d+', band.label)
        if match:
            min_val = int(match.group())
            if cantidad >= min_val:
                chosen_band_code = band.code

    return {
        "bag_type": bag_type,
        "material_code": material_code,
        "chosen_band_code": chosen_band_code,
        "breakdown": breakdown,
        "costs_by_band": costs_by_band,
        "prices_by_band_before_iva": prices_before,
        "prices_by_band_with_iva": prices_with_iva,
        "svg_preview": svg_preview,
    }