from typing import Dict, Any

from app.bags.plana_manija import PlanaManijaCalculator
from app.models import QuoteInputs


class PlanaTroquelCalculator(PlanaManijaCalculator):
    """
    BOLSA PLANA TROQUEL:
    “se descuenta la tela de la manija que no tiene”
    => En espejo, la diferencia principal es: Area 2 Manijas = 0
    Reutiliza TODO el motor de PLANA_MANIJA, pero forzando manijas a 0.
    """

    def compute(self, inputs: QuoteInputs, fixed_costs, material) -> Dict[str, Any]:
        # Clonar inputs (sin modificar el objeto original)
        cloned = inputs.model_copy(deep=True)
        cloned.manija1_cm = 0
        cloned.manija2_cm = 0
        cloned.ancho_manijas_cm = 0
        return super().compute(cloned, fixed_costs=fixed_costs, material=material)