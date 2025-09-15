from functools import lru_cache
import pandas as pd
import json
from .schemas import enforce_series_df, enforce_numeric
from pathlib import Path

@lru_cache(maxsize=64)
def load_building(building_id: str) -> pd.DataFrame:
    """Load canonical series for a building
    and rename to ds & y 
    """
    #read data
    path = f"/data/building_data/{building_id}/{building_id}_water.xlsx"
    df = pd.read_excel(path).dropna(axis=1, how='all').iloc[5:]

    #standardize column names
    rename_map = {'Unnamed: 4': 'ds', 'Unnamed: 5': 'y'}
    df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})
    df = enforce_numeric(df,cols=("y,"))
    df = enforce_series_df(df)
    df["building_id"] = building_id
    return df

def load_labels(building_id: str, tz: str = "America/Detroit") -> list[pd.Timestamp]:
    """Return list of known fault dates (ISO strings) for eval"""
    fp = Path(f"/data/building_data/{building_id}/{building_id}_faults.json")
    if not fp.exists():
        return []
    data = json.loads(fp.read_text())
    dates = data.get(building_id,[])
    ts = [pd.Timestamp(d).tz_localize(tz) for d in dates]  # canonicalize TZ
    ts = sorted(set(ts))  # unique + sorted
    return ts





