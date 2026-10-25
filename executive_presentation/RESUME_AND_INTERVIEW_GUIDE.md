# Global Sourcing & Supply Manager (GSSM) Interview & Resume Guide

This guide equips you to present this project on your resume and defend it with precision in Global Sourcing & Supply Management (GSSM) interviews.

---

## 1. How to Feature This Project on Your Resume

Add this as a featured project or under a dedicated **Procurement & Supply Chain Analytics Projects** section:

### Option A: Standard 3-Bullet Sourcing Format (Recommended)
```text
Supplier Intelligence & Procurement Optimization Model | Python, SQL, Excel, Power BI
• Developed an enterprise Total Cost of Ownership (TCO) and multi-criteria supplier scorecard for a 12M-unit consumer electronics display sub-assembly, analyzing 1,450+ POs across 6 global tier-1 suppliers.
• Built a quantitative landed-cost model factoring FOB pricing, Section 301 tariffs, inspection metrology, line scrap/rework, and inventory carrying costs, revealing a 14.8% ($5.60/unit) hidden cost penalty in the lowest-bidder quote.
• Designed a 70/30 dual-sourcing allocation model and stress-tested operations against a +25% launch demand surge and freight bottlenecks, delivering $23.38M in verified net enterprise savings while cutting supply risk by 44%.
```

### Option B: Concise 2-Bullet High-Impact Format
```text
Global Sourcing & Supply Chain Optimization Case | Python, SQL, Power BI, Advanced Excel
• Engineered an end-to-end supplier scorecard and TCO financial model in Excel/Python across 6 suppliers to evaluate $500M+ in procurement spend for a flagship smartphone display sub-assembly.
• Quantified trade-offs between quoted FOB price, quality yield (DPPM), and OTIF delivery, recommending a dual-sourcing allocation that achieved $23.38M in net savings and 99.89% line yield under stress-test scenarios.
```

---

## 2. Connecting to GSSM Intern Job Description

the company's Global Sourcing & Supply Manager (GSSM) role focuses on:
1. **Cost Modeling & Should-Cost Analytics:** Breaking down supplier cost drivers (BOM, yield, overhead, logistics).
2. **Supplier Performance Management:** Tracking OTD, DPPM, capacity utilization, and process Cpk.
3. **Allocation & Contract Strategy:** Balancing commercial leverage against operational single-point-of-failure risk.
4. **Executive Cross-Functional Influence:** Presenting data-driven sourcing trade-offs to Operations, Finance, and Engineering leadership.

This project covers all four pillars with real, defensible math.

---

## 3. Top 5 GSSM Interview Questions & Answers (STAR Method)

### Question 1: "How do you evaluate a supplier beyond their quoted unit price?"

**The Key Insight to Convey:** Quoted FOB price is just the tip of the iceberg; operational inefficiencies, tariffs, scrap, and lead time volatility create significant hidden landed costs.

**Your STAR Response:**
> "In my display sub-assembly sourcing project, I evaluated 6 tier-1 suppliers across 1,450 historical shipments. The lowest-priced bidder, Kestrel, quoted **$37.90**, which appeared to offer **$79M in savings** over the incumbent.
> 
> However, I built a comprehensive **Total Cost of Ownership (TCO) model** that accounted for five operational cost drivers beyond FOB price:
> 1. **Section 301 tariffs** (+7.5% duty on China origin = +$2.84/unit).
> 2. **Quality fallout & scrap costs**—Kestrel had an empirical defect rate of 5,239 DPPM, and because defective display modules caused assembly line fallout, each defect cost $35 in teardown and scrap.
> 3. **Mandatory 100% lot screening** ($0.45/unit) to protect final assembly lines.
> 4. **Safety stock carrying costs**—their 35-day lead time with high variance ($\sigma = 4.8$ days) required holding 18 additional days of safety stock at a 20% annual WACC.
> 5. **Emergency air freight expedites** to recover from delays.
> 
> When calculated, Kestrel's true landed TCO was **$43.50/unit**—a **14.8% penalty over their quote** that erased 85% of expected savings while introducing a severe risk of factory line-down events. This demonstrated that the cheapest supplier on paper is rarely the most cost-effective in production."

---

### Question 2: "Tell me about a trade-off you had to make between cost savings and supply-chain risk."

**The Key Insight to Convey:** Showing why dual-sourcing (70/30) is superior to both 100% single-sourcing and naive lowest-cost sourcing.

**Your STAR Response:**
> "I had to decide how to allocate 12 million units of annual demand across candidate suppliers.
> 
> The incumbent supplier, Apex (Korea), had flawless quality (420 DPPM) and 97.5% OTD, but their landed TCO was $46.41/unit, resulting in a **$560M annual enterprise spend**. On the other hand, awarding 100% of volume to the lowest cost contender, Vanguard (Taiwan), would maximize immediate savings but expose to single-fab capacity bottlenecks and geopolitical concentration in Taiwan.
> 
> Instead of choosing between extreme cost or extreme risk, I modeled an **optimal 70/30 dual-sourcing strategy**:
> - Awarding **70% (8.4M units) to Vanguard** captured scale efficiency at $43.21 TCO and kept their fab utilization at 73.7%, well within the safe 85% operating ceiling.
> - Awarding **30% (3.6M units) to Apex** kept our relationship and tooling active, provided high-yield stability for initial EVT/PVT ramp, and gave us an instant 250k unit/month surge buffer.
> 
> This dual-source approach achieved **$23.38M in verified net savings** vs the incumbent baseline while delivering a composite Risk Index of only **18.2 / 100**, the lowest of any strategy evaluated."

---

### Question 3: "How do you model inventory carrying costs and safety stock in your TCO calculation?"

**The Key Insight to Convey:** Demonstrating that longer lead times and high variance directly increase working capital.

**Your STAR Response:**
> "Inventory holding costs aren't static—they depend on transit cycle stock and lead time volatility.
> 
> In my model, I used the company's estimated **20% annual WACC** (cost of capital plus warehouse handling, insurance, and obsolescence risk), which translates to a daily holding rate of `0.20 / 365 = 0.0548%`.
> 
> The inventory tied up per unit equals:
> $$\text{Holding Cost} = \text{Unit Cost} \times \left(\frac{20\%}{365}\right) \times (\text{Transit Lead Time} + \text{Safety Stock Buffer Days})$$
> 
> For a predictable supplier like Apex with a 21-day lead time and $\sigma = 1.2$ days, safety stock buffer was only 14 days, resulting in **$0.43/unit** in carrying costs. For Kestrel, with a 35-day lead time and $\sigma = 4.8$ days, safety stock had to be expanded to 28 days to maintain a 98% service level ($Z = 2.05$), doubling holding costs to **$0.72/unit**. This mathematical approach quantified how poor supplier punctuality directly inflates working capital."

---

### Question 4: "How did you stress-test your sourcing recommendation against unexpected disruptions?"

**The Key Insight to Convey:** Showing resilience under demand shocks, logistics bottlenecks, and tariff changes.

**Your STAR Response:**
> "I developed four stress-test scenarios in Python and SQL:
> 1. **Baseline steady-state demand (12M units)**.
> 2. **Post-Keynote Demand Surge (+25% volume ramp)** to test supplier capacity ceilings.
> 3. **Logistics Bottleneck (+12 days port delay, 2.2x freight rates)** forcing air expedites.
> 4. **Geopolitical Tariff Escalation (+15% tariff on specific origins)**.
> 
> Under the +25% demand surge scenario, Kestrel breached 100% capacity (113% utilization), which would have triggered catastrophic line shutdowns or required multimillion-dollar factory overtime premiums.
> 
> In contrast, our **70/30 Vanguard/Apex split** absorbed the 15M unit surge with zero capacity breaches because Vanguard operated at 92% utilization while Apex scaled to 88%. Under the tariff hike scenario, our Taiwan and Korea dual-sourcing footprint had 0% tariff exposure, whereas a China-concentrated strategy would have suffered a **$113M cost surge**."

---

### Question 5: "If a supplier approached you two weeks before MP (Mass Production) offering an additional $2.00 discount, what would you do?"

**The Key Insight to Convey:** Understanding the cost of late engineering changes, tooling re-qualification, and quality ramp risks.

**Your STAR Response:**
> "As an GSSM, I would not shift volume two weeks before Mass Production without rigorous due diligence.
> 
> First, shifting allocation right before ramp introduces enormous yield and tooling qualification risks. Re-qualifying tooling or modifying allocation during PVT would cost millions in NRE and risk missing our keynote launch ship-date, where each day of delay costs tens of millions in lost retail revenue.
> 
> Second, I would evaluate their motive and cost structure: is this $2.00 price cut economically sustainable via genuine yield improvements and BOM should-cost reductions, or is the supplier buying business and likely to claw back margins via expediting fees or lower QA sampling later?
> 
> Instead, I would use that $2.00 offer as commercial leverage during our next quarterly business review (QBR) to renegotiate our primary supplier's tier pricing, and establish a development milestone for the offering supplier to compete for the next product generation."
