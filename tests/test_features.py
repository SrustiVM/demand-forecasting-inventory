import pandas as pd


def test_lag_features_do_not_use_current_demand():

    df = pd.DataFrame({
        "store_nbr": [1, 1, 1],
        "family": ["A", "A", "A"],
        "date": pd.date_range("2025-01-01", periods=3),
        "demand_units": [100, 200, 300],
    })

    df["lag_1"] = (
        df.groupby(["store_nbr", "family"])["demand_units"]
        .shift(1)
    )

    assert pd.isna(df.loc[0, "lag_1"])
    assert df.loc[1, "lag_1"] == 100
    assert df.loc[2, "lag_1"] == 200

    # Current demand must never equal its own lag.
    assert df.loc[1, "lag_1"] != df.loc[1, "demand_units"]