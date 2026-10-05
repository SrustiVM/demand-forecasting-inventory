
import pandas as pd


def check_forecast_quality(forecast: pd.DataFrame) -> dict:
    """Return basic production-quality checks for forecast output."""

    return {
        "rows": int(len(forecast)),
        "missing_predictions": int(
            forecast["forecast_demand_units"].isna().sum()
        ),
        "negative_predictions": int(
            (forecast["forecast_demand_units"] < 0).sum()
        ),
        "unique_series": int(
            forecast[["store_nbr", "family"]]
            .drop_duplicates()
            .shape[0]
        ),
        "forecast_days": int(
            forecast["date"].nunique()
        ),
        "total_forecast_units": float(
            forecast["forecast_demand_units"].sum()
        ),
        "mean_forecast_units": float(
            forecast["forecast_demand_units"].mean()
        )
    }


def validate_monitoring_result(result: dict) -> None:
    """Raise an error when critical forecast-quality checks fail."""

    if result["missing_predictions"] > 0:
        raise ValueError("Forecast contains missing predictions.")

    if result["negative_predictions"] > 0:
        raise ValueError("Forecast contains negative predictions.")

    if result["rows"] == 0:
        raise ValueError("Forecast contains no rows.")
