import math
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
    try:
        cfg = default_config()
        bag = get_bag(bag_type)
        material = cfg.materials.by_code.get(material_code)
        if material is None:
            return {"error": f"Material no existe: {material_code}", "status": "error"}

        normalized_inputs = dict(inputs or {})
        # El frontend puede no mandar cantidad; para cálculo visual usamos 1.
        cantidad = float(normalized_inputs.get("cantidad", 1) or 1)
        normalized_inputs["cantidad"] = cantidad

        quote_inputs = QuoteInputs(**normalized_inputs)
        
        # Calcular total de pasadas (Serigrafía)
        total_pasadas = 0
        costo_dtf_unitario = 0.0
        
        if quote_inputs.print_type == "DTF":
            # Lógica DTF: 5800 cm2 por metro ($22.500) + $400 operario
            w_eff = quote_inputs.dtf_ancho_cm + 3.0
            h_eff = quote_inputs.dtf_alto_cm + 3.0
            area_eff = w_eff * h_eff
            if area_eff > 0:
                logos_por_metro = math.floor(5800.0 / area_eff)
                if logos_por_metro < 1: logos_por_metro = 1
                costo_sticker = 22500.0 / logos_por_metro
                costo_dtf_unitario = costo_sticker + 400.0
            total_pasadas = 0 # No hay pasadas en DTF
        else:
            # Lógica Serigrafía existente
            if quote_inputs.caras == 0:
                total_pasadas = 0
            elif quote_inputs.caras == 1:
                total_pasadas = quote_inputs.tintas_c1
            else:
                total_pasadas = quote_inputs.tintas_c1 + quote_inputs.tintas_c2

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
        breakdown["total_pasadas"] = total_pasadas
        breakdown["print_type"] = quote_inputs.print_type
        if quote_inputs.print_type == "DTF":
            breakdown["costo_dtf_por_cara"] = costo_dtf_unitario

        prices_before = {}
        prices_with_iva = {}
        for band in cfg.bands:
            cost_row = costs_by_band.get(band.code, {})
            unit_before = float(cost_row.get("precio_final", 0))
            rentabilidad = float(cost_row.get("rentabilidad_pct", 30))
            
            # Ajuste global por cola de producción (centralizado)
            if cfg.cola_produccion_global < 50000:
                rentabilidad -= 3.0
                # Recalculamos el precio con la nueva rentabilidad ajustada
                c36 = float(cost_row.get("total_costos", 0))
                denom = 1.0 - (rentabilidad / 100.0)
                if denom <= 0: denom = 0.01
                unit_before = math.ceil(c36 / denom / float(band.redondeo)) * band.redondeo
            
            # Adición de Impresión (Serigrafía o DTF)
            if quote_inputs.print_type == "DTF":
                impresion_total = costo_dtf_unitario * quote_inputs.caras
                precio_pasada = 0
                costo_serigrafia_total = 0
            else:
                precio_pasada = cfg.serigrafia_precios.get(band.code, 0)
                costo_serigrafia_total = total_pasadas * precio_pasada
                impresion_total = costo_serigrafia_total
            
            unit_before += impresion_total

            unit_with_iva = round(unit_before * 1.19)

            prices_before[band.code] = {
                "label": band.label,
                "margen_base_pct": rentabilidad,
                "dto_L49_pct": dto_l49,
                "margen_real_pct": rentabilidad,
                "precio_unitario_sin_iva": int(round(unit_before)),
                "costo_serigrafia": int(costo_serigrafia_total),
                "precio_pasada": int(precio_pasada),
                "costo_dtf": int(impresion_total) if quote_inputs.print_type == "DTF" else 0,
                "is_public": band.is_public
            }
            prices_with_iva[band.code] = {
                "label": band.label,
                "precio_unitario_con_iva": int(unit_with_iva),
                "is_public": band.is_public
            }

        chosen_band_code = cfg.bands[0].code
        for band in cfg.bands:
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
    except Exception as e:
        return {"error": str(e), "status": "error"}