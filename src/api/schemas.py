from pydantic import BaseModel, Field


class ForecastRequest(BaseModel):
    store_nbr: int = Field(..., ge=1)
    family: str

    day_of_week: int = Field(..., ge=0, le=6)
    day_of_month: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    quarter: int = Field(..., ge=1, le=4)
    year: int
    week_of_year: int = Field(..., ge=1, le=53)

    is_weekend: int = Field(..., ge=0, le=1)
    is_holiday: int = Field(..., ge=0, le=1)
    is_event: int = Field(..., ge=0, le=1)

    promotion_rate: float = Field(..., ge=0, le=1)
    dcoilwtico: float

    lag_1: float = Field(..., ge=0)
    lag_7: float = Field(..., ge=0)
    lag_14: float = Field(..., ge=0)
    lag_28: float = Field(..., ge=0)

    rolling_mean_7: float = Field(..., ge=0)
    rolling_std_7: float = Field(..., ge=0)
    rolling_mean_28: float = Field(..., ge=0)
    rolling_std_28: float = Field(..., ge=0)


class ForecastResponse(BaseModel):
    predicted_demand: float
    safety_stock: float
    reorder_point: float