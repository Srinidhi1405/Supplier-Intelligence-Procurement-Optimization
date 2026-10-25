"""
GSSM Procurement Optimization & Sourcing Allocation Engine
Total Cost of Ownership (TCO) & Sourcing Optimization Model
Author: Global Sourcing & Supply Management (GSSM) Team
"""

import os
import json
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def load_data():
    suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
    pos = pd.read_csv(os.path.join(DATA_DIR, "purchase_orders.csv"))
    scenarios = pd.read_csv(os.path.join(DATA_DIR, "scenarios_definition.csv"))
    return suppliers, pos, scenarios

def calculate_empirical_supplier_metrics(pos):
    """
    Derives realistic operational metrics from PO historical execution data.
    """
    grouped = pos.groupby("supplier_id")
    metrics = {}
    
    for sup_id, group in grouped:
        total_delivered = group["delivered_qty"].sum()
        total_defects = group["defect_qty"].sum()
        avg_lead_time = group["lead_time_days"].mean()
        std_lead_time = group["lead_time_days"].std()
        otd_pct = (group["on_time_in_full"].sum() / len(group)) * 100.0
        expedited_pct = (group["expedited_flag"].sum() / len(group)) * 100.0
        weighted_dppm = (total_defects / total_delivered) * 1_000_000 if total_delivered > 0 else 0
        
        # Empirical cost breakdown per unit delivered
        unit_quoted = group["unit_quoted_price"].mean()
        unit_freight = group["total_freight_cost"].sum() / total_delivered
        unit_tariff = group["tariff_duty_cost"].sum() / total_delivered
        unit_inspection = group["inspection_cost"].sum() / total_delivered
        unit_scrap = group["defect_scrap_cost"].sum() / total_delivered
        unit_holding = group["inventory_holding_cost"].sum() / total_delivered
        unit_tco = group["total_po_tco"].sum() / total_delivered
        
        metrics[sup_id] = {
            "avg_lead_time": round(avg_lead_time, 1),
            "std_lead_time": round(std_lead_time, 2),
            "otd_pct": round(otd_pct, 1),
            "expedited_pct": round(expedited_pct, 1),
            "empirical_dppm": round(weighted_dppm, 0),
            "unit_quoted": round(unit_quoted, 2),
            "unit_freight": round(unit_freight, 2),
            "unit_tariff": round(unit_tariff, 2),
            "unit_inspection": round(unit_inspection, 2),
            "unit_scrap": round(unit_scrap, 2),
            "unit_holding": round(unit_holding, 2),
            "unit_tco": round(unit_tco, 2),
            "tco_penalty_per_unit": round(unit_tco - unit_quoted, 2),
            "tco_penalty_pct": round(((unit_tco - unit_quoted) / unit_quoted) * 100, 1)
        }
    return metrics

def build_supplier_scorecard(suppliers, empirical_metrics):
    """
    Multi-Criteria Sourcing Evaluation Framework:
    - Cost & TCO Efficiency: 30%
    - Quality & Process Capability (DPPM): 25%
    - Delivery & Agility (OTD %): 20%
    - Scalability & Surge Capacity: 15%
    - Geopolitical & ESG Resilience: 10%
    """
    scorecard = []
    
    # Extract min/max for normalization
    tco_values = [empirical_metrics[s["supplier_id"]]["unit_tco"] for _, s in suppliers.iterrows()]
    dppm_values = [empirical_metrics[s["supplier_id"]]["empirical_dppm"] for _, s in suppliers.iterrows()]
    capacity_values = suppliers["monthly_capacity_units"].tolist()
    
    min_tco, max_tco = min(tco_values), max(tco_values)
    min_dppm, max_dppm = min(dppm_values), max(dppm_values)
    min_cap, max_cap = min(capacity_values), max(capacity_values)
    
    for _, s in suppliers.iterrows():
        sup_id = s["supplier_id"]
        emp = empirical_metrics[sup_id]
        
        # 1. Cost Score (Lower TCO is better) -> 0 to 100
        cost_score = 100 - ((emp["unit_tco"] - min_tco) / (max_tco - min_tco + 1e-6)) * 100
        
        # 2. Quality Score (Lower DPPM is better) -> 0 to 100
        quality_score = 100 - ((emp["empirical_dppm"] - min_dppm) / (max_dppm - min_dppm + 1e-6)) * 100
        
        # 3. Delivery Score (Directly based on OTD % and lead time stability)
        delivery_score = emp["otd_pct"] * 0.8 + (100 - min(100, emp["std_lead_time"] * 10)) * 0.2
        
        # 4. Capacity Score (Higher monthly capacity is better) -> 0 to 100
        capacity_score = ((s["monthly_capacity_units"] - min_cap) / (max_cap - min_cap + 1e-6)) * 100
        
        # 5. Geopolitical & ESG Score
        # Tariffs penalize geopolitical score; ESG score considered directly
        geo_penalty = s["tariff_rate_pct"] * 3.0
        risk_score = max(0, min(100, (s["financial_stability_score"] * 0.5 + s["esg_sustainability_score"] * 0.5) - geo_penalty))
        
        # Total Weighted Score
        composite_score = round(
            0.30 * cost_score +
            0.25 * quality_score +
            0.20 * delivery_score +
            0.15 * capacity_score +
            0.10 * risk_score,
            1
        )
        
        scorecard.append({
            "supplier_id": sup_id,
            "supplier_name": s["supplier_name"],
            "country": s["country"],
            "quoted_price": s["quoted_unit_cost"],
            "effective_tco": emp["unit_tco"],
            "hidden_tco_cost": emp["tco_penalty_per_unit"],
            "defect_dppm": emp["empirical_dppm"],
            "otd_pct": emp["otd_pct"],
            "monthly_capacity": s["monthly_capacity_units"],
            "annual_capacity": s["monthly_capacity_units"] * 12,
            "score_cost": round(cost_score, 1),
            "score_quality": round(quality_score, 1),
            "score_delivery": round(delivery_score, 1),
            "score_capacity": round(capacity_score, 1),
            "score_geopolitical_esg": round(risk_score, 1),
            "composite_sourcing_score": composite_score
        })
        
    df_scorecard = pd.DataFrame(scorecard).sort_values(by="composite_sourcing_score", ascending=False)
    df_scorecard["rank"] = range(1, len(df_scorecard) + 1)
    return df_scorecard

def simulate_scenarios(suppliers, empirical_metrics, scenarios, annual_demand=12_000_000):
    """
    Calculates total enterprise spend and unit TCO under 4 stress-test scenarios for each supplier.
    """
    scenario_results = []
    
    for _, scn in scenarios.iterrows():
        scn_id = scn["scenario_id"]
        scn_name = scn["scenario_name"]
        vol = annual_demand * scn["volume_multiplier"]
        
        for _, sup in suppliers.iterrows():
            sup_id = sup["supplier_id"]
            emp = empirical_metrics[sup_id]
            
            # Base purchase price
            unit_purchase = sup["quoted_unit_cost"]
            
            # Freight adjusted for scenario freight multiplier & expedited air surge
            base_freight = emp["unit_freight"] * scn["freight_cost_multiplier"]
            # Disruption scenario induces additional emergency expedites
            if scn_id == "SCN-3":
                extra_expedite_risk = (100 - emp["otd_pct"]) / 100.0 * 2.5
                unit_freight = base_freight + extra_expedite_risk
            else:
                unit_freight = base_freight
                
            # Tariff adjusted for geopolitical scenario
            tariff_pct = sup["tariff_rate_pct"] + (scn["tariff_hike_pct"] if sup["country"] in ["China"] else 0.0)
            unit_tariff = unit_purchase * (tariff_pct / 100.0)
            
            # Inspection
            unit_inspect = emp["unit_inspection"]
            
            # Scrap cost adjusted for defect multiplier
            unit_scrap = emp["unit_scrap"] * scn["defect_multiplier"]
            
            # Holding cost adjusted for lead time expansion
            expanded_lead = emp["avg_lead_time"] + scn["lead_time_expansion_days"]
            daily_wacc = 0.20 / 365.0
            unit_holding = unit_purchase * daily_wacc * (expanded_lead + 14)
            
            scenario_unit_tco = round(unit_purchase + unit_freight + unit_tariff + unit_inspect + unit_scrap + unit_holding, 2)
            total_enterprise_spend = round(scenario_unit_tco * vol, 2)
            
            # Capacity check
            max_annual_cap = sup["monthly_capacity_units"] * 12
            capacity_utilization_pct = round((vol / max_annual_cap) * 100, 1)
            capacity_deficit = max(0, int(vol - max_annual_cap))
            
            scenario_results.append({
                "scenario_id": scn_id,
                "scenario_name": scn_name,
                "supplier_id": sup_id,
                "supplier_name": sup["supplier_name"],
                "country": sup["country"],
                "annual_volume_needed": int(vol),
                "unit_quoted_price": unit_purchase,
                "unit_freight": round(unit_freight, 2),
                "unit_tariff": round(unit_tariff, 2),
                "unit_scrap": round(unit_scrap, 2),
                "unit_holding": round(unit_holding, 2),
                "scenario_unit_tco": scenario_unit_tco,
                "total_spend_millions": round(total_enterprise_spend / 1_000_000, 2),
                "capacity_utilization_pct": capacity_utilization_pct,
                "capacity_breached": (capacity_deficit > 0)
            })
            
    return pd.DataFrame(scenario_results)

def calculate_sourcing_allocation_strategies(df_scorecard, empirical_metrics, suppliers, annual_demand=12_000_000):
    """
    Evaluates 4 executive procurement allocation models:
    1. 'Naive Price-Only' (100% Kestrel - SUP-004): Lowest quoted price
    2. 'Incumbent Sole-Source' (100% Apex - SUP-001): Zero risk, highest quote
    3. 'Aggressive Multi-Sourcing' (Equal split across top 3)
    4. 'GSSM Recommended Dual-Source' (70% Vanguard SUP-003 / 30% Apex SUP-001):
       Combines cost-leader capability with premium quality hedge and surge elasticity.
    """
    strategies = [
        {
            "strategy_name": "Strategy A: Naive Lowest-Quote (100% Kestrel)",
            "description": "Awarding 100% volume to the lowest quoted FOB bidder ($37.90). High operational exposure.",
            "allocations": {"SUP-004": 1.0}
        },
        {
            "strategy_name": "Strategy B: Incumbent Single-Source (100% Apex)",
            "description": "Awarding 100% volume to the safest, highest-quality incumbent ($44.50). Zero disruption, max cost.",
            "allocations": {"SUP-001": 1.0}
        },
        {
            "strategy_name": "Strategy C: 3-Way Equal Allocation (33/33/34)",
            "description": "Diversifying equally across Apex (33%), Lumina (33%), and Vanguard (34%). High tooling overhead.",
            "allocations": {"SUP-001": 0.33, "SUP-002": 0.33, "SUP-003": 0.34}
        },
        {
            "strategy_name": "Strategy D: GSSM Optimized Dual-Source (70% Vanguard / 30% Apex)",
            "description": "Strategic split: Vanguard (Taiwan) captures cost efficiency while Apex (Korea) ensures launch yield and surge buffer.",
            "allocations": {"SUP-003": 0.70, "SUP-001": 0.30}
        },
        {
            "strategy_name": "Strategy E: China+1 Regional Hedge (65% Vanguard / 35% Solaria Vietnam)",
            "description": "Geopolitical tariff shield: Taiwan primary paired with Vietnam emerging hub. Lowest blended tariff footprint.",
            "allocations": {"SUP-003": 0.65, "SUP-005": 0.35}
        }
    ]
    
    results = []
    
    for strat in strategies:
        blended_quoted_price = 0.0
        blended_tco_per_unit = 0.0
        blended_dppm = 0.0
        blended_otd = 0.0
        total_annual_spend = 0.0
        quoted_annual_spend = 0.0
        tooling_nre_cost = len(strat["allocations"]) * 3_500_000  # $3.5M tooling qualification per supplier
        
        for sup_id, share in strat["allocations"].items():
            sup_row = suppliers[suppliers["supplier_id"] == sup_id].iloc[0]
            emp = empirical_metrics[sup_id]
            vol_share = annual_demand * share
            
            blended_quoted_price += sup_row["quoted_unit_cost"] * share
            blended_tco_per_unit += emp["unit_tco"] * share
            blended_dppm += emp["empirical_dppm"] * share
            blended_otd += emp["otd_pct"] * share
            
            total_annual_spend += emp["unit_tco"] * vol_share
            quoted_annual_spend += sup_row["quoted_unit_cost"] * vol_share
            
        total_enterprise_cost = total_annual_spend + tooling_nre_cost
        
        # Risk assessment index (0 to 100, lower is safer)
        # Factors: Single source vulnerability (penalty 25), Defect DPPM penalty, OTD slippage penalty
        single_source_risk = 25 if len(strat["allocations"]) == 1 else 0
        dppm_risk = (blended_dppm / 4800.0) * 40
        otd_risk = ((100.0 - blended_otd) / 20.0) * 35
        composite_risk_index = round(single_source_risk + dppm_risk + otd_risk, 1)
        
        results.append({
            "strategy_name": strat["strategy_name"],
            "description": strat["description"],
            "supplier_allocation": json.dumps(strat["allocations"]),
            "blended_quoted_price": round(blended_quoted_price, 2),
            "blended_tco_per_unit": round(blended_tco_per_unit, 2),
            "hidden_tco_premium": round(blended_tco_per_unit - blended_quoted_price, 2),
            "blended_dppm": int(blended_dppm),
            "blended_otd_pct": round(blended_otd, 1),
            "procurement_spend_m": round(total_annual_spend / 1_000_000, 2),
            "tooling_nre_spend_m": round(tooling_nre_cost / 1_000_000, 2),
            "total_enterprise_cost_m": round(total_enterprise_cost / 1_000_000, 2),
            "risk_index": composite_risk_index
        })
        
    df_strat = pd.DataFrame(results)
    
    # Calculate savings relative to Strategy B (Incumbent Single Source baseline)
    baseline_cost = df_strat.loc[df_strat["strategy_name"].str.contains("Strategy B"), "total_enterprise_cost_m"].values[0]
    df_strat["net_savings_vs_incumbent_m"] = round(baseline_cost - df_strat["total_enterprise_cost_m"], 2)
    
    return df_strat

def main():
    print("Executing GSSM TCO and Optimization Engine...")
    suppliers, pos, scenarios = load_data()
    
    empirical_metrics = calculate_empirical_supplier_metrics(pos)
    
    # 1. Supplier Scorecard
    df_scorecard = build_supplier_scorecard(suppliers, empirical_metrics)
    df_scorecard.to_csv(os.path.join(DATA_DIR, "supplier_scorecard.csv"), index=False)
    print("Generated supplier_scorecard.csv")
    
    # 2. Scenario Simulation
    df_scenarios_sim = simulate_scenarios(suppliers, empirical_metrics, scenarios)
    df_scenarios_sim.to_csv(os.path.join(DATA_DIR, "scenario_simulation_results.csv"), index=False)
    print("Generated scenario_simulation_results.csv")
    
    # 3. Sourcing Allocation Comparison
    df_strategies = calculate_sourcing_allocation_strategies(df_scorecard, empirical_metrics, suppliers)
    df_strategies.to_csv(os.path.join(DATA_DIR, "sourcing_allocation_strategies.csv"), index=False)
    print("Generated sourcing_allocation_strategies.csv")
    
    print("\n--- EXECUTIVE SUMMARY OF SOURCING STRATEGIES ---")
    print(df_strategies[["strategy_name", "blended_quoted_price", "blended_tco_per_unit", "blended_dppm", "total_enterprise_cost_m", "net_savings_vs_incumbent_m", "risk_index"]].to_string())

if __name__ == "__main__":
    main()
