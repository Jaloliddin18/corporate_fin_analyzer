# 📊 Corporate Financial Health Analyzer

A powerful Streamlit web application for analyzing corporate financial health using the **Altman Z-Score** model with live industry benchmarking.

## 🌟 Features

- **Interactive Analysis**: Input financial data manually for custom company analysis
- **Quick Ticker Lookup**: Fetch real-time financial data from Yahoo Finance
- **Industry Benchmarking**: Compare against live data from industry peers
- **Custom Competitor Comparison**: Benchmark against your chosen competitors
- **Visual Analytics**: Comprehensive charts and graphs for financial insights
- **Risk Classification**: Automatic classification into Safe, Gray, or Distress zones

## 🚀 Live Demo

[View Live App on Streamlit Cloud](#) _(Add your deployment URL here)_

## 📋 Altman Z-Score Interpretation

- **🟢 Safe Zone (Z > 2.99)**: Low bankruptcy risk, strong financial health
- **🟡 Gray Zone (1.81 ≤ Z ≤ 2.99)**: Moderate risk, requires monitoring
- **🔴 Distress Zone (Z < 1.81)**: High bankruptcy risk, immediate action needed

## 🛠️ Installation

### Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/team10_project.git
   cd team10_project
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository: `YOUR_USERNAME/YOUR_REPO_NAME`
5. Set the main file path: `app.py`
6. Click **"Deploy"**

Your app will be live in a few minutes! 🎉

## 📊 Usage

### Mode 1: Interactive Analysis

1. Select "🏢 Interactive Analysis" from the sidebar
2. Enter company name and select industry
3. Input financial data (Total Assets, Current Assets, Liabilities, etc.)
4. Click "🚀 Analyze" to view results

### Mode 2: Quick Ticker Lookup

1. Select "🔍 Quick Ticker Lookup"
2. Enter a stock ticker symbol (e.g., AAPL, TSLA)
3. Click "🔍 Lookup" to fetch and analyze real-time data

### Mode 3: Example Analysis

1. Select "📝 Example Analysis"
2. Click "🎯 Run Example" to see a demo with sample data

### Mode 4: Custom Benchmark

1. Select "🎯 Custom Benchmark"
2. Enter your company's financial data
3. Input competitor ticker symbols (comma-separated)
4. Click "🎯 Analyze with Custom Benchmark"

## 🧮 Altman Z-Score Formula

```
Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5
```

Where:

- **X1** = Working Capital / Total Assets
- **X2** = Retained Earnings / Total Assets
- **X3** = EBIT / Total Assets
- **X4** = Market Value of Equity / Total Liabilities
- **X5** = Sales / Total Assets

## 📦 Dependencies

- `streamlit` - Web application framework
- `yfinance` - Financial data from Yahoo Finance
- `pandas` - Data manipulation and analysis
- `matplotlib` - Data visualization
- `seaborn` - Statistical data visualization
- `numpy` - Numerical computing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👥 Team

Team 10 - Corporate Financial Health Analysis Project

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This tool is for educational and analytical purposes. Always consult with financial professionals for investment decisions.
