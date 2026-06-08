# Trading Backtester

Algorithmic trading strategy backtester with Streamlit dashboard and CLI support.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
+
+## Architecture
+
+- `app.py` — Streamlit dashboard UI
+- `main.py` — CLI entry point
+- `config.py` — project configuration constants
+- `backtester/data_fetcher.py` — OHLCV data fetching and caching
+- `backtester/indicators.py` — SMA and EMA helpers
+- `backtester/engine.py` — trade simulation engine
+- `backtester/metrics.py` — performance metrics calculator
+- `visualizer/charts.py` — Plotly chart generation
+
+## Setup
+
+```bash
git clone <your-repo-url>
+cd trading-backtester
+python -m venv venv
+source venv/bin/activate   # macOS/Linux
+# or .\venv\Scripts\activate   # Windows
+pip install -r requirements.txt
+```
+
+## Usage
+
+```bash
+streamlit run app.py
+python main.py --symbol GC=F --start 2015-01-01
+```
+
+## Output
+
+The backtester produces these 10 metrics:
+
+1. total_return_pct
+2. cagr_pct
+3. sharpe_ratio
+4. max_drawdown_pct
+5. total_trades
+6. winning_trades
+7. win_rate_pct
+8. avg_win
+9. avg_loss
+10. profit_factor
+
+## Screenshot
+
+![Dashboard](docs/screenshot.png)
+
+## Freeze dependencies
+
+```bash
+pip freeze > requirements.txt
+```
