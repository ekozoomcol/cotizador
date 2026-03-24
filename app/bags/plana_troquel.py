from typing import Dict, Any

from app.bags.plana_manija import PlanaManijaCalculator
from app.models import QuoteInputs
from app.config import GlobalConfig
from app.pricing.materials import Material

class PlanaTroquelCalculator(PlanaManijaCalculator):
    """
    BOLSA PLANA TROQUEL:
    “se descuenta la tela de la manija que no tiene”
    Desperdicio multiplier is 1.2 instead of 1.15.
    """

    def compute(self, inputs: QuoteInputs, config: GlobalConfig, material: Material) -> Dict[str, Any]:
        import math

        B5 = float(inputs.ancho_cm)
        B6 = float(inputs.alto_cm)
        B7 = float(inputs.fuelle_cm)
        # B8 is dobles in Troquel, but in QuoteInputs it's dobles_cm
        B8 = float(inputs.dobles_cm)

        C5 = B5 / 100.0
        C6 = B6 / 100.0
        C7 = B7 / 100.0
        C8 = B8 / 100.0

        C2 = float(material.costo_por_m2)
        B2 = 1.6  

        # Regla Global de Produccion Maxima
        if (B5 + B6) < 40:
            F4 = 8000
        elif (B5 + B6) < 60:
            F4 = 7000
        else:
            F4 = 6000

        # G4 = Nomina Diaria (global)
        G4 = float(config.nomina_diaria)

        E5 = (B6 * 2) + B7 + (B8 * 2)
        F5 = 160 - (E5 * 2)

        E8 = 160 - E5

        C10 = C5 * C6
        C11 = C8 * C5 * 2
        C12 = C6 * C5
        C13 = C10 + C11 + C12  # Area total, sin manijas

        base_tela = C13 * C2 / B2
        C24 = base_tela

        # Desperdicio Tela (Troquel tenía factor 1.2 vs 1.15; mantengamos la curva un poco más alta o plano 10%)
        # El user dice "Usa todas las variables de ahora... usa solo la información de este ultimo excel"
        # Since the excel only has Plana Manija with 10%, we will apply exactly the same 10% to Troquel
        # as a monolithic base update, unless specified otherwise.
        C25 = C24 * 0.1
        C26 = C24 + C25

        C32 = float(config.fixed_costs.total)
        C34 = G4 / F4
        C36 = C34 + C32 + C26

        costs_by_band = {}
        for b in config.bands:
            rentabilidad = float(b.margen_base_pct)
            if config.cola_produccion_global < 50000:
                rentabilidad -= 3.0
                
            denom = 1.0 - (rentabilidad / 100.0)
            if denom <= 0: denom = 0.01
            
            p_final = math.ceil(C36 / denom / float(b.redondeo)) * b.redondeo
            
            costs_by_band[b.code] = {
                "operarios": {"base_operario": C34, "sum_op": 0},
                "desperdicio_cost": C25,
                "total_costos": C36,
                "uno_usd": 0,
                "cinco_usd": 0,
                "costo_real": C36,
                "rentabilidad_pct": rentabilidad,
                "precio_final": p_final
            }

        svg = self._svg_preview(B5, B6, B7)

        excel_vars = {
            "C5_ancho_m": C5,
            "C6_alto_m": C6,
            "C7_fuelle_m": C7,
            "C8_manija1_m": 0,
            "C9_manija2_m": 0,
            "C10_ancho_manijas_m": 0,
            "C11_dobles_m": C8, 
            "C13_area_2_manijas": 0,
            "C14_area_frente": C10,
            "C15_area_dobles": C11,
            "C16_area_atras": C12,
            "C17_area_total": C13,
            "C24_tela": C24,
            "C25_desperdicio": C25,
            "C26_total_tela": C26,
            "C32_gastos_fijos": C32,
            "C34_operarios_oficina": C34,
            "C36_total_costos": C36,
            "E5_alto_rollo_cm": E5,
            "F5_saldo_rollo_cm": F5,
            "E8_m2_proxy": E8,
            "material_costo_por_m2": C2,
            "B2_factor_rendimiento": B2,
            "sobrantes_cm_160_menos_E5": E8
        }

        return {
            "excel": excel_vars,
            "costs_by_band": costs_by_band,
            "svg_preview": svg,
        }