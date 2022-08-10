from pandas import DataFrame


def group_by_region(df: DataFrame):
    return df.groupby(by=["date", "loc1"], as_index=False).agg(
        {"price": "mean", "rooms": "mean", "area": "mean", "year": "mean"}).round(2)
