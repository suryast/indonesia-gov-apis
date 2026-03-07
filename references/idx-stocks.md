# IDX Stock Market Data

## Via Yahoo Finance (Recommended)

```python
import yfinance as yf

# Single stock — .JK suffix required
stock = yf.Ticker("BBCA.JK")
hist = stock.history(period="1mo")
print(hist[["Open", "High", "Low", "Close", "Volume"]])

# Company info
info = stock.info
print(f"Market Cap: {info.get('marketCap'):,}")
print(f"P/E: {info.get('trailingPE')}")

# Multiple stocks
tickers = yf.download(["BBCA.JK", "BBRI.JK", "TLKM.JK"], period="1mo")

# IHSG composite index
ihsg = yf.Ticker("^JKSE")
print(f"IHSG: {ihsg.history(period='1d')['Close'].iloc[-1]:.2f}")
```

## Common Tickers

| Ticker | Company | Sector |
|--------|---------|--------|
| BBCA.JK | Bank Central Asia | Banking |
| BBRI.JK | Bank Rakyat Indonesia | Banking |
| BMRI.JK | Bank Mandiri | Banking |
| TLKM.JK | Telkom Indonesia | Telecoms |
| ASII.JK | Astra International | Conglomerate |
| UNVR.JK | Unilever Indonesia | Consumer |
| GOTO.JK | GoTo Group | Tech |
| ^JKSE | IHSG Composite Index | Index |

## Gotchas
- `.JK` suffix required for all Indonesian stocks
- Yahoo Finance data has 15-minute delay
- Trading hours: 09:00-16:00 WIB (02:00-09:00 UTC), Mon-Fri
- IDX has no official public API — Yahoo Finance is the best free source
- Corporate actions (splits, rights) affect historical data
- `pip install yfinance` required
