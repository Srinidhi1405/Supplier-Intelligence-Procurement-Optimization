"""
GSSM Procurement Model Generator
Builds a professional multi-tab Excel Workbook with formatting, KPI cards, and formulas.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_EXCEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TechCorp_GSSM_Procurement_Optimization_Model.xlsx")

def create_styled_excel():
    print("Generating GSSM Financial Cost & Sourcing Excel Model...")
    
    # Load data
    df_suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
    df_scorecard = pd.read_csv(os.path.join(DATA_DIR, "supplier_scorecard.csv"))
    df_scenarios = pd.read_csv(os.path.join(DATA_DIR, "scenario_simulation_results.csv"))
    df_strategies = pd.read_csv(os.path.join(DATA_DIR, "sourcing_allocation_strategies.csv"))
    df_pos = pd.read_csv(os.path.join(DATA_DIR, "purchase_orders.csv")).head(150) # Sample 150 POs for the sheet
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # palette styles
    DARK_HEADER_FILL = PatternFill(start_color="1C1C1E", end_color="1C1C1E", fill_type="solid")
    ACCENT_BLUE_FILL = PatternFill(start_color="0071E3", end_color="0071E3", fill_type="solid")
    LIGHT_GRAY_FILL = PatternFill(start_color="F5F5F7", end_color="F5F5F7", fill_type="solid")
    CARD_BG_FILL = PatternFill(start_color="E8ECEF", end_color="E8ECEF", fill_type="solid")
    HIGHLIGHT_GREEN = PatternFill(start_color="D1E7DD", end_color="D1E7DD", fill_type="solid")
    HIGHLIGHT_AMBER = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
    HIGHLIGHT_RED = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")
    
    FONT_TITLE = Font(name="Segoe UI", size=16, bold=True, color="1C1C1E")
    FONT_SUBTITLE = Font(name="Segoe UI", size=10, italic=True, color="6E6E73")
    FONT_HEADER = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Segoe UI", size=10, bold=True, color="1C1C1E")
    FONT_REGULAR = Font(name="Segoe UI", size=10, color="1C1C1E")
    FONT_KPI_VAL = Font(name="Segoe UI", size=20, bold=True, color="0071E3")
    FONT_KPI_LABEL = Font(name="Segoe UI", size=9, bold=True, color="6E6E73")
    
    THIN_BORDER = Border(
        left=Side(style='thin', color='D2D2D7'),
        right=Side(style='thin', color='D2D2D7'),
        top=Side(style='thin', color='D2D2D7'),
        bottom=Side(style='thin', color='D2D2D7')
    )
    
    # ----------------------------------------------------
    # TAB 1: EXECUTIVE SUMMARY & ALLOCATION STRATEGIES
    # ----------------------------------------------------
    ws_exec = wb.create_sheet(title="Executive Summary")
    ws_exec.views.sheetView[0].showGridLines = True
    
    # Header Title
    ws_exec["B2"] = "TechCorp Inc.. | Global Sourcing & Supply Management (GSSM)"
    ws_exec["B2"].font = FONT_SUBTITLE
    ws_exec["B3"] = "Apollo Pro OLED Sourcing Optimization & TCO Model"
    ws_exec["B3"].font = FONT_TITLE
    ws_exec["B4"] = "Decision Case: Dual-Sourcing Allocation & Total Cost of Ownership Evaluation | Fiscal Year 2025-2026"
    ws_exec["B4"].font = FONT_SUBTITLE
    
    # KPI Metric Cards
    cards = [
        ("TOTAL ANNUAL DEMAND", "12.0M Units", "B6", "C7"),
        ("RECOMMENDED STRATEGY", "Strategy D (Dual)", "D6", "E7"),
        ("NET COST SAVINGS", "$23.38M vs Incumbent", "F6", "G7"),
        ("BLENDED QUALITY YIELD", "1,097 DPPM (99.89%)", "H6", "I7")
    ]
    for label, val, top_left, bot_right in cards:
        ws_exec.merge_cells(f"{top_left}:{bot_right}")
        cell = ws_exec[top_left]
        cell.value = f"{label}\n{val}"
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.fill = CARD_BG_FILL
        cell.font = FONT_BOLD
        cell.border = THIN_BORDER
    
    # Section Header: Sourcing Strategy Comparison
    ws_exec["B9"] = "Strategic Allocation Models & Financial Trade-Offs"
    ws_exec["B9"].font = Font(name="Segoe UI", size=13, bold=True, color="0071E3")
    
    strat_headers = [
        "Sourcing Strategy Name", "Allocation Split", "Blended Quoted Price ($)",
        "Blended TCO ($/Unit)", "Hidden Cost Delta ($)", "Blended DPPM", "Blended OTD %",
        "Total Enterprise Spend ($M)", "Net Savings vs Incumbent ($M)", "Risk Index (0-100)"
    ]
    
    for col_idx, h in enumerate(strat_headers, start=2):
        cell = ws_exec.cell(row=11, column=col_idx, value=h)
        cell.fill = DARK_HEADER_FILL
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    for r_idx, (_, row) in enumerate(df_strategies.iterrows(), start=12):
        ws_exec.cell(row=r_idx, column=2, value=row["strategy_name"]).font = FONT_BOLD
        ws_exec.cell(row=r_idx, column=3, value=row["supplier_allocation"]).alignment = Alignment(horizontal="center")
        ws_exec.cell(row=r_idx, column=4, value=row["blended_quoted_price"]).number_format = '$#,##0.00'
        ws_exec.cell(row=r_idx, column=5, value=row["blended_tco_per_unit"]).number_format = '$#,##0.00'
        ws_exec.cell(row=r_idx, column=6, value=row["hidden_tco_premium"]).number_format = '$#,##0.00'
        ws_exec.cell(row=r_idx, column=7, value=int(row["blended_dppm"])).number_format = '#,##0'
        ws_exec.cell(row=r_idx, column=8, value=row["blended_otd_pct"] / 100.0).number_format = '0.0%'
        ws_exec.cell(row=r_idx, column=9, value=row["total_enterprise_cost_m"]).number_format = '$#,##0.00'
        
        savings_cell = ws_exec.cell(row=r_idx, column=10, value=row["net_savings_vs_incumbent_m"])
        savings_cell.number_format = '$#,##0.00'
        if row["net_savings_vs_incumbent_m"] > 20:
            savings_cell.fill = HIGHLIGHT_GREEN
            savings_cell.font = FONT_BOLD
            
        risk_cell = ws_exec.cell(row=r_idx, column=11, value=row["risk_index"])
        risk_cell.number_format = '0.0'
        if row["risk_index"] > 80:
            risk_cell.fill = HIGHLIGHT_RED
            risk_cell.font = FONT_BOLD
        elif row["risk_index"] < 20:
            risk_cell.fill = HIGHLIGHT_GREEN
            risk_cell.font = FONT_BOLD
            
        for col_idx in range(2, 12):
            c = ws_exec.cell(row=r_idx, column=col_idx)
            c.border = THIN_BORDER
            if col_idx in [3, 7, 8, 11]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx >= 4:
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # Recommendation Callout Box
    ws_exec["B18"] = "EXECUTIVE RECOMMENDATION (GSSM SOURCING COMMITTEE):"
    ws_exec["B18"].font = Font(name="Segoe UI", size=11, bold=True, color="0071E3")
    
    rec_text = (
        "1. Adopt Strategy D (70% Vanguard Taichung / 30% Apex Paju) for the Apollo Pro ramp.\n"
        "2. The 'Lowest Quoted Bidder' (Kestrel @ $37.90) represents a classic procurement trap: post-landed TCO reaches $43.50 "
        "due to 5,239 DPPM, $0.45/unit mandatory sorting, and Section 301 tariffs, with extreme line-down risk (94.0 Risk Index).\n"
        "3. Strategy D captures $23.38M in hard net enterprise savings versus incumbent Apex single-sourcing while maintaining "
        "sub-1,100 DPPM, 95%+ OTIF fulfillment, and dual-fab redundancy across Taiwan and Korea."
    )
    ws_exec.merge_cells("B19:K22")
    callout = ws_exec["B19"]
    callout.value = rec_text
    callout.fill = LIGHT_GRAY_FILL
    callout.font = FONT_REGULAR
    callout.alignment = Alignment(vertical="top", wrap_text=True)
    callout.border = THIN_BORDER

    # ----------------------------------------------------
    # TAB 2: SUPPLIER SCORECARD (MCDA)
    # ----------------------------------------------------
    ws_score = wb.create_sheet(title="Supplier Scorecard")
    ws_score.views.sheetView[0].showGridLines = True
    
    ws_score["B2"] = "Sourcing Decision Matrix | Multi-Criteria Supplier Scorecard"
    ws_score["B2"].font = FONT_TITLE
    ws_score["B3"] = "Evaluation Weights: TCO Cost (30%), Quality (25%), Delivery (20%), Capacity (15%), Geopolitical/ESG (10%)"
    ws_score["B3"].font = FONT_SUBTITLE
    
    score_cols = [
        "Rank", "Supplier ID", "Supplier Name", "Location", "Quoted Price ($)", "Effective TCO ($)",
        "Hidden Penalty ($)", "Defect DPPM", "OTD %", "Cost Score (30%)", "Quality Score (25%)",
        "Delivery Score (20%)", "Capacity Score (15%)", "ESG/Geo Score (10%)", "Composite Score (100%)"
    ]
    
    for col_idx, col_name in enumerate(score_cols, start=2):
        cell = ws_score.cell(row=5, column=col_idx, value=col_name)
        cell.fill = DARK_HEADER_FILL
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    for r_idx, (_, row) in enumerate(df_scorecard.iterrows(), start=6):
        ws_score.cell(row=r_idx, column=2, value=row["rank"]).alignment = Alignment(horizontal="center")
        ws_score.cell(row=r_idx, column=3, value=row["supplier_id"]).alignment = Alignment(horizontal="center")
        ws_score.cell(row=r_idx, column=4, value=row["supplier_name"]).font = FONT_BOLD
        ws_score.cell(row=r_idx, column=5, value=row["country"]).alignment = Alignment(horizontal="center")
        ws_score.cell(row=r_idx, column=6, value=row["quoted_price"]).number_format = '$#,##0.00'
        ws_score.cell(row=r_idx, column=7, value=row["effective_tco"]).number_format = '$#,##0.00'
        ws_score.cell(row=r_idx, column=8, value=row["hidden_tco_cost"]).number_format = '$#,##0.00'
        ws_score.cell(row=r_idx, column=9, value=int(row["defect_dppm"])).number_format = '#,##0'
        ws_score.cell(row=r_idx, column=10, value=row["otd_pct"] / 100.0).number_format = '0.0%'
        
        ws_score.cell(row=r_idx, column=11, value=row["score_cost"]).number_format = '0.0'
        ws_score.cell(row=r_idx, column=12, value=row["score_quality"]).number_format = '0.0'
        ws_score.cell(row=r_idx, column=13, value=row["score_delivery"]).number_format = '0.0'
        ws_score.cell(row=r_idx, column=14, value=row["score_capacity"]).number_format = '0.0'
        ws_score.cell(row=r_idx, column=15, value=row["score_geopolitical_esg"]).number_format = '0.0'
        
        comp_cell = ws_score.cell(row=r_idx, column=16, value=row["composite_sourcing_score"])
        comp_cell.number_format = '0.0'
        comp_cell.font = FONT_BOLD
        if row["rank"] == 1:
            comp_cell.fill = HIGHLIGHT_GREEN
        elif row["rank"] >= 5:
            comp_cell.fill = HIGHLIGHT_RED
            
        for c_idx in range(2, 17):
            cell = ws_score.cell(row=r_idx, column=c_idx)
            cell.border = THIN_BORDER
            if c_idx in [2, 3, 5, 9, 10]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [4]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")

    # ----------------------------------------------------
    # TAB 3: TCO BREAKDOWN MATRIX
    # ----------------------------------------------------
    ws_tco = wb.create_sheet(title="TCO Cost Breakdown")
    ws_tco.views.sheetView[0].showGridLines = True
    
    ws_tco["B2"] = "Total Cost of Ownership (TCO) Granular Breakdown"
    ws_tco["B2"].font = FONT_TITLE
    ws_tco["B3"] = "Demonstrating Quoted FOB Price vs Landed Operational Costs (12.0M Annual Units)"
    ws_tco["B3"].font = FONT_SUBTITLE
    
    tco_headers = [
        "Supplier ID", "Supplier Name", "Origin", "Quoted FOB ($)", "Freight & Duty ($)",
        "Inspection ($)", "Scrap / Rework ($)", "Inventory Holding ($)", "Total Landed TCO ($)",
        "TCO Delta vs Quote ($)", "% Hidden Cost Penalty"
    ]
    for col_idx, h in enumerate(tco_headers, start=2):
        cell = ws_tco.cell(row=5, column=col_idx, value=h)
        cell.fill = DARK_HEADER_FILL
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER

    # Load empirical metrics for the TCO sheet
    df_kpi = pd.read_csv(os.path.join(DATA_DIR, "supplier_kpi_summary.csv"))
    for r_idx, (_, row) in enumerate(df_kpi.iterrows(), start=6):
        tot_units = row["total_units_delivered"]
        unit_freight_duty = (row["total_freight_spend"] + row["total_tariff_spend"]) / tot_units
        unit_inspect = row["total_inspection_spend"] / tot_units
        unit_scrap = row["total_defect_scrap_spend"] / tot_units
        unit_holding = row["total_holding_spend"] / tot_units
        
        ws_tco.cell(row=r_idx, column=2, value=row["supplier_id"]).alignment = Alignment(horizontal="center")
        ws_tco.cell(row=r_idx, column=3, value=row["supplier_name"]).font = FONT_BOLD
        ws_tco.cell(row=r_idx, column=4, value=row["country"]).alignment = Alignment(horizontal="center")
        ws_tco.cell(row=r_idx, column=5, value=row["avg_quoted_unit_price"]).number_format = '$#,##0.00'
        ws_tco.cell(row=r_idx, column=6, value=unit_freight_duty).number_format = '$#,##0.00'
        ws_tco.cell(row=r_idx, column=7, value=unit_inspect).number_format = '$#,##0.00'
        ws_tco.cell(row=r_idx, column=8, value=unit_scrap).number_format = '$#,##0.00'
        ws_tco.cell(row=r_idx, column=9, value=unit_holding).number_format = '$#,##0.00'
        ws_tco.cell(row=r_idx, column=10, value=row["avg_effective_tco_per_unit"]).number_format = '$#,##0.00'
        ws_tco.cell(row=r_idx, column=11, value=row["tco_cost_delta_per_unit"]).number_format = '$#,##0.00'
        
        pct_cell = ws_tco.cell(row=r_idx, column=12, value=row["tco_cost_delta_pct"] / 100.0)
        pct_cell.number_format = '0.0%'
        if row["tco_cost_delta_pct"] > 12.0:
            pct_cell.fill = HIGHLIGHT_RED
            pct_cell.font = FONT_BOLD
        else:
            pct_cell.fill = HIGHLIGHT_GREEN
            
        for c_idx in range(2, 13):
            cell = ws_tco.cell(row=r_idx, column=c_idx)
            cell.border = THIN_BORDER
            if c_idx in [2, 4]:
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="left")
            else:
                cell.alignment = Alignment(horizontal="right")

    # ----------------------------------------------------
    # TAB 4: SCENARIO STRESS-TEST ANALYSIS
    # ----------------------------------------------------
    ws_scn = wb.create_sheet(title="Scenario Stress-Testing")
    ws_scn.views.sheetView[0].showGridLines = True
    
    ws_scn["B2"] = "Supply Continuity & Scenario Stress-Testing"
    ws_scn["B2"].font = FONT_TITLE
    ws_scn["B3"] = "Sensitivity Analysis: Baseline vs +25% Demand Surge vs Logistics Shock vs Tariffs"
    ws_scn["B3"].font = FONT_SUBTITLE
    
    scn_headers = [
        "Scenario ID", "Scenario Description", "Supplier Name", "Origin", "Required Volume",
        "Base FOB ($)", "Freight ($)", "Duty ($)", "Scrap ($)", "Unit TCO ($)",
        "Enterprise Spend ($M)", "Capacity Util %", "Capacity Breached?"
    ]
    for col_idx, h in enumerate(scn_headers, start=2):
        cell = ws_scn.cell(row=5, column=col_idx, value=h)
        cell.fill = DARK_HEADER_FILL
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    for r_idx, (_, row) in enumerate(df_scenarios.iterrows(), start=6):
        ws_scn.cell(row=r_idx, column=2, value=row["scenario_id"]).alignment = Alignment(horizontal="center")
        ws_scn.cell(row=r_idx, column=3, value=row["scenario_name"]).font = FONT_BOLD
        ws_scn.cell(row=r_idx, column=4, value=row["supplier_name"])
        ws_scn.cell(row=r_idx, column=5, value=row["country"]).alignment = Alignment(horizontal="center")
        ws_scn.cell(row=r_idx, column=6, value=row["annual_volume_needed"]).number_format = '#,##0'
        ws_scn.cell(row=r_idx, column=7, value=row["unit_quoted_price"]).number_format = '$#,##0.00'
        ws_scn.cell(row=r_idx, column=8, value=row["unit_freight"]).number_format = '$#,##0.00'
        ws_scn.cell(row=r_idx, column=9, value=row["unit_tariff"]).number_format = '$#,##0.00'
        ws_scn.cell(row=r_idx, column=10, value=row["unit_scrap"]).number_format = '$#,##0.00'
        ws_scn.cell(row=r_idx, column=11, value=row["scenario_unit_tco"]).number_format = '$#,##0.00'
        ws_scn.cell(row=r_idx, column=12, value=row["total_spend_millions"]).number_format = '$#,##0.00'
        
        util_cell = ws_scn.cell(row=r_idx, column=13, value=row["capacity_utilization_pct"] / 100.0)
        util_cell.number_format = '0.0%'
        
        breach_cell = ws_scn.cell(row=r_idx, column=14, value="YES - CRITICAL" if row["capacity_breached"] else "NO - SUFFICIENT")
        breach_cell.alignment = Alignment(horizontal="center")
        if row["capacity_breached"]:
            breach_cell.fill = HIGHLIGHT_RED
            breach_cell.font = FONT_BOLD
        else:
            breach_cell.fill = HIGHLIGHT_GREEN
            
        for c_idx in range(2, 15):
            cell = ws_scn.cell(row=r_idx, column=c_idx)
            cell.border = THIN_BORDER
            if c_idx in [2, 5, 14]:
                cell.alignment = Alignment(horizontal="center")
            elif c_idx in [3, 4]:
                cell.alignment = Alignment(horizontal="left")
            else:
                cell.alignment = Alignment(horizontal="right")

    # ----------------------------------------------------
    # TAB 5: PURCHASE ORDERS LOG (AUDIT SAMPLE)
    # ----------------------------------------------------
    ws_pos = wb.create_sheet(title="PO Transactions Audit")
    ws_pos.views.sheetView[0].showGridLines = True
    
    ws_pos["B2"] = "Purchase Order Execution Audit Trail (Representative Sample)"
    ws_pos["B2"].font = FONT_TITLE
    ws_pos["B3"] = "Granular PO records showing committed vs actual lead times, DPPM, freight expediting, and TCO"
    ws_pos["B3"].font = FONT_SUBTITLE
    
    po_display_cols = [
        "po_number", "supplier_name", "quarter", "order_date", "actual_delivery_date",
        "ordered_qty", "delivered_qty", "defect_qty", "defect_dppm", "on_time_in_full",
        "freight_mode", "unit_quoted_price", "effective_tco_per_unit", "total_po_tco"
    ]
    po_headers = [
        "PO Number", "Supplier Name", "Quarter", "Order Date", "Delivery Date",
        "Ordered Qty", "Delivered Qty", "Defects", "DPPM", "OTIF?",
        "Freight Mode", "Quoted ($)", "TCO/Unit ($)", "Total PO TCO ($)"
    ]
    for col_idx, h in enumerate(po_headers, start=2):
        cell = ws_pos.cell(row=5, column=col_idx, value=h)
        cell.fill = DARK_HEADER_FILL
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = THIN_BORDER
        
    for r_idx, (_, row) in enumerate(df_pos.iterrows(), start=6):
        ws_pos.cell(row=r_idx, column=2, value=row["po_number"]).alignment = Alignment(horizontal="center")
        ws_pos.cell(row=r_idx, column=3, value=row["supplier_name"])
        ws_pos.cell(row=r_idx, column=4, value=row["quarter"]).alignment = Alignment(horizontal="center")
        ws_pos.cell(row=r_idx, column=5, value=row["order_date"]).alignment = Alignment(horizontal="center")
        ws_pos.cell(row=r_idx, column=6, value=row["actual_delivery_date"]).alignment = Alignment(horizontal="center")
        ws_pos.cell(row=r_idx, column=7, value=row["ordered_qty"]).number_format = '#,##0'
        ws_pos.cell(row=r_idx, column=8, value=row["delivered_qty"]).number_format = '#,##0'
        ws_pos.cell(row=r_idx, column=9, value=row["defect_qty"]).number_format = '#,##0'
        ws_pos.cell(row=r_idx, column=10, value=row["defect_dppm"]).number_format = '#,##0'
        
        otif_cell = ws_pos.cell(row=r_idx, column=11, value="YES" if row["on_time_in_full"] else "NO")
        otif_cell.alignment = Alignment(horizontal="center")
        if not row["on_time_in_full"]:
            otif_cell.fill = HIGHLIGHT_AMBER
            
        ws_pos.cell(row=r_idx, column=12, value=row["freight_mode"]).alignment = Alignment(horizontal="center")
        ws_pos.cell(row=r_idx, column=13, value=row["unit_quoted_price"]).number_format = '$#,##0.00'
        ws_pos.cell(row=r_idx, column=14, value=row["effective_tco_per_unit"]).number_format = '$#,##0.00'
        ws_pos.cell(row=r_idx, column=15, value=row["total_po_tco"]).number_format = '$#,##0.00'
        
        for c_idx in range(2, 16):
            cell = ws_pos.cell(row=r_idx, column=c_idx)
            cell.border = THIN_BORDER
            if c_idx in [2, 4, 5, 6, 11, 12]:
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="left")
            else:
                cell.alignment = Alignment(horizontal="right")

    # Auto-adjust column widths for all worksheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if '\n' in val_str:
                    val_str = max(val_str.split('\n'), key=len)
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
            
    wb.save(OUTPUT_EXCEL)
    print(f"Successfully generated Excel Model at: {OUTPUT_EXCEL}")

if __name__ == "__main__":
    create_styled_excel()
