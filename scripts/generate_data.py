"""
Global Sourcing & Supply Manager (GSSM) Analytics Engine
Synthetic Procurement & Sourcing Dataset Generator
Component: Flagship LTPO OLED Display Module (Apollo Pro 6.3")
Author: GSSM Procurement Analytics Team
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for perfect reproducibility
np.random.seed(42)
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. SUPPLIER MASTER DATA
# ---------------------------------------------------------
suppliers_data = [
    {
        "supplier_id": "SUP-001",
        "supplier_name": "Apex Display Technologies",
        "country": "South Korea",
        "city": "Paju",
        "quoted_unit_cost": 44.50,
        "standard_lead_time_days": 21,
        "target_dppm": 420,  # 0.042%
        "historical_otd_pct": 97.5,
        "monthly_capacity_units": 850000,
        "financial_stability_score": 96,  # 1-100
        "esg_sustainability_score": 92,  # 1-100
        "tariff_rate_pct": 0.00,  # Korea FTA
        "tier_level": 1,
        "primary_transport_mode": "Ocean",
        "ocean_transit_days": 18,
        "standard_freight_per_unit": 0.85,
        "expedited_air_cost_per_unit": 3.65,
    },
    {
        "supplier_id": "SUP-002",
        "supplier_name": "Lumina MicroOptics",
        "country": "Japan",
        "city": "Osaka",
        "quoted_unit_cost": 43.80,
        "standard_lead_time_days": 24,
        "target_dppm": 580,  # 0.058%
        "historical_otd_pct": 96.0,
        "monthly_capacity_units": 700000,
        "financial_stability_score": 94,
        "esg_sustainability_score": 95,
        "tariff_rate_pct": 0.00,
        "tier_level": 1,
        "primary_transport_mode": "Ocean",
        "ocean_transit_days": 20,
        "standard_freight_per_unit": 0.90,
        "expedited_air_cost_per_unit": 3.80,
    },
    {
        "supplier_id": "SUP-003",
        "supplier_name": "Vanguard Optoelectronics",
        "country": "Taiwan",
        "city": "Taichung",
        "quoted_unit_cost": 41.20,
        "standard_lead_time_days": 26,
        "target_dppm": 1250,  # 0.125%
        "historical_otd_pct": 94.2,
        "monthly_capacity_units": 950000,
        "financial_stability_score": 90,
        "esg_sustainability_score": 88,
        "tariff_rate_pct": 0.00,
        "tier_level": 1,
        "primary_transport_mode": "Ocean",
        "ocean_transit_days": 16,
        "standard_freight_per_unit": 0.80,
        "expedited_air_cost_per_unit": 3.40,
    },
    {
        "supplier_id": "SUP-004",
        "supplier_name": "Kestrel Panel Dynamics",
        "country": "China",
        "city": "Shenzhen",
        "quoted_unit_cost": 37.90,  # Aggressive low quote
        "standard_lead_time_days": 35,
        "target_dppm": 4800,  # 0.48% (High defect)
        "historical_otd_pct": 83.5,  # Low delivery reliability
        "monthly_capacity_units": 1100000,
        "financial_stability_score": 82,
        "esg_sustainability_score": 74,
        "tariff_rate_pct": 7.50,  # Section 301 tariffs
        "tier_level": 1,
        "primary_transport_mode": "Ocean",
        "ocean_transit_days": 22,
        "standard_freight_per_unit": 0.75,
        "expedited_air_cost_per_unit": 3.20,
    },
    {
        "supplier_id": "SUP-005",
        "supplier_name": "Solaria Micro-Devices",
        "country": "Vietnam",
        "city": "Bac Ninh",
        "quoted_unit_cost": 39.80,
        "standard_lead_time_days": 28,
        "target_dppm": 2100,  # 0.21%
        "historical_otd_pct": 91.0,
        "monthly_capacity_units": 650000,
        "financial_stability_score": 85,
        "esg_sustainability_score": 84,
        "tariff_rate_pct": 0.00,  # Vietnam FTA / GSP
        "tier_level": 1,
        "primary_transport_mode": "Ocean",
        "ocean_transit_days": 19,
        "standard_freight_per_unit": 0.82,
        "expedited_air_cost_per_unit": 3.50,
    },
    {
        "supplier_id": "SUP-006",
        "supplier_name": "Zenith Semiconductor Display",
        "country": "Malaysia",
        "city": "Penang",
        "quoted_unit_cost": 42.10,
        "standard_lead_time_days": 30,
        "target_dppm": 1600,  # 0.16%
        "historical_otd_pct": 89.5,
        "monthly_capacity_units": 500000,
        "financial_stability_score": 88,
        "esg_sustainability_score": 86,
        "tariff_rate_pct": 0.00,
        "tier_level": 1,
        "primary_transport_mode": "Ocean",
        "ocean_transit_days": 24,
        "standard_freight_per_unit": 0.88,
        "expedited_air_cost_per_unit": 3.70,
    }
]

df_suppliers = pd.DataFrame(suppliers_data)
df_suppliers.to_csv(os.path.join(DATA_DIR, "suppliers.csv"), index=False)
print(f"Generated {len(df_suppliers)} suppliers in suppliers.csv")

# ---------------------------------------------------------
# 2. PURCHASE ORDER TRANSACTIONS (1,500 POs across 4 Quarters)
# ---------------------------------------------------------
# Timeline: 2025-01-01 to 2025-12-31 (Full Fiscal Year)
# Total component demand ~ 12 Million units
# Order batches range from 5,000 to 25,000 units per PO

start_date = datetime(2025, 1, 1)
po_records = []
po_counter = 10001

# Distribution of PO volume by quarter to mirror ramp:
# Q1: 18%, Q2: 20%, Q3: 32% (Pre-launch ramp), Q4: 30% (Holiday peak)
quarter_weights = {1: 0.18, 2: 0.20, 3: 0.32, 4: 0.30}

# Sourcing share historically split among suppliers for baseline data:
supplier_order_shares = {
    "SUP-001": 0.35,  # Apex: Major primary
    "SUP-003": 0.25,  # Vanguard: Key secondary
    "SUP-002": 0.15,  # Lumina: Premium secondary
    "SUP-004": 0.12,  # Kestrel: Trial / low cost
    "SUP-005": 0.08,  # Solaria: Strategic diversification
    "SUP-006": 0.05   # Zenith: Niche
}

# Generate 1,450 purchase orders
total_target_pos = 1450
supplier_list = list(supplier_order_shares.keys())
supplier_probs = list(supplier_order_shares.values())

for i in range(total_target_pos):
    po_number = f"PO-2025-{po_counter}"
    po_counter += 1
    
    # Pick supplier based on distribution
    sup_id = np.random.choice(supplier_list, p=supplier_probs)
    sup_info = next(item for item in suppliers_data if item["supplier_id"] == sup_id)
    
    # Random date throughout the year with seasonal weighting
    quarter = np.random.choice([1, 2, 3, 4], p=[0.18, 0.20, 0.32, 0.30])
    q_start = datetime(2025, 3 * (quarter - 1) + 1, 1)
    day_offset = random.randint(0, 88)
    order_date = q_start + timedelta(days=day_offset)
    
    # Order quantity based on quarter
    base_qty = random.randint(6000, 15000)
    if quarter in [3, 4]:
        base_qty = int(base_qty * 1.35)  # Peak ramp scale
    
    # Lead time modeling with realistic stochastic variance
    nominal_lead = sup_info["standard_lead_time_days"]
    
    # Delay probability based on historical OTD
    is_delayed = (random.random() > (sup_info["historical_otd_pct"] / 100.0))
    if is_delayed:
        delay_days = int(np.random.exponential(scale=5.0)) + 1
        # Kestrel has worse tail delays
        if sup_id == "SUP-004":
            delay_days += random.randint(3, 10)
    else:
        # Delivered on time or even 1-2 days early
        delay_days = random.choice([0, 0, 0, -1, -2])
        
    promised_lead_time = nominal_lead
    actual_lead_time = max(7, nominal_lead + delay_days)
    
    promised_date = order_date + timedelta(days=promised_lead_time)
    actual_delivery_date = order_date + timedelta(days=actual_lead_time)
    
    # Quantity fulfillment
    delivered_qty = base_qty if not is_delayed or random.random() > 0.1 else int(base_qty * random.uniform(0.92, 0.99))
    
    # Defect rate modeling (Beta distribution calibrated to target DPPM)
    target_dppm = sup_info["target_dppm"]
    # Add random fluctuation around target DPPM
    actual_dppm = max(50, int(np.random.normal(target_dppm, target_dppm * 0.25)))
    
    # Occasional quality excursion (batch failure event)
    if random.random() < 0.04:  # 4% of POs suffer excursion
        actual_dppm = int(actual_dppm * random.uniform(2.5, 5.0))
        
    defect_count = int(delivered_qty * (actual_dppm / 1_000_000))
    accepted_qty = delivered_qty - defect_count
    
    # Logistics Mode: If delayed by >4 days, expedite via Air to protect production line
    freight_mode = "Ocean"
    unit_freight_cost = sup_info["standard_freight_per_unit"]
    expedited_flag = False
    
    if delay_days >= 4 or (quarter == 3 and delay_days >= 2):
        freight_mode = "Air Expedited"
        unit_freight_cost = sup_info["expedited_air_cost_per_unit"]
        expedited_flag = True
        
    # Cost Breakdown for PO
    unit_purchase_cost = sup_info["quoted_unit_cost"]
    total_purchase_cost = round(unit_purchase_cost * delivered_qty, 2)
    total_freight_cost = round(unit_freight_cost * delivered_qty, 2)
    tariff_cost = round(total_purchase_cost * (sup_info["tariff_rate_pct"] / 100.0), 2)
    
    # Incoming Inspection cost ($0.15 for standard sampling, $0.45 for 100% inspection if high defect history)
    unit_inspection_cost = 0.45 if (sup_id == "SUP-004" or actual_dppm > 2500) else 0.15
    total_inspection_cost = round(unit_inspection_cost * delivered_qty, 2)
    
    # Defect Fallout & Scrap Cost: Scrapped LTPO panel costs $35.00 in factory line teardown / replacement
    rework_scrap_cost_per_defect = 35.00
    total_defect_cost = round(defect_count * rework_scrap_cost_per_defect, 2)
    
    # Inventory Holding Cost:
    # Average inventory cycle stock + safety stock tied up during transit and warehouse
    # Annual holding rate = 20% (WACC + storage + obsolescence risk)
    daily_holding_rate = 0.20 / 365.0
    holding_days = actual_lead_time + 14  # Transit/lead time + 14 days factory buffer
    total_holding_cost = round(delivered_qty * unit_purchase_cost * daily_holding_rate * holding_days, 2)
    
    # Total Landed Cost of Ownership for this PO
    total_po_tco = round(
        total_purchase_cost + 
        total_freight_cost + 
        tariff_cost + 
        total_inspection_cost + 
        total_defect_cost + 
        total_holding_cost, 
        2
    )
    effective_tco_per_unit = round(total_po_tco / delivered_qty, 4) if delivered_qty > 0 else unit_purchase_cost

    po_records.append({
        "po_number": po_number,
        "supplier_id": sup_id,
        "supplier_name": sup_info["supplier_name"],
        "country": sup_info["country"],
        "order_date": order_date.strftime("%Y-%m-%d"),
        "quarter": f"Q{quarter}-2025",
        "promised_delivery_date": promised_date.strftime("%Y-%m-%d"),
        "actual_delivery_date": actual_delivery_date.strftime("%Y-%m-%d"),
        "lead_time_days": actual_lead_time,
        "lead_time_variance_days": delay_days,
        "on_time_in_full": (delay_days <= 0 and delivered_qty == base_qty),
        "ordered_qty": base_qty,
        "delivered_qty": delivered_qty,
        "accepted_qty": accepted_qty,
        "defect_qty": defect_count,
        "defect_dppm": actual_dppm,
        "freight_mode": freight_mode,
        "expedited_flag": expedited_flag,
        "unit_quoted_price": unit_purchase_cost,
        "total_purchase_cost": total_purchase_cost,
        "total_freight_cost": total_freight_cost,
        "tariff_duty_cost": tariff_cost,
        "inspection_cost": total_inspection_cost,
        "defect_scrap_cost": total_defect_cost,
        "inventory_holding_cost": total_holding_cost,
        "total_po_tco": total_po_tco,
        "effective_tco_per_unit": effective_tco_per_unit,
        "tco_premium_over_quote_pct": round(((effective_tco_per_unit - unit_purchase_cost) / unit_purchase_cost) * 100, 2)
    })

df_pos = pd.DataFrame(po_records)
df_pos.to_csv(os.path.join(DATA_DIR, "purchase_orders.csv"), index=False)
print(f"Generated {len(df_pos)} purchase orders in purchase_orders.csv")

# ---------------------------------------------------------
# 3. AGGREGATED SUPPLIER KPI BENCHMARKING TABLE
# ---------------------------------------------------------
kpi_summary = df_pos.groupby(["supplier_id", "supplier_name", "country"]).agg(
    total_pos=("po_number", "count"),
    total_units_delivered=("delivered_qty", "sum"),
    total_defects=("defect_qty", "sum"),
    avg_dppm=("defect_dppm", "mean"),
    weighted_defect_rate_pct=("defect_qty", lambda x: (x.sum() / df_pos.loc[x.index, "delivered_qty"].sum()) * 100),
    avg_actual_lead_time=("lead_time_days", "mean"),
    otd_rate_pct=("on_time_in_full", lambda x: (x.sum() / len(x)) * 100),
    expedited_shipment_pct=("expedited_flag", lambda x: (x.sum() / len(x)) * 100),
    avg_quoted_unit_price=("unit_quoted_price", "mean"),
    total_purchase_spend=("total_purchase_cost", "sum"),
    total_freight_spend=("total_freight_cost", "sum"),
    total_tariff_spend=("tariff_duty_cost", "sum"),
    total_inspection_spend=("inspection_cost", "sum"),
    total_defect_scrap_spend=("defect_scrap_cost", "sum"),
    total_holding_spend=("inventory_holding_cost", "sum"),
    total_tco_spend=("total_po_tco", "sum"),
    avg_effective_tco_per_unit=("effective_tco_per_unit", "mean")
).reset_index()

kpi_summary["tco_cost_delta_per_unit"] = round(kpi_summary["avg_effective_tco_per_unit"] - kpi_summary["avg_quoted_unit_price"], 2)
kpi_summary["tco_cost_delta_pct"] = round((kpi_summary["tco_cost_delta_per_unit"] / kpi_summary["avg_quoted_unit_price"]) * 100, 2)

kpi_summary.to_csv(os.path.join(DATA_DIR, "supplier_kpi_summary.csv"), index=False)
print(f"Generated supplier KPI summary in supplier_kpi_summary.csv")

# ---------------------------------------------------------
# 4. SCENARIO STRESS-TEST MATRIX DATASET
# ---------------------------------------------------------
# 4 Standard Scenarios tested in Operations:
# 1. Baseline Run-Rate (Normal quarterly execution)
# 2. Peak Launch Surge (+25% volume ramp in Q3/Q4)
# 3. Supply Chain Bottleneck (4-week port/customs delay + 3x air freight rates)
# 4. Geopolitical / Tariff Escalation (+15% tariff on select jurisdictions)

scenarios = [
    {
        "scenario_id": "SCN-1",
        "scenario_name": "Baseline Operations",
        "description": "Standard steady-state demand (12.0M units/year) with historical lead times and standard freight mix.",
        "volume_multiplier": 1.0,
        "freight_cost_multiplier": 1.0,
        "tariff_hike_pct": 0.0,
        "lead_time_expansion_days": 0,
        "defect_multiplier": 1.0
    },
    {
        "scenario_id": "SCN-2",
        "scenario_name": "Peak Demand Ramp (+25%)",
        "description": "Global demand surge post-keynote requiring +25% volume ramp. Stresses supplier capacity limits.",
        "volume_multiplier": 1.25,
        "freight_cost_multiplier": 1.15,
        "tariff_hike_pct": 0.0,
        "lead_time_expansion_days": 3,
        "defect_multiplier": 1.10
    },
    {
        "scenario_id": "SCN-3",
        "scenario_name": "Logistics Disruption & Bottleneck",
        "description": "Ocean port congestion and customs delays; forces 35% of shipments to emergency air expedites.",
        "volume_multiplier": 1.0,
        "freight_cost_multiplier": 2.20,
        "tariff_hike_pct": 0.0,
        "lead_time_expansion_days": 12,
        "defect_multiplier": 1.05
    },
    {
        "scenario_id": "SCN-4",
        "scenario_name": "Tariff Spike & Geopolitical Realignment",
        "description": "Escalation of Section 301 tariffs to 25% on specific origins; rewards regional diversification.",
        "volume_multiplier": 1.0,
        "freight_cost_multiplier": 1.10,
        "tariff_hike_pct": 15.0,
        "lead_time_expansion_days": 4,
        "defect_multiplier": 1.0
    }
]

df_scenarios = pd.DataFrame(scenarios)
df_scenarios.to_csv(os.path.join(DATA_DIR, "scenarios_definition.csv"), index=False)
print("Data generation complete!")
