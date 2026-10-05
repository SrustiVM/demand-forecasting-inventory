
import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_forecast_endpoint():
    response = client.get(
        "/forecast",
        params={
            "store_nbr": 1,
            "family": "AUTOMOTIVE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["store_nbr"] == 1
    assert data["family"] == "AUTOMOTIVE"
    assert len(data["forecast"]) == 16


def test_inventory_endpoint():
    response = client.get(
        "/inventory",
        params={
            "store_nbr": 1,
            "family": "AUTOMOTIVE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["store_nbr"] == 1
    assert data["family"] == "AUTOMOTIVE"
    assert data["recommended_order_quantity"] >= 0
