import argparse
import logging
from datetime import datetime

import config
from backtester.data_fetcher import DataFetcher
from backtester.engine import BacktestEngine
from backtester.metrics import MetricsCalculator
from strategies import GoldenCrossStrategy
from visualizer.charts import ChartBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("backtest.log"),
    ],
)

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Run a golden-cross backtest from the command line.")
    parser.add_argument("--symbol", default=config.DEFAULT_SYMBOL, help="Ticker e.g. GC=F")
    parser.add_argument("--start", default=config.START_DATE, help="Start date in YYYY-MM-DD")
    parser.add_argument("--end", default=datetime.today().strftime("%Y-%m-%d"), help="End date in YYYY-MM-DD")
    parser.add_argument("--short", type=int, default=config.SHORT_WINDOW, help="Short MA window")
    parser.add_argument("--long", type=int, default=config.LONG_WINDOW, help="Long MA window")
    parser.add_argument("--capital", type=float, default=config.INITIAL_CAPITAL, help="Initial capital")
    parser.add_argument("--no-chart", action="store_true", help="Skip opening chart in browser")
    return parser


def run_backtest(args: argparse.Namespace) -> None:
    """Run the backtest pipeline and print a summary."""
    logger.info("Starting backtest with params: symbol=%s, start=%s, end=%s, short=%s, long=%s, capital=%.2f", args.symbol, args.start, args.end, args.short, args.long, args.capital)

    try:
        fetcher = DataFetcher()
        df = fetcher.get_ohlcv(args.symbol, args.start, args.end)
        df = fetcher.validate_data(df, args.symbol)

        strategy = GoldenCrossStrategy(short_window=args.short, long_window=args.long)
        signals_df = strategy.generate_signals(df)

        engine = BacktestEngine(initial_capital=args.capital)
        result = engine.run(signals_df)

        metrics = MetricsCalculator().calculate(result)

        if not args.no_chart:
            fig = ChartBuilder().combined_dashboard(result["df"], args.symbol, args.capital)
            fig.show()

        total_return = metrics.get("total_return_pct", 0.0)
        cagr = metrics.get("cagr_pct", 0.0)
        sharpe = metrics.get("sharpe_ratio", 0.0)
        max_drawdown = metrics.get("max_drawdown_pct", 0.0)
        win_rate = metrics.get("win_rate_pct", 0.0)
        total_trades = metrics.get("total_trades", 0)
        buy_hold_return = metrics.get("buy_hold_return_pct", 0.0)

        summary = [
            "╔══════════════════════════════════╗",
            f"║  BACKTEST RESULTS — {args.symbol:<18}║",
            "╠══════════════════════════════════╣",
            f"║  Total Return       : {total_return:+7.2f}%  ║",
            f"║  CAGR               : {cagr:+7.2f}%  ║",
            f"║  Sharpe Ratio       : {sharpe:>7.2f}   ║",
            f"║  Max Drawdown       : {max_drawdown:+7.2f}%  ║",
            f"║  Win Rate           : {win_rate:>7.2f}%  ║",
            f"║  Total Trades       : {total_trades:>7d}   ║",
            f"║  Buy & Hold Return  : {buy_hold_return:+7.2f}%  ║",
            "╚══════════════════════════════════╝",
        ]

        print("\n".join(summary))
    except Exception:
        logger.exception("Backtest failed")
        raise


def main() -> None:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()
    run_backtest(args)


if __name__ == "__main__":
    main()
