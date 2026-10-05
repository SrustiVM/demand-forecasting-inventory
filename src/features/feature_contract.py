
FEATURE_COLUMNS = [
    "store_nbr",
    "family",
    "day_of_week",
    "day_of_month",
    "month",
    "quarter",
    "year",
    "week_of_year",
    "is_weekend",
    "is_holiday",
    "oil_price",
    "oil_missing",
    "promotion_rate",
    "promotion_data_available",
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "lag_364",
    "rolling_mean_7",
    "rolling_mean_28",
    "rolling_std_28",
]

TARGET_COLUMN = "target_demand_units"

FORECAST_COLUMN = "forecast_demand_units"
