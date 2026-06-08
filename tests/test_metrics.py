import unittest

import numpy as np
import pandas as pd

from backtester.metrics import MetricsCalculator


class MetricsCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        np.random.seed(42)
        dates = pd.date_range(start="2020-01-01", periods=500, freq="D")
        close = 100 + np.cumsum(np.random.normal(loc=0.0, scale=1.0, size=500))

        portfolio_value = np.empty(500, dtype=float)
        portfolio_value[0] = 100000.0
        for idx in range(1, 500):
            portfolio_value[idx] = portfolio_value[idx - 1] * 1.0005

        trade_log = [
            {"net_pnl": 500.0},
            {"net_pnl": 200.0},
            {"net_pnl": 100.0},
            {"net_pnl": -150.0},
        ]

        self.result = {
            "df": pd.DataFrame(
                {
                    "Date": dates,
                    "Close": close,
                    "Portfolio_Value": portfolio_value,
                    "Daily_Return": np.random.normal(loc=0.0, scale=0.01, size=500),
                }
            ),
            "trade_log": trade_log,
            "initial_capital": 100000.0,
        }

    def test_total_return(self) -> None:
        metrics = MetricsCalculator().calculate(self.result)
        expected = ((self.result["df"]["Portfolio_Value"].iloc[-1] - 100000.0) / 100000.0) * 100.0
        self.assertIsInstance(metrics["total_return_pct"], float)
        self.assertAlmostEqual(metrics["total_return_pct"], round(expected, 2))

    def test_sharpe_not_nan(self) -> None:
        metrics = MetricsCalculator().calculate(self.result)
        self.assertFalse(np.isnan(metrics["sharpe_ratio"]))

    def test_max_drawdown_negative(self) -> None:
        metrics = MetricsCalculator().calculate(self.result)
        self.assertLessEqual(metrics["max_drawdown_pct"], 0)

    def test_win_rate_range(self) -> None:
        metrics = MetricsCalculator().calculate(self.result)
        self.assertGreaterEqual(metrics["win_rate_pct"], 0)
        self.assertLessEqual(metrics["win_rate_pct"], 100)

    def test_empty_trade_log(self) -> None:
        metrics = MetricsCalculator().calculate({"df": self.result["df"], "trade_log": [], "initial_capital": 100000.0})
        self.assertEqual(metrics["total_trades"], 0)
        self.assertEqual(metrics["win_rate_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()
