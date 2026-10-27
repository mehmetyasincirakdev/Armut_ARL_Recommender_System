"""Dataset loading and event preparation."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ("UserId", "ServiceId", "CategoryId", "CreateDate")
DEFAULT_DATASET_PATH = Path(__file__).resolve().parent.parent / "Datasets" / "armut_data.csv"


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate raw events and add service, month, and basket identifiers."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing_columns)}")

    prepared = pd.DataFrame(data, columns=REQUIRED_COLUMNS).copy()
    if prepared.empty:
        raise ValueError("Dataset contains no service events.")

    parsed_dates = pd.to_datetime(prepared["CreateDate"], errors="coerce")
    invalid_rows = (
        prepared["UserId"].isna()
        | prepared["ServiceId"].isna()
        | prepared["CategoryId"].isna()
        | parsed_dates.isna()
    )
    invalid_row_count = int(invalid_rows.sum())
    if invalid_row_count:
        raise ValueError(
            f"Dataset contains {invalid_row_count} rows with missing required values "
            "or invalid CreateDate values."
        )
    prepared["CreateDate"] = parsed_dates

    prepared["UserId"] = prepared["UserId"].astype("string")
    prepared["Service"] = (
        prepared["ServiceId"].astype("string")
        + "_"
        + prepared["CategoryId"].astype("string")
    )
    prepared["YearMonth"] = prepared["CreateDate"].dt.to_period("M").astype("string")
    prepared["BasketID"] = prepared["UserId"] + "_" + prepared["YearMonth"]
    return prepared.reset_index(drop=True)


def load_data(path: Path = DEFAULT_DATASET_PATH) -> pd.DataFrame:
    """Load and prepare a local dataset without requiring a working directory."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Keep the dataset local and place it at "
            "Datasets/armut_data.csv, or pass --data-path."
        )

    data = pd.read_csv(
        path,
        dtype={"UserId": "string", "ServiceId": "string", "CategoryId": "string"},
    )
    return prepare_data(data)
