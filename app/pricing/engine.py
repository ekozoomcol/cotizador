from app.pricing.materials import catalog
from app.bags.registry import get_bag


def quote(bag_type: str, material_code: str, inputs: dict):

    bag = get_bag(bag_type)

    material = catalog.get(material_code)

    geometry = bag.calculate_geometry(inputs)

    area = geometry["area_m2"]

    costo_material = area * material.costo_por_m2

    costo_total = costo_material * inputs["cantidad"]

    return {
        "material": material.name,
        "bag_type": bag_type,
        "area_m2": area,
        "costo_material_unitario": costo_material,
        "precio_total": costo_total
    }