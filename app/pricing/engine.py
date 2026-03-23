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
    raw = bag.compute(quote_inputs, fixed_costs=cfg.fixed_costs, material=material)

    breakdown = dict(raw.get("excel", {}))
    costs_by_band = raw.get("costs_by_band", {})
    svg_preview = raw.get("svg_preview")

    discounts = DiscountsConfig()
    E5 = float(breakdown.get("E5_alto_rollo_cm", 0) or 0)
    F5 = float(breakdown.get("F5_saldo_rollo_cm", 0) or 0)
    P2 = float(normalized_inputs.get("cola_produccion", 0) or 0)
    dto_l49 = float(discounts.dto_final_L49(E5, F5, P2))
    breakdown["L49_dto_final_pct"] = dto_l49

    prices_before = {}
    prices_with_iva = {}
    for band in cfg.bands:
        cost_row = costs_by_band.get(band.code, {})
        costo_real = float(cost_row.get("costo_real", 0) or 0)

        margen_base = float(band.margen_base_pct)
        margen_real = max(0.0, margen_base - dto_l49 - float(cfg.extra_global_discount_pct))

        unit_before = costo_real * (1 + margen_real / 100.0)
        if band.redondeo > 0:
            unit_before = round(unit_before / band.redondeo) * band.redondeo
        unit_with_iva = round(unit_before * 1.19)

        prices_before[band.code] = {
            "label": band.label,
            "margen_base_pct": margen_base,
            "dto_L49_pct": dto_l49,
            "margen_real_pct": margen_real,
            "precio_unitario_sin_iva": int(round(unit_before)),
        }
        prices_with_iva[band.code] = {
            "label": band.label,
            "precio_unitario_con_iva": int(unit_with_iva),
        }

    return {
        "bag_type": bag_type,
        "material_code": material_code,
        "breakdown": breakdown,
        "costs_by_band": costs_by_band,
        "prices_by_band_before_iva": prices_before,
        "prices_by_band_with_iva": prices_with_iva,
        "svg_preview": svg_preview,
    }