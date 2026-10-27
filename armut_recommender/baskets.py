"""Basket construction utilities."""

import pandas as pd


def build_basket_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """Return one boolean service-presence row per user-month basket."""
    required = {"BasketID", "Service"}
    missing_columns = sorted(required - set(data.columns))
    if missing_columns:
        raise ValueError(f"Prepared data is missing columns: {', '.join(missing_columns)}")
    if data.empty:
        raise ValueError("Cannot build baskets from an empty dataset.")

    return (
        data.groupby(["BasketID", "Service"], sort=True)
        .size()
        .unstack(fill_value=0)
        .astype(bool)
    )
