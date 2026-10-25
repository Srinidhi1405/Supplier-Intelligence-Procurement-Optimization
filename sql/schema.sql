-- ==============================================================================
-- Global Sourcing & Supply Management (GSSM) Analytics
-- Enterprise Procurement & Sourcing Star Schema DDL
-- Compatible with: PostgreSQL, Snowflake, SQLite, Databricks
-- ==============================================================================

-- 1. DIMENSION: Suppliers
DROP TABLE IF EXISTS dim_suppliers;
CREATE TABLE dim_suppliers (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    quoted_unit_cost NUMERIC(10, 2) NOT NULL,
    standard_lead_time_days INTEGER NOT NULL,
    target_dppm INTEGER NOT NULL,
    historical_otd_pct NUMERIC(5, 2) NOT NULL,
    monthly_capacity_units INTEGER NOT NULL,
    financial_stability_score INTEGER NOT NULL CHECK (financial_stability_score BETWEEN 0 AND 100),
    esg_sustainability_score INTEGER NOT NULL CHECK (esg_sustainability_score BETWEEN 0 AND 100),
    tariff_rate_pct NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    tier_level INTEGER NOT NULL DEFAULT 1,
    primary_transport_mode VARCHAR(20) NOT NULL,
    standard_freight_per_unit NUMERIC(10, 2) NOT NULL,
    expedited_air_cost_per_unit NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. FACT: Purchase Orders Execution
DROP TABLE IF EXISTS fact_purchase_orders;
CREATE TABLE fact_purchase_orders (
    po_number VARCHAR(30) PRIMARY KEY,
    supplier_id VARCHAR(20) NOT NULL REFERENCES dim_suppliers(supplier_id),
    quarter VARCHAR(10) NOT NULL,
    order_date DATE NOT NULL,
    promised_delivery_date DATE NOT NULL,
    actual_delivery_date DATE NOT NULL,
    lead_time_days INTEGER NOT NULL,
    lead_time_variance_days INTEGER NOT NULL,
    on_time_in_full BOOLEAN NOT NULL,
    ordered_qty INTEGER NOT NULL,
    delivered_qty INTEGER NOT NULL,
    accepted_qty INTEGER NOT NULL,
    defect_qty INTEGER NOT NULL,
    defect_dppm INTEGER NOT NULL,
    freight_mode VARCHAR(20) NOT NULL,
    expedited_flag BOOLEAN NOT NULL,
    unit_quoted_price NUMERIC(10, 2) NOT NULL,
    total_purchase_cost NUMERIC(14, 2) NOT NULL,
    total_freight_cost NUMERIC(14, 2) NOT NULL,
    tariff_duty_cost NUMERIC(14, 2) NOT NULL,
    inspection_cost NUMERIC(14, 2) NOT NULL,
    defect_scrap_cost NUMERIC(14, 2) NOT NULL,
    inventory_holding_cost NUMERIC(14, 2) NOT NULL,
    total_po_tco NUMERIC(14, 2) NOT NULL,
    effective_tco_per_unit NUMERIC(10, 4) NOT NULL,
    tco_premium_over_quote_pct NUMERIC(6, 2) NOT NULL
);

-- Indexes for lightning-fast aggregation & procurement rollups
CREATE INDEX idx_po_supplier_id ON fact_purchase_orders(supplier_id);
CREATE INDEX idx_po_order_date ON fact_purchase_orders(order_date);
CREATE INDEX idx_po_quarter ON fact_purchase_orders(quarter);
CREATE INDEX idx_po_otif ON fact_purchase_orders(on_time_in_full);
