#!/usr/bin/env python3
"""
BTC What-If Calculator
Fetches the current BTC price and shows how much $100 invested at the yearly
average price would be worth today, for every year since Bitcoin's creation.

Usage:
  python btc_what_if.py               # print results to terminal
  python btc_what_if.py --update-readme  # also update README.md
"""

import json
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

BTC_START_YEAR = 2010  # 2009 had no real exchange price

# Yearly average BTC prices (USD) — hardcoded fallbacks for pre-API years
# and as a safety net if CoinGecko is unavailable.
# Sources: CoinGecko / CoinMarketCap historical averages
HISTORICAL_AVG_PRICES = {
    2010: 0.07,
    2011: 5.97,
    2012: 8.27,
    2013: 193.0,
    2014: 527.0,
    2015: 272.0,
    2016: 567.0,
    2017: 3996.0,
    2018: 7382.0,
    2019: 7379.0,
    2020: 11135.0,
    2021: 47111.0,
    2022: 28145.0,
    2023: 26890.0,
    2024: 65000.0,
    2025: 90000.0,
    2026: 84000.0,  # YTD average Jan 1 – Apr 9, 2026 (estimated)
}

README_START = "<!-- BTC_RESULTS_START -->"
README_END = "<!-- BTC_RESULTS_END -->"


def fetch_current_btc_price() -> float:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    req = urllib.request.Request(url, headers={"User-Agent": "btc-what-if/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return float(data["bitcoin"]["usd"])


def _unix(year: int, month: int, day: int) -> int:
    return int(datetime(year, month, day, tzinfo=timezone.utc).timestamp())


def fetch_yearly_avg_price(year: int, today: date) -> float:
    """Return the average daily closing price for the given year using CoinGecko."""
    if year < 2013:
        return HISTORICAL_AVG_PRICES.get(year, 0.0)

    from_ts = _unix(year, 1, 1)
    # For the current year use today as the end, otherwise Dec 31
    if year == today.year:
        to_ts = _unix(today.year, today.month, today.day)
    else:
        to_ts = _unix(year, 12, 31)

    url = (
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
        f"?vs_currency=usd&from={from_ts}&to={to_ts}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "btc-what-if/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        prices = [p[1] for p in data["prices"]]
        if not prices:
            return HISTORICAL_AVG_PRICES.get(year, 0.0)
        return sum(prices) / len(prices)
    except Exception:
        return HISTORICAL_AVG_PRICES.get(year, 0.0)


def format_usd_short(amount: float) -> str:
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    return f"${amount:,.2f}"


def gain_label(multiplier: float) -> str:
    if multiplier >= 1:
        return f"+{multiplier:.1f}x"
    loss_pct = (1 - multiplier) * 100
    return f"-{loss_pct:.1f}%"


def build_rows(current_price: float, today: date, investment: float = 100.0):
    rows = []
    for year in range(BTC_START_YEAR, today.year + 1):
        is_current_year = year == today.year
        print(f"  Fetching {year} average...", end=" ", flush=True)
        avg_price = fetch_yearly_avg_price(year, today)

        if not avg_price:
            print("N/A")
            rows.append({"year": year, "is_current_year": is_current_year, "skip": True})
            continue

        print(f"${avg_price:,.2f}")
        btc_bought = investment / avg_price
        value_today = btc_bought * current_price
        multiplier = value_today / investment
        rows.append({
            "year": year,
            "is_current_year": is_current_year,
            "skip": False,
            "avg_price": avg_price,
            "btc_bought": btc_bought,
            "value_today": value_today,
            "multiplier": multiplier,
        })
    return rows


def print_terminal(rows, current_price: float, today: date):
    W = 68
    print()
    print("=" * W)
    print("          BTC WHAT-IF CALCULATOR")
    print(f"          {today.strftime('%A, %B %d, %Y')}")
    print("=" * W)
    print(f"  Current BTC price: ${current_price:,.2f}\n")
    print(f"  $100 invested at each year's average price:\n")
    print(f"  {'Year':<7} {'Avg price':>13} {'BTC bought':>14} {'Value today':>16}  Return")
    print(f"  {'':-<7} {'':-<13} {'':-<14} {'':-<16}  {'':-<10}")

    for r in rows:
        label = f"{r['year']}*" if r["is_current_year"] else str(r["year"])
        if r["skip"]:
            print(f"  {label:<7} {'N/A':>13} {'N/A':>14} {'N/A':>16}")
            continue
        p = r["avg_price"]
        price_str = f"${p:.4f}" if p < 1 else f"${p:,.2f}"
        print(
            f"  {label:<7} {price_str:>13} {r['btc_bought']:>14.6f}"
            f" {format_usd_short(r['value_today']):>16}  {gain_label(r['multiplier'])}"
        )

    print(f"\n  * {today.year} is partial — average covers Jan 1 through today")
    print("=" * W)


def build_markdown_table(rows, current_price: float, today: date) -> str:
    lines = [
        f"_Last updated: **{today.strftime('%A, %B %d, %Y')}** — BTC price: **${current_price:,.2f}**_",
        "",
        "| Year | Avg BTC price | BTC you'd get for $100 | Value today | Return |",
        "|------|--------------|------------------------|-------------|--------|",
    ]
    for r in rows:
        label = f"{r['year']} \\*" if r["is_current_year"] else str(r["year"])
        if r["skip"]:
            lines.append(f"| {label} | N/A | N/A | N/A | N/A |")
            continue
        p = r["avg_price"]
        price_str = f"${p:.4f}" if p < 1 else f"${p:,.2f}"
        lines.append(
            f"| {label} | {price_str} | {r['btc_bought']:.6f} BTC"
            f" | {format_usd_short(r['value_today'])} | {gain_label(r['multiplier'])} |"
        )
    lines.append("")
    lines.append(f"\\* {today.year} is partial — average covers Jan 1 through today")
    return "\n".join(lines)


def update_readme(markdown_block: str, readme_path: Path):
    if not readme_path.exists():
        readme_path.write_text(
            "# BTC What-If\n\n"
            "How much would $100 invested in BTC at each year's average price be worth today?\n\n"
            f"{README_START}\n{markdown_block}\n{README_END}\n"
        )
        print(f"Created {readme_path}")
        return

    content = readme_path.read_text()
    if README_START in content and README_END in content:
        before = content[: content.index(README_START) + len(README_START)]
        after = content[content.index(README_END):]
        new_content = f"{before}\n{markdown_block}\n{after}"
    else:
        new_content = content.rstrip() + f"\n\n{README_START}\n{markdown_block}\n{README_END}\n"

    readme_path.write_text(new_content)
    print(f"Updated {readme_path}")


def main():
    update_readme_flag = "--update-readme" in sys.argv
    today = date.today()

    print("Fetching current BTC price...", end=" ", flush=True)
    try:
        current_price = fetch_current_btc_price()
        print(f"${current_price:,.2f}")
    except Exception as e:
        print(f"FAILED ({e})")
        raise SystemExit(1)

    print("Fetching yearly averages...")
    rows = build_rows(current_price, today)
    print_terminal(rows, current_price, today)

    if update_readme_flag:
        md = build_markdown_table(rows, current_price, today)
        update_readme(md, Path(__file__).parent / "README.md")


if __name__ == "__main__":
    main()
