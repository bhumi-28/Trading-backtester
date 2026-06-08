from typing import Any, Dict, List

import numpy as np
import pandas as pd

from config import RISK_FREE_RATE


class MetricsCalculator:
    """Calculate portfolio and trade performance metrics from backtest results."""

    def calculate(self, result: Dict[str, Any]) -> Dict[str, float]:
        """Calculate flat metrics from the output of BacktestEngine.run()."""
        df = pd.DataFrame(result.get("df", []))
        trade_log = list(result.get("trade_log", []))
        initial_capital = float(result.get("initial_capital", 0.0))

        final_portfolio_value = float(df["Portfolio_Value"].iloc[-1]) if not df.empty else 0.0
        start_date = pd.to_datetime(df["Date"].iloc[0], errors="coerce") if not df.empty else pd.NaT
        end_date = pd.to_datetime(df["Date"].iloc[-1], errors="coerce") if not df.empty else pd.NaT
        years = (end_date - start_date).days / 365.25 if pd.notna(start_date) and pd.notna(end_date) and end_date > start_date else 0.0

        total_return_pct = ((final_portfolio_value - initial_capital) / initial_capital * 100.0) if initial_capital else 0.0

        if initial_capital > 0 and final_portfolio_value > 0 and years > 0:
            cagr_pct = (((final_portfolio_value / initial_capital) ** (1 / years)) - 1) * 100.0
        else:
            cagr_pct = 0.0

        daily_returns = pd.Series(df["Daily_Return"].dropna()) if "Daily_Return" in df.columns else pd.Series(dtype=float)
        daily_risk_free = RISK_FREE_RATE / 252.0
        sharpe_ratio = np.nan
        if not daily_returns.empty and daily_returns.std() != 0:
            sharpe_ratio = (daily_returns.mean() - daily_risk_free) / daily_returns.std() * np.sqrt(252)

        portfolio_values = pd.Series(df["Portfolio_Value"].dropna(), dtype=float) if "Portfolio_Value" in df.columns else pd.Series(dtype=float)
        rolling_max = portfolio_values.cummax()
        drawdown = (portfolio_values - rolling_max) / rolling_max
        max_drawdown_pct = drawdown.min() * 100.0 if not drawdown.empty else 0.0

        total_trades = len(trade_log)
        winning_trades = [trade for trade in trade_log if float(trade.get("net_pnl", 0.0)) > 0]
        losing_trades = [trade for trade in trade_log if float(trade.get("net_pnl", 0.0)) < 0]

        if total_trades > 0:
            win_rate_pct = (len(winning_trades) / total_trades) * 100.0
            avg_win = float(np.mean([float(trade.get("net_pnl", 0.0)) for trade in winning_trades])) if winning_trades else 0.0
            avg_loss = float(np.mean([float(trade.get("net_pnl", 0.0)) for trade in losing_trades])) if losing_trades else 0.0
            sum_wins = float(np.sum([float(trade.get("net_pnl", 0.0)) for trade in winning_trades]))
            sum_losses = float(np.sum([float(trade.get("net_pnl", 0.0)) for trade in losing_trades]))
            profit_factor = abs(sum_wins) / abs(sum_losses) if sum_losses != 0 else float("inf")
        else:
            win_rate_pct = 0.0
            avg_win = 0.0
            avg_loss = 0.0
            profit_factor = 0.0

        buy_hold_return_pct = 0.0
        if not df.empty and "Close" in df.columns and len(df["Close"]) >= 2:
            close_series = pd.Series(df["Close"], dtype=float)
            buy_hold_return_pct = ((close_series.iloc[-1] - close_series.iloc[0]) / close_series.iloc[0]) * 100.0

        metrics = {
            "total_return_pct": round(total_return_pct, 2),
            "cagr_pct": round(cagr_pct, 2),
            "sharpe_ratio": round(float(sharpe_ratio), 2) if not np.isnan(sharpe_ratio) else np.nan,
            "max_drawdown_pct": round(max_drawdown_pct, 2),
            "total_trades": total_trades,
            "winning_trades": len(winning_trades),
            "win_rate_pct": round(win_rate_pct, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "profit_factor": round(profit_factor, 2) if np.isfinite(profit_factor) else float("inf"),
            "buy_hold_return_pct": round(buy_hold_return_pct, 2),
        }

        return metrics
