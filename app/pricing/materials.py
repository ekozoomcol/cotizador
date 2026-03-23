from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Material:
    code: str
    name: str
    costo_por_m2: float


class MaterialCatalog:

    def __init__(self, by_code: Dict[str, Material] | None = None):
        default_map: Dict[str, Material] = {
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
        self.materials: Dict[str, Material] = by_code or default_map
        # Alias para compatibilidad con código que usa cfg.materials.by_code.
        self.by_code: Dict[str, Material] = self.materials

    def get(self, code: str) -> Material:

        if code not in self.materials:
            raise Exception(f"Material no existe: {code}")

        return self.materials[code]


catalog = MaterialCatalog()