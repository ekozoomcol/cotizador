from typing import Dict, Any, List

from app.bags.base import BagCalculator
from app.config import FixedCosts
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

    def compute(self, inputs: QuoteInputs, fixed_costs: FixedCosts, material: Material) -> Dict[str, Any]:
        # ==========================
        # (1) cm -> m  (C5..C11)
        # ==========================
        C5 = inputs.ancho_cm / 100.0
        C6 = inputs.alto_cm / 100.0
        C7 = inputs.fuelle_cm / 100.0
        C8 = inputs.manija1_cm / 100.0
        C9 = inputs.manija2_cm / 100.0
        C10 = inputs.ancho_manijas_cm / 100.0
        C11 = inputs.dobles_cm / 100.0

        # ==========================
        # (2) Áreas (C13..C17)
        # ==========================
        C13 = (C8 + C9) * C10              # Area 2 Manijas
        C14 = C5 * C6                      # Area Frente
        C15 = C11 * C5 * 2                 # Area Dobles (m^2)
        C16 = C6 * C5                      # Area Atrás
        C17 = C13 + C14 + C15 + C16        # AREA TOTAL

        # ==========================
        # (3) Alto rollo / sobrantes (espejo a tu bloque)
        # ==========================
        # E5 = B6*2 + B7 + B11*2   (en cm)
        E5 = inputs.alto_cm * 2 + inputs.fuelle_cm + inputs.dobles_cm * 2

        # D? sobrantes 1,6: =160 - E5 (cm)
        sobrantes_cm = 160 - E5

        # F5 saldo rollo: =(160-(E5*2)) (cm)
        F5 = 160 - (E5 * 2)

        # ==========================
        # (4) Variables auxiliares del bloque que vimos:
        # E8 = F8*C5  (m2) donde F8 = E8/100 en tu hoja, pero ahí hay mezcla de celdas.
        # Para mantener espejo sin inventar demasiado: tratamos E8 como "alto rollo en m" * ancho en m
        # y lo usaremos solo en el SI(...) del TELA como tu hoja hace con E8<38.
        # OJO: si tú confirmas qué es exactamente E8 en tu hoja, aquí se ajusta 1 línea.
        E8_m2_proxy = (E5 / 100.0) * C5

        # ==========================
        # (5) TELA (C19) espejo:
        # C19 = SI(E8<38; ((C17*C2/B2)+F11); C17*C2/B2)
        # Aquí no tenemos B2 (en tu captura B2 era m2=1,6). Lo tratamos como factor_rendimiento_m2 = 1.6
        # y C2 = costo_por_m2 material.
        # ==========================
        B2_factor_rendimiento = 1.6  # de tu hoja (m2 1,6)
        fijo_F11 = inputs.fijo_F11 if inputs.fijo_F11 is not None else 0.0
        umbral_E8 = inputs.umbral_E8 if inputs.umbral_E8 is not None else 38.0

        base_tela = (C17 * material.costo_por_m2 / B2_factor_rendimiento)
        C19 = (base_tela + fijo_F11) if (E8_m2_proxy < umbral_E8) else base_tela

        # ==========================
        # (6) Costos fijos globales (C24)
        # ==========================
        C24 = fixed_costs.total

        # ==========================
        # (7) Desperdicio tela (por banda) – en tu hoja es algo tipo "*1,15" + $C$19 * ...
        # Aquí lo dejamos espejo pero parametrizable:
        # desperdicio_cost = C19 * (desperdicio_multiplicador_por_banda)
        # Como en tu Excel esto depende de B26..F26, lo dejamos como factores editables:
        # ==========================
        desperdicio_factor = 1.15

        # Estos factores son el equivalente conceptual de B26..G26.
        # Ajusta aquí si en tu hoja cada banda cambia (ej: por eficiencia).
        desperdicio_mult_por_banda = {
            "B100_200": 1.0,
            "B300_450": 1.0,
            "B500_1000": 1.0,
            "B1100_5000": 1.0,
            "B5500_10000": 1.0,
            "B11000P": 1.0,
        }

        # ==========================
        # (8) Operarios por banda (B29..B32 etc.)
        # En tu hoja se ve fórmula base:
        # =21+(($B$5+$B$6)/25)
        # y multiplicadores 1,2 o 1,3 según banda.
        # ==========================
        base_operario = 21 + ((inputs.ancho_cm + inputs.alto_cm) / 25.0)

        # Multiplicadores por banda (puedes editar sin tocar la estructura):
        oper_mult = {
            "B100_200":   [1.2, 1.2, 1.2, 1.2],
            "B300_450":   [1.3, 1.3, 1.3, 1.3],
            "B500_1000":  [1.3, 1.3, 1.3, 1.3],
            "B1100_5000": [1.3, 1.3, 1.3, 1.3],
            "B5500_10000":[1.3, 1.3, 1.3, 1.3],
            "B11000P":    [1.3, 1.3, 1.3, 1.3],
        }

        # ==========================
        # (9) Total costos + costo real por banda
        # Total_costos = C24 + SUMA(operarios) + desperdicio
        # Costo_real = Total_costos + (5$)  (en tu hoja: B39 = B34 + B37)
        # "5$" depende de "1$" (fila 36) *5.
        # En tu hoja el "1$" verde lo vimos en la última banda:
        # =MIN(MAX(F29; (($B$5*1+$B$6*1)-25)); F29*1,6)
        # Lo aplicamos por banda con un comportamiento espejo:
        # - default: 1usd = base_operario (o el operario1) con límites
        # - 5usd = 1usd*5
        # ==========================
        costs_by_band: Dict[str, Any] = {}

        for b in self.BAND_ORDER:
            mults = oper_mult[b]
            op_vals = [base_operario * m for m in mults]  # 4 operarios

            # desperdicio tela espejo: (C19 * desperdicio_factor) * mult_banda
            desperdicio_cost = (C19 * desperdicio_factor) * desperdicio_mult_por_banda[b]

            total_costos = C24 + sum(op_vals) + desperdicio_cost

            # 1$ / 5$ (modo espejo con tu fórmula verde)
            # Excel verde: MIN(MAX(F29; ((B5+B6)-25)); F29*1,6)
            # Donde F29 es Operario1 (o la celda base).
            op1 = op_vals[0]
            uno_usd = min(
                max(op1, (inputs.ancho_cm + inputs.alto_cm) - 25),
                op1 * 1.6
            )
            cinco_usd = uno_usd * 5

            costo_real = total_costos + cinco_usd

            costs_by_band[b] = {
                "operarios": {
                    "op1": round(op_vals[0], 6),
                    "op2": round(op_vals[1], 6),
                    "op3": round(op_vals[2], 6),
                    "op4": round(op_vals[3], 6),
                    "base_operario": round(base_operario, 6),
                    "mults": mults,
                },
                "desperdicio_cost": round(desperdicio_cost, 6),
                "total_costos": round(total_costos, 6),
                "uno_usd": round(uno_usd, 6),
                "cinco_usd": round(cinco_usd, 6),
                "costo_real": round(costo_real, 6),
            }

        # ==========================
        # (10) Preview SVG simple para orientación (anti 40x30 vs 30x40)
        # ==========================
        svg = self._svg_preview(inputs.ancho_cm, inputs.alto_cm, inputs.fuelle_cm)

        excel_vars = {
            "C5_ancho_m": C5,
            "C6_alto_m": C6,
            "C7_fuelle_m": C7,
            "C8_manija1_m": C8,
            "C9_manija2_m": C9,
            "C10_ancho_manijas_m": C10,
            "C11_dobles_m": C11,
            "C13_area_2_manijas": C13,
            "C14_area_frente": C14,
            "C15_area_dobles": C15,
            "C16_area_atras": C16,
            "C17_area_total": C17,
            "C19_tela": C19,
            "C24_costos_fijos": C24,
            "E5_alto_rollo_cm": E5,
            "sobrantes_cm_160_menos_E5": sobrantes_cm,
            "F5_saldo_rollo_cm": F5,
            "E8_m2_proxy": E8_m2_proxy,
            "material_costo_por_m2": material.costo_por_m2,
            "B2_factor_rendimiento": B2_factor_rendimiento,
            "umbral_E8": umbral_E8,
            "fijo_F11": fijo_F11,
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