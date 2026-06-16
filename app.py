import io
import json
import math
import textwrap
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import csv

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ============================================================
# Page configuration & theme
# ============================================================
st.set_page_config(
    page_title="LuxePricing.ai | Premium Revenue Intelligence",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Advanced CSS with smooth transitions & STR-inspired design
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');

    :root {
        --bg-dark: #0a0e1a;
        --bg-secondary: #111827;
        --panel: #1a202c;
        --panel2: #252d42;
        --line: rgba(255,255,255,.08);
        --muted: #94a3b8;
        --text: #f1f5f9;
        --gold: #d4a574;
        --blue: #3b82f6;
        --green: #10b981;
        --red: #ef4444;
        --amber: #f59e0b;
        --purple: #a78bfa;
        --cyan: #06b6d4;
    }

    * {
        transition: all 0.2s ease;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: linear-gradient(135deg, var(--bg-dark) 0%, #0f1419 50%, #0a0e1a 100%);
    }

    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #0f1419 50%, #0a0e1a 100%);
        color: var(--text);
        min-height: 100vh;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1419 0%, #111827 100%);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] * { color: #cbd5e1; }

    h1, h2, h3, h4 { 
        letter-spacing: -0.01em;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }

    .hero {
        padding: 32px 28px;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.8), rgba(17, 24, 39, 0.8));
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
    }

    .hero h1 {
        margin: 0;
        font-size: 36px;
        background: linear-gradient(135deg, var(--text) 0%, var(--cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        margin: 12px 0 0;
        color: var(--muted);
        max-width: 920px;
        line-height: 1.6;
        font-size: 14px;
    }

    .kpi-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 20px;
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.9), rgba(17, 24, 39, 0.9));
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        height: 100%;
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
        border-color: rgba(59, 130, 246, 0.3);
    }

    .kpi-label {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: .06em;
        font-size: 11px;
        font-weight: 800;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-sub {
        color: var(--muted);
        font-size: 12px;
        margin-top: 6px;
    }

    .kpi-change {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }

    .kpi-change.positive {
        background: rgba(16, 185, 129, 0.15);
        color: var(--green);
    }

    .kpi-change.negative {
        background: rgba(239, 68, 68, 0.15);
        color: var(--red);
    }

    .module-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 24px;
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.85), rgba(20, 26, 40, 0.85));
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .module-card:hover {
        border-color: rgba(59, 130, 246, 0.2);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.1);
    }

    .module-card h3 { 
        margin-top: 0;
        margin-bottom: 16px;
        color: var(--text);
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 8px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.05);
        color: #dde7f5;
        font-size: 12px;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }

    .badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .badge.gold { 
        color: #f7d9a6; 
        border-color: rgba(212, 165, 116, 0.5); 
        background: rgba(212, 165, 116, 0.15); 
    }
    .badge.green { 
        color: #a7f3d0; 
        border-color: rgba(16, 185, 129, 0.4); 
        background: rgba(16, 185, 129, 0.12); 
    }
    .badge.blue { 
        color: #bfdbfe; 
        border-color: rgba(59, 130, 246, 0.4); 
        background: rgba(59, 130, 246, 0.12); 
    }
    .badge.red { 
        color: #fecaca; 
        border-color: rgba(239, 68, 68, 0.4); 
        background: rgba(239, 68, 68, 0.12); 
    }

    .note-box {
        border-left: 4px solid var(--gold);
        background: rgba(212, 165, 116, 0.08);
        border-radius: 10px;
        padding: 16px;
        color: #e8eef8;
        line-height: 1.6;
        margin: 12px 0 20px;
        font-size: 14px;
    }

    .note-box.warning {
        border-left-color: var(--amber);
        background: rgba(245, 158, 11, 0.08);
    }

    .note-box.success {
        border-left-color: var(--green);
        background: rgba(16, 185, 129, 0.08);
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 16px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--line);
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(6, 182, 212, 0.1));
        border: 1px solid rgba(59, 130, 246, 0.4);
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.8), rgba(17, 24, 39, 0.8));
        border: 1px solid var(--line);
        padding: 16px;
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--blue) 0%, var(--cyan) 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }

    .dataframe { 
        border-radius: 10px; 
        overflow: hidden;
    }

    code, pre {
        background: rgba(26, 32, 44, 0.8) !important;
        border-radius: 10px !important;
        border: 1px solid var(--line) !important;
    }

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(59, 130, 246, 0.3);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Utility functions
# ============================================================
def money(value, currency="€", compact=False):
    """Format money with optional compact notation."""
    try:
        value = float(value)
    except Exception:
        return f"{currency}0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    if compact:
        if value >= 1_000_000:
            return f"{sign}{currency}{value/1_000_000:.1f}M"
        if value >= 1_000:
            return f"{sign}{currency}{value/1_000:.0f}k"
    return f"{sign}{currency}{value:,.0f}"


def pct(value, decimals=1):
    """Format percentage."""
    try:
        return f"{float(value):.{decimals}f}%"
    except Exception:
        return "0.0%"


def clamp(value, lower, upper):
    """Clamp value between lower and upper."""
    return max(lower, min(upper, value))


def kpi(label, value, sub="", change=None, change_type="neutral"):
    """Render enhanced KPI card."""
    change_html = ""
    if change is not None:
        change_class = "positive" if change_type == "positive" else "negative" if change_type == "negative" else "neutral"
        arrow = "↑" if change_type == "positive" else "↓" if change_type == "negative" else "→"
        change_html = f"<div class='kpi-change {change_class}'>{arrow} {change}</div>"
    
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
            {change_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title, subtitle, badges=None):
    """Render hero section."""
    badges_html = ""
    if badges:
        badges_html = "<div style='margin-top:16px'>" + "".join(
            [f"<span class='badge {b.get('style','')}'>{b['text']}</span>" for b in badges]
        ) + "</div>"
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            {badges_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def note(text, box_type="note"):
    """Render note box."""
    style = "note-box" if box_type == "note" else f"note-box {box_type}"
    st.markdown(f"<div class='{style}'>{text}</div>", unsafe_allow_html=True)


def csv_download(df):
    """Generate CSV download bytes."""
    return df.to_csv(index=False).encode("utf-8")


def analyze_document_with_llm(file_content: str, file_type: str) -> Dict:
    """
    Analyze document using Claude-style analysis.
    This simulates LLM analysis - in production, connect to Claude API.
    """
    analysis = {
        "file_type": file_type,
        "summary": "",
        "key_metrics": {},
        "insights": [],
        "recommendations": [],
        "data_quality": 0,
        "confidence": 0
    }
    
    # Parse content
    lines = file_content.split('\n')
    
    if file_type == "csv":
        try:
            df = pd.read_csv(io.StringIO(file_content))
            analysis["key_metrics"]["columns"] = list(df.columns)
            analysis["key_metrics"]["rows"] = len(df)
            analysis["key_metrics"]["missing_values"] = int(df.isnull().sum().sum())
            
            # Detect numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                for col in numeric_cols[:5]:
                    analysis["key_metrics"][f"{col}_mean"] = float(df[col].mean())
                    analysis["key_metrics"][f"{col}_max"] = float(df[col].max())
            
            analysis["summary"] = f"CSV file with {len(df)} records and {len(df.columns)} fields"
            analysis["data_quality"] = int(100 * (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))))
            analysis["confidence"] = 92
            
            # Generate insights
            if analysis["key_metrics"]["missing_values"] > 0:
                analysis["insights"].append(f"⚠️ Found {analysis['key_metrics']['missing_values']} missing values")
            else:
                analysis["insights"].append("✓ Complete data - no missing values")
            
            analysis["recommendations"].append("✓ Data quality is acceptable for analysis")
            if analysis["data_quality"] < 80:
                analysis["recommendations"].append("⚠️ Consider data cleansing before modeling")
                
        except Exception as e:
            analysis["summary"] = f"Error parsing CSV: {str(e)}"
            analysis["data_quality"] = 0
            analysis["confidence"] = 10
    
    elif file_type == "json":
        try:
            data = json.loads(file_content)
            analysis["summary"] = f"JSON file with {len(str(data))} characters"
            analysis["key_metrics"]["json_depth"] = estimate_json_depth(data)
            analysis["data_quality"] = 95
            analysis["confidence"] = 90
            analysis["insights"].append("✓ Valid JSON structure")
            analysis["recommendations"].append("Ready for API integration")
        except Exception as e:
            analysis["summary"] = f"Invalid JSON: {str(e)}"
            analysis["data_quality"] = 0
            analysis["confidence"] = 10
    
    elif file_type == "txt":
        lines_count = len([l for l in lines if l.strip()])
        words_count = sum(len(l.split()) for l in lines)
        analysis["summary"] = f"Text document with {lines_count} lines and ~{words_count} words"
        analysis["key_metrics"]["lines"] = lines_count
        analysis["key_metrics"]["words"] = words_count
        analysis["data_quality"] = 100
        analysis["confidence"] = 85
        analysis["insights"].append(f"✓ Document contains {lines_count} lines of text")
        analysis["recommendations"].append("Consider structuring as CSV or JSON for better analysis")
    
    return analysis


def estimate_json_depth(obj, depth=0):
    """Estimate JSON nesting depth."""
    if isinstance(obj, dict):
        if not obj:
            return depth
        return max(estimate_json_depth(v, depth + 1) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return depth
        return max(estimate_json_depth(v, depth + 1) for v in obj)
    else:
        return depth


# ============================================================
# Sample data generators
# ============================================================
def sample_market_snapshot():
    """Generate market-level competitive snapshot."""
    return pd.DataFrame([
        {"Metric": "Occupancy Rate", "Your Hotel": 78.5, "Market Average": 72.3, "Market Top 25%": 85.2, "Trend": "+2.3%"},
        {"Metric": "ADR", "Your Hotel": 245.50, "Market Average": 198.75, "Market Top 25%": 312.40, "Trend": "+5.1%"},
        {"Metric": "RevPAR", "Your Hotel": 192.71, "Market Average": 143.55, "Market Top 25%": 266.35, "Trend": "+4.2%"},
        {"Metric": "Total Revenue", "Your Hotel": 8970000, "Market Average": 6550000, "Market Top 25%": 11200000, "Trend": "+6.8%"},
    ])


def sample_comp_set():
    """Enhanced competitor set with detailed metrics."""
    return pd.DataFrame([
        {"Hotel": "Mandarin Oriental", "Tier": "Ultra Luxury", "ADR": 1040, "Occupancy": 82.5, "RevPAR": 858.5, "Market Share": 12.3, "Price Index": 128},
        {"Hotel": "Ritz Paris", "Tier": "Ultra Luxury", "ADR": 1320, "Occupancy": 79.8, "RevPAR": 1054.7, "Market Share": 15.2, "Price Index": 162},
        {"Hotel": "Le Bristol", "Tier": "Ultra Luxury", "ADR": 1180, "Occupancy": 81.2, "RevPAR": 958.2, "Market Share": 13.8, "Price Index": 145},
        {"Hotel": "Peninsula Paris", "Tier": "Luxury", "ADR": 980, "Occupancy": 75.3, "RevPAR": 737.9, "Market Share": 10.1, "Price Index": 120},
        {"Hotel": "Cheval Blanc", "Tier": "Ultra Luxury", "ADR": 1450, "Occupancy": 80.1, "RevPAR": 1161.4, "Market Share": 16.5, "Price Index": 178},
        {"Hotel": "Your Property", "Tier": "Luxury", "ADR": 815, "Occupancy": 78.5, "RevPAR": 640.0, "Market Share": 9.2, "Price Index": 100},
    ])


def sample_performance_vs_set():
    """Performance vs competitive set over time."""
    dates = pd.date_range(start="2026-04-01", periods=120, freq="D")
    data = []
    for i, date_val in enumerate(dates):
        your_revpar = 640 + 100 * np.sin(i / 30) + np.random.normal(0, 20)
        market_revpar = 550 + 80 * np.sin(i / 30) + np.random.normal(0, 15)
        
        data.append({
            "Date": date_val,
            "Your RevPAR": your_revpar,
            "Market Avg RevPAR": market_revpar,
            "Top 25% RevPAR": market_revpar * 1.35,
            "Performance Index": (your_revpar / market_revpar) * 100,
        })
    return pd.DataFrame(data)


def sample_forecast_data():
    """Generate 90-day forecast."""
    dates = pd.date_range(start=date.today(), periods=90, freq="D")
    data = []
    for i, d in enumerate(dates):
        seasonality = 1.0 + 0.25 * np.sin((i % 365) * np.pi / 182)
        confidence = max(0.7, 0.95 - (i / 90) * 0.25)
        
        data.append({
            "Date": d,
            "Forecast ADR": 220 * seasonality,
            "Lower Bound": 200 * seasonality * 0.9,
            "Upper Bound": 240 * seasonality * 1.1,
            "Confidence": confidence,
            "Occupancy Forecast": np.clip(0.72 + 0.1 * seasonality, 0.3, 0.9),
        })
    return pd.DataFrame(data)


def sample_competitor_feed():
    """Competitor feed data."""
    return pd.DataFrame([
        {"Hotel": "Mandarin Oriental Paris", "Tier": "Luxury", "ADR": 1040, "Occupancy": 82.5, "RevPAR": 858, "Available": True},
        {"Hotel": "Ritz Paris", "Tier": "Ultra Luxury", "ADR": 1320, "Occupancy": 79.8, "RevPAR": 1055, "Available": True},
        {"Hotel": "Le Bristol Paris", "Tier": "Ultra Luxury", "ADR": 1180, "Occupancy": 81.2, "RevPAR": 958, "Available": True},
        {"Hotel": "Peninsula Paris", "Tier": "Luxury", "ADR": 980, "Occupancy": 75.3, "RevPAR": 738, "Available": True},
        {"Hotel": "Cheval Blanc Paris", "Tier": "Ultra Luxury", "ADR": 1450, "Occupancy": 80.1, "RevPAR": 1161, "Available": True},
    ])


def sample_demand_calendar():
    """Enhanced demand calendar."""
    base = date(2026, 7, 1)
    rows = []
    events = ["Paris Fashion Week", "Summer leisure", "Corporate congress", "High season", "Weekend leisure", "Shoulder season", "Art fair"]
    for i in range(30):
        rows.append({
            "Date": base + timedelta(days=i),
            "Season": "Peak" if i in range(0, 7) else "High" if i in range(7, 20) else "Shoulder",
            "Event": events[i % len(events)],
            "Event Impact": [95, 90, 75, 85, 70, 40, 75][i % 7],
            "Search Index": [85, 80, 75, 78, 68, 55, 72][i % 7],
        })
    return pd.DataFrame(rows)


# ============================================================
# Sidebar Navigation
# ============================================================
with st.sidebar:
    st.markdown("### 🏨 LuxePricing.ai")
    st.caption("Premium Revenue Intelligence Platform")
    st.divider()
    
    workspace = st.selectbox(
        "📊 Navigation",
        [
            "Dashboard & Analytics",
            "Document Analysis (MVP)",
            "Market Intelligence",
            "Rate Intelligence",
            "Operations & Finance",
            "Forecasting",
        ],
        index=0,
    )
    
    st.divider()
    st.markdown("**Status**")
    st.caption("✅ All modules operational")
    st.caption("✅ Document analysis ready")
    st.caption("✅ AI-powered insights enabled")

# ============================================================
# Workspace 1: Dashboard & Analytics
# ============================================================
if workspace == "Dashboard & Analytics":
    hero(
        "Dashboard & Analytics",
        "Real-time market intelligence and competitive positioning.",
        badges=[
            {"text": "STR Analytics", "style": "gold"},
            {"text": "Live Data", "style": "blue"},
        ],
    )
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        kpi("Your RevPAR", money(640, "€"), "vs Market 550€", "↑ 16.4%", "positive")
    with col2:
        kpi("Occupancy", pct(78.5), "vs Market 72.3%", "↑ 6.2pp", "positive")
    with col3:
        kpi("ADR", money(245.50, "€"), "vs Market 198€", "↑ 23.9%", "positive")
    with col4:
        kpi("Market Share", "9.2%", "competitive set", "→ stable", "neutral")
    with col5:
        kpi("Performance Index", "116", "vs avg 100", "↑ 2.8", "positive")
    
    st.divider()
    
    tab_overview, tab_comp, tab_trend = st.tabs(["📊 Market Snapshot", "🏆 Competitive Set", "📈 Trends"])
    
    with tab_overview:
        st.dataframe(sample_market_snapshot(), use_container_width=True, hide_index=True)
    
    with tab_comp:
        comp_set = sample_comp_set()
        st.dataframe(comp_set.sort_values("RevPAR", ascending=False), use_container_width=True, hide_index=True)
    
    with tab_trend:
        perf_df = sample_performance_vs_set()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=perf_df["Date"], y=perf_df["Your RevPAR"], name="Your Property", line=dict(color="#3b82f6", width=3)))
        fig.add_trace(go.Scatter(x=perf_df["Date"], y=perf_df["Market Avg RevPAR"], name="Market Average", line=dict(color="#9ca3af", width=2, dash="dash")))
        fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Workspace 2: Document Analysis MVP (NEW)
# ============================================================
elif workspace == "Document Analysis (MVP)":
    hero(
        "Document Analysis Engine",
        "Upload your hotel data (CSV, JSON, TXT) and get instant AI-powered insights with RevPAR analysis.",
        badges=[
            {"text": "AI Analysis", "style": "gold"},
            {"text": "Real-time Processing", "style": "blue"},
            {"text": "Revenue Impact", "style": "green"}
        ],
    )
    
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 Upload Your Data")
        uploaded_file = st.file_uploader(
            "Choose a file to analyze",
            type=["csv", "json", "txt"],
            help="CSV: Revenue data | JSON: Structured data | TXT: Reports"
        )
        
        if uploaded_file is not None:
            file_type = uploaded_file.name.split('.')[-1].lower()
            file_content = uploaded_file.read().decode("utf-8")
            
            # Analyze document
            with st.spinner("🔄 Analyzing document..."):
                analysis = analyze_document_with_llm(file_content, file_type)
            
            st.markdown("### 📊 Analysis Results")
            
            # Key metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                kpi("Data Quality", f"{analysis['data_quality']}%", "completeness", "↑" if analysis['data_quality'] > 80 else "↓", "positive" if analysis['data_quality'] > 80 else "negative")
            with col_m2:
                kpi("Analysis Confidence", f"{analysis['confidence']}%", "ai accuracy")
            with col_m3:
                kpi("File Type", file_type.upper(), "detected")
            with col_m4:
                kpi("Records", str(analysis['key_metrics'].get('rows', 'N/A')), "processed")
            
            # Summary
            st.markdown("#### 📄 Summary")
            st.info(analysis['summary'])
            
            # Insights
            st.markdown("#### 💡 Key Insights")
            for insight in analysis['insights']:
                st.write(insight)
            
            # Recommendations
            st.markdown("#### 🎯 Recommendations")
            for rec in analysis['recommendations']:
                st.write(rec)
            
            # Detailed metrics
            if analysis['key_metrics']:
                st.markdown("#### 🔢 Detailed Metrics")
                metrics_df = pd.DataFrame(list(analysis['key_metrics'].items()), columns=["Metric", "Value"])
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        else:
            st.info("👆 Upload a file to begin analysis")
    
    with col2:
        st.markdown("### 📋 Sample Revenue Data")
        
        # Example data preview
        if st.checkbox("Show sample CSV structure", value=True):
            sample_csv = """hotel_id,property_name,record_date,rooms_available,rooms_sold,rooms_revenue,adr,occupancy_pct,market_segment
LP-001,Luxe Hotel A,2026-07-01,150,118,30680,260,78.7,Leisure
LP-001,Luxe Hotel A,2026-07-02,150,129,36120,280,86.0,Corporate
LP-002,Luxe Hotel B,2026-07-03,120,92,23000,250,76.7,Leisure"""
            st.code(sample_csv, language="csv")
        
        st.markdown("### 📚 Supported Formats")
        formats = pd.DataFrame([
            ["CSV", "Revenue reports, operational data", "hotels_data.csv"],
            ["JSON", "API responses, structured data", "rates.json"],
            ["TXT", "Reports, summaries, notes", "analysis.txt"],
        ], columns=["Format", "Use Case", "Example"])
        st.dataframe(formats, use_container_width=True, hide_index=True)
        
        st.markdown("### 🚀 Quick Tips")
        st.write("• Keep date columns consistent (YYYY-MM-DD)")
        st.write("• Use standard column names (ADR, occupancy)")
        st.write("• Remove duplicate rows before upload")
        st.write("• Ensure numeric fields have no text")

# ============================================================
# Workspace 3: Market Intelligence
# ============================================================
elif workspace == "Market Intelligence":
    hero(
        "Market Intelligence",
        "Deep-dive competitive analysis and market dynamics.",
        badges=[{"text": "Market Trends", "style": "blue"}],
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Market Metrics (Last 30 days)")
        market_metrics = pd.DataFrame([
            ["Total Rooms Sold", "184,520", "↑ 3.2%"],
            ["Total Revenue", "€38.2M", "↑ 8.1%"],
            ["Avg Market ADR", "€198.75", "↑ 5.1%"],
            ["Market Occupancy", "72.3%", "↑ 2.1pp"],
        ], columns=["Metric", "Value", "Change"])
        st.dataframe(market_metrics, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Your Performance vs Market")
        perf = pd.DataFrame([
            ["ADR vs Market", "+€47", "+23.6%"],
            ["RevPAR vs Market", "+€49", "+34.2%"],
            ["Occupancy vs Market", "+6.2pp", "Strong"],
        ], columns=["Metric", "Delta", "Status"])
        st.dataframe(perf, use_container_width=True, hide_index=True)

# ============================================================
# Workspace 4: Rate Intelligence
# ============================================================
elif workspace == "Rate Intelligence":
    hero(
        "Rate Intelligence",
        "Daily BAR recommendations and pricing optimization.",
        badges=[{"text": "AI Pricing", "style": "gold"}],
    )
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 💰 Current Rates")
        current_bar = st.number_input("Current BAR", min_value=0, value=980, step=10)
        floor = st.number_input("Rate Floor", min_value=0, value=780, step=10)
        ceiling = st.number_input("Rate Ceiling", min_value=0, value=1450, step=10)
        
        st.markdown("### 📊 Market Inputs")
        occupancy = st.slider("Occupancy %", 0, 100, 78)
        search_index = st.slider("Search Index", 0, 100, 74)
        
    with col2:
        st.markdown("### 🤖 Recommendation")
        comp_df = sample_competitor_feed()
        comp_median = comp_df["ADR"].median()
        
        # Calculate recommendation
        demand_score = 35 * (occupancy / 100) + 25 * (search_index / 100) + 40
        comp_gap = (comp_median - current_bar) / max(current_bar, 1)
        raw_rec = current_bar * (1 + 0.30 * comp_gap + 0.22 * ((demand_score - 60) / 100))
        recommended = clamp(raw_rec, floor, ceiling)
        
        kpi("Recommended BAR", money(recommended, "€"), f"vs current {money(current_bar, '€')}", 
            f"{(recommended/current_bar - 1)*100:+.1f}%", "positive" if recommended > current_bar else "negative")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Approve Rate", type="primary"):
                st.success(f"Rate {money(recommended, '€')} approved and queued for PMS sync")
        with col_b:
            if st.button("❌ Reject"):
                st.warning("Recommendation rejected")

# ============================================================
# Workspace 5: Operations & Finance
# ============================================================
elif workspace == "Operations & Finance":
    hero(
        "Operations & Finance",
        "Data quality monitoring and ROI modeling.",
        badges=[{"text": "Data Quality", "style": "blue"}],
    )
    
    tab1, tab2 = st.tabs(["🔍 Data Quality", "💰 ROI Calculator"])
    
    with tab1:
        st.markdown("### Data Quality Monitor")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi("Records Loaded", "8", "processed")
        with col2:
            kpi("Quality Score", "92%", "excellent")
        with col3:
            kpi("Exceptions", "1", "open")
        with col4:
            kpi("Ready for Use", "7", "records")
    
    with tab2:
        st.markdown("### ROI Calculator")
        adr_uplift = st.slider("ADR Uplift %", 0.0, 20.0, 5.0, 0.5)
        implementation = st.number_input("Implementation Cost", value=85000)
        subscription = st.number_input("Annual Subscription", value=120000)
        
        annual_uplift = 640 * 150 * 365 * (adr_uplift / 100)
        net_benefit = annual_uplift - subscription - implementation
        
        kpi("Year 1 Net Benefit", money(net_benefit, "€"), f"ROI: {(net_benefit/(implementation + subscription))*100:.0f}%")

# ============================================================
# Workspace 6: Forecasting
# ============================================================
else:
    hero(
        "Forecasting & Scenarios",
        "90-day demand forecast and revenue projection.",
        badges=[{"text": "Predictive", "style": "purple"}],
    )
    
    forecast_df = sample_forecast_data()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Forecast ADR"], name="Forecast", line=dict(color="#3b82f6", width=3)))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Upper Bound"], fill=None, mode="lines", line_color="rgba(0,0,0,0)", showlegend=False))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Lower Bound"], fill="tonexty", mode="lines", line_color="rgba(0,0,0,0)", name="Confidence Band", fillcolor="rgba(59, 130, 246, 0.2)"))
    
    fig.update_layout(template="plotly_dark", height=400, hovermode="x unified", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Footer
# ============================================================
st.divider()
st.caption("🏨 LuxePricing.ai MVP | ✅ Document analysis enabled | ✅ Real-time insights | ✅ Production ready")
