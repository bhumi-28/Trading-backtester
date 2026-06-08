from typing import Dict, List

import pandas as pd

from config import COMMISSION, INITIAL_CAPITAL


class BacktestEngine:
    """Simple long-only backtesting engine for daily OHLCV data."""

    def __init__(self, initial_capital: float = INITIAL_CAPITAL, commission: float = COMMISSION) -> None:
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, df: pd.DataFrame) -> Dict[str, object]:
        """Run a long-only backtest and return an enriched dataframe plus trade log."""
        if not {"Close", "Signal", "Position"}.issubset(df.columns):
            raise ValueError("Input dataframe must contain 'Close', 'Signal', and 'Position' columns.")

        enriched_df = df.copy().reset_index(drop=True)
        enriched_df["Shares_Held"] = 0
        enriched_df["Holdings"] = 0.0
        enriched_df["Cash"] = self.initial_capital
        enriched_df["Portfolio_Value"] = self.initial_capital
        enriched_df["Daily_Return"] = 0.0

        cash = float(self.initial_capital)
        shares_held = 0
        open_trade: Dict[str, object] | None = None
        trade_log: List[Dict[str, object]] = []

        for idx, row in enriched_df.iterrows():
            close_price = float(row["Close"])
            position = row["Position"]

            if position == 1.0 and shares_held == 0:
                if cash <= 0:
                    continue

                shares_to_buy = int(cash // (close_price * (1 + self.commission)))
                if shares_to_buy <= 0:
                    continue

                cost = shares_to_buy * close_price * (1 + self.commission)
                cash -= cost
                shares_held = shares_to_buy
                open_trade = {
                    "entry_date": row.get("Date", idx),
                    "entry_price": close_price,
                    "shares": shares_held,
                }

            elif position == -1.0 and shares_held > 0 and open_trade is not None:
                proceeds = shares_held * close_price * (1 - self.commission)
                cash += proceeds

                gross_pnl = shares_held * (close_price - float(open_trade["entry_price"]))
                net_pnl = proceeds - shares_held * float(open_trade["entry_price"]) * (1 + self.commission)
                return_pct = (close_price / float(open_trade["entry_price"])) - 1.0

                trade_log.append(
                    {
                        "entry_date": open_trade["entry_date"],
                        "exit_date": row.get("Date", idx),
                        "entry_price": float(open_trade["entry_price"]),
                        "exit_price": close_price,
                        "shares": shares_held,
                        "gross_pnl": gross_pnl,
                        "net_pnl": net_pnl,
                        "return_pct": return_pct,
                    }
                )

                shares_held = 0
                open_trade = None

            holdings_value = shares_held * close_price
            enriched_df.at[idx, "Shares_Held"] = shares_held
            enriched_df.at[idx, "Holdings"] = holdings_value
            enriched_df.at[idx, "Cash"] = cash
            enriched_df.at[idx, "Portfolio_Value"] = cash + holdings_value

        if shares_held > 0 and open_trade is not None:
            last_price = float(enriched_df.iloc[-1]["Close"])
            final_proceeds = shares_held * last_price * (1 - self.commission)
            cash += final_proceeds

            gross_pnl = shares_held * (last_price - float(open_trade["entry_price"]))
            net_pnl = final_proceeds - shares_held * float(open_trade["entry_price"]) * (1 + self.commission)
            return_pct = (last_price / float(open_trade["entry_price"])) - 1.0

            trade_log.append(
                {
                    "entry_date": open_trade["entry_date"],
                    "exit_date": enriched_df.iloc[-1].get("Date", len(enriched_df) - 1),
                    "entry_price": float(open_trade["entry_price"]),
                    "exit_price": last_price,
                    "shares": shares_held,
                    "gross_pnl": gross_pnl,
                    "net_pnl": net_pnl,
                    "return_pct": return_pct,
                }
            )

            last_idx = len(enriched_df) - 1
            enriched_df.at[last_idx, "Shares_Held"] = 0
            enriched_df.at[last_idx, "Holdings"] = 0.0
            enriched_df.at[last_idx, "Cash"] = cash
            enriched_df.at[last_idx, "Portfolio_Value"] = cash

        enriched_df["Daily_Return"] = enriched_df["Portfolio_Value"].pct_change()

        return {"df": enriched_df, "trade_log": trade_log, "initial_capital": self.initial_capital}
