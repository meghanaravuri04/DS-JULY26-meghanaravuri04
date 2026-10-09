"""
streamlit_app.py
----------------
Motor Insurance Analytics Dashboard.
Run:  streamlit run app/streamlit_app.py
"""

import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

# Allow `from src...` imports when running from repo root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logger import setup_logger, log_pipeline_step
from src.insurance_analysis import (
    calculate_total_customers, calculate_total_policies,
    calculate_active_policies, calculate_expired_policies,
    calculate_cancelled_policies, calculate_renewed_policies,
    calculate_total_premium, calculate_average_premium,
    calculate_total_claims, calculate_approved_claims,
    calculate_rejected_claims, calculate_pending_claims,
    calculate_total_claim_amount, calculate_average_claim_amount,
    calculate_claim_approval_rate, calculate_average_claim_settlement_days,
    calculate_total_payment_amount, calculate_claim_to_premium_ratio, calculate_claim_to_coverage_ratio,
    calculate_paid_claim_ratio,
    analyze_customer_claims, analyze_vehicle_claims,
)
from src.insights import generate_business_recommendations

logger = setup_logger()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Motor Insurance Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETTE = px.colors.qualitative.Bold


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading cleaned data...")
def load_dashboard_data(data_dir: str = "data/cleaned") -> dict:
    """Load cleaned CSVs into a dict of DataFrames."""
    log_pipeline_step(f"Dashboard loading cleaned data from {data_dir}")
    files = {
        "customers": "customers_cleaned.csv",
        "vehicles":  "vehicles_cleaned.csv",
        "policies":  "policies_cleaned.csv",
        "claims":    "claims_cleaned.csv",
        "payments":  "payments_cleaned.csv",
    }
    data = {}
    for k, f in files.items():
        path = os.path.join(data_dir, f)
        if not os.path.exists(path):
            st.error(f"Missing file: {path}. Run `python run_pipeline.py` first.")
            st.stop()
        if os.path.getsize(path) == 0:
            st.error(
                f"Cleaned file is empty: {path}. "
                "Rebuild the cleaned data by running `python run_pipeline.py` "
                "from the project folder, then restart the dashboard."
            )
            st.stop()
        data[k] = pd.read_csv(path)

    # Re-parse date columns
    for col in ["policy_start_date", "policy_end_date"]:
        data["policies"][col] = pd.to_datetime(data["policies"][col], errors="coerce")
    for col in ["claim_date", "accident_date", "approval_date", "settlement_date"]:
        data["claims"][col] = pd.to_datetime(data["claims"][col], errors="coerce")
    data["payments"]["payment_date"] = pd.to_datetime(data["payments"]["payment_date"], errors="coerce")
    data["customers"]["date_of_birth"] = pd.to_datetime(data["customers"]["date_of_birth"], errors="coerce")
    return data


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
def show_sidebar_filters(data: dict) -> dict:
    """Return a dict of filter selections and apply them to the data."""
    st.sidebar.title("🔎 Filters")

    p = data["policies"]
    cl = data["claims"]
    v = data["vehicles"]

    policy_types = ["All"] + sorted(p["policy_type"].dropna().unique().tolist())
    policy_status = ["All"] + sorted(p["policy_status"].dropna().unique().tolist())
    claim_status = ["All"] + sorted(cl["claim_status"].dropna().unique().tolist())
    claim_types = ["All"] + sorted(cl["claim_type"].dropna().unique().tolist())
    vehicle_types = ["All"] + sorted(v["vehicle_type"].dropna().unique().tolist())
    vehicle_makes = ["All"] + sorted(v["vehicle_make"].dropna().unique().tolist())
    states = ["All"] + sorted(data["customers"]["state"].dropna().unique().tolist())
    severity = ["All"] + sorted(cl["damage_severity"].dropna().unique().tolist())

    filters = {
        "policy_type":   st.sidebar.selectbox("Policy Type", policy_types),
        "policy_status": st.sidebar.selectbox("Policy Status", policy_status),
        "claim_status":  st.sidebar.selectbox("Claim Status", claim_status),
        "claim_type":    st.sidebar.selectbox("Claim Type", claim_types),
        "vehicle_type":  st.sidebar.selectbox("Vehicle Type", vehicle_types),
        "vehicle_make":  st.sidebar.selectbox("Vehicle Make", vehicle_makes),
        "state":         st.sidebar.selectbox("State", states),
        "damage_severity": st.sidebar.selectbox("Damage Severity", severity),
    }

    # Date range
    if not cl["claim_date"].dropna().empty:
        min_d, max_d = cl["claim_date"].min().date(), cl["claim_date"].max().date()
        date_range = st.sidebar.date_input("Claim Date Range", (min_d, max_d))
        filters["date_range"] = date_range

    return filters


def apply_filters(data: dict, f: dict) -> dict:
    """Apply sidebar filters and return the filtered data dict."""
    p = data["policies"].copy()
    cl = data["claims"].copy()
    v = data["vehicles"].copy()
    c = data["customers"].copy()
    pay = data["payments"].copy()

    # Policies
    if f["policy_type"] != "All":
        p = p[p["policy_type"] == f["policy_type"]]
    if f["policy_status"] != "All":
        p = p[p["policy_status"] == f["policy_status"]]

    # Vehicles
    if f["vehicle_type"] != "All":
        v = v[v["vehicle_type"] == f["vehicle_type"]]
    if f["vehicle_make"] != "All":
        v = v[v["vehicle_make"] == f["vehicle_make"]]

    # Customers
    if f["state"] != "All":
        c = c[c["state"] == f["state"]]

    # Claims
    if f["claim_status"] != "All":
        cl = cl[cl["claim_status"] == f["claim_status"]]
    if f["claim_type"] != "All":
        cl = cl[cl["claim_type"] == f["claim_type"]]
    if f["damage_severity"] != "All":
        cl = cl[cl["damage_severity"] == f["damage_severity"]]
    if "date_range" in f and isinstance(f["date_range"], tuple) and len(f["date_range"]) == 2:
        d1, d2 = pd.to_datetime(f["date_range"][0]), pd.to_datetime(f["date_range"][1])
        cl = cl[(cl["claim_date"] >= d1) & (cl["claim_date"] <= d2)]

    # Cascade: keep only policies/customers/vehicles still present
    p = p[p["customer_id"].isin(c["customer_id"]) & p["vehicle_id"].isin(v["vehicle_id"])]
    cl = cl[cl["policy_id"].isin(p["policy_id"])]
    pay = pay[pay["claim_id"].isin(cl["claim_id"])]

    return {"customers": c, "vehicles": v, "policies": p, "claims": cl, "payments": pay}


# ---------------------------------------------------------------------------
# KPI card helper
# ---------------------------------------------------------------------------
def kpi_row(cards: list):
    """Render a row of KPI cards. cards = [(label, value), ...]"""
    cols = st.columns(len(cards))
    for col, (label, value) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg,#1f77b4,#4a90e2);
                            padding:14px;border-radius:10px;color:white;
                            text-align:center;">
                    <div style="font-size:13px;opacity:0.9;">{label}</div>
                    <div style="font-size:22px;font-weight:700;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Insight card renderer
# ---------------------------------------------------------------------------
def render_insight_card(card: dict, idx: int):
    """Render a single structured insight card."""
    st.markdown(
        f"""
        <div style="border-left:5px solid #d62728;
                    background:#fafafa;padding:14px;border-radius:8px;
                    margin-bottom:12px;">
            <div style="font-weight:700;color:#d62728;margin-bottom:6px;">
                🔴 PATTERN #{idx}
            </div>
            <div style="margin-bottom:8px;">{card['PATTERN']}</div>
            <div style="font-weight:700;color:#1f77b4;">📊 EVIDENCE</div>
            <div style="margin-bottom:8px;">{card['EVIDENCE']}</div>
            <div style="font-weight:700;color:#2ca02c;">💼 BUSINESS MEANING</div>
            <div style="margin-bottom:8px;">{card['BUSINESS_MEANING']}</div>
            <div style="font-weight:700;color:#ff7f0e;">✅ RECOMMENDATION</div>
            <div>{card['RECOMMENDATION']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def show_overview(data: dict):
    st.header("📊 Executive Overview")
    kpi_row([
        ("Total Customers", f"{calculate_total_customers(data):,}"),
        ("Total Policies",  f"{calculate_total_policies(data):,}"),
        ("Active Policies", f"{calculate_active_policies(data):,}"),
        ("Total Premium",   f"₹{calculate_total_premium(data):,.0f}"),
        ("Total Claims",    f"{calculate_total_claims(data):,}"),
        ("Total Claim ₹",   f"₹{calculate_total_claim_amount(data):,.0f}"),
        ("Approval Rate",   f"{calculate_claim_approval_rate(data):.1f}%"),
        ("Avg Settlement",  f"{calculate_average_claim_settlement_days(data):.1f} d"),
    ])

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        vc = data["policies"]["policy_status"].value_counts().reset_index()
        vc.columns = ["Status", "Count"]
        fig = px.pie(vc, names="Status", values="Count", hole=0.45,
                     title="Policy Status", color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        df = data["claims"].copy()
        if not df["claim_date"].dropna().empty:
            df["month"] = df["claim_date"].dt.to_period("M").astype(str)
            g = df.groupby("month").size().reset_index(name="Claims")
            fig = px.line(g, x="month", y="Claims", markers=True,
                          title="Monthly Claims", color_discrete_sequence=["crimson"])
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        vc = data["claims"]["claim_status"].value_counts().reset_index()
        vc.columns = ["Status", "Count"]
        fig = px.bar(vc, x="Status", y="Count", color="Status",
                     title="Claim Status", color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        p = data["policies"].copy()
        if not p["policy_start_date"].dropna().empty:
            p["month"] = p["policy_start_date"].dt.to_period("M").astype(str)
            g = p.groupby("month")["premium_amount"].sum().reset_index()
            fig = px.line(g, x="month", y="premium_amount", markers=True,
                          title="Monthly Premium Trend",
                          color_discrete_sequence=["green"])
            st.plotly_chart(fig, use_container_width=True)


def show_policy_analysis(data: dict):
    st.header("📋 Policy Analysis")
    kpi_row([
        ("Total",     f"{calculate_total_policies(data):,}"),
        ("Active",    f"{calculate_active_policies(data):,}"),
        ("Expired",   f"{calculate_expired_policies(data):,}"),
        ("Cancelled", f"{calculate_cancelled_policies(data):,}"),
        ("Renewed",   f"{calculate_renewed_policies(data):,}"),
        ("Avg Premium", f"₹{calculate_average_premium(data):,.0f}"),
    ])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        vc = data["policies"]["policy_type"].value_counts().reset_index()
        vc.columns = ["Type", "Count"]
        fig = px.pie(vc, names="Type", values="Count", hole=0.45,
                     title="Policy Type Distribution",
                     color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        g = (data["policies"].groupby("policy_type")["premium_amount"].sum()
             .reset_index().sort_values("premium_amount"))
        fig = px.bar(g, x="premium_amount", y="policy_type", orientation="h",
                     title="Total Premium by Policy Type",
                     color="premium_amount", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)


def show_claim_analysis(data: dict):
    st.header("⚠️ Claims Analysis")
    kpi_row([
        ("Total Claims", f"{calculate_total_claims(data):,}"),
        ("Approved",     f"{calculate_approved_claims(data):,}"),
        ("Rejected",     f"{calculate_rejected_claims(data):,}"),
        ("Pending",      f"{calculate_pending_claims(data):,}"),
        ("Avg Claim ₹",  f"₹{calculate_average_claim_amount(data):,.0f}"),
        ("Approval %",   f"{calculate_claim_approval_rate(data):.1f}%"),
    ])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        vc = data["claims"]["claim_type"].value_counts().reset_index()
        vc.columns = ["Type", "Count"]
        fig = px.bar(vc, x="Count", y="Type", orientation="h",
                     title="Claim Type Distribution",
                     color="Count", color_continuous_scale="Sunset")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(data["claims"], x="claim_amount", nbins=30,
                           title="Claim Amount Distribution",
                           color_discrete_sequence=["teal"])
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        claim_policies = data["policies"][["policy_id", "vehicle_id"]]
        df = data["claims"].merge(claim_policies, on="policy_id", how="left")
        df = df.merge(
            data["vehicles"][["vehicle_id", "vehicle_type"]],
            on="vehicle_id", how="left")
        fig = px.box(df, x="vehicle_type", y="claim_amount", color="vehicle_type",
                     title="Claim Amount by Vehicle Type",
                     color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        vc = data["claims"]["damage_severity"].value_counts().reset_index()
        vc.columns = ["Severity", "Count"]
        fig = px.bar(vc, x="Severity", y="Count", color="Severity",
                     title="Damage Severity Distribution",
                     color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)


def show_customer_analysis(data: dict):
    st.header("👥 Customer Analysis")
    df = analyze_customer_claims(data)

    if df.empty:
        st.info("No customer-level claim data available for current filter.")
        return

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df, x="age_group", y="total_claim_amount",
                     title="Claim Amount by Age Group",
                     color="total_claim_amount", color_continuous_scale="Plasma")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(df, x="age_group", y="total_claims",
                     title="Claim Count by Age Group",
                     color="total_claims", color_continuous_scale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer age vs Claim amount")
    m = data["claims"].merge(data["customers"][["customer_id", "customer_age"]],
                             on="customer_id", how="left")
    fig = px.scatter(m, x="customer_age", y="claim_amount", opacity=0.5,
                     title="Customer Age vs Claim Amount",
                     color_discrete_sequence=["purple"])
    st.plotly_chart(fig, use_container_width=True)


def show_vehicle_analysis(data: dict):
    st.header("🚗 Vehicle Analysis")
    df = analyze_vehicle_claims(data)

    if df.empty:
        st.info("No vehicle-claim data available.")
        return

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df, x="vehicle_type", y="total_claim_amount",
                     title="Total Claim Amount by Vehicle Type",
                     color="total_claim_amount", color_continuous_scale="Turbo")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(df, x="vehicle_type", y="avg_claim_amount",
                     title="Average Claim Amount by Vehicle Type",
                     color="avg_claim_amount", color_continuous_scale="Magma")
        st.plotly_chart(fig, use_container_width=True)

    # Fuel type
    v = data["vehicles"]
    vc = v["fuel_type"].value_counts().reset_index()
    vc.columns = ["Fuel", "Count"]
    fig = px.pie(vc, names="Fuel", values="Count", hole=0.4,
                 title="Vehicles by Fuel Type", color_discrete_sequence=PALETTE)
    st.plotly_chart(fig, use_container_width=True)


def show_premium_analysis(data: dict):
    st.header("💰 Premium & Risk")
    kpi_row([
        ("Avg Premium",   f"₹{calculate_average_premium(data):,.0f}"),
        ("Total Premium", f"₹{calculate_total_premium(data):,.0f}"),
        ("Total Payments",f"₹{calculate_total_payment_amount(data):,.0f}"),
        ("Claim/Premium", f"{calculate_claim_to_premium_ratio(data):.2f}"),
        ("Claim/Coverage",f"{calculate_claim_to_coverage_ratio(data):.2f}"),
        ("Paid/Claim",    f"{calculate_paid_claim_ratio(data):.2f}"),
    ])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        g = (data["claims"].groupby("policy_type")["claim_to_premium_ratio"]
             .mean().dropna().reset_index())
        fig = px.bar(g, x="policy_type", y="claim_to_premium_ratio",
                     title="Claim-to-Premium Ratio by Policy Type",
                     color="claim_to_premium_ratio", color_continuous_scale="Reds")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        vc = data["payments"]["payment_status"].value_counts().reset_index()
        vc.columns = ["Status", "Count"]
        fig = px.pie(vc, names="Status", values="Count", hole=0.4,
                     title="Payment Status", color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)


def show_insights(data: dict):
    st.header("💡 Insights & Recommendations")
    st.caption("All insights are computed live from the current filter selection.")
    cards = generate_business_recommendations(data)
    if not cards:
        st.info("No insights available for current filter.")
        return
    for i, card in enumerate(cards, 1):
        render_insight_card(card, i)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    st.title("🚗 Motor Insurance Analytics Dashboard")
    st.caption("End-to-end analytics — Portfolio · Premium · Claims · Risk")

    data = load_dashboard_data()
    filters = show_sidebar_filters(data)
    filtered = apply_filters(data, filters)

    page = st.sidebar.radio(
        "📄 Navigation",
        ["Executive Overview", "Policy Analysis", "Claims Analysis",
         "Customer Analysis", "Vehicle Analysis",
         "Premium & Risk", "Insights & Recommendations"],
    )

    if page == "Executive Overview":
        show_overview(filtered)
    elif page == "Policy Analysis":
        show_policy_analysis(filtered)
    elif page == "Claims Analysis":
        show_claim_analysis(filtered)
    elif page == "Customer Analysis":
        show_customer_analysis(filtered)
    elif page == "Vehicle Analysis":
        show_vehicle_analysis(filtered)
    elif page == "Premium & Risk":
        show_premium_analysis(filtered)
    elif page == "Insights & Recommendations":
        show_insights(filtered)


if __name__ == "__main__":
    main()