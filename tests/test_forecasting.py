from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROJECT_ROOT / "models" / "lightgbm_forecaster.joblib"


def test_forecast_artifact_exists():
    path = PROCESSED_DIR / "test_store_family_forecast.parquet"
    assert path.exists()


def test_forecast_quality():
    path = PROCESSED_DIR / "test_store_family_forecast.parquet"
    data = pd.read_parquet(path)

    assert len(data) > 0
    assert data["forecast_demand_units"].notna().all()
    assert (data["forecast_demand_units"] >= 0).all()
    assert data["store_nbr"].nunique() == 54
    assert data["date"].nunique() == 16


def test_model_artifact_exists():
    assert MODEL_PATH.exists()


def test_inventory_artifact_exists():
    path = PROCESSED_DIR / "inventory_recommendations_production.parquet"
    assert path.exists()
