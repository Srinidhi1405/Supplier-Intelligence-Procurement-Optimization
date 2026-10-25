"""
Initializes SQLite database from CSV files and runs test queries.
"""
import os
import sqlite3
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "procurement.db")

conn = sqlite3.connect(DB_PATH)

df_suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
df_pos = pd.read_csv(os.path.join(DATA_DIR, "purchase_orders.csv"))

df_suppliers.to_sql("dim_suppliers", conn, if_exists="replace", index=False)
df_pos.to_sql("fact_purchase_orders", conn, if_exists="replace", index=False)

print("SQLite Database initialized successfully at:", DB_PATH)

# Test query 1
cursor = conn.cursor()
cursor.execute("""
SELECT
    s.supplier_name,
    COUNT(f.po_number) AS total_shipments,
    ROUND(AVG(f.lead_time_days), 1) AS avg_lead_time_days,
    ROUND(100.0 * SUM(CASE WHEN f.on_time_in_full = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS otif_rate_pct,
    ROUND(SUM(f.total_po_tco) / SUM(f.delivered_qty), 2) AS effective_tco
FROM dim_suppliers s
JOIN fact_purchase_orders f ON s.supplier_id = f.supplier_id
GROUP BY s.supplier_name
ORDER BY effective_tco ASC
""")

print("\n--- SQL QUERY TEST RESULT (OTIF & TCO Rollup) ---")
for row in cursor.fetchall():
    print(f"Supplier: {row[0]:<30} | POs: {row[1]:<4} | Lead Time: {row[2]}d | OTIF: {row[3]}% | TCO: ${row[4]}")

conn.close()
