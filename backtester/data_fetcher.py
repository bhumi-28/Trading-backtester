import logging
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

from config import DATA_DIR

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch and cache OHLCV market data for backtesting."""

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self.data_dir = Path(data_dir) if data_dir is not None else DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, symbol: str, start: str, end: str) -> Path:
        safe_symbol = symbol.replace(" ", "_").replace("/", "_").replace("\\", "_")
        return self.data_dir / f"{safe_symbol}_{start}_{end}.csv"

    def get_ohlcv(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """Return OHLCV data from cache or download it when needed."""
        cache_path = self._cache_path(symbol, start, end)

        if cache_path.exists():
            logger.info("Cache hit for %s at %s", symbol, cache_path)
            df = pd.read_csv(cache_path)
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            return self.validate_data(df, symbol)

        try:
            logger.info("Downloading fresh data for %s from %s to %s", symbol, start, end)
            df = yf.download(symbol, start=start, end=end, auto_adjust=True, progress=False)
        except Exception as exc:
            raise RuntimeError(f"Failed to download data for ticker '{symbol}': {exc}") from exc

        if df is None or df.empty:
            raise ValueError(f"No data returned for ticker '{symbol}'.")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        logger.debug(f"Columns after download: {list(df.columns)}")
        df = df.reset_index()
        df = df.rename(columns={"Datetime": "Date", "index": "Date"})
        if "Date" not in df.columns:
            df = df.reset_index().rename(columns={"index": "Date"})
        df["Date"] = pd.to_datetime(df["Date"])

        if "Adj Close" in df.columns:
            df = df.drop(columns=["Adj Close"])

        keep_columns = [column for column in ("Date", "Open", "High", "Low", "Close", "Volume") if column in df.columns]
        df = df.loc[:, keep_columns].copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Close"]).copy()

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache_path, index=False)

        logger.info("Fresh download saved to %s", cache_path)
        return self.validate_data(df, symbol)

    def validate_data(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Validate OHLCV data and ensure it contains enough rows for analysis."""
        validated_df = df.copy()
        validated_df["Date"] = pd.to_datetime(validated_df.get("Date", pd.Series(dtype="datetime64[ns]")), errors="coerce")
        validated_df = validated_df.dropna(subset=["Close"]).copy()

        if len(validated_df) < 252:
            raise ValueError(
                f"Not enough data for {symbol}: {len(validated_df)} rows remain after dropping NaNs; "
                "need at least 252 rows (1 year of daily data)."
            )

        start_date = validated_df["Date"].min().strftime("%Y-%m-%d")
        end_date = validated_df["Date"].max().strftime("%Y-%m-%d")
        logger.info(
            "Validated %s: %d rows, date range %s to %s",
            symbol,
            len(validated_df),
            start_date,
            end_date,
        )
        return validated_df
