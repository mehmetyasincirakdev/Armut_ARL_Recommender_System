"""Association-rule mining and service recommendations."""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

from armut_recommender.baskets import build_basket_matrix

RECOMMENDATION_COLUMNS = ("service", "confidence", "lift", "support")


def recommend_for_user(
    data: pd.DataFrame,
    user_id: str,
    *,
    min_support: float = 0.01,
    min_confidence: float = 0.1,
    top_n: int = 5,
) -> pd.DataFrame:
    """Recommend services for a user's latest monthly basket."""
    if not 0 < min_support <= 1:
        raise ValueError("min_support must be greater than 0 and at most 1.")
    if not 0 <= min_confidence <= 1:
        raise ValueError("min_confidence must be between 0 and 1.")
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    required = {"UserId", "CreateDate", "BasketID", "Service"}
    missing_columns = sorted(required - set(data.columns))
    if missing_columns:
        raise ValueError(f"Prepared data is missing columns: {', '.join(missing_columns)}")
    user_events = data.loc[data["UserId"].astype("string") == str(user_id)]
    if user_events.empty:
        return pd.DataFrame(columns=RECOMMENDATION_COLUMNS)

    latest_basket_id = user_events.loc[user_events["CreateDate"].idxmax(), "BasketID"]
    basket_services = set(
        data.loc[data["BasketID"] == latest_basket_id, "Service"].astype(str)
    )
    basket_matrix = build_basket_matrix(data)
    frequent_itemsets = apriori(
        basket_matrix,
        min_support=min_support,
        use_colnames=True,
    )
    if frequent_itemsets.empty or not frequent_itemsets["itemsets"].map(len).ge(2).any():
        return pd.DataFrame(columns=RECOMMENDATION_COLUMNS)

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence,
        return_metrics=["support", "confidence", "lift"],
    )
    matching_rules = rules.loc[
        rules["antecedents"].map(lambda items: items.issubset(basket_services))
    ]

    recommendations: list[dict[str, float | str]] = []
    for rule in matching_rules.itertuples(index=False):
        for service in rule.consequents - basket_services:
            recommendations.append(
                {
                    "service": service,
                    "confidence": float(rule.confidence),
                    "lift": float(rule.lift),
                    "support": float(rule.support),
                }
            )

    if not recommendations:
        return pd.DataFrame(columns=RECOMMENDATION_COLUMNS)

    return (
        pd.DataFrame(recommendations, columns=RECOMMENDATION_COLUMNS)
        .sort_values(
            ["confidence", "lift", "support", "service"],
            ascending=[False, False, False, True],
        )
        .drop_duplicates(subset="service", keep="first")
        .head(top_n)
        .reset_index(drop=True)
    )
