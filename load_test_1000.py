import asyncio
import httpx
import time
from collections import Counter

API_URL = "https://cotizador-772286866733.us-central1.run.app/quote"

base_payload = {
    "bag_type": "PLANA_MANIJA",
    "material_code": "CAMBREL_70",
    "inputs": {
        "ancho_cm": 35,
        "alto_cm": 40,
        "fuelle_cm": 0,
        "manija1_cm": 40,
        "manija2_cm": 0,
        "ancho_manijas_cm": 2.5,
        "dobles_cm": 4,
        "caras": 1,
        "tintas": 1,
        "cola_produccion": 0
    }
}

async def fetch(client, i, latencies, statuses):
    start = time.time()
    try:
        r = await client.post(API_URL, json=base_payload)
        statuses[r.status_code] += 1
    except Exception as e:
        statuses[type(e).__name__] += 1
    latencies.append(time.time() - start)

async def main():
    print("Iniciando prueba de carga de 1000 requests simultáneos...")
    print("Calentando cliente HTTP...")
    # It's important to increase the connection pool limits for a real 1000 concurrent hit
    limits = httpx.Limits(max_connections=1200, max_keepalive_connections=1200)
    timeout = httpx.Timeout(30.0)
    
    start_time = time.time()
    latencies = []
    statuses = Counter()
    
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        tasks = [fetch(client, i, latencies, statuses) for i in range(1000)]
        await asyncio.gather(*tasks)
        
    total_time = time.time() - start_time
    
    print("\n--- RESULTADOS ---")
    print(f"Tiempo Total: {total_time:.2f} segundos")
    print(f"RPS (Requests por Segundo): {1000 / total_time:.2f}")
    print("\nStatus Codes devueltos:")
    for k, v in statuses.items():
        print(f"  {k}: {v} peticiones")
        
    if latencies:
        print(f"\nLatencias (segundos):")
        print(f"  Mínima: {min(latencies):.4f}s")
        print(f"  Máxima: {max(latencies):.4f}s")
        print(f"  Media:  {sum(latencies)/len(latencies):.4f}s")

if __name__ == "__main__":
    # Required for Windows to prevent "Too many open files" errors 
    # when making thousands of connections if modifying loop policy, but Proactor works fine.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except Exception as e:
        # Revert to default if selector fails
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.run(main())
