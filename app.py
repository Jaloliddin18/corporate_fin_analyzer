"""
Corporate Financial Health Analyzer - Streamlit Web App
Team 10 Final Project

A user-friendly web interface for Altman Z-Score analysis with live benchmarking.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import io

# Page configuration
st.set_page_config(
    page_title="Financial Health Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .safe-zone { color: #28a745; font-weight: bold; }
    .gray-zone { color: #ffc107; font-weight: bold; }
    .distress-zone { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Industry ticker mappings
INDUSTRIES = {
    'Manufacturing': ['F', 'GM', 'CAT', 'DE', 'BA', 'GE', 'MMM', 'HON'],
    'Retail': ['WMT', 'TGT', 'COST', 'HD', 'LOW', 'AMZN', 'EBAY'],
    'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'ORCL'],
    'Healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'DHR', 'BMY'],
    'Food & Beverage': ['KO', 'PEP', 'MCD', 'SBUX', 'KHC', 'GIS', 'K', 'HSY'],
    'Transportation': ['UPS', 'FDX', 'UAL', 'DAL', 'AAL', 'LUV', 'NSC', 'UNP'],
    'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO'],
    'Finance': ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'SCHW'],
    'Consumer Goods': ['PG', 'KMB', 'CL', 'EL', 'NKE', 'LULU', 'TJX', 'ROST'],
    'Automotive': ['TSLA', 'F', 'GM', 'TM', 'HMC', 'STLA', 'RIVN'],
    'Telecommunications': ['T', 'VZ', 'TMUS', 'CMCSA', 'DIS', 'NFLX']
}


@st.cache_data(ttl=3600)
def fetch_financials(ticker):
    """Fetch quarterly financial data from Yahoo Finance with comprehensive field name alternatives."""
    try:
        company = yf.Ticker(ticker)
        bs = company.quarterly_balance_sheet.iloc[:, 0]
        inc = company.quarterly_financials.iloc[:, 0]
        
        # Helper function to try multiple field names
        def get_field(source, field_names, default=0):
            """Try multiple field name variations and return the first non-zero value found."""
            for field in field_names:
                value = source.get(field, None)
                if value is not None and value != 0:
                    return value, field
            return default, None
        
        # Try multiple field name variations for each variable
        total_assets, ta_field = get_field(bs, [
            'Total Assets', 'TotalAssets'
        ])
        
        current_assets, ca_field = get_field(bs, [
            'Current Assets', 'CurrentAssets'
        ])
        
        current_liabilities, cl_field = get_field(bs, [
            'Current Liabilities', 'CurrentLiabilities'
        ])
        
        retained_earnings, re_field = get_field(bs, [
            'Retained Earnings', 'RetainedEarnings', 'Accumulated Deficit'
        ])
        
        ebit, ebit_field = get_field(inc, [
            'EBIT', 'Operating Income', 'OperatingIncome', 
            'Earnings Before Interest And Taxes'
        ])
        
        total_liabilities, tl_field = get_field(bs, [
            'Total Liabilities Net Minority Interest', 
            'Total Liabilities', 'TotalLiabilities'
        ])
        
        market_value_equity, mve_field = get_field(bs, [
            'Common Stock Equity', 'Stockholders Equity', 
            'StockholdersEquity', 'Total Equity Gross Minority Interest'
        ])
        
        total_revenue, tr_field = get_field(inc, [
            'Total Revenue', 'TotalRevenue', 'Revenue'
        ])
        
        # Build data dictionary
        data = {
            'total_assets': total_assets,
            'current_assets': current_assets,
            'current_liabilities': current_liabilities,
            'retained_earnings': retained_earnings,
            'ebit': ebit,
            'total_liabilities': total_liabilities,
            'market_value_equity': market_value_equity,
            'total_revenue': total_revenue
        }
        
        # Build diagnostics dictionary
        diagnostics = {
            'total_assets': {'value': total_assets, 'field': ta_field, 'found': ta_field is not None},
            'current_assets': {'value': current_assets, 'field': ca_field, 'found': ca_field is not None},
            'current_liabilities': {'value': current_liabilities, 'field': cl_field, 'found': cl_field is not None},
            'retained_earnings': {'value': retained_earnings, 'field': re_field, 'found': re_field is not None},
            'ebit': {'value': ebit, 'field': ebit_field, 'found': ebit_field is not None},
            'total_liabilities': {'value': total_liabilities, 'field': tl_field, 'found': tl_field is not None},
            'market_value_equity': {'value': market_value_equity, 'field': mve_field, 'found': mve_field is not None},
            'total_revenue': {'value': total_revenue, 'field': tr_field, 'found': tr_field is not None}
        }
        
        # Check if critical fields are missing
        if total_assets == 0 or total_revenue == 0:
            return None, diagnostics
        
        return data, diagnostics
    except Exception as e:
        return None, {'error': str(e)}


def calculate_z_score(data):
    """Calculate Altman Z-Score from financial data."""
    df = pd.DataFrame([data])
    
    wc = df['current_assets'] - df['current_liabilities']
    df['x1'] = wc / df['total_assets']
    df['x2'] = df['retained_earnings'] / df['total_assets']
    df['x3'] = df['ebit'] / df['total_assets']
    df['x4'] = df['market_value_equity'] / df['total_liabilities'].replace(0, 1)
    df['x5'] = df['total_revenue'] / df['total_assets']
    
    df['z_score'] = (1.2 * df['x1'] + 1.4 * df['x2'] + 3.3 * df['x3'] + 
                     0.6 * df['x4'] + 1.0 * df['x5'])
    
    return df.iloc[0]


def get_risk_zone(z_score):
    """Classify financial health based on Altman Z-Score."""
    if z_score > 2.99:
        return 'Safe Zone', 'safe-zone', '🟢'
    elif z_score >= 1.81:
        return 'Gray Zone', 'gray-zone', '🟡'
    return 'Distress Zone', 'distress-zone', '🔴'


def display_data_diagnostics(diagnostics, ticker):
    """Display data quality diagnostics for fetched financial data."""
    st.subheader("📋 Data Quality Report")
    
    if 'error' in diagnostics:
        st.error(f"Error fetching data: {diagnostics['error']}")
        return
    
    # Field labels for display
    field_labels = {
        'total_assets': 'Total Assets',
        'current_assets': 'Current Assets',
        'current_liabilities': 'Current Liabilities',
        'retained_earnings': 'Retained Earnings',
        'ebit': 'EBIT',
        'total_liabilities': 'Total Liabilities',
        'market_value_equity': 'Market Value of Equity',
        'total_revenue': 'Total Revenue'
    }
    
    # Create diagnostic table
    diag_data = []
    missing_count = 0
    
    for key, label in field_labels.items():
        info = diagnostics[key]
        if info['found']:
            status = '✓ Found'
            status_color = '🟢'
            field_used = info['field']
        else:
            status = '✗ Missing'
            status_color = '🔴'
            field_used = 'N/A'
            missing_count += 1
        
        diag_data.append({
            'Field': label,
            'Status': f"{status_color} {status}",
            'Value': f"${info['value']:,.0f}" if info['value'] != 0 else "$0",
            'Field Name Used': field_used if field_used else 'N/A'
        })
    
    # Display table
    diag_df = pd.DataFrame(diag_data)
    st.dataframe(diag_df, use_container_width=True, hide_index=True)
    
    # Summary message
    if missing_count == 0:
        st.success(f"✓ All 8 required fields found for {ticker}")
    elif missing_count <= 2:
        st.warning(f"⚠ {missing_count} field(s) missing for {ticker}. Z-score may be less accurate.")
    else:
        st.error(f"✗ {missing_count} field(s) missing for {ticker}. Z-score calculation may be unreliable.")
    
    # Helpful tips
    if missing_count > 0:
        with st.expander("💡 Why are some fields missing?"):
            st.markdown("""
            **Common reasons for missing data:**
            - Company doesn't report certain metrics publicly
            - Different accounting standards or reporting formats
            - Recent IPO or limited financial history
            - Data not yet available for the most recent quarter
            
            **Suggestions:**
            - Try a different ticker symbol
            - Check if the company is publicly traded
            - Use a larger, more established company for more complete data
            """)


@st.cache_data(ttl=3600)
def get_industry_benchmark(industry, max_companies=8):
    """Fetch live benchmark data from industry companies."""
    tickers = INDUSTRIES.get(industry, INDUSTRIES['Manufacturing'])[:max_companies]
    
    z_scores = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"Fetching {ticker}...")
        result = fetch_financials(ticker)
        if result and result[0]:  # Check if data was fetched successfully
            data, _ = result  # Unpack tuple, ignore diagnostics for benchmark
            calc_result = calculate_z_score(data)
            if not np.isnan(calc_result['z_score']) and not np.isinf(calc_result['z_score']):
                z_scores.append(calc_result['z_score'])
        progress_bar.progress((i + 1) / len(tickers))
    
    progress_bar.empty()
    status_text.empty()
    
    if len(z_scores) < 3:
        st.warning(f"Only {len(z_scores)} companies fetched successfully")
    
    return {
        'industry': industry,
        'count': len(z_scores),
        'avg': np.mean(z_scores),
        'median': np.median(z_scores),
        'top_25': np.percentile(z_scores, 75),
        'bottom_25': np.percentile(z_scores, 25),
        'scores': z_scores
    }


def get_custom_benchmark(ticker_string):
    """Fetch benchmark data from user-specified competitor tickers."""
    tickers = [t.strip().upper() for t in ticker_string.split(',') if t.strip()]
    
    if not tickers:
        return None
    
    z_scores = []
    successful_tickers = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"Fetching {ticker}...")
        result = fetch_financials(ticker)
        if result and result[0]:  # Check if data was fetched successfully
            data, _ = result  # Unpack tuple, ignore diagnostics for benchmark
            calc_result = calculate_z_score(data)
            if not np.isnan(calc_result['z_score']) and not np.isinf(calc_result['z_score']):
                z_scores.append(calc_result['z_score'])
                successful_tickers.append(ticker)
        progress_bar.progress((i + 1) / len(tickers))
    
    progress_bar.empty()
    status_text.empty()
    
    if len(z_scores) < 2:
        st.error(f"Only {len(z_scores)} companies fetched. Need at least 2 for benchmark.")
        return None
    
    st.success(f"✓ Benchmark created from {len(z_scores)} companies: {', '.join(successful_tickers)}")
    
    return {
        'industry': 'Custom Comparison',
        'count': len(z_scores),
        'companies': successful_tickers,
        'avg': np.mean(z_scores),
        'median': np.median(z_scores),
        'top_25': np.percentile(z_scores, 75),
        'bottom_25': np.percentile(z_scores, 25),
        'scores': z_scores
    }


def create_visualization(company_name, result, benchmark):
    """Create visual analysis charts."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
    
    z = result['z_score']
    color = '#28a745' if z > 2.99 else '#ffc107' if z >= 1.81 else '#dc3545'
    
    # Chart 1: Z-Score gauge
    ax1.barh(['Your Company'], [z], color=color, alpha=0.7, edgecolor='black', linewidth=2)
    ax1.axvline(2.99, color='green', linestyle='--', label='Safe Zone (>2.99)', linewidth=2)
    ax1.axvline(1.81, color='orange', linestyle='--', label='Gray Zone (1.81-2.99)', linewidth=2)
    ax1.set_xlabel('Z-Score', fontsize=12, fontweight='bold')
    ax1.set_title(f'{company_name} - Altman Z-Score', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    
    # Chart 2: Industry comparison
    companies = ['You', 'Avg', 'Top 25%', 'Bottom 25%']
    scores = [z, benchmark['avg'], benchmark['top_25'], benchmark['bottom_25']]
    colors_comp = [color, '#6c757d', '#28a745', '#dc3545']
    ax2.bar(companies, scores, color=colors_comp, alpha=0.7, edgecolor='black', linewidth=2)
    ax2.set_ylabel('Z-Score', fontsize=12, fontweight='bold')
    ax2.set_title('Industry Comparison', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Chart 3: Component breakdown
    components = ['X1\nWorking\nCapital', 'X2\nRetained\nEarnings', 
                  'X3\nEBIT', 'X4\nMarket\nValue', 'X5\nSales']
    contributions = [1.2*result['x1'], 1.4*result['x2'], 3.3*result['x3'], 
                     0.6*result['x4'], 1.0*result['x5']]
    ax3.bar(components, contributions, color='steelblue', alpha=0.7, edgecolor='black', linewidth=2)
    ax3.set_ylabel('Contribution to Z-Score', fontsize=12, fontweight='bold')
    ax3.set_title('Component Contributions', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Chart 4: Industry distribution
    ax4.hist(benchmark['scores'], bins=15, color='lightblue', edgecolor='black', alpha=0.7)
    ax4.axvline(z, color=color, linestyle='--', linewidth=3, label=f'Your Score: {z:,.0f}')
    ax4.axvline(benchmark['avg'], color='gray', linestyle=':', linewidth=2, label=f'Industry Avg: {benchmark["avg"]:,.0f}')
    ax4.set_xlabel('Z-Score', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax4.set_title('Industry Z-Score Distribution', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def display_analysis(company_name, result, benchmark):
    """Display comprehensive analysis results."""
    z = result['z_score']
    zone, zone_class, emoji = get_risk_zone(z)
    
    # Header
    st.markdown(f"<h2 style='text-align: center;'>{emoji} Financial Health Report: {company_name}</h2>", 
                unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>Industry: {benchmark['industry']}</p>", 
                unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Z-Score", f"{z:,.0f}")
    with col2:
        st.metric("Classification", zone)
    with col3:
        st.metric("Industry Avg", f"{benchmark['avg']:,.0f}")
    with col4:
        percentile = "Top 25%" if z >= benchmark['top_25'] else \
                     "Above Avg" if z >= benchmark['median'] else \
                     "Below Avg" if z >= benchmark['bottom_25'] else "Bottom 25%"
        st.metric("Percentile", percentile)
    
    # Component breakdown
    st.subheader("📊 Component Breakdown")
    breakdown_df = pd.DataFrame({
        'Component': [
            'X1: Working Capital / Total Assets',
            'X2: Retained Earnings / Total Assets',
            'X3: EBIT / Total Assets',
            'X4: Market Value / Total Liabilities',
            'X5: Sales / Total Assets'
        ],
        'Ratio': [result['x1'], result['x2'], result['x3'], result['x4'], result['x5']],
        'Weight': [1.2, 1.4, 3.3, 0.6, 1.0],
        'Contribution': [
            1.2*result['x1'], 1.4*result['x2'], 3.3*result['x3'],
            0.6*result['x4'], 1.0*result['x5']
        ]
    })
    st.dataframe(breakdown_df.style.format({
        'Ratio': '{:,.0f}',
        'Weight': '{:,.0f}',
        'Contribution': '{:,.0f}'
    }), use_container_width=True)
    
    # Visualization
    st.subheader("📈 Visual Analysis")
    fig = create_visualization(company_name, result, benchmark)
    st.pyplot(fig)
    
    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 Download Chart",
        data=buf,
        file_name=f"financial_health_{company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.png",
        mime="image/png"
    )
    
    # Recommendations
    st.subheader("💡 Recommendations")
    if z > 2.99:
        st.success("✓ Excellent financial health. Focus on strategic growth opportunities.")
    elif z >= 1.81:
        st.warning("⚠ Moderate risk detected. Monitor liquidity and profitability closely.")
    else:
        st.error("✗ High distress risk. Immediate action needed to improve financial position.")


# Main App
def main():
    st.markdown("<div class='main-header'>📊 Corporate Financial Health Analyzer</div>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Altman Z-Score Analysis with Live Industry Benchmarking</p>", 
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Analysis Mode")
    mode = st.sidebar.radio(
        "Select Mode:",
        ["🏢 Interactive Analysis", "🔍 Quick Ticker Lookup", 
         "📝 Example Analysis", "🎯 Custom Benchmark"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About This Tool:**
    
    Uses the Altman Z-Score model to assess corporate financial health and bankruptcy risk.
    
    **Z-Score Ranges:**
    - 🟢 > 2.99: Safe Zone
    - 🟡 1.81-2.99: Gray Zone
    - 🔴 < 1.81: Distress Zone
    """)
    
    # Mode 1: Interactive Analysis
    if mode == "🏢 Interactive Analysis":
        st.header("Interactive Company Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="Enter company name")
            industry = st.selectbox("Industry", list(INDUSTRIES.keys()))
        
        with col2:
            st.markdown("**Enter Financial Data** (in same currency)")
            col_a, col_b = st.columns(2)
            
            with col_a:
                total_assets = st.number_input("Total Assets ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 2,000,000", format="%.0f")
                current_assets = st.number_input("Current Assets ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 1,000,000", format="%.0f")
                current_liabilities = st.number_input("Current Liabilities ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 300,000", format="%.0f")
                retained_earnings = st.number_input("Retained Earnings ($)", min_value=-1e12, max_value=1e12, value=None, placeholder="e.g., 800,000", format="%.0f")
            
            with col_b:
                ebit = st.number_input("EBIT ($)", min_value=-1e12, max_value=1e12, value=None, placeholder="e.g., 500,000", format="%.0f")
                total_liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 500,000", format="%.0f")
                market_value = st.number_input("Market Value of Equity ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 2,500,000", format="%.0f")
                revenue = st.number_input("Total Revenue ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 700,000", format="%.0f")
        
        if st.button("🚀 Analyze", type="primary", use_container_width=True):
            # Validation
            if not company_name:
                st.error("Please enter a company name")
            elif any(v is None for v in [total_assets, current_assets, current_liabilities, 
                                          retained_earnings, ebit, total_liabilities, 
                                          market_value, revenue]):
                st.error("Please fill in all financial data fields")
            else:
                with st.spinner("Analyzing..."):
                    data = {
                        'total_assets': total_assets,
                        'current_assets': current_assets,
                        'current_liabilities': current_liabilities,
                        'retained_earnings': retained_earnings,
                        'ebit': ebit,
                        'total_liabilities': total_liabilities,
                        'market_value_equity': market_value,
                        'total_revenue': revenue
                    }
                
                    result = calculate_z_score(data)
                    benchmark = get_industry_benchmark(industry)
                    
                    display_analysis(company_name, result, benchmark)
    
    # Mode 2: Quick Ticker Lookup
    elif mode == "🔍 Quick Ticker Lookup":
        st.header("Quick Ticker Analysis")
        
        ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL, TSLA)", "AAPL").upper()
        
        if st.button("🔍 Lookup", type="primary"):
            with st.spinner(f"Fetching data for {ticker}..."):
                result = fetch_financials(ticker)
                
                if result and result[0]:  # Check if data was fetched successfully
                    data, diagnostics = result  # Unpack tuple
                    calc_result = calculate_z_score(data)
                    z = calc_result['z_score']
                    zone, _, emoji = get_risk_zone(z)
                    
                    st.success(f"✓ Data fetched successfully for {ticker}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Z-Score", f"{z:,.2f}")
                    with col2:
                        st.metric("Status", f"{emoji} {zone}")
                    with col3:
                        st.metric("Total Assets", f"${data['total_assets']:,.0f}")
                    
                    st.subheader("Component Scores")
                    comp_col1, comp_col2, comp_col3, comp_col4, comp_col5 = st.columns(5)
                    with comp_col1:
                        st.metric("X1", f"{calc_result['x1']:.3f}")
                    with comp_col2:
                        st.metric("X2", f"{calc_result['x2']:.3f}")
                    with comp_col3:
                        st.metric("X3", f"{calc_result['x3']:.3f}")
                    with comp_col4:
                        st.metric("X4", f"{calc_result['x4']:.3f}")
                    with comp_col5:
                        st.metric("X5", f"{calc_result['x5']:.3f}")
                    
                    # Display data quality diagnostics
                    st.markdown("---")
                    display_data_diagnostics(diagnostics, ticker)
                else:
                    st.error(f"❌ Could not fetch data for {ticker}. Please check the ticker symbol.")
    
    # Mode 3: Example Analysis
    elif mode == "📝 Example Analysis":
        st.header("Example Analysis Demo")
        st.info("Click below to run analysis with predefined sample data")
        
        if st.button("🎯 Run Example", type="primary", use_container_width=True):
            with st.spinner("Running example analysis..."):
                sample_data = {
                    'total_assets': 2000000,
                    'current_assets': 1000000,
                    'current_liabilities': 300000,
                    'retained_earnings': 800000,
                    'ebit': 500000,
                    'total_liabilities': 500000,
                    'market_value_equity': 2500000,
                    'total_revenue': 700000
                }
                
                result = calculate_z_score(sample_data)
                benchmark = get_industry_benchmark('Manufacturing')
                
                display_analysis("Example Company", result, benchmark)
    
    # Mode 4: Custom Benchmark
    else:
        st.header("Custom Competitor Benchmark")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="Enter company name", key="custom_name")
            st.markdown("**Competitor Tickers**")
            ticker_input = st.text_area(
                "Enter comma-separated tickers",
                placeholder="e.g., AAPL, MSFT, GOOGL, META",
                help="Example: AAPL, MSFT, GOOGL"
            )
        
        with col2:
            st.markdown("**Enter Financial Data**")
            col_a, col_b = st.columns(2)
            
            with col_a:
                total_assets = st.number_input("Total Assets ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 2,000,000", format="%.0f", key="custom_ta")
                current_assets = st.number_input("Current Assets ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 1,000,000", format="%.0f", key="custom_ca")
                current_liabilities = st.number_input("Current Liabilities ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 300,000", format="%.0f", key="custom_cl")
                retained_earnings = st.number_input("Retained Earnings ($)", min_value=-1e12, max_value=1e12, value=None, placeholder="e.g., 800,000", format="%.0f", key="custom_re")
            
            with col_b:
                ebit = st.number_input("EBIT ($)", min_value=-1e12, max_value=1e12, value=None, placeholder="e.g., 500,000", format="%.0f", key="custom_ebit")
                total_liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 500,000", format="%.0f", key="custom_tl")
                market_value = st.number_input("Market Value of Equity ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 2,500,000", format="%.0f", key="custom_mv")
                revenue = st.number_input("Total Revenue ($)", min_value=0.0, max_value=1e12, value=None, placeholder="e.g., 700,000", format="%.0f", key="custom_rev")
        
        if st.button("🎯 Analyze with Custom Benchmark", type="primary", use_container_width=True):
            # Validation
            if not company_name:
                st.error("Please enter a company name")
            elif not ticker_input.strip():
                st.error("Please enter at least one competitor ticker")
            elif any(v is None for v in [total_assets, current_assets, current_liabilities, 
                                          retained_earnings, ebit, total_liabilities, 
                                          market_value, revenue]):
                st.error("Please fill in all financial data fields")
            else:
                with st.spinner("Analyzing..."):
                    data = {
                        'total_assets': total_assets,
                        'current_assets': current_assets,
                        'current_liabilities': current_liabilities,
                        'retained_earnings': retained_earnings,
                        'ebit': ebit,
                        'total_liabilities': total_liabilities,
                        'market_value_equity': market_value,
                        'total_revenue': revenue
                    }
                    
                    result = calculate_z_score(data)
                    benchmark = get_custom_benchmark(ticker_input)
                    
                    if benchmark:
                        display_analysis(company_name, result, benchmark)


if __name__ == "__main__":
    main()
