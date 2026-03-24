from app.bags.plana_manija import PlanaManijaCalculator
from app.bags.plana_troquel import PlanaTroquelCalculator
from app.models import QuoteInputs
from app.pricing.materials import Material
from app.config import default_config

def test_plana_manija_marzo():
    inputs = QuoteInputs(
        ancho_cm=30,
        alto_cm=37,
        fuelle_cm=0,
        manija1_cm=60,
        manija2_cm=60,
        ancho_manijas_cm=5,
        dobles_cm=3,
        caras=1,
        tintas=1,
        cantidad=500
    )

    # Use the real config so we get all 8 bands and real global values
    real_config = default_config()
    
    # Check that fixed costs total 160 (maquila 25, luz 50, agua 10, arriendo 75)
    # Wait, in the March Excel, we used maquila 25, luz 50, agua 10, arriendo 75. Let's force them just in case.
    from app.config import FixedCosts
    real_config.fixed_costs = FixedCosts(maquila_bolsas=25, luz=50, agua=10, arriendo=75)
    real_config.nomina_diaria = 1500000.0
    # Override cola_produccion_global so we don't get the discount (-3 points) to match the Excel baseline
    real_config.cola_produccion_global = 999999.0

    material = Material(code="cambrel", name="Cambrel", costo_por_m2=1100.0)

    calc = PlanaManijaCalculator()
    result = calc.compute(inputs, real_config, material)

    print("--- TEST PLANA MANIJA NEW MARZO LOGIC ---")
    print("Expected Prices: B200=1240, B300=1120, B500=1030, B1500=960, B5500=885, B11000=875, B30000=865, B50000=850")
    print("Actual Prices:")
    costs = result["costs_by_band"]
    out = {}
    for k, v in costs.items():
        out[k] = v["precio_final"]
        print(f"  {k}: {v['precio_final']}")
        
    expected = {
        "B200_299": 1240,
        "B300_499": 1120,
        "B500_1499": 1030,
        "B1500_5499": 960,
        "B5500_10999": 885,
        "B11000_29999": 875,
        "B30000_49999": 865,
        "B50000P": 850
    }
    
    success = True
    for k, ev in expected.items():
        if out.get(k) != ev:
            print(f"FAIL: {k} expected {ev} got {out.get(k)}")
            success = False
            
    if success:
        print("SUCCESS! Plana Manija perfectly matches March Excel.")
    else:
        print("FAILED Plana Manija Test.")

if __name__ == "__main__":
    test_plana_manija_marzo()
