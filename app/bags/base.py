from abc import ABC, abstractmethod
from typing import Dict, Any

from app.config import FixedCosts
from app.models import QuoteInputs
from app.pricing.materials import Material


class BagCalculator(ABC):
    """
    Interface para agregar más bolsas.
    Cada bolsa debe:
    - calcular variables tipo Excel (C5.. etc)
    - devolver costos por banda (equivalente a B39..G39)
    """

    @abstractmethod
    def compute(self, inputs: QuoteInputs, fixed_costs: FixedCosts, material: Material) -> Dict[str, Any]:
        raise NotImplementedError