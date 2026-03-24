import json
from app.models import QuoteInputs
from app.config import FixedCosts
from app.pricing.materials import Material
from app.bags.plana_troquel import PlanaTroquelCalculator

def run_debug():
    inputs = QuoteInputs(
        ancho_cm=16,
        alto_cm=25,
        fuelle_cm=0,
        dobles_cm=6,
        caras=1,
        tintas=1,
        cola_produccion=999999,
        material_code="CAMBREL_70"
    )
    
    class MockFixedCosts:
        @property
        def total(self):
            return 180.0
            
    fixed_costs = MockFixedCosts()
    material = Material(code="cambrel", name="Cambrel", costo_por_m2=1100.0)
    
    calc = PlanaTroquelCalculator()
    res = calc.compute(inputs, fixed_costs, material)
    
    print("=== EXCEL VARS ===")
    for k, v in res["excel"].items():
        print(f"{k}: {v}")
    
    # We will compute the steps manually to see if anything is wrong.
    C5 = 16 / 100.0
    C6 = 25 / 100.0
    C8 = 6 / 100.0
    E5 = (25*2) + 0 + (6*2)
    F5 = 160 - (E5 * 2)
    E8 = 160 - E5
    F8 = E8 / 100.0
    G8 = F8 * C5
    F11 = G8 * 1100.0
    
    C10 = C5 * C6
    C11 = C8 * C5 * 2
    C12 = C6 * C5
    C13 = C10 + C11 + C12
    base_tela = C13 * 1100.0 / 1.6
    C15 = (base_tela + F11) if E8 < 38 else base_tela
    
    print("\n=== MANUAL TELA ===")
    print(f"C5: {C5}, C6: {C6}, C8: {C8}")
    print(f"E5: {E5}, F5: {F5}, E8: {E8}")
    print(f"F8: {F8}, G8: {G8}, F11: {F11}")
    print(f"C10: {C10}, C11: {C11}, C12: {C12}, C13: {C13}")
    print(f"base_tela: {base_tela}")
    print(f"C15 (tela_final): {C15}")
    
if __name__ == "__main__":
    run_debug()
