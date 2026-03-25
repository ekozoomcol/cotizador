import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models import QuoteInputs
from app.pricing.materials import Material

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

material = Material(code="cambrel", name="Cambrel", costo_por_m2=1100.0)

# Simulate OLD logic
# PlanaManija formulas for Tela:
B5, B6, B7, B11 = 16, 25, 0, 6
C5, C6, C7, C11 = B5/100.0, B6/100.0, B7/100.0, B11/100.0
# Troquel has manijas=0
C8, C9, C10 = 0, 0, 0
C13_manijas = 0
C14_frente = C5 * C6 # 0.16 * 0.25 = 0.04
C15_dobles = C11 * C5 * 2 # 0.06 * 0.16 * 2 = 0.0192
C16_atras = C6 * C5 # 0.04
C17 = C13_manijas + C14_frente + C15_dobles + C16_atras

E5 = (B6 * 2) + B7 + (B11 * 2) # 25*2 + 0 + 6*2 = 62
E8 = 160 - E5 # 98
F8 = E8 / 100.0
G8 = F8 * C5
F11 = G8 * 1100

base_tela = C17 * 1100 / 1.6
C19 = (base_tela + F11) if E8 < 38 else base_tela

print(f"OLD PlanaManija tela for Troquel: {C19}")

# Simulate NEW logic for Troquel
C10_frente = C5 * C6 # 0.04
C11_dobles = C8 * C5 * 2 # wait, C8 is dobles here? Yes, B8 is dobles. C8 = 6/100 = 0.06. C11 = 0.06 * 0.16 * 2 = 0.0192
C12_atras = C6 * C5 # 0.04
C13_total = C10_frente + C11_dobles + C12_atras # 0.0992

base_tela_new = C13_total * 1100 / 1.6
C15_new = (base_tela_new + F11) if E8 < 38 else base_tela_new

print(f"NEW PlanaTroquel tela: {C15_new}")
