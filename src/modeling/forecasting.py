
from pathlib import Path
import joblib
import pandas as pd


def load_forecaster(model_path: str | Path):
    """Load a persisted forecasting model."""
    return joblib.load(model_path)


def validate_forecast_output(
    forecast: pd.DataFrame,
    required_columns: list[str] | None = None,
) -> None:
    """Validate forecast structure and values."""

    if required_columns is None:
        required_columns = [
            "date",
            "store_nbr",
            "family",
            "forecast_demand_units",
        ]

    missing = [
        column
        for column in required_columns
        if column not in forecast.columns
    ]

    if missing:
        raise ValueError(f"Missing forecast columns: {missing}")

    if forecast["forecast_demand_units"].isna().any():
        raise ValueError("Forecast contains null values.")

    if (forecast["forecast_demand_units"] < 0).any():
        raise ValueError("Forecast contains negative values.")


def summarize_forecast(
    forecast: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate forecast demand by date."""

    return (
        forecast
        .groupby("date", as_index=False)
        .agg(
            total_forecast_units=(
                "forecast_demand_units",
                "sum",
            ),
            mean_forecast_units=(
                "forecast_demand_units",
                "mean",
            ),
        )
    )
