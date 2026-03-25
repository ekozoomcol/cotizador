from typing import Dict, Any, List

from app.bags.base import BagCalculator
from app.config import GlobalConfig
from app.models import QuoteInputs
from app.pricing.materials import Material
from app.utils import clamp


class PlanaManijaCalculator(BagCalculator):
    """
    BOLSA PLANA MANIJA (modo espejo)
    Replica:
    - C5..C11 conversiones
    - C13..C17 áreas
    - E5 (alto rollo), F5 (saldo rollo)
    - C19 (TELA) con SI(E8 < umbral; +F11; ...)
    - C24 (fijos)
    - Desperdicio 15%
    - Operarios por banda (parametrizable)
    - Total costos y costo real por banda
    - Ajuste "1$" y "5$" (según tu fórmula verde para la última banda)
    """

    # Bandas: deben calzar con config.py
    BAND_ORDER = ["B100_200","B300_450","B500_1000","B1100_5000","B5500_10000","B11000P"]

    def compute(self, inputs: QuoteInputs, config: GlobalConfig, material: Material) -> Dict[str, Any]:
        import math

        B5 = float(inputs.ancho_cm)
        B6 = float(inputs.alto_cm)
        B7 = float(inputs.fuelle_cm)
        B8 = float(inputs.manija1_cm)
        B9 = float(inputs.manija2_cm)
        B10 = float(inputs.ancho_manijas_cm)
        B11 = float(inputs.dobles_cm)

        C5 = B5 / 100.0
        C6 = B6 / 100.0
        C7 = B7 / 100.0
        C8 = B8 / 100.0
        C9 = B9 / 100.0
        C10 = B10 / 100.0
        C11 = B11 / 100.0

        C2 = float(material.costo_por_m2)
        B2 = 1.6  # Default based on Excel

        # Regla Global de Produccion Maxima
        if (B5 + B6) < 40:
            F4 = 8000
        elif (B5 + B6) < 60:
            F4 = 7000
        else:
            F4 = 6000

        # G4 = Nomina Diaria (global)
        G4 = float(config.nomina_diaria)

        E5 = (B6 * 2) + B7 + (B11 * 2)
        F5 = 160 - (E5 * 2)

        E8 = 160 - E5

        C16 = (C8 + C9) * C10
        C17 = C5 * C6
        C18 = C11 * C5 * 2
        C19 = C6 * C5
        C20 = C16 + C17 + C18 + C19

        base_tela = C20 * C2 / B2
        C24 = base_tela  # La formula de Excel fue simplificada: ya no suma sobrantes si E8 < 38

        # Desperdicio Tela plano 10%
        C25 = C24 * 0.1
        C26 = C24 + C25

        # Gastos fijos (C32)
        C32 = float(config.fixed_costs.total)

        # Operarios + Oficina (C34)
        C34 = G4 / F4

        # Total Costos (C36 monolítico)
        C36 = C34 + C32 + C26

        costs_by_band = {}
        for b in config.bands:
            rentabilidad = float(b.margen_base_pct)
                
            denom = 1.0 - (rentabilidad / 100.0)
            if denom <= 0: denom = 0.01
            
            p_final = math.ceil(C36 / denom / float(b.redondeo)) * b.redondeo
            
            # Map new variables to old frontend expected keys
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
            "C8_manija1_m": C8,
            "C9_manija2_m": C9,
            "C10_ancho_manijas_m": C10,
            "C11_dobles_m": C11,
            "C13_area_2_manijas": C16,
            "C14_area_frente": C17,
            "C15_area_dobles": C18,
            "C16_area_atras": C19,
            "C17_area_total": C20,
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

    def _svg_preview(self, ancho_cm: float, alto_cm: float, fuelle_cm: float) -> str:
        # Simple: rectángulo proporcional + flechas con texto
        # Normalizamos a un canvas 300x260
        W = 300
        H = 260
        pad = 40

        # escala proporcional
        aw = max(ancho_cm, 1)
        ah = max(alto_cm, 1)
        scale = min((W - 2*pad) / aw, (H - 2*pad) / ah)

        rw = aw * scale
        rh = ah * scale
        x = (W - rw) / 2
        y = (H - rh) / 2

        fuelle_txt = f"{fuelle_cm:.0f} cm fuelle" if fuelle_cm and fuelle_cm > 0 else "sin fuelle"

        svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect x="0" y="0" width="{W}" height="{H}" fill="white"/>
  <rect x="{x:.2f}" y="{y:.2f}" width="{rw:.2f}" height="{rh:.2f}" fill="none" stroke="black" stroke-width="2"/>

  <!-- Etiquetas -->
  <text x="{W/2:.2f}" y="22" font-size="14" text-anchor="middle">Preview orientación</text>
  <text x="{W/2:.2f}" y="{H-10}" font-size="12" text-anchor="middle">{fuelle_txt}</text>

  <!-- Flecha ancho -->
  <line x1="{x:.2f}" y1="{y+rh+12:.2f}" x2="{x+rw:.2f}" y2="{y+rh+12:.2f}" stroke="black" stroke-width="2"/>
  <text x="{W/2:.2f}" y="{y+rh+28:.2f}" font-size="12" text-anchor="middle">ANCHO {ancho_cm:.0f} cm</text>

  <!-- Flecha alto -->
  <line x1="{x-12:.2f}" y1="{y:.2f}" x2="{x-12:.2f}" y2="{y+rh:.2f}" stroke="black" stroke-width="2"/>
  <text x="{x-18:.2f}" y="{H/2:.2f}" font-size="12" text-anchor="middle" transform="rotate(-90 {x-18:.2f} {H/2:.2f})">ALTO {alto_cm:.0f} cm</text>
</svg>
""".strip()
        return svg