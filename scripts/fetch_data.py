"""
Descarga precios mensuales ajustados de Yahoo Finance y guarda
data/prices.json para que la web los consuma.
"""
import json
import os
from datetime import datetime, timezone
import yfinance as yf

# Universo por defecto. Puedes aÃ±adir/quitar tickers aquÃ­.
TICKERS = {
    "SPY":     {"name": "SPDR S&P 500 ETF Trust",              "role": "Equity USA",  "isin": "US78462F1030"},
    "IWDA.AS": {"name": "iShares Core MSCI World UCITS ETF",   "role": "Equity DM",   "isin": "IE00B4L5Y983"},
    "EEM":     {"name": "iShares MSCI Emerging Markets ETF",   "role": "Equity EM",   "isin": "US4642872349"},
    "AGGH.MI": {"name": "iShares Core Global Agg Bond UCITS",  "role": "Bonds",       "isin": "IE00BDBRDM35"},
    "IGLN.L":  {"name": "iShares Physical Gold ETC",           "role": "Gold",        "isin": "IE00B4ND3602"},
    "XEON.DE": {"name": "Xtrackers EUR Overnight Rate Swap",   "role": "Cash",        "isin": "LU0290358497"},
}

PERIOD = "15y"
INTERVAL = "1mo"

def main() -> None:
    data = {}
    for ticker, meta in TICKERS.items():
        try:
            df = yf.download(
                ticker, period=PERIOD, interval=INTERVAL,
                auto_adjust=True, progress=False,
            )
            if df is None or df.empty:
                print(f"FAIL {ticker}: sin datos")
                continue
            df = df.dropna()
            dates = [d.strftime("%Y-%m-%d") for d in df.index]
            close = [float(x) for x in df["Close"].values.flatten()]
            data[ticker] = {
                "meta": meta,
                "dates": dates,
                "close": close,
            }
            print(f"OK   {ticker}: {len(dates)} filas ({dates[0]} â†’ {dates[-1]})")
        except Exception as exc:
            print(f"FAIL {ticker}: {exc}")

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Yahoo Finance via yfinance",
        "period": PERIOD,
        "interval": INTERVAL,
        "data": data,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/prices.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"OK   data/prices.json ({len(data)} instrumentos)")

if __name__ == "__main__":
    main()
