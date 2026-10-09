"""Rule-based business insights for the motor insurance dashboard."""

import pandas as pd


def generate_business_recommendations(data: dict) -> list[dict[str, str]]:
    """Return actionable insight cards for the currently selected data."""
    claims = data.get("claims", pd.DataFrame())
    policies = data.get("policies", pd.DataFrame())
    cards: list[dict[str, str]] = []

    def add_card(pattern: str, evidence: str, meaning: str, recommendation: str) -> None:
        cards.append({
            "PATTERN": pattern,
            "EVIDENCE": evidence,
            "BUSINESS_MEANING": meaning,
            "RECOMMENDATION": recommendation,
        })

    if "claim_to_premium_ratio" in claims.columns and not claims.empty:
        ratios = pd.to_numeric(claims["claim_to_premium_ratio"], errors="coerce").dropna()
        if not ratios.empty and ratios.mean() > 1:
            average_ratio = ratios.mean()
            add_card(
                "Average claim amount is higher than the associated premium.",
                f"Average claim-to-premium ratio: {average_ratio:.2f} ({average_ratio:.0%}).",
                "Claims are costly relative to the premiums associated with them.",
                "Review pricing and underwriting for the affected portfolio segments.",
            )

    if "claim_status" in claims.columns and not claims.empty:
        statuses = claims["claim_status"].astype("string").str.strip().str.casefold()
        total_claims = int(statuses.notna().sum())
        if total_claims:
            pending_count = int(statuses.eq("pending").sum())
            if pending_count:
                add_card(
                    "Pending claims are awaiting a decision.",
                    f"{pending_count:,} of {total_claims:,} claims are pending "
                    f"({pending_count / total_claims:.1%}).",
                    "Unresolved claims may increase customer wait times and service workload.",
                    "Review pending claims regularly and prioritize older submissions.",
                )

            rejected_count = int(statuses.eq("rejected").sum())
            rejection_rate = rejected_count / total_claims
            if rejection_rate > 0.20:
                add_card(
                    "The claim rejection rate is elevated.",
                    f"{rejected_count:,} of {total_claims:,} claims were rejected "
                    f"({rejection_rate:.1%}).",
                    "Frequent rejections can indicate claim-quality issues or gaps in customer expectations.",
                    "Review rejection reasons and clarify claim requirements to customers.",
                )

    if "claim_settlement_days" in claims.columns and not claims.empty:
        settlement_days = pd.to_numeric(
            claims["claim_settlement_days"], errors="coerce"
        ).dropna()
        if not settlement_days.empty and settlement_days.mean() > 30:
            average_days = settlement_days.mean()
            add_card(
                "Claims are taking a long time to settle.",
                f"Average claim settlement time: {average_days:.1f} days.",
                "Long settlement times can reduce customer satisfaction.",
                "Investigate process bottlenecks and monitor settlement time by claim type.",
            )

    if "damage_severity" in claims.columns and not claims.empty:
        severity = claims["damage_severity"].astype("string").str.strip().str.casefold()
        classified_count = int(severity.notna().sum())
        high_count = int(severity.eq("high").sum())
        if classified_count and high_count / classified_count > 0.30:
            add_card(
                "High-severity damage makes up a notable share of claims.",
                f"{high_count:,} of {classified_count:,} classified claims are high severity "
                f"({high_count / classified_count:.1%}).",
                "A larger share of severe incidents may increase claim costs and portfolio risk.",
                "Review risk controls and pricing for segments with frequent high-severity claims.",
            )

    if "policy_status" in policies.columns and not policies.empty:
        statuses = policies["policy_status"].astype("string").str.strip().str.casefold()
        total_policies = int(statuses.notna().sum())
        if total_policies:
            expired_count = int(statuses.eq("expired").sum())
            expired_rate = expired_count / total_policies
            if expired_rate > 0.20:
                add_card(
                    "A notable share of the selected policies has expired.",
                    f"{expired_count:,} of {total_policies:,} policies are expired "
                    f"({expired_rate:.1%}).",
                    "Expired policies may represent missed renewal opportunities.",
                    "Start renewal outreach before policy end dates and follow up on recent expirations.",
                )

    return cards