from dataclasses import dataclass
import pandas as pd

REQUIRED_COLS = ("ds", "y")  # timestamp, target value

@dataclass
class SeriesSchema:
    required: tuple[str, ...] = REQUIRED_COLS
    tz: str = "America/Detroit"

def enforce_series_df(df:pd.DataFrame, tz: str = "America/Detroit") -> pd.DataFrame:
    """Ensure the data is valid:
        Required columns exist (timestamp and value)
        ds is timezone-aware datetime
        data is sorted
        no duplicates
    """
    #get each required column that is missing in the data
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing: raise ValueError(f"Missing columns: {missing}")
    df = df.copy()
    df["ds"] = pd.to_datetime(df["ds"],errors = "raise")
    if df["ds"].dt.tz is None:
        df["ds"] = df["ds"].dt.tz_localize(tz)
    else:
        df["ds"] = df["ds"].dt.tz_convert(tz)
    df = df.sort_values("ds").drop_duplicates(subset=["ds"]).reset_index(drop=True)
    return df

def enforce_numeric(df: pd.DataFrame, cols = ("y,")) -> pd.DataFrame:
    """Make all data columns numeric"""
    df = df.copy()
    for c in cols: df[c] = pd.to_numeric(df[c],errors="coerce")
    return df






    