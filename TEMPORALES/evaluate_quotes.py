import asyncio
import httpx
import json

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

async def fetch_and_print():
    async with httpx.AsyncClient() as client:
        # Request 1: Standard Plana Manija
        print("--- REQUEST 1: Standard Plana Manija ---")
        try:
            r1 = await client.post(API_URL, json=base_payload)
            data1 = r1.json()
            if "svg_preview" in data1: del data1["svg_preview"]
            print(json.dumps(data1, indent=2))
        except Exception as e:
            print("Error:", e)

        # Request 2: Plana Troquel
        print("\n--- REQUEST 2: Plana Troquel ---")
        payload2 = base_payload.copy()
        payload2["bag_type"] = "PLANA_TROQUEL"
        payload2["inputs"] = base_payload["inputs"].copy()
        try:
            r2 = await client.post(API_URL, json=payload2)
            data2 = r2.json()
            if "svg_preview" in data2: del data2["svg_preview"]
            print(json.dumps(data2, indent=2))
        except Exception as e:
            print("Error:", e)

        # Request 3: Large order Plana Manija
        print("\n--- REQUEST 3: Large Bag Plana Manija (55x60x10) ---")
        payload3 = base_payload.copy()
        payload3["inputs"] = base_payload["inputs"].copy()
        payload3["inputs"]["ancho_cm"] = 55
        payload3["inputs"]["alto_cm"] = 60
        payload3["inputs"]["fuelle_cm"] = 10
        try:
            r3 = await client.post(API_URL, json=payload3)
            data3 = r3.json()
            if "svg_preview" in data3: del data3["svg_preview"]
            print(json.dumps(data3, indent=2))
        except Exception as e:
            print("Error:", e)

        # Request 4: Missing fields (Stress Test behavior)
        print("\n--- REQUEST 4: Missing Fields ---")
        payload4 = {"bag_type": "PLANA_MANIJA"}
        try:
            r4 = await client.post(API_URL, json=payload4)
            print(r4.status_code, r4.text)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(fetch_and_print())
