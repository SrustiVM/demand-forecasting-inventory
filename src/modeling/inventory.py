
import numpy as np
import pandas as pd


def calculate_inventory_recommendations(
    forecast: pd.DataFrame,
    validation: pd.DataFrame,
    lead_time_days: int = 7,
    service_level_z: float = 1.645,
) -> pd.DataFrame:
    """Calculate safety stock and reorder points."""

    error_stats = (
        validation
        .groupby(["store_nbr", "family"])
        .agg(
            error_std=("error", "std"),
            validation_rows=("error", "count"),
        )
        .reset_index()
    )

    global_error_std = validation["error"].std()

    error_stats["error_std"] = (
        error_stats["error_std"]
        .fillna(global_error_std)
    )

    demand = (
        forecast
        .groupby(["store_nbr", "family"])
        .agg(
            forecast_total_units=(
                "forecast_demand_units",
                "sum",
            ),
            forecast_daily_mean=(
                "forecast_demand_units",
                "mean",
            ),
        )
        .reset_index()
    )

    result = demand.merge(
        error_stats,
        on=["store_nbr", "family"],
        how="left",
    )

    result["safety_stock"] = (
        service_level_z
        * result["error_std"]
        * np.sqrt(lead_time_days)
    )

    result["lead_time_demand"] = (
        result["forecast_daily_mean"]
        * lead_time_days
    )

    result["reorder_point"] = (
        result["lead_time_demand"]
        + result["safety_stock"]
    )

    result["recommended_order_quantity"] = (
        result["reorder_point"].clip(lower=0)
    )

    return result
