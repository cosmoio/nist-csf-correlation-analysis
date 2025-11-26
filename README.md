# NIST CSF 2.0 Rater Correlation Analysis

Analyze and visualize inter-rater reliability for NIST CSF 2.0 security assessments using Python

### Why this exists

When assessing security maturity, different managers often have different perceptions. This tool uses Spearman's Rank Correlation to visualize:
* Global Alignment: Do managers generally agree on the security posture?
* Category Drill-down: Are there specific domains (e.g., PROTECT or DETECT) where the team is misaligned?

### Visuals

### How to use
1. Clone the repo.
2. Install requirements: pip install -r requirements.txt
3. Replace data/synthetic_ratings.csv with your internal assessment data.
4. (Optional) Run the Jupyter Notebook or on console

## Sample Analysis & Interpretation

The following analysis is based on the provided synthetic_nist_ratings.csv dataset.

### Global Alignment (The "Big Picture")

In our synthetic dataset, we observe a Global Spearman Correlation ranging between 0.65 and 0.85 for most manager pairs.

**Interpretation:** This indicates a generally strong consensus on the organization's security posture.

**Outlier Detection:** Manager_4 consistently shows lower correlation (approx 0.45) with the rest of the group. This suggests Manager_4 may be using a different baseline for "maturity" (e.g., they might be a "strict rater" compared to the group).

### Domain-Specific Friction (Category Breakdown)

When we drill down into specific NIST Functions, distinct patterns emerge:
**High Agreement in PROTECT (PR):** The correlation is highest in the PROTECT function (> 0.85). This is expected, as technical controls (e.g., "Is MFA enabled?") are binary and objective.
**Divergence in GOVERN (GV):** The correlation drops significantly in the GOVERN function (< 0.50). Policy interpretation is subjective; one manager might rate a policy as "Implemented" (Tier 3) while another rates it as "Partial" (Tier 2) because it lacks automation.

### Top Disagreements (Actionable Insights)

The script identified the following subcategories with the highest Standard Deviation (σ>1.5):
GV.OC-03 (Organizational Culture): High variance suggests leadership is not aligned on the definition of security culture.
DE.AE-01 (Anomalies Detected): Disagreement here often stems from visibility gaps—some managers may not be aware of specific monitoring tools.

### Deep Dive: Category Analysis

The tool also generates correlation matrices for individual NIST Categories (e.g., GV.OC, PR.DS).

**Why this matters:** Global metrics often hide specific operational disagreements. For example, managers might align on Governance overall, but have negative correlation specifically on Supply Chain Risk Management (GV.SC), indicating a specific area where policy definitions are unclear.

## How to Read These Results

If you are using this tool for your own organization, use this guide to interpret your correlation coefficients (ρ):

| Spearman ρ  | Interpretation      | Recommended Action                                                                                                                               |
| ----------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0.80 - 1.00 | Strong Alignment    | No action needed. The team shares a unified view of risk.                                                                                        |
| 0.50 - 0.79 | Moderate Alignment  | Calibration Required. Discuss the specific Categories where the dip occurs.                                                                      |
| < 0.50      | Weak / No Alignment | Urgent Review. The team is fundamentally misaligned. You are likely assessing different scopes or have different definitions of the scale (1-5). |

