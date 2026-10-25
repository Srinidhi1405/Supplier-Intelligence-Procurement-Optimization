-- ==============================================================================
-- Global Sourcing & Supply Management (GSSM) Analytics
-- Advanced Procurement & Sourcing Optimization SQL Queries
-- Demonstrating: CTEs, Window Functions, Aggregate Rollups, KPI Metrics
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Supplier Scorecard & Delivery Reliability (OTIF & Lead Time Variance)
-- Purpose: Evaluate whether suppliers meet strict delivery SLA (95%+ OTIF)
-- ------------------------------------------------------------------------------
WITH delivery_metrics AS (
    SELECT
        s.supplier_id,
        s.supplier_name,
        s.country,
        COUNT(f.po_number) AS total_shipments,
        SUM(f.ordered_qty) AS total_units_ordered,
        SUM(f.delivered_qty) AS total_units_delivered,
        ROUND(AVG(f.lead_time_days), 1) AS avg_lead_time_days,
        ROUND(AVG(f.lead_time_variance_days), 1) AS avg_delay_days,
        SUM(CASE WHEN f.on_time_in_full = TRUE THEN 1 ELSE 0 END) AS otif_shipments,
        SUM(CASE WHEN f.expedited_flag = TRUE THEN 1 ELSE 0 END) AS expedited_shipments
    FROM dim_suppliers s
    JOIN fact_purchase_orders f ON s.supplier_id = f.supplier_id
    GROUP BY s.supplier_id, s.supplier_name, s.country
)
SELECT
    supplier_id,
    supplier_name,
    country,
    total_shipments,
    total_units_delivered,
    avg_lead_time_days,
    avg_delay_days,
    ROUND(100.0 * otif_shipments / total_shipments, 2) AS otif_delivery_rate_pct,
    ROUND(100.0 * expedited_shipments / total_shipments, 2) AS expedited_freight_rate_pct
FROM delivery_metrics
ORDER BY otif_delivery_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 2: The "Lowest Bidder Trap" - Quoted Price vs Total Cost of Ownership (TCO)
-- Purpose: Quantify the hidden cost penalty of cheap suppliers like Kestrel (China)
-- ------------------------------------------------------------------------------
SELECT
    s.supplier_id,
    s.supplier_name,
    s.country,
    ROUND(AVG(f.unit_quoted_price), 2) AS quoted_fob_price,
    ROUND(SUM(f.total_po_tco) / SUM(f.delivered_qty), 4) AS landed_tco_per_unit,
    ROUND((SUM(f.total_po_tco) / SUM(f.delivered_qty)) - AVG(f.unit_quoted_price), 2) AS hidden_tco_delta_per_unit,
    ROUND(
        100.0 * ((SUM(f.total_po_tco) / SUM(f.delivered_qty)) - AVG(f.unit_quoted_price)) / AVG(f.unit_quoted_price), 
        2
    ) AS hidden_cost_markup_pct,
    DENSE_RANK() OVER (ORDER BY AVG(f.unit_quoted_price) ASC) AS rank_by_quoted_price,
    DENSE_RANK() OVER (ORDER BY (SUM(f.total_po_tco) / SUM(f.delivered_qty)) ASC) AS rank_by_true_tco
FROM dim_suppliers s
JOIN fact_purchase_orders f ON s.supplier_id = f.supplier_id
GROUP BY s.supplier_id, s.supplier_name, s.country
ORDER BY rank_by_true_tco ASC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Granular TCO Cost Element Breakdown (% Share of Total Spend)
-- Purpose: Unpack where each dollar is spent across Freight, Tariffs, Scrap, Inspection, and Holding
-- ------------------------------------------------------------------------------
SELECT
    s.supplier_name,
    s.country,
    ROUND(SUM(f.total_purchase_cost) / 1000000.0, 2) AS purchase_fob_spend_m,
    ROUND(SUM(f.total_freight_cost) / 1000000.0, 2) AS freight_spend_m,
    ROUND(SUM(f.tariff_duty_cost) / 1000000.0, 2) AS customs_tariff_spend_m,
    ROUND(SUM(f.inspection_cost) / 1000000.0, 2) AS quality_inspection_spend_m,
    ROUND(SUM(f.defect_scrap_cost) / 1000000.0, 2) AS factory_scrap_rework_spend_m,
    ROUND(SUM(f.inventory_holding_cost) / 1000000.0, 2) AS inventory_carrying_spend_m,
    ROUND(SUM(f.total_po_tco) / 1000000.0, 2) AS total_tco_spend_m,
    ROUND(100.0 * SUM(f.total_purchase_cost) / SUM(f.total_po_tco), 1) AS purchase_spend_share_pct,
    ROUND(100.0 * (SUM(f.total_po_tco) - SUM(f.total_purchase_cost)) / SUM(f.total_po_tco), 1) AS non_purchase_hidden_cost_share_pct
FROM dim_suppliers s
JOIN fact_purchase_orders f ON s.supplier_id = f.supplier_id
GROUP BY s.supplier_name, s.country
ORDER BY total_tco_spend_m DESC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Quality & Yield Capability - Defect DPPM & Line Scrap Financial Impact
-- Purpose: Measure defect ppm vs the company's 1,000 DPPM tier-1 target
-- ------------------------------------------------------------------------------
SELECT
    s.supplier_id,
    s.supplier_name,
    SUM(f.delivered_qty) AS units_received,
    SUM(f.defect_qty) AS units_defective,
    ROUND((SUM(f.defect_qty)::FLOAT / SUM(f.delivered_qty)::FLOAT) * 1000000.0, 0) AS weighted_defect_dppm,
    ROUND(100.0 * (1.0 - (SUM(f.defect_qty)::FLOAT / SUM(f.delivered_qty)::FLOAT)), 3) AS quality_yield_pct,
    ROUND(SUM(f.defect_scrap_cost), 2) AS total_scrap_financial_cost,
    ROUND(SUM(f.defect_scrap_cost) / SUM(f.delivered_qty), 4) AS scrap_cost_per_delivered_unit
FROM dim_suppliers s
JOIN fact_purchase_orders f ON s.supplier_id = f.supplier_id
GROUP BY s.supplier_id, s.supplier_name
ORDER BY weighted_defect_dppm ASC;


-- ------------------------------------------------------------------------------
-- QUERY 5: Quarterly Ramp Execution & Lead Time Trend (Window Functions)
-- Purpose: Monitor supplier performance stability as volumes scale from Q1 to Q4 peak
-- ------------------------------------------------------------------------------
WITH quarterly_rollup AS (
    SELECT
        f.supplier_id,
        s.supplier_name,
        f.quarter,
        SUM(f.delivered_qty) AS quarter_volume,
        ROUND(AVG(f.lead_time_days), 1) AS avg_lead_time,
        ROUND(100.0 * SUM(CASE WHEN f.on_time_in_full THEN 1 ELSE 0 END) / COUNT(*), 1) AS quarter_otd_pct,
        ROUND(AVG(f.defect_dppm), 0) AS avg_dppm
    FROM fact_purchase_orders f
    JOIN dim_suppliers s ON f.supplier_id = s.supplier_id
    GROUP BY f.supplier_id, s.supplier_name, f.quarter
)
SELECT
    supplier_name,
    quarter,
    quarter_volume,
    avg_lead_time,
    quarter_otd_pct,
    avg_dppm,
    LAG(avg_lead_time, 1) OVER (PARTITION BY supplier_name ORDER BY quarter) AS prev_quarter_lead_time,
    ROUND(avg_lead_time - LAG(avg_lead_time, 1) OVER (PARTITION BY supplier_name ORDER BY quarter), 1) AS lead_time_drift_days
FROM quarterly_rollup
ORDER BY supplier_name, quarter;


-- ------------------------------------------------------------------------------
-- QUERY 6: Emergency Air Expediting Premium Analysis
-- Purpose: Calculate how much budget was burned on emergency air freight to cover delays
-- ------------------------------------------------------------------------------
SELECT
    s.supplier_name,
    COUNT(CASE WHEN f.freight_mode = 'Air Expedited' THEN 1 END) AS expedited_po_count,
    COUNT(CASE WHEN f.freight_mode = 'Ocean' THEN 1 END) AS ocean_po_count,
    ROUND(SUM(CASE WHEN f.freight_mode = 'Air Expedited' THEN f.total_freight_cost ELSE 0 END), 2) AS air_freight_spend,
    ROUND(SUM(CASE WHEN f.freight_mode = 'Ocean' THEN f.total_freight_cost ELSE 0 END), 2) AS ocean_freight_spend,
    ROUND(
        SUM(CASE WHEN f.freight_mode = 'Air Expedited' THEN f.total_freight_cost ELSE 0 END) -
        (SUM(CASE WHEN f.freight_mode = 'Air Expedited' THEN f.delivered_qty ELSE 0 END) * s.standard_freight_per_unit),
        2
    ) AS expedited_premium_waste_spend
FROM fact_purchase_orders f
JOIN dim_suppliers s ON f.supplier_id = s.supplier_id
GROUP BY s.supplier_name, s.standard_freight_per_unit
ORDER BY expedited_premium_waste_spend DESC;


-- ------------------------------------------------------------------------------
-- QUERY 7: Capacity Utilization Under 25% Keynote Demand Surge Stress Test
-- Purpose: Flag suppliers that breach the 85% safe capacity threshold during ramp
-- ------------------------------------------------------------------------------
SELECT
    s.supplier_id,
    s.supplier_name,
    s.country,
    s.monthly_capacity_units,
    (s.monthly_capacity_units * 12) AS annual_rated_capacity,
    12000000 AS baseline_annual_demand,
    ROUND(12000000.0 * 1.25, 0) AS surge_annual_demand,
    ROUND((12000000.0 * 1.25) / (s.monthly_capacity_units * 12) * 100.0, 1) AS surge_capacity_utilization_pct,
    CASE 
        WHEN (12000000.0 * 1.25) / (s.monthly_capacity_units * 12) > 1.0 THEN 'CRITICAL DEFICIT: Cannot Solo Source'
        WHEN (12000000.0 * 1.25) / (s.monthly_capacity_units * 12) > 0.85 THEN 'WARNING: Exceeds 85% Safe Operating Cap'
        ELSE 'OPTIMAL: Sufficient Buffer'
    END AS capacity_risk_status
FROM dim_suppliers s
ORDER BY surge_capacity_utilization_pct DESC;
