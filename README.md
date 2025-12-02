# Corporate Financial Health Analyzer

A powerful Streamlit web application for analyzing corporate financial health using the **Altman Z-Score** model with live industry benchmarking.

## Features

- **Interactive Analysis**: Input financial data manually for custom company analysis
- **Quick Ticker Lookup**: Fetch real-time financial data from Yahoo Finance
- **Industry Benchmarking**: Compare against live data from industry peers
- **Custom Competitor Comparison**: Benchmark against your chosen competitors
- **Visual Analytics**: Comprehensive charts and graphs for financial insights
- **Risk Classification**: Automatic classification into Safe, Gray, or Distress zones

## 📋 Altman Z-Score Interpretation

- **🟢 Safe Zone (Z > 2.99)**: Low bankruptcy risk, strong financial health
- **🟡 Gray Zone (1.81 ≤ Z ≤ 2.99)**: Moderate risk, requires monitoring
- **🔴 Distress Zone (Z < 1.81)**: High bankruptcy risk, immediate action needed

### Mode 1: Interactive Analysis

1. Select "🏢 Interactive Analysis" from the sidebar
2. Enter company name and select industry
3. Input financial data (Total Assets, Current Assets, Liabilities, etc.)
4. Click " Analyze" to view results

### Mode 2: Quick Ticker Lookup

1. Select " Quick Ticker Lookup"
2. Enter a stock ticker symbol (e.g., AAPL, TSLA)
3. Click " Lookup" to fetch and analyze real-time data

### Mode 3: Example Analysis

1. Select " Example Analysis"
2. Click " Run Example" to see a demo with sample data

### Mode 4: Custom Benchmark

1. Select " Custom Benchmark"
2. Enter your company's financial data
3. Input competitor ticker symbols (comma-separated)
4. Click " Analyze with Custom Benchmark"

## Altman Z-Score Formula

```
Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5
```

Where:

- **X1** = Working Capital / Total Assets
- **X2** = Retained Earnings / Total Assets
- **X3** = EBIT / Total Assets
- **X4** = Market Value of Equity / Total Liabilities
- **X5** = Sales / Total Assets

## Dependencies

- `streamlit` - Web application framework
- `yfinance` - Financial data from Yahoo Finance
- `pandas` - Data manipulation and analysis
- `matplotlib` - Data visualization
- `seaborn` - Statistical data visualization
- `numpy` - Numerical computing
