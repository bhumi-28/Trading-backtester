import unittest

import pandas as pd

from backtester.engine import BacktestEngine


class BacktestEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame(
            {
                "Date": pd.date_range("2020-01-01", periods=250, freq="D"),
                "Close": [100 + i * 0.1 for i in range(250)],
                "Signal": [0.0] * 250,
                "Position": [0.0] * 250,
            }
        )
        self.df.loc[50, "Position"] = 1.0
        self.df.loc[150, "Position"] = -1.0

    def test_trade_count(self) -> None:
        result = BacktestEngine(initial_capital=100000.0, commission=0.001).run(self.df)
        self.assertEqual(len(result["trade_log"]), 1)

    def test_portfolio_value_length(self) -> None:
        result = BacktestEngine(initial_capital=100000.0, commission=0.001).run(self.df)
        self.assertEqual(len(result["df"]), len(self.df))
        self.assertIn("Portfolio_Value", result["df"].columns)

    def test_commission_applied(self) -> None:
        result = BacktestEngine(initial_capital=100000.0, commission=0.001).run(self.df)
        entry_price = result["trade_log"][0]["entry_price"]
        shares = result["trade_log"][0]["shares"]
        buy_cost = entry_price * shares * (1 + 0.001)
        self.assertGreater(buy_cost, shares * self.df.loc[50, "Close"])

    def test_unclosed_position(self) -> None:
        df = self.df.copy()
        df.loc[50, "Position"] = 1.0
        df.loc[149, "Position"] = 0.0
        result = BacktestEngine(initial_capital=100000.0, commission=0.001).run(df)
        self.assertGreaterEqual(len(result["trade_log"]), 1)


if __name__ == "__main__":
    unittest.main()
