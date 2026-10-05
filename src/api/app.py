
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

FORECAST_PATH = (
    PROCESSED_DIR / "test_store_family_forecast.parquet"
)

INVENTORY_PATH = (
    PROCESSED_DIR / "inventory_recommendations_production.parquet"
)

forecast = pd.read_parquet(FORECAST_PATH)
inventory = pd.read_parquet(INVENTORY_PATH)

app = FastAPI(
    title="DemandForecast API",
    description="Demand forecasting and inventory optimization API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "forecast_rows": len(forecast),
        "inventory_rows": len(inventory),
    }


@app.get("/forecast")
def get_forecast(
    store_nbr: int,
    family: str,
):
    result = forecast[
        (forecast["store_nbr"] == store_nbr)
        & (forecast["family"].astype(str) == family)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Forecast series not found.",
        )

    result = result.copy()
    result["date"] = result["date"].astype(str)

    return {
        "store_nbr": store_nbr,
        "family": family,
        "forecast": result.to_dict(orient="records"),
    }


@app.get("/inventory")
def get_inventory(
    store_nbr: int,
    family: str,
):
    result = inventory[
        (inventory["store_nbr"] == store_nbr)
        & (inventory["family"].astype(str) == family)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Inventory recommendation not found.",
        )

    return result.to_dict(orient="records")[0]
