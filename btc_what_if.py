#!/usr/bin/env python3
"""
BTC What-If Calculator
Fetches the current BTC price and shows how much $100 invested on January 1st
of each year (since Bitcoin's creation in 2009) would be worth today.

Usage:
  python btc_what_if.py               # print results to terminal
  python btc_what_if.py --update-readme  # also update README.md
"""

import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

BTC_START_YEAR = 2010  # 2009 had no real exchange price

# Jan 1st BTC prices (USD) — hardcoded fallbacks / pre-2013 values
# Sources: CoinGecko / public historical data
HISTORICAL_JAN1_PRICES = {
    2010: 0.00099,
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

README_START = "<!-- BTC_RESULTS_START -->"
README_END = "<!-- BTC_RESULTS_END -->"


def fetch_current_btc_price() -> float:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    req = urllib.request.Request(url, headers={"User-Agent": "btc-what-if/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return float(data["bitcoin"]["usd"])


def fetch_jan1_price(year: int):
    if year < 2013:
        return HISTORICAL_JAN1_PRICES.get(year)

    date_str = f"01-01-{year}"
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={date_str}&localization=false"
    req = urllib.request.Request(url, headers={"User-Agent": "btc-what-if/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return float(data["market_data"]["current_price"]["usd"])
    except Exception:
        return HISTORICAL_JAN1_PRICES.get(year)


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


def build_rows(current_price: float, current_year: int, investment: float = 100.0):
    rows = []
    for year in range(BTC_START_YEAR, current_year + 1):
        is_current_year = year == current_year
        if is_current_year:
            jan1_price = HISTORICAL_JAN1_PRICES.get(year)
        else:
            jan1_price = fetch_jan1_price(year)

        if not jan1_price:
            rows.append({"year": year, "is_current_year": is_current_year, "skip": True})
            continue

        btc_bought = investment / jan1_price
        value_today = btc_bought * current_price
        multiplier = value_today / investment
        rows.append({
            "year": year,
            "is_current_year": is_current_year,
            "skip": False,
            "jan1_price": jan1_price,
            "btc_bought": btc_bought,
            "value_today": value_today,
            "multiplier": multiplier,
        })
    return rows


def print_terminal(rows, current_price: float, today: date):
    W = 66
    print("=" * W)
    print("         BTC WHAT-IF CALCULATOR")
    print(f"         {today.strftime('%A, %B %d, %Y')}")
    print("=" * W)
    print(f"  Current BTC price: ${current_price:,.2f}\n")
    print(f"  If you had invested $100 on January 1st of each year:\n")
    print(f"  {'Year':<7} {'Jan 1 price':>13} {'BTC bought':>14} {'Value today':>16}  Return")
    print(f"  {'':-<7} {'':-<13} {'':-<14} {'':-<16}  {'':-<10}")

    for r in rows:
        label = f"{r['year']}*" if r["is_current_year"] else str(r["year"])
        if r["skip"]:
            print(f"  {label:<7} {'N/A':>13} {'N/A':>14} {'N/A':>16}")
            continue
        p = r["jan1_price"]
        price_str = f"${p:.5f}" if p < 1 else f"${p:,.2f}"
        print(
            f"  {label:<7} {price_str:>13} {r['btc_bought']:>14.6f}"
            f" {format_usd_short(r['value_today']):>16}  {gain_label(r['multiplier'])}"
        )

    print(f"\n  * Jan 1, {today.year} price not yet available — using stored value")
    print("=" * W)


def build_markdown_table(rows, current_price: float, today: date) -> str:
    lines = [
        f"_Last updated: **{today.strftime('%A, %B %d, %Y')}** — BTC price: **${current_price:,.2f}**_",
        "",
        "| Year | BTC price on Jan 1 | BTC you'd get for $100 | Value today | Return |",
        "|------|-------------------|------------------------|-------------|--------|",
    ]
    for r in rows:
        label = f"{r['year']} \\*" if r["is_current_year"] else str(r["year"])
        if r["skip"]:
            lines.append(f"| {label} | N/A | N/A | N/A | N/A |")
            continue
        p = r["jan1_price"]
        price_str = f"${p:.5f}" if p < 1 else f"${p:,.2f}"
        lines.append(
            f"| {label} | {price_str} | {r['btc_bought']:.6f} BTC"
            f" | {format_usd_short(r['value_today'])} | {gain_label(r['multiplier'])} |"
        )
    lines.append("")
    lines.append(f"\\* Jan 1, {today.year} price not yet available — using stored value")
    return "\n".join(lines)


def update_readme(markdown_block: str, readme_path: Path):
    if not readme_path.exists():
        readme_path.write_text(
            f"# BTC What-If\n\n"
            f"How much would $100 invested in BTC on January 1st of each year be worth today?\n\n"
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

    rows = build_rows(current_price, today.year)
    print_terminal(rows, current_price, today)

    if update_readme_flag:
        md = build_markdown_table(rows, current_price, today)
        update_readme(md, Path(__file__).parent / "README.md")


if __name__ == "__main__":
    main()
