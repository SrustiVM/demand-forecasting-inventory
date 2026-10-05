# DemandForecast — Demand Forecasting & Inventory Optimization

## Overview

End-to-end retail demand forecasting and inventory optimization system built using the Favorita Grocery Sales dataset.

The system processes 125M+ sales records, creates store-family daily time-series data, engineers forecasting features, trains a global LightGBM model, performs chronological validation, generates multi-step forecasts, and produces inventory recommendations.

## Architecture

Raw CSV data
-> DuckDB out-of-core processing
-> Daily store-family Parquet
-> Time-series feature engineering
-> Forecasting baselines
-> LightGBM global model
-> Walk-forward validation
-> Multi-step forecasting
-> Inventory optimization
-> FastAPI
-> Pytest
-> Docker
-> CI

## Data

- 125M+ historical sales records
- 54 stores
- 33 product families
- Historical period: 2013-01-01 to 2017-08-15
- Forecast horizon: 16 days
- Forecast grain: store x product family x day

## Forecasting

Features include:

- Calendar features
- Promotion information
- Holiday information
- Oil-price information
- Lag features
- Rolling statistics

The forecasting model is a global LightGBM regression model evaluated with chronological walk-forward validation to prevent temporal leakage.

## Inventory Optimization

Forecasts are converted into reorder recommendations using:

- Forecasted lead-time demand
- Validation error variability
- Safety stock
- Service-level assumptions
- Reorder point

Actual supplier lead times, inventory levels and service policies were unavailable, so inventory parameters are explicitly treated as assumptions.

## Production Engineering

- FastAPI prediction service
- Pydantic validation
- Automated Pytest tests
- Docker containerization
- GitHub Actions CI
- Basic monitoring
- Parquet artifacts
- Joblib model serialization

## Important Assumptions

- Negative sales are treated as returns or adjustments.
- Missing active-series observations are treated as zero recorded demand while preserving missingness information.
- Promotion missingness is distinguished from confirmed no-promotion.
- Oil prices are forward-filled causally.
- Holiday records are aggregated by date before joining.
- Cold-start store-family combinations receive a zero forecast.
- Inventory lead time and service level are assumed parameters.

## Limitations

The dataset does not contain actual inventory levels, supplier lead times, stockouts or service-level policies. Inventory recommendations are therefore analytical recommendations rather than direct purchase orders.

## Technology Stack

Python, Pandas, NumPy, DuckDB, PyArrow, LightGBM, scikit-learn, FastAPI, Pytest, Docker and GitHub Actions.

## Project Structure

demand-forecasting-inventory/
- data/
- notebooks/
- src/
- tests/
- configs/
- models/
- mlruns/
- logs/
- Dockerfile
- requirements.txt
- README.md
