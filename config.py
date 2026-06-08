from datetime import datetime
from pathlib import Path

SYMBOLS = {
    "Crude Oil": "CL=F",
    "Gold": "GC=F",
    "Nifty 50": "^NSEI",
}

DEFAULT_SYMBOL = "GC=F"
START_DATE = "2015-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")
INITIAL_CAPITAL = 100000.0
COMMISSION = 0.001
RISK_FREE_RATE = 0.06
SHORT_WINDOW = 50
LONG_WINDOW = 200
DATA_DIR = Path("data/")
