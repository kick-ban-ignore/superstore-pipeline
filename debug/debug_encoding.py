# debug_encoding.py
import pandas as pd

files = {
    "orders":          "data/orders.csv",
    "products":        "data/products.csv",
    "people":          "data/people.csv",
    "returned_orders": "data/returned_orders.csv",
}

for name, path in files.items():
    for encoding in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(path, encoding=encoding, nrows=5)
            print(f"✅ {name:20s} → funktioniert mit: {encoding}")
            break
        except Exception:
            print(f"❌ {name:20s} → klappt NICHT mit: {encoding}")