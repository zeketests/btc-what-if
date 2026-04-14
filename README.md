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
_Last updated: **Tuesday, April 14, 2026** — BTC price: **$74,543.00**_

| Year | Avg BTC price | BTC you'd get for $100 | Value today | Return |
|------|--------------|------------------------|-------------|--------|
| 2010 | $0.0700 | 1428.571429 BTC | $106.49M | +1064900.0x |
| 2011 | $5.97 | 16.750419 BTC | $1.25M | +12486.3x |
| 2012 | $8.27 | 12.091898 BTC | $901,366.38 | +9013.7x |
| 2013 | $193.00 | 0.518135 BTC | $38,623.32 | +386.2x |
| 2014 | $527.00 | 0.189753 BTC | $14,144.78 | +141.4x |
| 2015 | $272.00 | 0.367647 BTC | $27,405.51 | +274.1x |
| 2016 | $567.00 | 0.176367 BTC | $13,146.91 | +131.5x |
| 2017 | $3,996.00 | 0.025025 BTC | $1,865.44 | +18.7x |
| 2018 | $7,382.00 | 0.013546 BTC | $1,009.79 | +10.1x |
| 2019 | $7,379.00 | 0.013552 BTC | $1,010.20 | +10.1x |
| 2020 | $11,135.00 | 0.008981 BTC | $669.45 | +6.7x |
| 2021 | $47,111.00 | 0.002123 BTC | $158.23 | +1.6x |
| 2022 | $28,145.00 | 0.003553 BTC | $264.85 | +2.6x |
| 2023 | $26,890.00 | 0.003719 BTC | $277.21 | +2.8x |
| 2024 | $65,000.00 | 0.001538 BTC | $114.68 | +1.1x |
| 2025 | $90,000.00 | 0.001111 BTC | $82.83 | -17.2% |
| 2026 \* | $84,000.00 | 0.001190 BTC | $88.74 | -11.3% |

\* 2026 is partial — average covers Jan 1 through today
<!-- BTC_RESULTS_END -->
