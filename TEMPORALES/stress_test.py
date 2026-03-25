import asyncio
import httpx
import time

API_URL = "http://127.0.0.1:8000/quote"

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

async def send_req(client, payload, name):
    try:
        resp = await client.post(API_URL, json=payload, timeout=5.0)
        return name, resp.status_code, resp.text[:200]
    except Exception as e:
        return name, "ERROR", str(e)

async def run_stress_test():
    async with httpx.AsyncClient() as client:
        # Test 1: Normal Request
        print("1. Normal Request")
        n_name, n_status, n_text = await send_req(client, base_payload, "Normal")
        print(f"[{n_status}] {n_text}\n")

        # Test 2: Missing fields (should be caught by Pydantic)
        malformed = {"bag_type": "PLANA_MANIJA"}
        print("2. Missing Fields")
        m_name, m_status, m_text = await send_req(client, malformed, "Missing")
        print(f"[{m_status}] {m_text}\n")

        # Test 3: Negative dimensions
        neg_payload = base_payload.copy()
        neg_payload["inputs"] = base_payload["inputs"].copy()
        neg_payload["inputs"]["ancho_cm"] = -10
        print("3. Negative Dimensions")
        ng_name, ng_status, ng_text = await send_req(client, neg_payload, "Negative")
        print(f"[{ng_status}] {ng_text}\n")

        # Test 4: Extreme values
        extreme_payload = base_payload.copy()
        extreme_payload["inputs"] = base_payload["inputs"].copy()
        extreme_payload["inputs"]["ancho_cm"] = 999999999
        extreme_payload["inputs"]["alto_cm"] = 999999999
        print("4. Extreme Dimensions")
        ex_name, ex_status, ex_text = await send_req(client, extreme_payload, "Extreme")
        print(f"[{ex_status}] {ex_text}\n")

        # Test 5: Concurrency Spam (50 requests at once)
        print("5. Concurrency Load Test (50 reqs)...")
        tasks = [send_req(client, base_payload, f"Req-{i}") for i in range(50)]
        start = time.time()
        results = await asyncio.gather(*tasks)
        dur = time.time() - start
        success = sum(1 for r in results if r[1] == 200)
        print(f"Finished in {dur:.2f}s. {success}/50 succeeded.")

if __name__ == "__main__":
    asyncio.run(run_stress_test())
