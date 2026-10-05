
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "favorita"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CONFIGS_DIR = PROJECT_ROOT / "configs"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

MODEL_BASE_PATH = PROCESSED_DIR / "model_base.parquet"
FEATURES_PATH = PROCESSED_DIR / "forecast_features.parquet"
BASELINE_PATH = PROCESSED_DIR / "baseline_results.parquet"

SPLITS_PATH = CONFIGS_DIR / "forecasting_splits.json"
MODEL_PATH = MODELS_DIR / "lightgbm_forecaster.joblib"

for directory in [
    PROCESSED_DIR,
    CONFIGS_DIR,
    MODELS_DIR,
    LOGS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

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
