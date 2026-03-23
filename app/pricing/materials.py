from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Material:
    code: str
    name: str
    costo_por_m2: float


class MaterialCatalog:

    def __init__(self):
        self.materials: Dict[str, Material] = {
            "CAMBREL_70": Material(
                code="CAMBREL_70",
                name="Cambrel 70g",
                costo_por_m2=0.42
            ),
            "CAMBREL_80": Material(
                code="CAMBREL_80",
                name="Cambrel 80g",
                costo_por_m2=0.48
            ),
            "CAMBREL_90": Material(
                code="CAMBREL_90",
                name="Cambrel 90g",
                costo_por_m2=0.55
            ),
        }

    def get(self, code: str) -> Material:

        if code not in self.materials:
            raise Exception(f"Material no existe: {code}")

        return self.materials[code]


catalog = MaterialCatalog()