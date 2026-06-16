import io
import json
import math
import textwrap
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

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

    .stSidebar .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--blue) 0%, var(--cyan) 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    h1, h2, h3, h4 { 
        letter-spacing: -0.01em;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }

    /* Hero card with gradient */
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

    /* KPI card - enhanced */
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

    /* Metric change indicator */
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

    /* Module card */
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

    /* Badge enhancements */
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
    .badge.purple { 
        color: #d8b4fe; 
        border-color: rgba(167, 139, 250, 0.4); 
        background: rgba(167, 139, 250, 0.12); 
    }

    /* Note box */
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

    /* Tabs enhancement */
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

    /* Metric card */
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

    /* Input styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(26, 32, 44, 0.8) !important;
        border: 1px solid var(--line) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* Button styling */
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

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--green) 0%, #059669 100%) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }

    /* Dataframe styling */
    .dataframe { 
        border-radius: 10px; 
        overflow: hidden;
    }

    code, pre {
        background: rgba(26, 32, 44, 0.8) !important;
        border-radius: 10px !important;
        border: 1px solid var(--line) !important;
    }

    /* Scrollbar */
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

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.3s ease;
    }

    /* STR-inspired metrics display */
    .str-metric-box {
        border-left: 4px solid var(--blue);
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(6, 182, 212, 0.05));
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }

    .str-metric-box.warning {
        border-left-color: var(--amber);
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
    }

    .str-metric-box.success {
        border-left-color: var(--green);
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
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
    style = "note-box" if box_type == "note" else f"str-metric-box {box_type}"
    st.markdown(f"<div class='{style}'>{text}</div>", unsafe_allow_html=True)


def csv_download(df):
    """Generate CSV download bytes."""
    return df.to_csv(index=False).encode("utf-8")

# ============================================================
# Sample data generators - Enhanced with STR-style data
# ============================================================
def sample_market_snapshot():
    """Generate market-level competitive snapshot (STR-style)."""
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


def sample_str_market_intelligence():
    """STR-style market intelligence dashboard data."""
    dates = pd.date_range(start="2026-01-01", periods=180, freq="D")
    data = []
    for date in dates:
        day_offset = (date - pd.Timestamp("2026-01-01")).days
        seasonality = 1.0 + 0.3 * np.sin((day_offset % 365) * np.pi / 182)
        noise = np.random.normal(0, 0.05)
        
        data.append({
            "Date": date,
            "Market Occupancy": np.clip(0.68 + 0.12 * seasonality + noise, 0.2, 0.95),
            "Your Occupancy": np.clip(0.72 + 0.15 * seasonality + noise + 0.05, 0.25, 0.98),
            "Market ADR": 185 * seasonality * (1 + noise),
            "Your ADR": 220 * seasonality * (1 + noise + 0.08),
            "Event Index": 50 + 30 * np.sin((day_offset % 365) * np.pi / 182),
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
    """Original competitor feed."""
    return pd.DataFrame([
        {"Hotel": "Mandarin Oriental Paris", "Tier": "Luxury", "Room Type": "Deluxe King", "Refundable Rate": 1040, "Non-refundable Rate": 970, "Available": True, "Source": "approved_rate_shopper", "Captured At": "2026-06-16 08:15"},
        {"Hotel": "Ritz Paris", "Tier": "Ultra luxury", "Room Type": "Deluxe King", "Refundable Rate": 1320, "Non-refundable Rate": 1250, "Available": True, "Source": "approved_rate_shopper", "Captured At": "2026-06-16 08:16"},
        {"Hotel": "Le Bristol Paris", "Tier": "Ultra luxury", "Room Type": "Deluxe King", "Refundable Rate": 1180, "Non-refundable Rate": 1100, "Available": True, "Source": "approved_rate_shopper", "Captured At": "2026-06-16 08:16"},
        {"Hotel": "The Peninsula Paris", "Tier": "Luxury", "Room Type": "Deluxe King", "Refundable Rate": 980, "Non-refundable Rate": 920, "Available": True, "Source": "approved_rate_shopper", "Captured At": "2026-06-16 08:17"},
        {"Hotel": "Cheval Blanc Paris", "Tier": "Ultra luxury", "Room Type": "Deluxe King", "Refundable Rate": 1450, "Non-refundable Rate": 1380, "Available": True, "Source": "approved_rate_shopper", "Captured At": "2026-06-16 08:17"},
    ])


def sample_demand_calendar():
    """Enhanced demand calendar with more details."""
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
            "Compression": ["High", "High", "Medium", "Medium", "Medium", "Low", "Medium"][i % 7],
            "Forecast Occ%": [88, 85, 72, 78, 68, 45, 70][i % 7],
            "Recommended ADR": [950, 920, 780, 850, 720, 450, 750][i % 7],
        })
    return pd.DataFrame(rows)


def sample_performance_vs_set():
    """Performance vs competitive set over time."""
    dates = pd.date_range(start="2026-04-01", periods=120, freq="D")
    data = []
    for i, date in enumerate(dates):
        your_revpar = 640 + 100 * np.sin(i / 30) + np.random.normal(0, 20)
        market_revpar = 550 + 80 * np.sin(i / 30) + np.random.normal(0, 15)
        
        data.append({
            "Date": date,
            "Your RevPAR": your_revpar,
            "Market Avg RevPAR": market_revpar,
            "Top 25% RevPAR": market_revpar * 1.35,
            "Performance Index": (your_revpar / market_revpar) * 100,
        })
    return pd.DataFrame(data)

# ============================================================
# Rate recommendation algorithm - Enhanced
# ============================================================
def calculate_rate_recommendation(current_bar, rooms_available, on_books, pickup_7d, search_index, event_impact, floor, ceiling, comp_df, max_change_pct):
    """Enhanced rate recommendation with STR-style logic."""
    clean = comp_df[(comp_df.get("Available", True) == True) & (comp_df.get("Refundable Rate", 0) > 0)].copy()
    comp_median = float(clean["Refundable Rate"].median()) if len(clean) else current_bar
    
    occ_on_books = on_books / rooms_available if rooms_available else 0
    pickup_pressure = min(100, (pickup_7d / max(1, rooms_available)) * 500)
    demand_score = (0.35 * occ_on_books * 100 + 0.20 * pickup_pressure + 
                    0.25 * search_index + 0.20 * event_impact)
    comp_gap = (comp_median - current_bar) / max(current_bar, 1)
    demand_factor = (demand_score - 60) / 100
    
    raw = current_bar * (1 + 0.30 * comp_gap + 0.22 * demand_factor)
    raw = 0.65 * raw + 0.35 * comp_median
    
    max_up = current_bar * (1 + max_change_pct / 100)
    max_down = current_bar * (1 - max_change_pct / 100)
    rec = clamp(raw, max_down, max_up)
    rec = clamp(rec, floor, ceiling)
    rec = round(rec / 5) * 5
    
    confidence = (55 + min(22, len(clean) * 4) + min(13, demand_score / 10) - 
                  min(12, abs(comp_gap) * 20))
    confidence = int(clamp(confidence, 45, 96))
    
    return {
        "clean_comp_count": len(clean),
        "comp_median": comp_median,
        "occupancy_on_books": occ_on_books,
        "pickup_pressure": pickup_pressure,
        "demand_score": demand_score,
        "raw_recommendation": raw,
        "recommended_bar": rec,
        "delta": rec - current_bar,
        "delta_pct": (rec / current_bar - 1) * 100 if current_bar else 0,
        "confidence": confidence,
    }

# ============================================================
# Data quality scanning
# ============================================================
def scan_data_quality(df):
    """Enhanced data quality scan."""
    required = ["hotel_id", "property_name", "record_date", "rooms_available", "rooms_sold", "rooms_revenue", "adr", "occupancy_pct"]
    exceptions = []
    df = df.copy()
    df["quality_status"] = "Clean"
    df["quality_issues"] = ""

    def add_issue(idx, severity, rule, issue, owner):
        exceptions.append({"Row": idx + 1, "Severity": severity, "Rule": rule, "Issue": issue, "Owner": owner})
        df.loc[idx, "quality_status"] = "Blocked" if severity == "High" else "Review"
        current = df.loc[idx, "quality_issues"]
        df.loc[idx, "quality_issues"] = (current + "; " if current else "") + issue

    for col in required:
        if col not in df.columns:
            continue
        missing = df[col].isna() | (df[col].astype(str).str.strip() == "")
        for idx in df[missing].index:
            add_issue(idx, "High", "Completeness", f"Missing: {col}", "Data Ops")

    for idx, r in df.iterrows():
        occ = pd.to_numeric(r.get("occupancy_pct"), errors="coerce")
        if pd.notna(occ) and (occ < 0 or occ > 100):
            add_issue(idx, "High", "Validity", "Occupancy outside 0–100%", "Revenue Manager")

    score = int(clamp(100 - (len(exceptions) * 5), 0, 100))
    clean_df = df[df["quality_status"] == "Clean"].copy()
    
    return df, pd.DataFrame(exceptions) if exceptions else pd.DataFrame(), clean_df, score

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
            "Market Intelligence",
            "Rate Intelligence",
            "Operations & Finance",
            "Forecasting & Scenarios",
            "Strategy & Corporate",
        ],
        index=0,
    )
    
    st.divider()
    st.markdown("**Core Modules**")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("AI Marketing", True, disabled=True, label_visibility="collapsed")
        st.checkbox("AI Sales", True, disabled=True, label_visibility="collapsed")
        st.checkbox("AI Finance", True, disabled=True, label_visibility="collapsed")
    with col2:
        st.checkbox("AI Ops", True, disabled=True, label_visibility="collapsed")
        st.checkbox("AI Tech", True, disabled=True, label_visibility="collapsed")
        st.checkbox("AI Agent", True, disabled=True, label_visibility="collapsed")
    
    st.divider()
    st.caption("✓ All data governance: human approval required")

# ============================================================
# Workspace 1: Dashboard & Analytics (STR-inspired)
# ============================================================
if workspace == "Dashboard & Analytics":
    hero(
        "Dashboard & Analytics",
        "Real-time market intelligence, competitive positioning, and performance metrics.",
        badges=[
            {"text": "STR-Style Analytics", "style": "gold"},
            {"text": "Live Benchmarking", "style": "blue"},
            {"text": "Market Position", "style": "green"}
        ],
    )
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        kpi("Your RevPAR", money(640, "€"), "vs Market 550€", "↑ 16.4%", "positive")
    with col2:
        kpi("Occupancy", pct(78.5), "vs Market 72.3%", "↑ 6.2pp", "positive")
    with col3:
        kpi("ADR", money(245.50, "€"), "vs Market 198€", "↑ 23.9%", "positive")
    with col4:
        kpi("Market Share", "9.2%", "of competitive set", "→ stable", "neutral")
    with col5:
        kpi("Performance Index", "116", "vs market avg 100", "↑ 2.8", "positive")
    
    st.divider()
    
    # Market snapshot
    tab_overview, tab_comp, tab_trend, tab_forecast = st.tabs([
        "📊 Market Snapshot", 
        "🏆 Competitive Set",
        "📈 Historical Trends",
        "🔮 Forecast"
    ])
    
    with tab_overview:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            snapshot_df = sample_market_snapshot()
            st.dataframe(snapshot_df, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("#### Positioning")
            positioning = pd.DataFrame([
                ["Top 25% Hotels", "✓ Above market in RevPAR", "✓ Premium positioning"],
                ["Market Average", "Baseline comparison", "Steady state"],
                ["Your Property", "✓ +16.4% RevPAR Index", "✓ Market Leader"],
            ], columns=["Segment", "Status", "Performance"])
            st.dataframe(positioning, use_container_width=True, hide_index=True)
    
    with tab_comp:
        comp_set = sample_comp_set()
        st.dataframe(comp_set.sort_values("RevPAR", ascending=False), use_container_width=True, hide_index=True)
        
        fig = go.Figure()
        for _, row in comp_set.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["ADR"]], y=[row["Occupancy"]], 
                mode='markers+text',
                name=row["Hotel"],
                text=row["Hotel"],
                textposition="top center",
                marker=dict(size=row["RevPAR"]/50, 
                           color=row["RevPAR"],
                           colorscale="Viridis",
                           showscale=(row["Hotel"]=="Your Property")),
            ))
        
        fig.update_layout(
            title="Competitive Set: ADR vs Occupancy (bubble size = RevPAR)",
            xaxis_title="ADR (€)",
            yaxis_title="Occupancy %",
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab_trend:
        perf_df = sample_performance_vs_set()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=perf_df["Date"], y=perf_df["Your RevPAR"],
            name="Your Property", line=dict(color="#3b82f6", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=perf_df["Date"], y=perf_df["Market Avg RevPAR"],
            name="Market Average", line=dict(color="#9ca3af", width=2, dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=perf_df["Date"], y=perf_df["Top 25% RevPAR"],
            name="Top 25% Set", line=dict(color="#10b981", width=2, dash="dot")
        ))
        
        fig.update_layout(
            title="RevPAR Performance vs Competitive Set",
            xaxis_title="Date",
            yaxis_title="RevPAR (€)",
            template="plotly_dark",
            height=400,
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
        
        current_pi = 116
        prev_pi = 112
        note(f"Performance Index: <b>{current_pi}</b> (↑ {current_pi - prev_pi} from prior period). "
             f"You are outperforming market by {current_pi - 100}%.", "success")
    
    with tab_forecast:
        forecast_df = sample_forecast_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"], y=forecast_df["Forecast ADR"],
            name="Forecast ADR", line=dict(color="#3b82f6", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"], y=forecast_df["Upper Bound"],
            fill=None, mode="lines", line_color="rgba(0,0,0,0)", 
            name="Upper Bound (P90)", showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"], y=forecast_df["Lower Bound"],
            fill="tonexty", mode="lines", line_color="rgba(0,0,0,0)",
            name="Confidence Band (80%)",
            fillcolor="rgba(59, 130, 246, 0.2)"
        ))
        
        fig.update_layout(
            title="90-Day ADR Forecast with Confidence Intervals",
            xaxis_title="Date",
            yaxis_title="ADR (€)",
            template="plotly_dark",
            height=400,
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Workspace 2: Market Intelligence (New - STR-inspired)
# ============================================================
elif workspace == "Market Intelligence":
    hero(
        "Market Intelligence",
        "Deep-dive competitive analysis, market dynamics, and strategic positioning.",
        badges=[
            {"text": "Market Trends", "style": "blue"},
            {"text": "Competitive Dynamics", "style": "gold"},
            {"text": "Supply & Demand", "style": "purple"}
        ],
    )
    
    intel_tab1, intel_tab2, intel_tab3, intel_tab4 = st.tabs([
        "🔍 Market Overview",
        "🏢 Comp Set Deep Dive",
        "📊 Supply & Demand",
        "💡 Strategic Insights"
    ])
    
    with intel_tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Market Metrics (Last 30 days)")
            market_metrics = pd.DataFrame([
                ["Total Rooms Sold", "184,520", "↑ 3.2%"],
                ["Total Revenue", "€38.2M", "↑ 8.1%"],
                ["Avg Market ADR", "€198.75", "↑ 5.1%"],
                ["Market Occupancy", "72.3%", "↑ 2.1pp"],
                ["Avg Market RevPAR", "€143.55", "↑ 7.2%"],
                ["RevPAR Index (Your Hotel)", "116.3", "↑ 2.8"],
            ], columns=["Metric", "Value", "Change"])
            st.dataframe(market_metrics, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Market Composition")
            comp_comp = pd.DataFrame([
                ["Ultra Luxury (>€800)", "15 hotels", "38.2%"],
                ["Luxury (€400–€800)", "28 hotels", "42.1%"],
                ["Upper Midscale (€200–€400)", "18 hotels", "19.7%"],
                ["Total Competitive Set", "61 hotels", "100%"],
            ], columns=["Segment", "Count", "% of Market"])
            st.dataframe(comp_comp, use_container_width=True, hide_index=True)
    
    with intel_tab2:
        st.markdown("#### Competitive Set Performance (Last 30 Days)")
        comp_deep = pd.DataFrame([
            ["Ritz Paris", "Ultra Lux", 1320, 79.8, 1054.7, "↑ 6.2%", "🟢"],
            ["Cheval Blanc", "Ultra Lux", 1450, 80.1, 1161.4, "↑ 4.8%", "🟢"],
            ["Mandarin Oriental", "Ultra Lux", 1040, 82.5, 858.5, "→ 0.2%", "🟡"],
            ["Le Bristol", "Ultra Lux", 1180, 81.2, 958.2, "↑ 2.1%", "🟢"],
            ["Your Property", "Luxury", 815, 78.5, 640.0, "↑ 7.3%", "🟢"],
            ["Peninsula Paris", "Luxury", 980, 75.3, 737.9, "↑ 1.5%", "🟡"],
        ], columns=["Hotel", "Tier", "ADR", "Occ%", "RevPAR", "RevPAR Change", "Status"])
        st.dataframe(comp_deep.sort_values("RevPAR", ascending=False), use_container_width=True, hide_index=True)
        
        st.markdown("#### Your Property vs Top Performers")
        benchmark_comp = pd.DataFrame([
            ["ADR vs Top Performer", "−€635", "−43.8%", "Strategic positioning below ultra-luxury tier"],
            ["RevPAR vs Avg Comp", "+€97", "+17.9%", "Outperforming market in yield efficiency"],
            ["Occupancy vs Market", "+6.2pp", "Strong demand capture"],
            ["Revenue per Room", "+€168/day", "Premium mix and pricing power"],
        ], columns=["Comparison", "Value", "%", "Insight"])
        st.dataframe(benchmark_comp, use_container_width=True, hide_index=True)
    
    with intel_tab3:
        st.markdown("#### Market Supply & Demand Dynamics")
        
        col1, col2 = st.columns(2)
        with col1:
            supply = pd.DataFrame([
                ["Total Market Keys", "8,450", "Growth: +2.1% YoY"],
                ["New Properties (12m)", "342 rooms", "Planned: 156 rooms"],
                ["Closures (12m)", "89 rooms", "Pipeline: +253 rooms"],
                ["Net Growth", "+214 rooms", "2.5% capacity increase"],
            ], columns=["Supply Metric", "Value", "Trend"])
            st.dataframe(supply, use_container_width=True, hide_index=True)
        
        with col2:
            demand = pd.DataFrame([
                ["Searches (30d)", "487,230", "↑ 8.2% vs prior month"],
                ["Search Growth (YoY)", "+12.3%", "Strong leisure demand"],
                ["Avg LOS", "2.8 nights", "↓ 0.3 from prior year"],
                ["Booking Window", "22 days", "→ consistent"],
            ], columns=["Demand Metric", "Value", "Insight"])
            st.dataframe(demand, use_container_width=True, hide_index=True)
        
        # Supply vs Demand chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        dates = pd.date_range(start="2026-01-01", periods=180, freq="D")
        occupancy = 68 + 12 * np.sin(np.arange(180) * np.pi / 90)
        searches = 400 + 120 * np.sin(np.arange(180) * np.pi / 90)
        
        fig.add_trace(
            go.Scatter(x=dates, y=occupancy, name="Market Occupancy %", line=dict(color="#3b82f6")),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=dates, y=searches, name="Search Index", line=dict(color="#10b981")),
            secondary_y=True,
        )
        
        fig.update_yaxes(title_text="Occupancy %", secondary_y=False)
        fig.update_yaxes(title_text="Search Index", secondary_y=True)
        fig.update_layout(
            title="Supply (Occupancy) vs Demand (Searches)",
            template="plotly_dark",
            height=400,
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with intel_tab4:
        st.markdown("#### Strategic Recommendations")
        insights = [
            ("📈 Revenue Opportunity", "You are outperforming RevPAR index by 16.3% — this pricing power positions you well for rate increases.", "success"),
            ("⚠️ Competitive Pressure", "Ultra-luxury segment showing strong occupancy (80%+) — monitor pricing elasticity carefully.", "warning"),
            ("🎯 Positioning", "Your property commands luxury pricing without ultra-luxury ADR — ideal sweet spot for market leadership.", "success"),
            ("📊 Demand Trend", "Strong YoY growth (+12.3% searches) suggests pricing runway before elasticity impacts occupancy.", "success"),
            ("⛔ Risk Factor", "New supply (+2.5% market growth) could compress occupancy — recommend rate floors to protect yield.", "warning"),
        ]
        
        for title, text, insight_type in insights:
            note(f"<b>{title}</b><br>{text}", insight_type)

# ============================================================
# Workspace 3: Rate Intelligence (Enhanced from Live Demo)
# ============================================================
elif workspace == "Rate Intelligence":
    hero(
        "Rate Intelligence",
        "AI-powered daily BAR recommendations with competitive rate-shopping, demand signals, and human approval.",
        badges=[
            {"text": "AI Rate Agent", "style": "gold"},
            {"text": "Human Approval", "style": "green"},
            {"text": "Real-time Data", "style": "blue"}
        ],
    )

    if "comp_df" not in st.session_state:
        st.session_state.comp_df = sample_competitor_feed()
    if "agent_audit" not in st.session_state:
        st.session_state.agent_audit = []
    if "approved_rates" not in st.session_state:
        st.session_state.approved_rates = []

    left, right = st.columns([0.95, 1.05], gap="large")
    
    with left:
        st.markdown("### 📋 Property & Demand Inputs")
        c1, c2 = st.columns(2)
        hotel_name = c1.text_input("Hotel / Asset", "Maison Lumière Paris")
        target_date = c2.date_input("Target Rate Date", date(2026, 7, 1))
        
        c3, c4, c5 = st.columns(3)
        current_bar = c3.number_input("Current BAR", min_value=0, value=980, step=10)
        floor = c4.number_input("Rate Floor", min_value=0, value=780, step=10)
        ceiling = c5.number_input("Rate Ceiling", min_value=0, value=1450, step=10)
        
        c6, c7, c8 = st.columns(3)
        rooms_available = c6.number_input("Rooms Available", min_value=1, value=120)
        on_books = c7.number_input("Rooms on Books", min_value=0, value=86)
        pickup_7d = c8.number_input("7-Day Pickup", min_value=0, value=18)
        
        c9, c10, c11 = st.columns(3)
        search_index = c9.slider("Search/Demand Index", 0, 100, 74)
        event_impact = c10.slider("Event Impact Score", 0, 100, 90)
        max_change_pct = c11.slider("Max Daily Change %", 5, 35, 18)
        
        event_name = st.text_input("Demand Driver / Event", "Paris Fashion Week")

        uploaded_comp = st.file_uploader("Upload Competitor Feed CSV", type=["csv"])
        if uploaded_comp is not None:
            try:
                comp_uploaded = pd.read_csv(uploaded_comp)
                for col in ["Refundable Rate", "Non-refundable Rate"]:
                    if col in comp_uploaded.columns:
                        comp_uploaded[col] = pd.to_numeric(comp_uploaded[col], errors="coerce")
                if "Available" in comp_uploaded.columns:
                    comp_uploaded["Available"] = comp_uploaded["Available"].astype(str).str.lower().isin(["true", "yes", "1"])
                st.session_state.comp_df = comp_uploaded
                st.success("✓ Competitor feed uploaded")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

        with st.expander("📊 Competitor Rate-Shopper Feed", expanded=True):
            st.dataframe(st.session_state.comp_df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Download Feed", csv_download(st.session_state.comp_df), "competitor_feed.csv", "text/csv")

    rec = calculate_rate_recommendation(current_bar, rooms_available, on_books, pickup_7d, search_index, event_impact, floor, ceiling, st.session_state.comp_df, max_change_pct)

    with right:
        st.markdown("### 🤖 AI Agent Output")
        a, b, c, d = st.columns(4)
        with a: kpi("Current BAR", money(current_bar), "from PMS/RMS")
        with b: kpi("Comp Median", money(rec["comp_median"]), "clean rates")
        with c: kpi("Demand Score", f"{rec['demand_score']:.0f}/100", f"Event: {event_name}")
        with d: kpi("Recommended BAR", money(rec["recommended_bar"]), f"{rec['delta_pct']:+.1f}%", f"{rec['confidence']}%", "positive" if rec['delta'] > 0 else "negative" if rec['delta'] < 0 else "neutral")

        st.markdown("#### 🖥️ Reasoning Terminal")
        terminal = f"""
        [INIT] Property: {hotel_name} | Target: {target_date}
        [DATA] Competitors: {rec['clean_comp_count']} | Median: {money(rec['comp_median'])}
        [DEMAND] Occupancy: {rec['occupancy_on_books']*100:.1f}% | Pickup: {pickup_7d} rooms
        [EVENT] {event_name} | Impact: {event_impact}/100
        [GUARDRAILS] Floor: {money(floor)} | Ceiling: {money(ceiling)} | Max: ±{max_change_pct}%
        [RECOMMENDATION] BAR: {money(rec['recommended_bar'])} | Confidence: {rec['confidence']}%
        [STATUS] ⏳ Awaiting Revenue Manager approval
        """
        st.code(textwrap.dedent(terminal).strip(), language="text")

        explanation = (
            f"Recommending **{money(rec['recommended_bar'])}** — demand is {rec['demand_score']:.0f}/100, "
            f"current BAR is {'below' if current_bar < rec['comp_median'] else 'above'} competitor median, "
            f"within all guardrails."
        )
        note(explanation)
        
        col_a, col_b, col_c = st.columns([1, 1, 1])
        if col_a.button("✅ Approve Rate", type="primary"):
            row = {
                "Hotel": hotel_name,
                "Date": str(target_date),
                "Room Type": "Deluxe King",
                "Approved BAR": rec["recommended_bar"],
                "Current BAR": current_bar,
                "Confidence": rec["confidence"],
                "Status": "Approved"
            }
            st.session_state.approved_rates.append(row)
            st.session_state.agent_audit.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Action": "Rate Approved",
                "Value": money(rec["recommended_bar"]),
                "User": "Revenue Manager"
            })
            st.success("✓ Rate moved to queue")
        
        if col_b.button("❌ Reject"):
            st.session_state.agent_audit.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Action": "Rate Rejected",
                "Value": money(rec["recommended_bar"]),
                "User": "Revenue Manager"
            })
            st.warning("✗ Recommendation rejected")
        
        if col_c.button("🔄 Refresh Data"):
            df = sample_competitor_feed()
            noise = np.random.default_rng().normal(0, 35, len(df))
            df["Refundable Rate"] = (df["Refundable Rate"] + noise).round(-1).astype(int)
            st.session_state.comp_df = df
            st.session_state.agent_audit.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Action": "Data Refreshed",
                "Value": "Competitor feed updated",
                "User": "Agent"
            })
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["✓ Approval Queue", "📅 Demand Calendar", "💬 LLM Prompt"])
    
    with tab1:
        approved_df = pd.DataFrame(st.session_state.approved_rates)
        audit_df = pd.DataFrame(st.session_state.agent_audit)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Approved Recommendations")
            if len(approved_df):
                st.dataframe(approved_df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download", csv_download(approved_df), "approved_rates.csv", "text/csv")
            else:
                st.info("No rates approved yet")
        with c2:
            st.markdown("#### Audit Trail")
            if len(audit_df):
                st.dataframe(audit_df, use_container_width=True, hide_index=True)
            else:
                st.info("No events logged")
    
    with tab2:
        demand_df = sample_demand_calendar()
        st.dataframe(demand_df.head(15), use_container_width=True, hide_index=True)
        
        fig = px.line(
            demand_df, x="Date", y=["Event Impact", "Search Index"],
            markers=True,
            title="Demand Calendar Signals (30-day)"
        )
        fig.update_layout(
            template="plotly_dark", height=360,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        provider = st.selectbox("LLM Provider", ["ChatGPT", "Gemini", "Claude"], key="agent_provider")
        prompt = f"""
        You are a hotel revenue-management AI inside LuxePricing.ai.
        Provider: {provider}

        Task: Recommend daily BAR for {hotel_name} on {target_date}.
        
        Inputs:
        - Current BAR: {money(current_bar)}
        - Floor/Ceiling: {money(floor)} / {money(ceiling)}
        - Rooms Available: {rooms_available}
        - On Books: {on_books}
        - 7-Day Pickup: {pickup_7d}
        - Demand Index: {search_index}/100
        - Event: {event_name} (impact {event_impact}/100)
        - Competitor Median: {money(rec['comp_median'])}
        - AI Recommended BAR: {money(rec['recommended_bar'])}

        Output:
        1. Plain English explanation
        2. Risk assessment
        3. Revenue manager approval note
        4. Do not claim live scraping; use approved rate-shopping feeds or CSV uploads only
        """
        st.code(textwrap.dedent(prompt).strip(), language="text")

# ============================================================
# Workspace 4: Operations & Finance (Refined)
# ============================================================
elif workspace == "Operations & Finance":
    hero(
        "Operations & Finance",
        "CRM data quality monitoring + USALI-style ROI financial modeling.",
        badges=[{"text": "Data Quality", "style": "blue"}, {"text": "ROI Calculator", "style": "gold"}],
    )

    ops_tab, finance_tab = st.tabs(["🔍 Ops: CRM Quality", "💰 Finance: ROI"])

    with ops_tab:
        st.markdown("### Data Quality Monitor")
        
        source_map = pd.DataFrame([
            ["PMS/CRS", "Rooms sold, available, arrivals", "Ops/IT"],
            ["RMS", "ADR, RevPAR, pickup", "Revenue Manager"],
            ["Finance Reports", "GOP, NOI, fees", "Finance"],
            ["CRM", "Contacts, property record", "CRM Admin"],
            ["Rate-Shopper", "Competitor ADR", "Revenue Ops"],
        ], columns=["Source", "Data", "Owner"])
        st.dataframe(source_map, use_container_width=True, hide_index=True)
        
        ops_df = pd.DataFrame([
            ["LP-001", "Hotel A", "2026-07-01", 150, 118, 30680, 260, 78.7, "Clean"],
            ["LP-001", "Hotel A", "2026-07-02", 150, 129, 36120, 280, 86.0, "Clean"],
            ["LP-002", "Hotel B", "2026-07-03", 120, 92, 23000, 250, 76.7, "Review"],
        ], columns=["ID", "Property", "Date", "Keys", "Sold", "Revenue", "ADR", "Occ%", "Status"])
        
        scanned_df, exceptions_df, clean_df, score = scan_data_quality(ops_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: kpi("Records", len(ops_df), "loaded")
        with col2: kpi("Quality Score", f"{score}%", "threshold: 90%")
        with col3: kpi("Exceptions", len(exceptions_df), "open")
        with col4: kpi("Clean Records", len(clean_df), "ready")
        
        st.dataframe(scanned_df, use_container_width=True, hide_index=True)

    with finance_tab:
        st.markdown("### ROI Calculator")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Scenario Inputs")
            keys = st.number_input("Keys", value=150, min_value=1)
            days = st.number_input("Operating Days", value=365, min_value=1)
            current_adr = st.number_input("Current ADR", value=215.0, step=5.0)
            current_occ = st.number_input("Occupancy %", value=75.0, step=0.5)
            adr_uplift = st.slider("ADR Uplift %", 0.0, 20.0, 5.0, 0.5)
            implementation = st.number_input("Implementation Cost", value=85000.0, step=5000.0)
            subscription = st.number_input("Annual Subscription", value=120000.0, step=5000.0)
        
        with col2:
            st.markdown("#### Financial Output")
            current_revpar = (current_adr * current_occ) / 100
            scenario_adr = current_adr * (1 + adr_uplift / 100)
            scenario_revpar = (scenario_adr * current_occ) / 100
            
            kpi("Current RevPAR", money(current_revpar, "€"), "baseline")
            kpi("Scenario RevPAR", money(scenario_revpar, "€"), f"↑ {money(scenario_revpar - current_revpar, '€')}")
            
            annual_uplift = (scenario_revpar - current_revpar) * keys * days
            net_benefit = annual_uplift - subscription - implementation
            roi = (net_benefit / (implementation + subscription)) * 100 if (implementation + subscription) > 0 else 0
            
            kpi("Year 1 Net Benefit", money(net_benefit, "€"), f"ROI: {roi:.0f}%", f"{'+' if net_benefit > 0 else ''}{pct(net_benefit/100000)}", "positive" if net_benefit > 0 else "negative")

# ============================================================
# Workspace 5: Forecasting & Scenarios
# ============================================================
elif workspace == "Forecasting & Scenarios":
    hero(
        "Forecasting & Scenarios",
        "90-day demand forecast, scenario modeling, and revenue projection.",
        badges=[{"text": "Predictive Models", "style": "purple"}, {"text": "Scenario Planning", "style": "blue"}],
    )
    
    forecast_tab1, forecast_tab2, forecast_tab3 = st.tabs([
        "🔮 90-Day Forecast",
        "📊 Scenario Comparison",
        "📈 Revenue Projection"
    ])
    
    with forecast_tab1:
        forecast_df = sample_forecast_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"], y=forecast_df["Forecast ADR"],
            name="Forecast ADR", line=dict(color="#3b82f6", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"], y=forecast_df["Upper Bound"],
            fill=None, mode="lines", line_color="rgba(0,0,0,0)", showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"], y=forecast_df["Lower Bound"],
            fill="tonexty", mode="lines", line_color="rgba(0,0,0,0)",
            name="Confidence Band (±1σ)", fillcolor="rgba(59, 130, 246, 0.2)"
        ))
        
        fig.update_layout(
            title="90-Day ADR Forecast with Confidence Intervals",
            xaxis_title="Date", yaxis_title="ADR (€)",
            template="plotly_dark", height=400,
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Forecast Metrics")
            avg_forecast = forecast_df["Forecast ADR"].mean()
            st.metric("Avg Forecast ADR", money(avg_forecast, "€"))
            st.metric("Min ADR", money(forecast_df["Forecast ADR"].min(), "€"))
            st.metric("Max ADR", money(forecast_df["Forecast ADR"].max(), "€"))
        
        with col2:
            st.markdown("#### Forecast Confidence")
            avg_conf = forecast_df["Confidence"].mean()
            st.metric("Avg Confidence", pct(avg_conf * 100))
            st.metric("Day 1-30", pct(forecast_df[forecast_df["Date"] <= forecast_df["Date"].min() + pd.Timedelta(days=30)]["Confidence"].mean() * 100))
            st.metric("Day 60-90", pct(forecast_df[forecast_df["Date"] >= forecast_df["Date"].max() - pd.Timedelta(days=30)]["Confidence"].mean() * 100))
    
    with forecast_tab2:
        st.markdown("#### Scenario Comparison")
        scenarios = pd.DataFrame([
            ["Conservative", "2% ADR↑", "0.5pp Occ↑", "€658K", "€42K", "51%"],
            ["Base Case", "5% ADR↑", "1.5pp Occ↑", "€892K", "€652K", "341%"],
            ["Optimistic", "8% ADR↑", "2.5pp Occ↑", "€1.24M", "€1.02M", "536%"],
            ["Aggressive", "12% ADR↑", "4pp Occ↑", "€1.68M", "€1.46M", "768%"],
        ], columns=["Scenario", "ADR Assumption", "Occ Assumption", "Gross Uplift", "Net Benefit Y1", "ROI"])
        st.dataframe(scenarios, use_container_width=True, hide_index=True)
    
    with forecast_tab3:
        st.markdown("#### 12-Month Revenue Projection")
        months = pd.date_range(start="2026-07-01", periods=12, freq="M")
        revenue_proj = []
        for m in months:
            seasonality = 1.0 + 0.25 * np.sin((m.month % 12) * np.pi / 6)
            base_rev = 8_970_000
            projected = base_rev * seasonality
            revenue_proj.append({
                "Month": m.strftime("%b %Y"),
                "Current Path": projected * 0.95,
                "With AI Uplift (5%)": projected * 1.05,
                "Incremental": projected * 0.10
            })
        
        proj_df = pd.DataFrame(revenue_proj)
        fig = px.bar(proj_df, x="Month", y=["Current Path", "With AI Uplift (5%)"], 
                    title="12-Month Revenue Projection", barmode="group")
        fig.update_layout(
            template="plotly_dark", height=400,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Workspace 6: Strategy & Corporate
# ============================================================
else:
    hero(
        "Strategy & Corporate",
        "GTM strategy, organizational design, and integrated planning.",
        badges=[{"text": "Marketing", "style": "gold"}, {"text": "Sales", "style": "blue"}, {"text": "Organization", "style": "green"}],
    )
    
    strat_tab1, strat_tab2, strat_tab3 = st.tabs([
        "📢 AI Marketing",
        "🤝 AI Sales",
        "👥 Organization"
    ])
    
    with strat_tab1:
        st.markdown("#### AI Brand & Campaign Generator")
        col1, col2 = st.columns(2)
        with col1:
            hotel = st.text_input("Hotel Name", "Maison Atlas Lisbon")
            positioning = st.selectbox("Positioning", ["Quiet luxury", "Heritage", "Wellness", "Design-led", "Business"])
        with col2:
            audience = st.text_area("Target Audience", "Affluent leisure, design-conscious travelers")
        
        cal_df = sample_marketing_calendar()
        st.markdown("#### Campaign Calendar")
        st.dataframe(cal_df, use_container_width=True, hide_index=True)
    
    with strat_tab2:
        st.markdown("#### AI Sales Outreach")
        account = st.text_input("Target Account", "Accor Europe")
        role = st.selectbox("Buyer Role", ["VP Development", "CRO", "Asset Manager"])
        
        email_draft = f"""
        Subject: LuxePricing.ai for {account} hotel portfolio

        Dear {role},

        We connect revenue strategy, data quality, and dynamic pricing for hotel groups.
        For {account}, this means faster feasibility decisions and consistent revenue governance.

        Open to a 20-minute demo?

        Best regards,
        LuxePricing.ai
        """
        st.text_area("Email Draft", email_draft, height=180)
    
    with strat_tab3:
        st.markdown("#### Recommended Revenue Organization")
        org = pd.DataFrame([
            ["Chief Revenue Officer", "Total revenue strategy & AI governance"],
            ["Revenue Manager", "Pricing, forecasting, RMS"],
            ["Sales Lead", "Outreach, corporate accounts"],
            ["Marketing Manager", "Campaigns, brand standards"],
            ["AI Revenue Ops", "Data quality, model monitoring"],
            ["Brand Guardian", "Luxury guardrails, exceptions"],
        ], columns=["Role", "Responsibility"])
        st.dataframe(org, use_container_width=True, hide_index=True)
        
        kpis = pd.DataFrame([
            ["RevPAR Index", "Weekly"],
            ["Revenue Quality", "Daily"],
            ["AI Adoption", "Weekly"],
            ["Brand Protection", "Weekly"],
        ], columns=["KPI", "Cadence"])
        st.dataframe(kpis, use_container_width=True, hide_index=True)

# ============================================================
# Footer
# ============================================================
st.divider()
st.caption(
    "🏨 LuxePricing.ai Premium Revenue Intelligence | "
    "✓ STR-inspired analytics | ✓ Human approval required | "
    "✓ No unauthorized scraping | ✓ Prototype mode"
)
