
import pandas as pd

from .feature_contract import FEATURE_COLUMNS


def validate_model_features(
    data: pd.DataFrame,
) -> None:
    """Validate that model input contains the required features."""

    missing = [
        column
        for column in FEATURE_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing model features: {missing}"
        )


def validate_feature_nulls(
    data: pd.DataFrame,
) -> None:
    """Check for unexpected null values in model features."""

    null_counts = data[FEATURE_COLUMNS].isna().sum()
    problematic = null_counts[null_counts > 0]

    if not problematic.empty:
        raise ValueError(
            f"Null values found in model features: "
            f"{problematic.to_dict()}"
        )
