### 🚀 [View the Live Interactive Dashboard](https://srinidhi1405.github.io/Supplier-Intelligence-Procurement-Optimization/)

Explore the interactive supplier sourcing strategies, total cost of ownership (TCO), annual savings, quality metrics, and sourcing risk analysis.
# Global Sourcing & Supply Manager (GSSM) Decision Project
## Supplier Intelligence & Procurement Optimization Model

![GSSM](https://img.shields.io/badge/Role-TechCorp%20GSSM%20Intern-black?style=for-the-badge&logo=TechCorp)
![Domain](https://img.shields.io/badge/Domain-Global%20Procurement%20%26%20Supply%20Chain-blue?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20|%20SQL%20|%20Excel%20|%20Power%20BI-success?style=for-the-badge)

An enterprise-grade procurement decision model and business case tailored specifically for the company's **Global Sourcing & Supply Manager (GSSM)** role. 

This project analyzes **1,450 purchase orders across 6 global tier-1 display manufacturers** competing for a **12,000,000-unit annual contract** ($500M+ spend) for flagship **6.3" LTPO OLED Display Sub-Assembly**.

---

## 🎯 Executive Sourcing Summary

| Sourcing Strategy | Blended Quoted FOB | Blended Landed TCO | Blended DPPM | Total Enterprise Spend | Net Savings vs Incumbent | Sourcing Risk Index | Recommendation Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Strategy A: Naive Lowest-Bidder (100% Kestrel)** | $37.90 | $43.50 | 5,239 | $525.50M | +$34.92M | 94.0 / 100 | **REJECTED (High Disruption Risk)** |
| **Strategy B: Incumbent Sole-Source (100% Apex)** | $44.50 | $46.41 | 428 | $560.42M | Baseline ($0.00) | 32.6 / 100 | Inefficient Commercial Leverage |
| **Strategy C: 3-Way Equal Allocation (33/33/34)** | $43.15 | $45.13 | 800 | $552.11M | +$8.31M | 14.6 / 100 | Tooling NRE Dilution |
| **Strategy D: GSSM Optimal Dual-Source (70% TW / 30% KR)** | **$42.19** | **$44.17** | **1,097** | **$537.04M** | **+$23.38M** | **18.2 / 100** | **APPROVED & RECOMMENDED** |
| **Strategy E: China+1 Regional Hedge (65% TW / 35% VN)** | $40.71 | $42.75 | 1,634 | $520.02M | +$40.40M | 26.6 / 100 | Long-Term Strategic Target (FY27) |

### Key Sourcing Takeaway:
* **The "Lowest Bidder Trap":** Kestrel Dynamics (China) offered an apparent $6.60/unit discount ($37.90 vs $44.50). However, post-landed TCO analysis proved their true cost is **$43.50/unit**—a **+$5.60/unit (+14.8%) hidden penalty** driven by Section 301 tariffs, scrap fallout (5,239 DPPM requiring $35 assembly teardown), 100% lot screening, and emergency air expedites.
* **The Winning Decision:** Awarding **70% to Vanguard (Taichung, Taiwan)** and **30% to Apex (Paju, South Korea)** captures **$23.38M in verified net savings**, sustains **99.89% line yield (1,097 DPPM)**, and provides immediate launch surge elasticity with the lowest risk profile (**18.2 Risk Index**).

---

## 📁 Repository Structure

```text
TechCorp_GSSM_Procurement_Project/
├──_GSSM_Procurement_Optimization_Model.xlsx  # Multi-tab executive financial cost model
├── README.md                                      # Master project documentation
├── data/
│   ├── suppliers.csv                              # Supplier master profiles (capacity, lead time, baseline tariffs)
│   ├── purchase_orders.csv                        # 1,450 detailed PO execution records
│   ├── supplier_kpi_summary.csv                   # Historical metrics & cost rollups
│   ├── supplier_scorecard.csv                     # Multi-criteria decision matrix (MCDA)
│   ├── scenario_simulation_results.csv            # Stress-test scenario outcomes
│   ├── sourcing_allocation_strategies.csv         # Comparative allocation models
│   └── procurement.db                             # Relational SQLite database
├── scripts/
│   ├── generate_data.py                           # Stochastic procurement transaction generator
│   ├── tco_cost_model.py                          # TCO mathematical engine & allocation optimizer
│   ├── build_excel_model.py                       # Automated Excel model generator with formatting
│   └── init_sqlite_db.py                          # SQLite database initializer and test runner
├── sql/
│   ├── schema.sql                                 # Star-schema DDL (PostgreSQL/Snowflake/SQLite)
│   └── procurement_kpis.sql                       # 7 advanced analytical queries (CTEs, Window functions)
├── dashboard/
│   ├── index.html                                 # Standalone interactive dark-mode web dashboard
│   └── PowerBI_Setup_Guide.md                     # Power BI star schema, DAX formulas & layout instructions
└── executive_presentation/
    ├── EXECUTIVE_SOURCING_MEMO.md                 # Formal Sourcing Decision Memo for Ops VP
    └── RESUME_AND_INTERVIEW_GUIDE.md              # Tailored resume bullets & 5 STAR interview responses
```

---

## 🔬 Mathematical TCO Formulation

The model computes True Landed TCO using:

$$\text{Landed TCO} = C_{\text{FOB}} + C_{\text{Freight}} + C_{\text{Tariff}} + C_{\text{Inspection}} + C_{\text{Scrap/Rework}} + C_{\text{Holding}}$$

Where:
* **$C_{\text{Freight}}$**: Blended ocean transport ($0.80-$0.90/unit) plus emergency air expediting ($3.20-$3.80/unit) triggered by late shipments.
* **$C_{\text{Tariff}}$**: Customs and Section 301 tariffs (7.5% on China origin, 0% on Korea/Taiwan/Vietnam under FTAs).
* **$C_{\text{Inspection}}$**: Incoming metrology testing ($0.15/unit for standard AQL sampling, $0.45/unit for 100% screening on erratic suppliers).
* **$C_{\text{Scrap/Rework}}$**: Defective parts causing factory teardown:
  $$C_{\text{Scrap}} = \left(\frac{\text{DPPM}}{1,000,000}\right) \times \$35.00$$
* **$C_{\text{Holding}}$**: Cost of capital (20% annual WACC) tied up in transit cycle stock and lead time safety stock:
  $$C_{\text{Holding}} = C_{\text{FOB}} \times \left(\frac{0.20}{365}\right) \times (\text{Lead Time} + \text{Safety Buffer Days})$$

---

## 🚀 How to Run & Explore

### 1. Run the Python Models
```bash
# Re-generate synthetic data and run cost optimization
python scripts/generate_data.py
python scripts/tco_cost_model.py
python scripts/build_excel_model.py
```

### 2. View the Excel Financial Cost Model
Open `TechCorp_GSSM_Procurement_Optimization_Model.xlsx`. It includes:
* `Executive Summary`: KPI cards, strategy comparison table, and GSSM recommendations.
* `Supplier Scorecard`: Multi-criteria weighted scores (Cost, Quality, Delivery, Capacity, ESG).
* `TCO Cost Breakdown`: Element-by-element cost breakdown showing FOB vs Landed costs.
* `Scenario Stress-Testing`: Sensitivity tables for +25% launch surge, logistics delays, and tariffs.
* `PO Transactions Audit`: 150-row granular transaction audit trail.

### 3. Open the Interactive Web Dashboard
Simply double-click or open `dashboard/index.html` in any web browser to view the interactive dashboard featuring:
* Interactive Sourcing Strategy Evaluator (switch between Strategies A through E)
* Dynamic Chart.js visualizations (Quoted FOB vs TCO, Radar Scorecard, Scenario Spend)
* Live insight callouts explaining why cheap suppliers fail standards.

### 4. Review the SQL Analytics
Open `sql/procurement_kpis.sql` to inspect 7 production SQL queries utilizing CTEs, `DENSE_RANK()`, `LAG()`, and aggregation rollups against `data/procurement.db`.

### 5. Review Executive Memo & Resume Guide
* Sourcing Decision Memo: `executive_presentation/EXECUTIVE_SOURCING_MEMO.md`
* Resume Bullets & Interview Guide: `executive_presentation/RESUME_AND_INTERVIEW_GUIDE.md`
