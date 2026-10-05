FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY models ./models
COPY data/processed/test_store_family_forecast.parquet ./data/processed/test_store_family_forecast.parquet
COPY data/processed/inventory_recommendations_production.parquet ./data/processed/inventory_recommendations_production.parquet

EXPOSE 8000

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
