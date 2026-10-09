# 🚗 Motor Insurance Analytics

End-to-end analytics project for a motor insurance company:
data validation → cleaning pipeline → EDA → KPIs → insights → Streamlit dashboard →
Docker → AWS ECR → AWS EC2.

## 📌 Business Scenario
A motor insurance company manages customers, vehicles, policies, claims, and payments.
Management needs to understand policy activity, premium collections, claim behavior,
severity, settlement performance, and risk patterns.

## 🎯 Objectives
- Clean & validate raw operational data
- Compute insurance KPIs
- Answer business questions
- Identify patterns and recommend actions
- Deliver a Streamlit dashboard
- Deploy on AWS EC2 via Docker + ECR

## 🧰 Technology Stack
Python · Pandas · NumPy · Matplotlib · Seaborn · Plotly · Streamlit · Pytest ·
Docker · AWS ECR · AWS EC2 · Git

## 🗂 Data Model
| Table | Primary Key | Relationships |
|-------|-------------|---------------|
| customers | customer_id | → policies |
| vehicles | vehicle_id | → policies |
| policies | policy_id | customer_id, vehicle_id |
| claims | claim_id | policy_id, customer_id |
| payments | payment_id | claim_id, policy_id |

## 📁 Project Structure
See tree in repository root.

## ⚙️ Installation
```bash
git clone <repo_url>
cd motor_insurance_analytics
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt