from .plana_manija import PlanaManijaCalculator
from .plana_troquel import PlanaTroquelCalculator


BAG_TYPES = {
    "PLANA_MANIJA": PlanaManijaCalculator,
    "PLANA_TROQUEL": PlanaTroquelCalculator,
}


def get_bag(bag_type: str):

    if bag_type not in BAG_TYPES:
        raise Exception(f"Tipo de bolsa no existe: {bag_type}")

    return BAG_TYPES[bag_type]()