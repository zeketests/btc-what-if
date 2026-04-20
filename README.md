# BTC What-If

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/120px-Bitcoin.svg.png" alt="Bitcoin logo" />
</p>

> **"What if I had bought Bitcoin?"**

This project answers the question everyone in crypto eventually asks: *how much would **$100** have grown if invested in Bitcoin at the average price of any given year?*

Starting from 2010 — the first year BTC had a real exchange price — the script fetches the live BTC/USD rate from CoinGecko, computes yearly average prices, and calculates the hypothetical return on a $100 investment for every year since.

## How it works

- **Investment assumption:** $100 invested at the yearly average USD price for BTC
- **Price source:** [CoinGecko API](https://www.coingecko.com/) — live spot price + historical yearly averages
- **Auto-updated:** A GitHub Actions workflow runs daily and commits fresh results to this README

## Returns at a glance (2013 – 2026)

_Value today of $100 invested at each year's average price (USD):_

```mermaid
xychart-beta
    title "Value today of $100 invested in BTC by year"
    x-axis ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","2026"]
    y-axis "Value today (USD)" 0 --> 40000
    bar [37517, 13740, 26621, 12770, 1812, 981, 981, 650, 154, 257, 269, 111, 80, 86]
```

> Earlier years (2010–2012) are off the chart — $100 in 2010 would be worth **~$103 million** today.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/BTC_Logo.svg/200px-BTC_Logo.svg.png" alt="Bitcoin symbol" width="80"/>
</p>

## Full results table

<!-- BTC_RESULTS_START -->
_Last updated: **Monday, April 20, 2026** — BTC price: **$75,193.00**_

| Year | Avg BTC price | BTC you'd get for $100 | Value today | Return |
|------|--------------|------------------------|-------------|--------|
| 2010 | $0.0700 | 1428.571429 BTC | $107.42M | +1074185.7x |
| 2011 | $5.97 | 16.750419 BTC | $1.26M | +12595.1x |
| 2012 | $8.27 | 12.091898 BTC | $909,226.12 | +9092.3x |
| 2013 | $193.00 | 0.518135 BTC | $38,960.10 | +389.6x |
| 2014 | $527.00 | 0.189753 BTC | $14,268.12 | +142.7x |
| 2015 | $272.00 | 0.367647 BTC | $27,644.49 | +276.4x |
| 2016 | $567.00 | 0.176367 BTC | $13,261.55 | +132.6x |
| 2017 | $3,996.00 | 0.025025 BTC | $1,881.71 | +18.8x |
| 2018 | $7,382.00 | 0.013546 BTC | $1,018.60 | +10.2x |
| 2019 | $7,379.00 | 0.013552 BTC | $1,019.01 | +10.2x |
| 2020 | $11,135.00 | 0.008981 BTC | $675.29 | +6.8x |
| 2021 | $47,111.00 | 0.002123 BTC | $159.61 | +1.6x |
| 2022 | $28,145.00 | 0.003553 BTC | $267.16 | +2.7x |
| 2023 | $26,890.00 | 0.003719 BTC | $279.63 | +2.8x |
| 2024 | $65,000.00 | 0.001538 BTC | $115.68 | +1.2x |
| 2025 | $90,000.00 | 0.001111 BTC | $83.55 | -16.5% |
| 2026 \* | $84,000.00 | 0.001190 BTC | $89.52 | -10.5% |

\* 2026 is partial — average covers Jan 1 through today
<!-- BTC_RESULTS_END -->
