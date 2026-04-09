#!/usr/bin/env python3
"""
BTC What-If Calculator
Fetches the current BTC price and shows how much $100 invested on January 1st
of each year (since Bitcoin's creation in 2009) would be worth today.
"""

import json
import urllib.request
import urllib.error
from datetime import date, datetime

# Bitcoin's first year with any meaningful price data
BTC_START_YEAR = 2010  # 2009 had no real exchange price

# Jan 1st BTC prices (USD) — historical open prices
# Sources: CoinGecko / public historical data
HISTORICAL_JAN1_PRICES = {
    2010: 0.00099,   # ~$0.001 (first recorded price ~Oct 2009, used here as approx)
    2011: 0.30,
    2012: 5.27,
    2013: 13.30,
    2014: 771.40,
    2015: 314.25,
    2016: 434.33,
    2017: 998.33,
    2018: 13412.44,
    2019: 3843.52,
    2020: 7200.17,
    2021: 29374.15,
    2022: 47686.81,
    2023: 16547.50,
    2024: 42531.91,
    2025: 93429.00,
}


def fetch_current_btc_price() -> float:
    """Fetch the current BTC/USD price from CoinGecko's free API."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    req = urllib.request.Request(url, headers={"User-Agent": "btc-what-if/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return float(data["bitcoin"]["usd"])


def fetch_jan1_price(year: int) -> "float | None":
    """
    Fetch the BTC price on January 1st of the given year from CoinGecko.
    Falls back to None if the data is unavailable.
    """
    if year < 2013:
        # CoinGecko history only goes back reliably to 2013; use hardcoded values
        return HISTORICAL_JAN1_PRICES.get(year)

    # CoinGecko /history endpoint — date format dd-mm-yyyy
    date_str = f"01-01-{year}"
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={date_str}&localization=false"
    req = urllib.request.Request(url, headers={"User-Agent": "btc-what-if/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return float(data["market_data"]["current_price"]["usd"])
    except Exception:
        # Fall back to hardcoded values if API call fails
        return HISTORICAL_JAN1_PRICES.get(year)


def format_usd(amount: float) -> str:
    if amount >= 1_000_000:
        return f"${amount:,.0f}  ({amount / 1_000_000:.2f}M)"
    return f"${amount:,.2f}"


def main():
    today = date.today()
    current_year = today.year

    print("=" * 62)
    print("        BTC WHAT-IF CALCULATOR")
    print(f"        {today.strftime('%A, %B %d, %Y')}")
    print("=" * 62)

    print("\nFetching current BTC price...", end=" ", flush=True)
    try:
        current_price = fetch_current_btc_price()
        print(f"${current_price:,.2f}")
    except Exception as e:
        print(f"FAILED ({e})")
        raise SystemExit(1)

    investment = 100.0
    years = range(BTC_START_YEAR, current_year + 1)

    print(f"\nIf you had invested ${investment:.0f} on January 1st of each year:\n")
    print(f"  {'Year':<6} {'BTC price Jan 1':>16} {'BTC bought':>14} {'Value today':>20}  Return")
    print(f"  {'':-<6} {'':-<16} {'':-<14} {'':-<20}  {'':-<10}")

    for year in years:
        if year == current_year:
            # For the current year use the hardcoded price if already stored,
            # otherwise skip — the year isn't over yet and we already show current price
            jan1_price = HISTORICAL_JAN1_PRICES.get(year)
            label = f"{year}*"
        else:
            jan1_price = fetch_jan1_price(year)
            label = str(year)

        if jan1_price is None or jan1_price == 0:
            print(f"  {label:<6} {'N/A':>16} {'N/A':>14} {'N/A':>20}")
            continue

        btc_bought = investment / jan1_price
        value_today = btc_bought * current_price
        multiplier = value_today / investment

        if multiplier >= 1:
            gain_str = f"+{multiplier:.1f}x"
        else:
            loss_pct = (1 - multiplier) * 100
            gain_str = f"-{loss_pct:.1f}%"

        if jan1_price < 1:
            price_str = f"${jan1_price:.5f}"
        else:
            price_str = f"${jan1_price:,.2f}"

        print(
            f"  {label:<6} {price_str:>16} {btc_bought:>14.6f} {format_usd(value_today):>20}  {gain_str}"
        )

    print()
    print(f"  * Current year — price as of Jan 1, {current_year}")
    print(f"\n  Current BTC price: ${current_price:,.2f}")
    print("=" * 62)


if __name__ == "__main__":
    main()
