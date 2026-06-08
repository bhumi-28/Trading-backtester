import pandas as pd

from backtester.indicators import add_sma
from config import LONG_WINDOW, SHORT_WINDOW

from .base_strategy import BaseStrategy


class GoldenCrossStrategy(BaseStrategy):
    """Simple golden cross strategy using moving averages."""

    def __init__(self, short_window: int = SHORT_WINDOW, long_window: int = LONG_WINDOW) -> None:
        self._short_window = short_window
        self._long_window = long_window

    @property
    def name(self) -> str:
        return "Golden Cross"

    @property
    def description(self) -> str:
        return "Buy when 50-day SMA crosses above 200-day SMA; sell when it crosses below"

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        strategy_df = add_sma(df, self._short_window, "SMA_Short")
        strategy_df = add_sma(strategy_df, self._long_window, "SMA_Long")

        strategy_df["Signal"] = (strategy_df["SMA_Short"] > strategy_df["SMA_Long"]).astype(float)
        strategy_df["Position"] = strategy_df["Signal"].diff()

        strategy_df = strategy_df.dropna().copy()
        return strategy_df
