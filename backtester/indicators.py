import pandas as pd


def add_sma(df: pd.DataFrame, window: int, col_name: str) -> pd.DataFrame:
    """Add a simple moving average column to the dataframe."""
    result_df = df.copy()
    result_df[col_name] = result_df["Close"].rolling(window=window).mean()
    return result_df


def add_ema(df: pd.DataFrame, window: int, col_name: str) -> pd.DataFrame:
    """Add an exponential moving average column to the dataframe."""
    result_df = df.copy()
    result_df[col_name] = result_df["Close"].ewm(span=window, adjust=False).mean()
    return result_df
