import time
from app.pricing.engine import quote

def run_perf_test(iterations=100):
    inputs = {
        'ancho_cm': 35,
        'alto_cm': 40,
        'tintas_c1': 2,
        'tintas_c2': 1,
        'cantidad': 500,
        'material_code': 'CAMBREL_70'
    }
    
    start_total = time.perf_counter()
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        quote('PLANA_MANIJA', 'CAMBREL_70', inputs)
        end = time.perf_counter()
        times.append(end - start)
        
    end_total = time.perf_counter()
    
    avg_time = sum(times) / iterations
    max_time = max(times)
    min_time = min(times)
    
    print(f"--- Resultados de Rendimiento ({iterations} iteraciones) ---")
    print(f"Tiempo Total: {(end_total - start_total)*1000:.2f} ms")
    print(f"Promedio por cálculo: {avg_time*1000:.4f} ms")
    print(f"Máximo: {max_time*1000:.4f} ms")
    print(f"Mínimo: {min_time*1000:.4f} ms")

if __name__ == "__main__":
    run_perf_test()
