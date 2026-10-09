# Motor Insurance Analytics — Business Report

## 1. Executive Summary
This report presents an analytical review of the motor insurance portfolio covering
policies, premiums, claims, settlements, and customer / vehicle segments. The cleaned
data and KPIs reveal portfolio concentration, claim severity patterns, and risk
indicators that management can act upon.

## 2. Business Problem
Management needs a reliable view of:
- Active vs expired policies
- Premium concentration by policy type
- Claim volume, severity, and approval behavior
- Regional and vehicle-based risk patterns
- Claim-to-premium ratios signalling unprofitable segments

## 3. Data and Table Summary
| Table | Rows | Key |
|-------|------|-----|
| customers | — | customer_id |
| vehicles | — | vehicle_id |
| policies | — | policy_id |
| claims | — | claim_id |
| payments | — | payment_id |

Relationships:
- policies → customers, vehicles
- claims → policies, customers
- payments → claims, policies

## 4. Data Quality Findings
- Missing values handled with median (numeric) and "Unknown" (categorical)
- Duplicate rows removed from each table
- Invalid statuses and negative amounts dropped
- Date columns coerced to datetime

## 5. Cleaning Performed
- Standardized text columns
- Enforced business rules (premium > 0, dates valid)
- Created derived columns: policy_duration_days, customer_age, vehicle_age,
  claim_processing_days, claim_settlement_days, claim_to_premium_ratio,
  claim_to_coverage_ratio, paid_claim_ratio, policy_active_flag

## 6. KPI Summary
- Total Policies / Active / Expired / Cancelled / Renewed
- Total Premium, Avg Premium, Avg Coverage
- Total Claims, Approval %, Rejection %, Avg Claim Amount
- Avg Processing / Settlement Days
- Claim-to-Premium Ratio, Paid-Claim Ratio

## 7. EDA Findings
- Policy type distribution is skewed to one product
- Claim amount distribution is right-skewed
- Certain vehicle types produce significantly higher average claim amounts
- Settlement time varies by claim type

## 8. Important Patterns
- A small set of vehicle groups contributes a disproportionate share of claim value
- One region shows higher claim frequency than the portfolio average
- One policy segment shows a high claim-to-premium ratio

## 9. Business Insights
- Portfolio active share is healthy / low (see dashboard)
- Claims are concentrated in one claim type — cost concentration risk
- Some vehicle types & regions require deeper underwriting review

## 10. Recommendations
- Re-price or re-underwrite high claim-to-premium policy types
- Automate settlement workflows for the slowest claim type
- Launch renewal campaigns for lapsed policies
- Targeted retention for the top-premium age segment

## 11. Dashboard Summary
7 pages: Executive Overview, Policy, Claims, Customer, Vehicle,
Premium & Risk, Insights & Recommendations.
Sidebar filters drive KPIs, charts, and insights live.

## 12. Deployment Summary
- Containerized with Docker
- Image pushed to Amazon ECR
- Deployed on AWS EC2
- Streamlit served on port 8501
- Live URL submitted via Admin Google Form

## 13. Conclusion
The Motor Insurance Analytics solution converts raw operational tables into a
validated, reusable analytical pipeline with KPIs, dashboards, and actionable
insights. It provides a scalable foundation for underwriting, pricing, and
operational improvements.