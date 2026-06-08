from datetime import datetime

import pandas as pd
import streamlit as st

import config
from backtester.data_fetcher import DataFetcher
from backtester.engine import BacktestEngine
from backtester.metrics import MetricsCalculator
from strategies import GoldenCrossStrategy
from visualizer.charts import ChartBuilder

st.set_page_config(page_title="📈 Trading Backtester", layout="wide")


@st.cache_data
def fetch_cached_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch OHLCV data with caching enabled for the Streamlit app."""
    return DataFetcher().get_ohlcv(symbol, start_date, end_date)


def main() -> None:
    """Render the Streamlit dashboard for the trading backtester."""
    st.sidebar.title("⚙️ Strategy Config")

    symbol_names = list(config.SYMBOLS.keys())
    selected_symbol_name = st.sidebar.selectbox("Symbol", symbol_names, index=symbol_names.index("Gold"))
    symbol = config.SYMBOLS[selected_symbol_name]

    start_default = datetime.strptime(config.START_DATE, "%Y-%m-%d").date()
    end_default = datetime.today().date()
    start_date = st.sidebar.date_input("Start Date", value=start_default, format="YYYY-MM-DD")
    end_date = st.sidebar.date_input("End Date", value=end_default, format="YYYY-MM-DD")

    short_window = st.sidebar.slider("Short MA", 10, 100, config.SHORT_WINDOW, step=5)
    long_window = st.sidebar.slider("Long MA", 100, 300, config.LONG_WINDOW, step=10)
    initial_capital = st.sidebar.number_input("Initial Capital", min_value=10000.0, max_value=10000000.0, value=float(config.INITIAL_CAPITAL), step=10000.0)
    commission = st.sidebar.number_input("Commission", min_value=0.0, max_value=0.02, value=float(config.COMMISSION), step=0.001, format="%.3f")
    run_backtest = st.sidebar.button("▶ Run Backtest")

    st.title(f"📈 Golden Cross Strategy — {selected_symbol_name} ({symbol})")

    if run_backtest:
        try:
            with st.spinner("Running backtest..."):
                df = fetch_cached_data(symbol, start_date.isoformat(), end_date.isoformat())
                df = DataFetcher().validate_data(df, symbol)
                signals_df = GoldenCrossStrategy(short_window=short_window, long_window=long_window).generate_signals(df)
                result = BacktestEngine(initial_capital=initial_capital, commission=commission).run(signals_df)
                metrics = MetricsCalculator().calculate(result)
                fig = ChartBuilder().combined_dashboard(result["df"], symbol, initial_capital)

            st.subheader("Performance Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Return", f"{metrics['total_return_pct']}%", delta=f"vs {metrics['buy_hold_return_pct']}%")
            with col2:
                st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
            with col3:
                st.metric("Max Drawdown", f"{metrics['max_drawdown_pct']}%")
            with col4:
                st.metric("Win Rate", f"{metrics['win_rate_pct']}%")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("CAGR", f"{metrics['cagr_pct']}%")
            with c2:
                st.metric("Total Trades", metrics['total_trades'])
            with c3:
                st.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
            with c4:
                st.metric("Avg Win / Avg Loss", f"{metrics['avg_win']:.2f} / {metrics['avg_loss']:.2f}")

            st.subheader("Charts")
            st.plotly_chart(fig, use_container_width=True)

            trade_log = result.get("trade_log", [])
            if trade_log:
                trade_df = pd.DataFrame(trade_log)
                currency_columns = ["entry_price", "exit_price", "gross_pnl", "net_pnl"]
                for column in currency_columns:
                    trade_df[column] = trade_df[column].apply(lambda value: f"{float(value):.2f}")
                trade_df["return_pct"] = trade_df["return_pct"].apply(lambda value: f"{float(value):.2%}")
                trade_df["shares"] = trade_df["shares"].astype(int)
                st.subheader("Trade Log")
                st.dataframe(trade_df, use_container_width=True)
                csv_data = trade_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download Trade Log CSV", data=csv_data, file_name="trade_log.csv", mime="text/csv")
            else:
                st.info("No completed trades were generated in this run.")
        except Exception as exc:
            st.error(f"Backtest failed: {exc}")


if __name__ == "__main__":
    main()
