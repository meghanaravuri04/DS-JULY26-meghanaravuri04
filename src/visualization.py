"""Matplotlib/Seaborn chart functions. Every chart has title + labels."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from src.logger import setup_logger
from src.insurance_analysis import merge_claims_with_vehicle_data

logger = setup_logger()
sns.set_style("whitegrid")
PALETTE = "viridis"


def _finalize(title, xlabel=None, ylabel=None):
    plt.title(title, fontsize=13, fontweight="bold")
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()


def _boxplot_by_category(ax, data, category, value):
    grouped = data.groupby(category, sort=True, observed=True)[value]
    labels = list(grouped.groups)
    if not labels:
        return
    values = [grouped.get_group(label).dropna().to_numpy() for label in labels]
    artists = ax.boxplot(values, patch_artist=True)
    for patch, color in zip(artists["boxes"], sns.color_palette(PALETTE, len(labels))):
        patch.set_facecolor(color)
    ax.set_xticks(range(1, len(labels) + 1), labels=labels)


def plot_policy_status(data):
    df = data["policies"]["policy_status"].value_counts()
    plt.figure(figsize=(7, 5))
    sns.barplot(x=df.index, y=df.values, hue=df.index, palette=PALETTE, legend=False)
    _finalize("Policy Status Distribution", "Status", "Count")
    return plt.gcf()


def plot_policy_type_distribution(data):
    df = data["policies"]["policy_type"].value_counts()
    plt.figure(figsize=(7, 5))
    plt.pie(df.values, labels=df.index, autopct="%1.1f%%",
            colors=sns.color_palette(PALETTE, len(df)))
    plt.title("Policy Type Distribution", fontsize=13, fontweight="bold")
    plt.tight_layout()
    return plt.gcf()


def plot_premium_by_policy_type(data):
    df = data["policies"].groupby("policy_type")["premium_amount"].sum().sort_values()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df.values, y=df.index, hue=df.index, palette=PALETTE, legend=False)
    _finalize("Total Premium by Policy Type", "Premium", "Policy Type")
    return plt.gcf()


def plot_monthly_claims(data):
    df = data["claims"].copy()
    df["month"] = df["claim_date"].dt.to_period("M").astype(str)
    g = df.groupby("month").size()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=g.index, y=g.values, marker="o", color="crimson")
    _finalize("Monthly Claims Trend", "Month", "Claims")
    return plt.gcf()


def plot_claim_status(data):
    df = data["claims"]["claim_status"].value_counts()
    plt.figure(figsize=(7, 5))
    sns.barplot(x=df.index, y=df.values, hue=df.index, palette="magma", legend=False)
    _finalize("Claim Status Distribution", "Status", "Count")
    return plt.gcf()


def plot_claim_type_distribution(data):
    df = data["claims"]["claim_type"].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df.values, y=df.index, hue=df.index, palette="coolwarm", legend=False)
    _finalize("Claim Type Distribution", "Count", "Claim Type")
    return plt.gcf()


def plot_claim_amount_distribution(data):
    plt.figure(figsize=(8, 5))
    sns.histplot(data["claims"]["claim_amount"], kde=True, color="teal", bins=30)
    _finalize("Claim Amount Distribution", "Claim Amount", "Frequency")
    return plt.gcf()


def plot_claim_amount_by_vehicle_type(data):
    df = merge_claims_with_vehicle_data(data)
    fig, ax = plt.subplots(figsize=(9, 5))
    _boxplot_by_category(ax, df, "vehicle_type", "claim_amount")
    _finalize("Claim Amount by Vehicle Type", "Vehicle Type", "Claim Amount")
    return fig


def plot_claims_by_region(data):
    df = data["claims"]["accident_location"].value_counts().head(10)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=df.values, y=df.index, hue=df.index, palette="Spectral", legend=False)
    _finalize("Top 10 Claim Regions", "Claims", "Region")
    return plt.gcf()


def plot_claim_severity_by_region(data):
    df = data["claims"].groupby(["accident_location", "damage_severity"]).size().unstack(fill_value=0)
    df = df.head(10)
    df.plot(kind="bar", stacked=True, figsize=(10, 5), colormap="viridis")
    _finalize("Claim Severity by Region", "Region", "Claims")
    return plt.gcf()


def plot_average_settlement_time(data):
    df = data["claims"].groupby("claim_type")["claim_settlement_days"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df.values, y=df.index, hue=df.index, palette="rocket", legend=False)
    _finalize("Average Settlement Time by Claim Type", "Days", "Claim Type")
    return plt.gcf()


def plot_claim_to_premium_by_policy_type(data):
    df = data["claims"].groupby("policy_type")["claim_to_premium_ratio"].mean().dropna()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df.index, y=df.values, hue=df.index, palette="flare", legend=False)
    _finalize("Claim-to-Premium Ratio by Policy Type", "Policy Type", "Ratio")
    return plt.gcf()


def plot_vehicle_age_vs_claim_amount(data):
    df = merge_claims_with_vehicle_data(data)
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="vehicle_age", y="claim_amount", data=df, alpha=0.5, color="darkorange")
    _finalize("Vehicle Age vs Claim Amount", "Vehicle Age", "Claim Amount")
    return plt.gcf()


def plot_customer_age_vs_claim_amount(data):
    df = data["claims"].merge(
        data["customers"][["customer_id", "customer_age"]],
        on="customer_id", how="left")
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="customer_age", y="claim_amount", data=df, alpha=0.5, color="purple")
    _finalize("Customer Age vs Claim Amount", "Customer Age", "Claim Amount")
    return plt.gcf()


def plot_vehicle_type_claim_performance(data):
    df = merge_claims_with_vehicle_data(data)
    g = df.groupby("vehicle_type")["claim_amount"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=g.values, y=g.index, hue=g.index, palette="crest", legend=False)
    _finalize("Average Claim by Vehicle Type", "Avg Claim", "Vehicle Type")
    return plt.gcf()


def plot_damage_severity_distribution(data):
    df = data["claims"]["damage_severity"].value_counts()
    plt.figure(figsize=(7, 5))
    sns.barplot(x=df.index, y=df.values, hue=df.index, palette="YlOrRd", legend=False)
    _finalize("Damage Severity Distribution", "Severity", "Count")
    return plt.gcf()


def plot_payment_status(data):
    df = data["payments"]["payment_status"].value_counts()
    plt.figure(figsize=(7, 5))
    sns.barplot(x=df.index, y=df.values, hue=df.index, palette="Blues", legend=False)
    _finalize("Payment Status Distribution", "Status", "Count")
    return plt.gcf()


def plot_monthly_premium_trend(data):
    df = data["policies"].copy()
    df["month"] = df["policy_start_date"].dt.to_period("M").astype(str)
    g = df.groupby("month")["premium_amount"].sum()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=g.index, y=g.values, marker="o", color="green")
    _finalize("Monthly Premium Trend", "Month", "Premium")
    return plt.gcf()