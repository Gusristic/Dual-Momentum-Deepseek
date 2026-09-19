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
    "0P0001CLDM.F": {"name": "Fidelity S&P 500 Index Fund EUR P Acc", "role": "Equity USA", "isin": "IE00BYX5MX67"},
    "0P0001CJGN.F": {"name": "Fidelity MSCI Europe Index Fund EUR P Acc", "role": "Equity Europe", "isin": "IE00BYX5MD61"},
    "0P0001CLDI.F": {"name": "Fidelity MSCI Japan Index Fund EUR P Acc", "role": "Equity Japan", "isin": "IE00BYX5N771"},
    "0P0001AN9J.F": {"name": "iShares Pacific Index Fund (IE) D Acc EUR", "role": "Equity Pacific", "isin": "IE00BDRK7R97"},
    "0P0001AINL.F": {"name": "iShares Emerging Markets Index Fund (IE) D Acc EUR", "role": "Equity EM", "isin": "IE00BYWYCC39"},
    "0P0000Y354.F": {"name": "iShares Developed Real Estate Index Fund (IE) Inst Acc EUR", "role": "Real Estate", "isin": "IE00B83YJG36"},
    "0P00012I66.F": {"name": "Vanguard Global Small-Cap Index Fund Inv EUR Acc", "role": "Small Cap", "isin": "IE00B42W3S00"},
    "IWDA.AS": {"name": "iShares Core MSCI World UCITS ETF (benchmark)", "role": "Benchmark", "isin": "IE00B4L5Y983"},
    "0P00000F24.F": {"name": "AXA Trésor Court Terme C", "role": "Cash", "isin": "FR0000447823"},
    "0P0001CFWF.F": {"name": "Croci sector plus", "role": "Value", "isin": "LU1278917452"},
}
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
