from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException

from .schemas import ForecastRequest, ForecastResponse


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = (
    BASE_DIR
    / "data"
    / "raw"
    / "favorita"
    / "processed"
    / "models"
)

MODEL_PATH = MODEL_DIR / "lightgbm_demand_model.joblib"
META_PATH = MODEL_DIR / "feature_metadata.joblib"


model = joblib.load(MODEL_PATH)
metadata = joblib.load(META_PATH)


app = FastAPI(
    title="Favorita Demand Forecasting API",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):

    family_code = metadata["family_map"].get(request.family)

    if family_code is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown family: {request.family}"
        )

    features = {
        "store_nbr": request.store_nbr,
        "family_code": family_code,

        "day_of_week": request.day_of_week,
        "day_of_month": request.day_of_month,
        "month": request.month,
        "quarter": request.quarter,
        "year": request.year,
        "week_of_year": request.week_of_year,

        "is_weekend": request.is_weekend,
        "is_holiday": request.is_holiday,
        "is_event": request.is_event,

        "is_additional": 0,
        "is_transferred": 0,
        "holiday_count": 0,

        "promotion_rate": request.promotion_rate,
        "dcoilwtico": request.dcoilwtico,

        "lag_1": request.lag_1,
        "lag_7": request.lag_7,
        "lag_14": request.lag_14,
        "lag_28": request.lag_28,

        "rolling_mean_7": request.rolling_mean_7,
        "rolling_std_7": request.rolling_std_7,
        "rolling_mean_28": request.rolling_mean_28,
        "rolling_std_28": request.rolling_std_28,
    }

    X = pd.DataFrame([features])[
        metadata["feature_cols"]
    ]

    prediction = max(
        0.0,
        float(model.predict(X)[0])
    )

    lead_time = metadata["lead_time_days"]
    z = metadata["service_level_z"]

    uncertainty = request.rolling_std_28

    safety_stock = (
        z
        * uncertainty
        * np.sqrt(lead_time)
    )

    reorder_point = (
        prediction * lead_time
        + safety_stock
    )

    return ForecastResponse(
        predicted_demand=prediction,
        safety_stock=float(safety_stock),
        reorder_point=float(reorder_point),
    )