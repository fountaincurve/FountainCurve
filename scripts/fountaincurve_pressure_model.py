import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Step 1: Download data
    spy = yf.download("SPY", start="2023-01-01", end="2025-07-01")
    vix = yf.download("^VIX", start="2023-01-01", end="2025-07-01")
    vvix = yf.download("^VVIX", start="2023-01-01", end="2025-07-01")

    # Step 2: Calculate core signals
    spy['Return'] = spy["Close"].pct_change()
    spy['HV20'] = spy['Return'].rolling(window=20).std() * (252 ** 0.5) * 100

    # Step 3: Align and combine
    combined = pd.DataFrame(index=spy.index)
    combined["SPY_HV20"] = spy["HV20"]
    combined["VIX"] = vix["Close"]
    combined["VVIX"] = vvix["Close"]

    # Step 4: Add derived variables
    combined["VIX_VVIX_ratio"] = combined["VIX"] / combined["VVIX"]

    # Step 5: Clean and resample
    combined.dropna(inplace=True)
    monthly = combined.resample("ME").last()

    # Step 6: Ensure folders exist
    os.makedirs("output", exist_ok=True)
    os.makedirs("charts", exist_ok=True)

    # Step 7: Save to CSV for future analysis
    combined.to_csv("output/vol_pressure_daily.csv")
    monthly.to_csv("output/vol_pressure_monthly.csv")

    # Step 8: Basic plot
    plt.figure(figsize=(12, 6))
    plt.plot(monthly.index, monthly["SPY_HV20"], label="HV20", linewidth=2)
    plt.plot(monthly.index, monthly["VIX"], label="VIX", linestyle="--")
    plt.plot(monthly.index, monthly["VVIX"], label="VVIX", linestyle=":")
    plt.fill_between(monthly.index, monthly["SPY_HV20"], monthly["VIX"],
                     where=(monthly["SPY_HV20"] > monthly["VIX"]),
                     color='red', alpha=0.3, label="Suppression Zone")
    plt.title("Volatility Pressure Model (FountainCurve)")
    plt.xlabel("Date")
    plt.ylabel("Volatility (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.savefig("charts/vol_pressure_model.png")
    plt.show()

if __name__ == "__main__":
    main()

