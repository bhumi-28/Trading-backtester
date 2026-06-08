# 📈 Algorithmic Trading Backtester: Backtest, Visualize & Analyze Trading Strategies in Python

> A Python-based backtesting framework for building, testing, and visualizing algorithmic trading strategies using real market data — with interactive Plotly charts, SMA signals, and portfolio analytics.

**Algorithmic Trading Backtester** is a modular Python project that lets you define trading strategies, run them against historical price data, and visualize results with interactive charts. Instead of guessing if your strategy works, you get real signal plots, equity curves, and performance metrics.

**Start here:** [New Here? Start Here!](#-new-here-start-here) · [Installation](#-installation) · [How to Use](#-how-to-use) · [Strategies](#-strategies--core-concepts) · [Visualizations](#-visualizations) · [Contributing](#-contributing)

---

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Plotly](https://img.shields.io/badge/Charts-Plotly-purple?style=flat-square&logo=plotly)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat-square&logo=pandas)
![GitHub](https://img.shields.io/badge/GitHub-bhumi--28-black?style=flat-square&logo=github)

---

**Current release: v1.0.0.** A full backtesting pipeline that goes from raw OHLCV data → strategy signals → trade execution → interactive performance charts — all in Python.

---

## Why Developers Star This Repo

- **Modular, not monolithic**: strategies, data loaders, executors, and visualizers are separate modules you can swap out independently.
- **Real interactive charts**: uses Plotly to render price charts with buy/sell markers, SMA overlays, and equity curves — not static images.
- **Strategy-first design**: define a new strategy by implementing a single class; the engine handles the rest.
- **Beginner-friendly structure**: clear folder layout, inline comments, and readable code — great for learning quant concepts through code.
- **Extensible by design**: add new indicators, data sources, or export formats without touching core logic.

---

## Table of Contents

- 🚀 [New Here? Start Here!](#-new-here-start-here)
- 🧠 [Core Concepts](#-strategies--core-concepts)
- ⚙️ [Installation](#-installation)
- ▶️ [How to Use](#-how-to-use)
- 📊 [Visualizations](#-visualizations)
- 🗂️ [Project Structure](#️-project-structure)
- 📐 [Compatibility & Requirements](#-compatibility--requirements)
- ❓ [Quick FAQ](#-quick-faq)
- 🐛 [Troubleshooting](#-troubleshooting)
- 🤝 [Contributing](#-contributing)
- ⚖️ [License](#️-license)

---

## 🚀 New Here? Start Here!

If you landed here looking for a **Python backtesting project**, an **algorithmic trading example**, or a **Plotly trading chart** — this is your fastest path to running a backtest and seeing results the same day.

### 1. 🧭 Context: What is this?

**Algorithmic Trading Backtester** (v1.0.0) is a Python project that simulates trading strategies on historical stock data. It computes indicators like SMA, generates buy/sell signals, tracks portfolio value over time, and renders interactive Plotly charts — all locally, no paid APIs required.

The goal is simple: **test your strategy before you risk real money.**

### 2. ⚡ Quick Start (2 minutes)

**1. Clone the repo:**

```bash
git clone https://github.com/bhumi-28/Trading-backtester.git
cd Trading-backtester
```

**2. Create a virtual environment and install dependencies:**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

**3. Run the backtester:**

```bash
python main.py
```

**4. Open the chart** — a Plotly chart will open in your browser showing price, SMA lines, and buy/sell signals.

### 3. 🧪 How to Use

Once installed, configure your strategy in `config.py` and run `main.py`:

```python
# config.py
SYMBOL       = "AAPL"       # Stock ticker
START_DATE   = "2022-01-01"
END_DATE     = "2024-01-01"
SMA_SHORT    = 20           # Short SMA window
SMA_LONG     = 50           # Long SMA window
INITIAL_CASH = 10000        # Starting portfolio value
```

Then run:

```bash
python main.py
```

### 4. 📦 Pick your starting point

- **Learning quant trading?** → Start with `strategies/sma_crossover.py`
- **Want to visualize signals?** → Check `visualizer/charts.py`
- **Adding your own strategy?** → Read [Strategies & Core Concepts](#-strategies--core-concepts)

---

## 🧠 Strategies & Core Concepts

Before adding strategies or modifying the engine, understand these four building blocks:

- **Strategy**: a class that takes OHLCV data and outputs a `Position` column (+1 = buy, -1 = sell, 0 = hold).
- **Backtester**: the engine that feeds data to a strategy, tracks trades, and computes portfolio value.
- **Visualizer**: the `ChartBuilder` class that takes backtest results and renders Plotly figures.
- **Config**: a central `config.py` file that controls all parameters — ticker, dates, SMA windows, initial cash.

### Currently implemented strategies

| Strategy | Description | File |
|---|---|---|
| SMA Crossover | Buy when short SMA crosses above long SMA; sell on cross below | `strategies/sma_crossover.py` |
| Buy & Hold | Baseline — buy on day 1, hold until end | `strategies/buy_and_hold.py` |

---

## ⚙️ Installation

### Requirements

| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| pandas | latest | Data manipulation |
| plotly | latest | Interactive charts |
| numpy | latest | Numerical computation |
| yfinance | latest | Historical price data |

### Install steps

```bash
# 1. Clone
git clone https://github.com/bhumi-28/Trading-backtester.git
cd Trading-backtester

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

---

## ▶️ How to Use

### Run a backtest

```bash
python main.py
```

### Change the stock and date range

Edit `config.py`:

```python
SYMBOL     = "TSLA"
START_DATE = "2021-01-01"
END_DATE   = "2023-12-31"
```

### Add your own strategy

1. Create a new file in `strategies/`, e.g. `strategies/rsi_strategy.py`
2. Implement the `generate_signals(df)` method that returns a DataFrame with a `Position` column
3. Import and register it in `main.py`

```python
from strategies.rsi_strategy import RSIStrategy
strategy = RSIStrategy(config)
```

---

## 📊 Visualizations

The `visualizer/charts.py` module uses Plotly to produce:

- **Price + SMA chart** — closing price with short and long SMA lines overlaid
- **Buy/Sell markers** — green triangles (▲) for buy signals, red triangles (▽) for sell signals
- **Portfolio equity curve** — how your portfolio value changed over the backtest period
- **Dark theme** — rendered with `plotly_dark` for a clean trading-terminal look

All charts open automatically in your browser when you run `main.py`.

---

## 🗂️ Project Structure

```
trading-backtester/
│
├── main.py                   # Entry point — runs the full pipeline
├── config.py                 # All user-configurable parameters
├── requirements.txt          # Python dependencies
│
├── data/
│   └── data_loader.py        # Downloads OHLCV data via yfinance
│
├── strategies/
│   ├── sma_crossover.py      # SMA crossover strategy
│   └── buy_and_hold.py       # Baseline buy-and-hold strategy
│
├── backtester/
│   └── engine.py             # Core backtest engine
│
└── visualizer/
    └── charts.py             # Plotly chart builder
```

---

## 📐 Compatibility & Requirements

| Environment | Supported | Notes |
|---|---|---|
| Windows 10/11 | ✅ | Tested — primary dev environment |
| macOS 12+ | ✅ | Should work out of the box |
| Linux (Ubuntu 20+) | ✅ | Standard Python setup |
| Python 3.10+ | ✅ | Required |
| Python < 3.10 | ❌ | Not tested |
| Jupyter Notebook | ✅ | Charts render inline with `fig.show()` |

---

## ❓ Quick FAQ

**Q: Where does the historical data come from?**  
A: From Yahoo Finance via the `yfinance` library — free, no API key required.

**Q: Can I test on crypto or forex?**  
A: Yes — any ticker supported by Yahoo Finance works (e.g. `BTC-USD`, `EURUSD=X`).

**Q: Does this support live trading?**  
A: No — this is a backtesting tool only. It simulates trades on historical data.

**Q: How do I add a new indicator (e.g. RSI, MACD)?**  
A: Compute it in your strategy file using pandas, then use it in `generate_signals()`.

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'plotly'`**  
→ Run `pip install -r requirements.txt` inside your virtual environment.

**Charts not opening in browser**  
→ Try `fig.show(renderer="browser")` explicitly in `charts.py`.

**`yfinance` returns empty data**  
→ Check your ticker symbol and date range. Some tickers or date ranges return no data.

**`template` error in Plotly**  
→ Use `template="plotly_dark"` (string, not a variable) in `go.Layout(...)`.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-strategy`
3. Make your changes and commit: `git commit -m "Add RSI strategy"`
4. Push to your fork: `git push origin feature/my-strategy`
5. Open a Pull Request

Ideas for contributions: new strategies, additional indicators, CSV export, performance metrics (Sharpe ratio, max drawdown), or a CLI interface.

---

## ⚖️ License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

*Built with 🐍 Python · 📊 Plotly · 🐼 Pandas · ❤️ by [Bhumi](https://github.com/bhumi-28)*