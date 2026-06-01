"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       APL LOGISTICS — SUPPLY CHAIN INTELLIGENCE DASHBOARD  v2.1            ║
║       Senior Analyst Edition  |  Streamlit + Plotly                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

HOW TO RUN
──────────
  pip install streamlit plotly pandas numpy
  streamlit run apl_dashboard_v2.py

Place  APL_Logistics_Cleaned.csv  in the SAME folder as this script.
"""

# ── Imports ───────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="APL Logistics Intelligence",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════════
# THEME & STYLING
# ═════════════════════════════════════════════════════════════════════════════
COLORS = {
    "bg":     "#0A0E1A",
    "card":   "#111827",
    "border": "#1E293B",
    "accent": "#3B82F6",
    "green":  "#10B981",
    "red":    "#EF4444",
    "yellow": "#F59E0B",
    "purple": "#8B5CF6",
    "text":   "#F1F5F9",
    "muted":  "#64748B",
    "grid":   "#1E293B",
}

# ── Clean PLOTLY_TEMPLATE (no axis/title/legend/margin overrides here) ────────
PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font": {
            "color":  COLORS["text"],
            "family": "Inter, sans-serif",
            "size":   12,
        },
        "hoverlabel": {
            "bgcolor":     COLORS["card"],
            "bordercolor": COLORS["border"],
            "font":        {"color": COLORS["text"]},
        },
        "colorway": [
            COLORS["accent"],
            COLORS["green"],
            COLORS["yellow"],
            COLORS["red"],
            COLORS["purple"],
        ],
    }
}

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    background-color: {COLORS['bg']} !important;
    color: {COLORS['text']};
  }}

  /* ── Sidebar ──────────────────────────────── */
  section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0F172A 0%, {COLORS['bg']} 100%) !important;
    border-right: 1px solid {COLORS['border']};
  }}
  section[data-testid="stSidebar"] * {{ color: #CBD5E1 !important; }}
  section[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: #1E293B !important; border-color: #334155 !important;
  }}
  section[data-testid="stSidebar"] .stMultiSelect > div > div {{
    background: #1E293B !important; border-color: #334155 !important;
  }}

  /* ── Main content ─────────────────────────── */
  .block-container {{ padding: 1rem 2rem 2rem 2rem !important; max-width: 100%; }}

  /* ── KPI Card ─────────────────────────────── */
  .kpi-wrap {{
    background: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 14px;
    padding: 20px 18px 16px;
    position: relative;
    overflow: hidden;
    height: 120px;
    transition: box-shadow .2s;
  }}
  .kpi-wrap:hover {{ box-shadow: 0 0 0 1px {COLORS['accent']}44; }}
  .kpi-bar {{
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 14px 14px 0 0;
  }}
  .kpi-icon  {{ font-size: 1.5rem; line-height: 1; }}
  .kpi-val   {{ font-size: 2rem; font-weight: 700; color: {COLORS['text']}; margin: 4px 0 2px; line-height: 1; }}
  .kpi-label {{ font-size: .72rem; color: {COLORS['muted']}; text-transform: uppercase; letter-spacing: .07em; font-weight: 600; }}
  .kpi-sub   {{ font-size: .78rem; margin-top: 5px; font-weight: 500; }}
  .good {{ color: {COLORS['green']}; }}
  .bad  {{ color: {COLORS['red']}; }}
  .warn {{ color: {COLORS['yellow']}; }}
  .info {{ color: {COLORS['accent']}; }}
  .purp {{ color: {COLORS['purple']}; }}

  /* ── Section header ───────────────────────── */
  .sec-hdr {{
    display: flex; align-items: center; gap: 12px;
    background: linear-gradient(90deg, {COLORS['accent']}18, transparent);
    border-left: 3px solid {COLORS['accent']};
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin: 26px 0 14px;
  }}
  .sec-hdr h3 {{ margin: 0; font-size: 1rem; font-weight: 600; color: {COLORS['text']}; }}
  .sec-hdr p  {{ margin: 2px 0 0; font-size: .8rem; color: {COLORS['muted']}; }}

  /* ── Insight box ──────────────────────────── */
  .insight {{
    background: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
    font-size: .83rem;
    color: #CBD5E1;
    line-height: 1.5;
  }}
  .insight strong {{ color: {COLORS['text']}; }}

  /* ── Divider ──────────────────────────────── */
  hr {{ border-color: {COLORS['border']} !important; margin: 8px 0; }}

  /* ── Tabs ─────────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {{
    gap: 6px; background: {COLORS['card']};
    border-radius: 10px; padding: 4px;
    border: 1px solid {COLORS['border']};
  }}
  .stTabs [data-baseweb="tab"] {{
    background: transparent; border-radius: 8px;
    color: {COLORS['muted']} !important;
    font-size: .85rem; font-weight: 500; padding: 6px 16px;
  }}
  .stTabs [aria-selected="true"] {{
    background: {COLORS['accent']} !important; color: white !important;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ padding-top: 12px; }}

  /* ── DataFrame ────────────────────────────── */
  .stDataFrame {{ border-radius: 10px; overflow: hidden; }}
  [data-testid="stDataFrame"] > div {{ background: {COLORS['card']}; }}

  /* ── Download button ──────────────────────── */
  .stDownloadButton button {{
    background: {COLORS['accent']}; color: white;
    border: none; border-radius: 8px;
    font-weight: 600; font-size: .84rem; padding: 8px 18px;
  }}
  .stDownloadButton button:hover {{ opacity: .85; }}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# DATA LOADING & FEATURE ENGINEERING
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["Order Region"] = df["Order Region"].str.strip()

    df["Is_Late"]   = (df["Late_delivery_risk"] == 1).astype(int)
    df["Is_OnTime"] = (df["Delivery Performance"] == "On-Time").astype(int)
    df["Is_Early"]  = (df["Delivery Performance"] == "Early").astype(int)

    # Simulate quarter from row index (no date column in dataset)
    df["Quarter"] = pd.cut(
        df.index, bins=4, labels=["Q1","Q2","Q3","Q4"]
    ).astype(str)

    # SLA flag: actual ≤ scheduled → compliant
    df["SLA_Compliant"] = (
        df["Days for shipping (real)"] <= df["Days for shipment (scheduled)"]
    ).astype(int)

    return df


with st.spinner("🔄 Loading supply chain data…"):
    try:
        RAW = load_data("APL_Logistics_Cleaned_2.csv")
    except FileNotFoundError:
        st.error("❌  **APL_Logistics_Cleaned_2.csv** not found. Place it in the same folder as this script.")
        st.stop()

TOTAL_RECORDS = len(RAW)


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR — FILTERS
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 4px 8px;">
      <div style="font-size:2rem;">🚢</div>
      <div style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-top:4px;">APL Logistics</div>
      <div style="font-size:.78rem;color:{COLORS['muted']};">Supply Chain Intelligence</div>
    </div>
    <hr/>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='font-size:.8rem;color:{COLORS['muted']};font-weight:600;"
        f"text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;'>"
        f"🎛️  Dashboard Filters</div>",
        unsafe_allow_html=True,
    )

    all_modes    = sorted(RAW["Shipping Mode"].dropna().unique())
    sel_modes    = st.multiselect("🚛  Shipping Mode",    all_modes,    default=all_modes)

    all_markets  = sorted(RAW["Market"].dropna().unique())
    sel_markets  = st.multiselect("🌍  Market",           all_markets,  default=all_markets)

    all_regions  = sorted(RAW["Order Region"].dropna().unique())
    sel_regions  = st.multiselect("📍  Order Region",     all_regions,  default=all_regions)

    all_segments = sorted(RAW["Customer Segment"].dropna().unique())
    sel_segments = st.multiselect("👤  Customer Segment", all_segments, default=all_segments)

    all_quarters = ["Q1","Q2","Q3","Q4"]
    sel_quarters = st.multiselect(
        "📅  Quarter (Simulated)", all_quarters, default=all_quarters,
        help="Dataset has no date column — rows are split into 4 equal quarters as a proxy.",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:.78rem;color:{COLORS['muted']};line-height:1.8;'>"
        f"📦 Total records: <strong style='color:#F1F5F9;'>{TOTAL_RECORDS:,}</strong><br/>"
        f"⚙️  Version: <strong style='color:#F1F5F9;'>2.1</strong></div>",
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ═════════════════════════════════════════════════════════════════════════════
df = RAW[
    RAW["Shipping Mode"].isin(sel_modes)      &
    RAW["Market"].isin(sel_markets)            &
    RAW["Order Region"].isin(sel_regions)      &
    RAW["Customer Segment"].isin(sel_segments) &
    RAW["Quarter"].isin(sel_quarters)
].copy()

if df.empty:
    st.warning("⚠️  No data matches the current filters. Please widen your selection.")
    st.stop()

N = len(df)


# ═════════════════════════════════════════════════════════════════════════════
# KPI CALCULATIONS
# ═════════════════════════════════════════════════════════════════════════════
on_time_rate    = df["Is_OnTime"].mean() * 100
late_risk_ratio = df["Is_Late"].mean()   * 100
sla_compliance  = df["SLA_Compliant"].mean() * 100
early_rate      = df["Is_Early"].mean()  * 100

delayed_only    = df[df["Delivery Gap"] > 0]["Delivery Gap"]
avg_delay       = delayed_only.mean() if len(delayed_only) else 0.0

avg_real        = df["Days for shipping (real)"].mean()
avg_sched       = df["Days for shipment (scheduled)"].mean()
eff_index       = (avg_sched - avg_real) / avg_sched * 100

mode_risk       = df.groupby("Shipping Mode")["Is_Late"].mean() * 100
best_mode       = mode_risk.idxmin()
worst_mode      = mode_risk.idxmax()

region_risk     = df.groupby("Order Region")["Is_Late"].mean() * 100
worst_region    = region_risk.idxmax()
best_region     = region_risk.idxmin()

# ── Fix 3: department insight using idxmax ────────────────────────────────────
worst_dept = (
    df.groupby("Department Name")["Is_Late"]
      .mean()
      .idxmax()
)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="
  background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #0F172A 100%);
  border: 1px solid {COLORS['border']};
  border-radius: 16px;
  padding: 24px 28px;
  display: flex; align-items: center; gap: 18px;
  margin-bottom: 6px;
">
  <div style="font-size:3rem;line-height:1;">🚢</div>
  <div>
    <div style="font-size:1.55rem;font-weight:700;color:{COLORS['text']};letter-spacing:-.02em;">
      APL Logistics — Supply Chain Intelligence
    </div>
    <div style="font-size:.88rem;color:{COLORS['muted']};margin-top:3px;">
      Delivery Performance · Risk Analysis · Shipping Mode Benchmarking · Regional Heatmaps
    </div>
  </div>
  <div style="margin-left:auto;text-align:right;">
    <div style="font-size:1.4rem;font-weight:700;color:{COLORS['accent']};">{N:,}</div>
    <div style="font-size:.72rem;color:{COLORS['muted']};text-transform:uppercase;letter-spacing:.06em;">
      Filtered Shipments
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# KPI SCORECARDS
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="sec-hdr">
  <div>
    <h3>📊 Key Performance Indicators</h3>
    <p>Aggregated across {N:,} filtered shipments</p>
  </div>
</div>
""", unsafe_allow_html=True)


def kpi_card(icon, label, value, sub, sub_cls, bar_color):
    return (
        f'<div class="kpi-wrap">'
        f'  <div class="kpi-bar" style="background:{bar_color};"></div>'
        f'  <div class="kpi-icon">{icon}</div>'
        f'  <div class="kpi-val">{value}</div>'
        f'  <div class="kpi-label">{label}</div>'
        f'  <div class="kpi-sub {sub_cls}">{sub}</div>'
        f'</div>'
    )


k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(kpi_card(
        "✅", "On-Time Delivery", f"{on_time_rate:.1f}%",
        "▲ Target ≥ 70%" if on_time_rate >= 70 else "▼ Below Target",
        "good" if on_time_rate >= 70 else "bad",
        COLORS["green"],
    ), unsafe_allow_html=True)

with k2:
    st.markdown(kpi_card(
        "⚠️", "Late Risk Ratio", f"{late_risk_ratio:.1f}%",
        "High Risk" if late_risk_ratio > 55 else ("Moderate" if late_risk_ratio > 40 else "Low Risk"),
        "bad" if late_risk_ratio > 55 else ("warn" if late_risk_ratio > 40 else "good"),
        COLORS["red"],
    ), unsafe_allow_html=True)

with k3:
    st.markdown(kpi_card(
        "🕐", "Avg Delay (Late)", f"{avg_delay:.2f}d",
        f"{len(delayed_only):,} delayed shipments",
        "warn",
        COLORS["yellow"],
    ), unsafe_allow_html=True)

with k4:
    st.markdown(kpi_card(
        "📋", "SLA Compliance", f"{sla_compliance:.1f}%",
        "Actual ≤ Scheduled",
        "good" if sla_compliance >= 60 else "bad",
        COLORS["accent"],
    ), unsafe_allow_html=True)

with k5:
    st.markdown(kpi_card(
        "⚡", "Shipping Efficiency", f"{eff_index:+.1f}%",
        f"Best mode: {best_mode.split()[0]}",
        "good" if eff_index >= 0 else "bad",
        COLORS["purple"],
    ), unsafe_allow_html=True)

with k6:
    st.markdown(kpi_card(
        "🚀", "Early Delivery", f"{early_rate:.1f}%",
        "Arrived before schedule",
        "info",
        "#06B6D4",
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 Delivery Performance",
    "⚠️ Delay Risk Analysis",
    "🚛 Shipping Mode",
    "🌍 Regional Heatmaps",
    "🔬 Data Explorer",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — DELIVERY PERFORMANCE OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>📦 Delivery Performance Overview</h3>
      <p>On-time vs late · Status breakdown · Quarter trend · Order type split</p>
    </div></div>""", unsafe_allow_html=True)

    # ── Row 1 ─────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1.1, 1.3, 1.6])

    # Donut — delivery performance split
    with c1:
        perf = df["Delivery Performance"].value_counts().reset_index()
        perf.columns = ["Status", "Count"]
        cmap = {"On-Time": COLORS["green"], "Delayed": COLORS["red"], "Early": COLORS["accent"]}
        fig = px.pie(
            perf, names="Status", values="Count",
            color="Status", color_discrete_map=cmap,
            hole=0.58, title="Delivery Performance Split",
        )
        fig.update_traces(
            textinfo="percent+label", textfont_size=11,
            marker=dict(line=dict(color=COLORS["bg"], width=2)),
            pull=[0.03 if s == "Delayed" else 0 for s in perf["Status"]],
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            showlegend=False,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Delivery Performance Split",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            annotations=[dict(
                text=f"<b>{on_time_rate:.0f}%</b><br>On-Time",
                x=0.5, y=0.5, font_size=13,
                font_color=COLORS["text"], showarrow=False,
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Horizontal bar — delivery status breakdown
    with c2:
        status = df["Delivery Status"].value_counts().reset_index()
        status.columns = ["Status", "Count"]
        sc = {
            "Late delivery":     COLORS["red"],
            "Shipping on time":  COLORS["green"],
            "Advance shipping":  COLORS["accent"],
            "Shipping canceled": COLORS["yellow"],
        }
        fig = px.bar(
            status.sort_values("Count"), x="Count", y="Status",
            orientation="h", color="Status", color_discrete_map=sc,
            title="Delivery Status Breakdown", text="Count",
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside", marker_line_width=0)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            showlegend=False,
            margin=dict(t=45, b=10, l=10, r=50),
            title=dict(text="Delivery Status Breakdown",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig.update_xaxes(gridcolor=COLORS["grid"])
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    # Line — quarterly KPI trend
    with c3:
        q_trend = df.groupby("Quarter").agg(
            On_Time   = ("Is_OnTime",    "mean"),
            Late_Risk = ("Is_Late",      "mean"),
            SLA       = ("SLA_Compliant","mean"),
        ).reset_index()
        q_trend[["On_Time","Late_Risk","SLA"]] *= 100

        fig = go.Figure()
        for col, name, color in [
            ("On_Time",   "On-Time Rate",   COLORS["green"]),
            ("Late_Risk", "Late Risk",      COLORS["red"]),
            ("SLA",       "SLA Compliance", COLORS["accent"]),
        ]:
            fig.add_trace(go.Scatter(
                x=q_trend["Quarter"], y=q_trend[col], name=name,
                mode="lines+markers+text",
                line=dict(color=color, width=2.5),
                marker=dict(size=8, color=color, line=dict(color=COLORS["bg"], width=2)),
                text=q_trend[col].round(1).astype(str) + "%",
                textposition="top center", textfont=dict(size=10, color=color),
            ))
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Quarterly Delivery KPI Trend (%)",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"], range=[0, 110])
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2 ─────────────────────────────────────────────────────────────────
    c4, c5 = st.columns([2, 1])

    # Grouped bar — segment × quarter risk
    with c4:
        seg_q = df.groupby(["Quarter","Customer Segment"])["Is_Late"].mean().reset_index()
        seg_q["Late Risk %"] = seg_q["Is_Late"] * 100
        fig = px.bar(
            seg_q, x="Quarter", y="Late Risk %",
            color="Customer Segment", barmode="group",
            title="Late Risk % — Customer Segment × Quarter",
            color_discrete_sequence=[COLORS["accent"], COLORS["green"], COLORS["yellow"]],
            text=seg_q["Late Risk %"].round(1).astype(str) + "%",
        )
        fig.update_traces(textposition="outside", textfont_size=10, marker_line_width=0)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            bargap=0.25,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Late Risk % — Customer Segment × Quarter",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"], range=[0, 115])
        st.plotly_chart(fig, use_container_width=True)

    # Bar — late risk by payment type
    with c5:
        type_perf = df.groupby("Type")["Is_Late"].mean().reset_index()
        type_perf["Late Risk %"] = type_perf["Is_Late"] * 100
        fig = px.bar(
            type_perf, x="Type", y="Late Risk %",
            color="Late Risk %",
            color_continuous_scale=[[0,COLORS["green"]],[0.5,COLORS["yellow"]],[1,COLORS["red"]]],
            title="Late Risk by Payment Type",
            text=type_perf["Late Risk %"].round(1).astype(str) + "%",
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Late Risk by Payment Type",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"], range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    # Insight
    top_q = q_trend.loc[q_trend["On_Time"].idxmax(), "Quarter"]
    st.markdown(f"""
    <div class="insight">
      📌 <strong>Analyst Insight:</strong> On-time delivery rate stands at
      <strong>{on_time_rate:.1f}%</strong>. The highest performing quarter is
      <strong>{top_q}</strong>. Late delivery risk is
      {'elevated at ' if late_risk_ratio > 50 else 'at '}
      <strong>{late_risk_ratio:.1f}%</strong>
      — {'action required to improve SLA adherence.' if late_risk_ratio > 50 else 'within acceptable bounds.'}
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DELAY RISK ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>⚠️ Delay Risk Analysis Dashboard</h3>
      <p>Risk distribution · Delay gap histograms · Actual vs Scheduled · Segment exposure</p>
    </div></div>""", unsafe_allow_html=True)

    # ── Row 1 ─────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 1.3, 1.7])

    # Donut — risk flag distribution
    with c1:
        risk_counts = df["Late_delivery_risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]
        risk_counts["Label"] = risk_counts["Risk"].map({1: "At Risk", 0: "Not at Risk"})
        fig = px.pie(
            risk_counts, names="Label", values="Count",
            color="Label",
            color_discrete_map={"At Risk": COLORS["red"], "Not at Risk": COLORS["green"]},
            hole=0.55, title="Late Delivery Risk Distribution",
        )
        fig.update_traces(
            textinfo="percent+label", textfont_size=12,
            marker=dict(line=dict(color=COLORS["bg"], width=2)),
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            showlegend=False,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Late Delivery Risk Distribution",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            annotations=[dict(
                text=f"<b>{late_risk_ratio:.0f}%</b><br>At Risk",
                x=0.5, y=0.5, font_size=13,
                font_color=COLORS["red"], showarrow=False,
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Overlapping histogram — delivery gap
    with c2:
        late_df  = df[df["Delivery Gap"] > 0]
        mean_gap = late_df["Delivery Gap"].mean() if len(late_df) else 0

        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df["Delivery Gap"], name="All", nbinsx=10,
            marker_color=COLORS["accent"], opacity=0.4,
            hovertemplate="Gap: %{x}d<br>Count: %{y:,}<extra>All</extra>",
        ))
        fig.add_trace(go.Histogram(
            x=late_df["Delivery Gap"], name="Late Only", nbinsx=8,
            marker_color=COLORS["red"], opacity=0.75,
            hovertemplate="Gap: %{x}d<br>Count: %{y:,}<extra>Late</extra>",
        ))
        fig.add_vline(
            x=mean_gap, line_dash="dash", line_color=COLORS["yellow"],
            annotation_text=f"μ={mean_gap:.1f}d",
            annotation_font_color=COLORS["yellow"],
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            barmode="overlay",
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Delivery Gap Distribution (Days)",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(title_text="Delivery Gap (Days)", gridcolor=COLORS["grid"])
        fig.update_yaxes(title_text="Shipments",           gridcolor=COLORS["grid"])
        st.plotly_chart(fig, use_container_width=True)

    # Scatter — scheduled vs actual
    with c3:
        sample = df.sample(min(5000, N), random_state=42)
        fig = px.scatter(
            sample,
            x="Days for shipment (scheduled)",
            y="Days for shipping (real)",
            color="Delivery Performance",
            color_discrete_map={
                "On-Time": COLORS["green"],
                "Delayed": COLORS["red"],
                "Early":   COLORS["accent"],
            },
            opacity=0.4,
            title="Scheduled vs Actual Shipping Days",
            labels={
                "Days for shipment (scheduled)": "Scheduled Days",
                "Days for shipping (real)":      "Actual Days",
            },
        )
        mv = max(
            sample["Days for shipment (scheduled)"].max(),
            sample["Days for shipping (real)"].max(),
        )
        fig.add_shape(type="line", x0=0, y0=0, x1=mv, y1=mv,
                      line=dict(color=COLORS["muted"], dash="dash", width=1.5))
        fig.add_annotation(x=mv * 0.85, y=mv * 0.75, text="SLA Line",
                           font_color=COLORS["muted"], showarrow=False, font_size=10)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=300,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Scheduled vs Actual Shipping Days",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(gridcolor=COLORS["grid"])
        fig.update_yaxes(gridcolor=COLORS["grid"])
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2 ─────────────────────────────────────────────────────────────────
    c4, c5 = st.columns([1.5, 1.5])

    # Heatmap — segment × quarter risk
    with c4:
        pivot = (
            df.pivot_table(
                index="Customer Segment", columns="Quarter",
                values="Is_Late", aggfunc="mean",
            ) * 100
        )
        fig = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0,COLORS["green"]],[0.4,COLORS["yellow"]],[1,COLORS["red"]]],
            text=np.round(pivot.values, 1),
            texttemplate="%{text}%", textfont_size=13,
            colorbar=dict(
                title=dict(text="Risk %",  font=dict(color=COLORS["muted"])),
                tickfont=dict(color=COLORS["muted"]),
            ),
            hovertemplate="Segment: %{y}<br>Quarter: %{x}<br>Risk: %{z:.1f}%<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=280,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Late Risk Heatmap — Segment × Quarter",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig.update_xaxes(side="top")
        st.plotly_chart(fig, use_container_width=True)

    # Bar — department risk
    with c5:
        dept_risk = (
            df.groupby("Department Name")["Is_Late"]
              .mean()
              .reset_index()
        )
        dept_risk["Late Risk %"] = dept_risk["Is_Late"] * 100
        dept_risk = dept_risk.sort_values("Late Risk %", ascending=True)

        fig = px.bar(
            dept_risk, x="Late Risk %", y="Department Name",
            orientation="h",
            color="Late Risk %",
            color_continuous_scale=[[0,COLORS["green"]],[0.5,COLORS["yellow"]],[1,COLORS["red"]]],
            title="Late Risk % by Department",
            text=dept_risk["Late Risk %"].round(1).astype(str) + "%",
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=280,
            margin=dict(t=45, b=10, l=10, r=55),
            title=dict(text="Late Risk % by Department",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig.update_xaxes(gridcolor=COLORS["grid"], range=[0, 105])
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
      📌 <strong>Analyst Insight:</strong> The mean delay on late shipments is
      <strong>{avg_delay:.2f} days</strong>. Highest risk department:
      <strong>{worst_dept}</strong>. The SLA reference line in the scatter chart shows
      shipments above the diagonal are all delayed — these represent your primary
      intervention opportunities.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — SHIPPING MODE COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>🚛 Shipping Mode Comparison</h3>
      <p>SLA compliance · Mode-wise delay performance · Efficiency benchmarking · Cost vs risk</p>
    </div></div>""", unsafe_allow_html=True)

    mode_stats = df.groupby("Shipping Mode").agg(
        Total      = ("Is_Late",                        "count"),
        Late_Risk  = ("Is_Late",                        "mean"),
        On_Time    = ("Is_OnTime",                      "mean"),
        SLA        = ("SLA_Compliant",                  "mean"),
        Avg_Real   = ("Days for shipping (real)",        "mean"),
        Avg_Sched  = ("Days for shipment (scheduled)",   "mean"),
        Avg_Gap    = ("Delivery Gap",                   "mean"),
        Avg_Sales  = ("Sales",                          "mean"),
        Avg_Profit = ("Order Profit Per Order",         "mean"),
    ).reset_index()

    for c in ["Late_Risk","On_Time","SLA"]:
        mode_stats[c] *= 100
    mode_stats["Eff_Index"] = (
        (mode_stats["Avg_Sched"] - mode_stats["Avg_Real"])
        / mode_stats["Avg_Sched"] * 100
    )

    mode_colors = {
        "First Class":    COLORS["accent"],
        "Second Class":   COLORS["yellow"],
        "Standard Class": COLORS["green"],
    }

    # ── Row 1 ─────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    # Grouped bar — SLA / on-time / late risk by mode
    with c1:
        fig = go.Figure()
        for _, row in mode_stats.iterrows():
            fig.add_trace(go.Bar(
                name=row["Shipping Mode"],
                x=["SLA Compliance","On-Time Rate","Late Risk"],
                y=[row["SLA"], row["On_Time"], row["Late_Risk"]],
                marker_color=mode_colors.get(row["Shipping Mode"], COLORS["accent"]),
                text=[f"{v:.1f}%" for v in [row["SLA"], row["On_Time"], row["Late_Risk"]]],
                textposition="outside",
            ))
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=310,
            barmode="group",
            bargap=0.2,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="SLA / On-Time / Late Risk by Mode",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"], range=[0, 115])
        st.plotly_chart(fig, use_container_width=True)

    # Overlay bar — scheduled vs actual days
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Avg Scheduled",
            x=mode_stats["Shipping Mode"],
            y=mode_stats["Avg_Sched"],
            marker_color=COLORS["muted"], opacity=0.5,
        ))
        fig.add_trace(go.Bar(
            name="Avg Actual",
            x=mode_stats["Shipping Mode"],
            y=mode_stats["Avg_Real"],
            marker_color=mode_stats["Shipping Mode"].map(mode_colors).tolist(),
            text=mode_stats["Avg_Real"].round(2).astype(str) + "d",
            textposition="outside",
        ))
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=310,
            barmode="overlay",
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Avg Scheduled vs Actual Days",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"])
        st.plotly_chart(fig, use_container_width=True)

    # Radar — mode performance
    with c3:
        cats       = ["On-Time Rate","SLA Compliance","Efficiency","Low Risk","Avg Profit"]
        max_profit = mode_stats["Avg_Profit"].max()

        fig = go.Figure()
        for _, row in mode_stats.iterrows():
            mode = row["Shipping Mode"]
            r = [
                row["On_Time"],
                row["SLA"],
                min(max(row["Eff_Index"] + 50, 0), 100),
                100 - row["Late_Risk"],
                (row["Avg_Profit"] / max_profit * 100) if max_profit > 0 else 50,
            ]
            fig.add_trace(go.Scatterpolar(
                r=r + [r[0]], theta=cats + [cats[0]],
                name=mode, fill="toself", opacity=0.35,
                line=dict(color=mode_colors.get(mode, COLORS["accent"]), width=2.5),
            ))
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=310,
            margin=dict(t=50, b=10, l=30, r=30),
            title=dict(text="Mode Performance Radar",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    gridcolor=COLORS["grid"],
                    range=[0, 110],
                    tickfont=dict(color=COLORS["muted"]),
                ),
                angularaxis=dict(
                    gridcolor=COLORS["border"],
                    tickfont=dict(color=COLORS["text"], size=10),
                ),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2 ─────────────────────────────────────────────────────────────────
    c4, c5 = st.columns(2)

    # Box — shipping duration distribution
    with c4:
        fig = px.box(
            df, x="Shipping Mode", y="Days for shipping (real)",
            color="Shipping Mode", color_discrete_map=mode_colors,
            points=False, title="Shipping Duration Distribution (Actual Days)",
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=280,
            showlegend=False,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Shipping Duration Distribution (Actual Days)",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"])
        st.plotly_chart(fig, use_container_width=True)

    # Line — quarterly late risk trend by mode
    with c5:
        mode_q = df.groupby(["Quarter","Shipping Mode"])["Is_Late"].mean().reset_index()
        mode_q["Late Risk %"] = mode_q["Is_Late"] * 100
        fig = px.line(
            mode_q, x="Quarter", y="Late Risk %",
            color="Shipping Mode", color_discrete_map=mode_colors,
            markers=True, title="Late Risk Trend by Mode (Quarterly)",
            text=mode_q["Late Risk %"].round(1).astype(str) + "%",
        )
        fig.update_traces(marker_size=8, textposition="top center", textfont_size=10)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=280,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Late Risk Trend by Mode (Quarterly)",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
                        borderwidth=1, font=dict(size=11)),
        )
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(gridcolor=COLORS["grid"], range=[0, 110])
        st.plotly_chart(fig, use_container_width=True)

    # Mode summary table
    st.markdown("<br>", unsafe_allow_html=True)
    tbl = mode_stats[[
        "Shipping Mode","Total","On_Time","Late_Risk","SLA",
        "Avg_Real","Avg_Gap","Avg_Sales",
    ]].copy()
    tbl.columns = [
        "Mode","Shipments","On-Time %","Late Risk %","SLA %",
        "Avg Days","Avg Gap","Avg Sales $",
    ]
    for c in ["On-Time %","Late Risk %","SLA %"]:
        tbl[c] = tbl[c].round(1)
    for c in ["Avg Days","Avg Gap","Avg Sales $"]:
        tbl[c] = tbl[c].round(2)
    st.dataframe(tbl, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="insight">
      📌 <strong>Analyst Insight:</strong>
      <strong>{best_mode}</strong> achieves the lowest late-delivery risk at
      <strong>{mode_risk.min():.1f}%</strong>, while
      <strong>{worst_mode}</strong> has the highest at
      <strong>{mode_risk.max():.1f}%</strong>.
      Shipping Efficiency Index: <strong>{eff_index:+.1f}%</strong>
      {'— actual days shorter than scheduled on average, indicating conservative SLA setting.'
       if eff_index > 0 else '— actual days exceed scheduled, indicating SLA pressure.'}
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — REGIONAL & MARKET HEATMAPS
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>🌍 Regional & Market Delay Intelligence</h3>
      <p>Geographic delay index · Market efficiency matrix · Region × Market heatmap</p>
    </div></div>""", unsafe_allow_html=True)

    # ── Row 1 ─────────────────────────────────────────────────────────────────
    c1, c2 = st.columns([1.4, 1.6])

    # Horizontal bar — all 23 regions
    with c1:
        region_stats = df.groupby("Order Region").agg(
            Total     = ("Is_Late","count"),
            Late_Risk = ("Is_Late","mean"),
            Avg_Gap   = ("Delivery Gap","mean"),
            On_Time   = ("Is_OnTime","mean"),
        ).reset_index()
        region_stats["Late Risk %"] = region_stats["Late_Risk"] * 100
        region_stats["On-Time %"]   = region_stats["On_Time"]   * 100
        region_stats = region_stats.sort_values("Late Risk %", ascending=True)

        fig = px.bar(
            region_stats,
            x="Late Risk %", y="Order Region", orientation="h",
            color="Late Risk %",
            color_continuous_scale=[[0,COLORS["green"]],[0.45,COLORS["yellow"]],[1,COLORS["red"]]],
            title="Regional Late Delivery Risk Index (%)",
            text=region_stats["Late Risk %"].round(1).astype(str) + "%",
            hover_data={"Total": True, "Avg_Gap": ":.2f"},
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color=COLORS["text"]),
            marker_line_width=0,
        )
        fig.update_coloraxes(showscale=False)
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=560,
            margin=dict(t=45, b=10, l=10, r=55),
            title=dict(text="Regional Late Delivery Risk Index (%)",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig.update_xaxes(gridcolor=COLORS["grid"], range=[0, 110])
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        market_stats = df.groupby("Market").agg(
            Total     = ("Is_Late","count"),
            Late_Risk = ("Is_Late","mean"),
            Avg_Gap   = ("Delivery Gap","mean"),
            On_Time   = ("Is_OnTime","mean"),
            Avg_Sales = ("Sales","mean"),
        ).reset_index()
        market_stats["Late Risk %"] = market_stats["Late_Risk"] * 100
        market_stats["On-Time %"]   = market_stats["On_Time"]   * 100
        market_stats["Vol %"]       = (
            market_stats["Total"] / market_stats["Total"].sum() * 100
        )

        # Bubble chart — market efficiency matrix
        fig = px.scatter(
            market_stats,
            x="Avg_Gap", y="On-Time %",
            size="Vol %", color="Late Risk %",
            text="Market",
            color_continuous_scale=[[0,COLORS["green"]],[0.45,COLORS["yellow"]],[1,COLORS["red"]]],
            title="Market Efficiency Matrix",
            labels={
                "Avg_Gap":    "Avg Delay Gap (Days)",
                "On-Time %":  "On-Time Rate (%)",
            },
            size_max=55,
        )
        fig.update_traces(
            textposition="top center",
            textfont=dict(color=COLORS["text"], size=12, family="Inter"),
            marker_line_color=COLORS["bg"], marker_line_width=2,
        )
        fig.update_coloraxes(
            colorbar=dict(
                title=dict(text="Late Risk %", font=dict(color=COLORS["muted"])),
                tickfont=dict(color=COLORS["muted"]),
            )
        )
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=310,
            margin=dict(t=70, b=10, l=10, r=10),
            title=dict(
                text="Market Efficiency Matrix<br>"
                     "<sup>Bubble size = shipment volume | Color = late risk</sup>",
                font=dict(size=14, color=COLORS["text"]),
                x=0.02, xanchor="left",
            ),
        )
        fig.update_xaxes(gridcolor=COLORS["grid"])
        fig.update_yaxes(gridcolor=COLORS["grid"])
        st.plotly_chart(fig, use_container_width=True)

        # Bar — market late risk
        ms_sorted = market_stats.sort_values("Late Risk %", ascending=False)
        fig2 = px.bar(
            ms_sorted, x="Market", y="Late Risk %",
            color="Late Risk %",
            color_continuous_scale=[[0,COLORS["green"]],[0.5,COLORS["yellow"]],[1,COLORS["red"]]],
            title="Late Risk % by Market",
            text=ms_sorted["Late Risk %"].round(1).astype(str) + "%",
        )
        fig2.update_traces(textposition="outside", marker_line_width=0)
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=230,
            margin=dict(t=45, b=10, l=10, r=10),
            title=dict(text="Late Risk % by Market",
                       font=dict(size=14, color=COLORS["text"]),
                       x=0.02, xanchor="left"),
        )
        fig2.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig2.update_yaxes(gridcolor=COLORS["grid"], range=[0, 105])
        st.plotly_chart(fig2, use_container_width=True)

    # ── Market × Region heatmap ────────────────────────────────────────────────
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>🗺️ Market × Region Late Risk Heatmap</h3>
      <p>Full cross-dimensional delay intensity map</p>
    </div></div>""", unsafe_allow_html=True)

    pivot_mr = (
        df.pivot_table(
            index="Market", columns="Order Region",
            values="Is_Late", aggfunc="mean",
        ) * 100
    )
    fig = go.Figure(go.Heatmap(
        z=pivot_mr.values,
        x=pivot_mr.columns.tolist(),
        y=pivot_mr.index.tolist(),
        colorscale=[
            [0,   COLORS["green"]],
            [0.35, COLORS["yellow"]],
            [0.6,  COLORS["red"]],
            [1,   "#7F0000"],
        ],
        text=np.round(pivot_mr.fillna(0).values, 1),
        texttemplate="%{text}%", textfont_size=9,
        colorbar=dict(
            title=dict(text="Late Risk %", font=dict(color=COLORS["muted"])),
            tickfont=dict(color=COLORS["muted"]),
        ),
        hovertemplate="Market: %{y}<br>Region: %{x}<br>Risk: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_TEMPLATE["layout"],
        height=320,
        margin=dict(t=50, b=100, l=80, r=10),
        title=dict(text="Market × Region Late Delivery Risk Heatmap",
                   font=dict(size=14, color=COLORS["text"]),
                   x=0.02, xanchor="left"),
    )
    fig.update_xaxes(tickangle=-38, tickfont=dict(size=10), side="bottom",
                     gridcolor="rgba(0,0,0,0)")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Choropleth — by order country ─────────────────────────────────────────
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>🗺️ Geographic Delay Map — By Order Country</h3>
      <p>Choropleth of late delivery risk across order destination countries</p>
    </div></div>""", unsafe_allow_html=True)

    country_risk = df.groupby("Order Country").agg(
        Late_Risk = ("Is_Late","mean"),
        Total     = ("Is_Late","count"),
    ).reset_index()
    country_risk["Late Risk %"] = country_risk["Late_Risk"] * 100

    fig = px.choropleth(
        country_risk,
        locations="Order Country", locationmode="country names",
        color="Late Risk %",
        hover_name="Order Country",
        hover_data={"Total": True, "Late Risk %": ":.1f"},
        color_continuous_scale=[[0,COLORS["green"]],[0.4,COLORS["yellow"]],[1,COLORS["red"]]],
        title="Late Delivery Risk by Destination Country",
    )
    fig.update_layout(
        **PLOTLY_TEMPLATE["layout"],
        height=420,
        margin=dict(t=45, b=5, l=0, r=0),
        title=dict(text="Late Delivery Risk by Destination Country",
                   font=dict(size=14, color=COLORS["text"]),
                   x=0.02, xanchor="left"),
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="rgba(0,0,0,0)",
            landcolor="#1E293B",
            showframe=False,
            showcountries=True,
            countrycolor=COLORS["border"],
            showcoastlines=False,
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Late Risk %", font=dict(color=COLORS["muted"])),
            tickfont=dict(color=COLORS["muted"]),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
      📌 <strong>Analyst Insight:</strong>
      Worst performing region: <strong>{worst_region}</strong>
      ({region_risk.max():.1f}% late risk).
      Best performing region: <strong>{best_region}</strong>
      ({region_risk.min():.1f}% late risk).
      The choropleth above highlights countries requiring priority logistics review.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>🔬 Data Explorer & Operational Scorecard</h3>
      <p>Drill-down summary · Export-ready · Full filtered dataset</p>
    </div></div>""", unsafe_allow_html=True)

    # Summary table
    summary = df.groupby(
        ["Market","Order Region","Shipping Mode","Customer Segment"]
    ).agg(
        Shipments      = ("Is_Late",                       "count"),
        On_Time_Rate   = ("Is_OnTime",                     "mean"),
        Late_Risk      = ("Is_Late",                       "mean"),
        SLA_Compliance = ("SLA_Compliant",                 "mean"),
        Avg_Delay_Days = ("Delivery Gap",                  "mean"),
        Avg_Real_Days  = ("Days for shipping (real)",       "mean"),
        Avg_Sched_Days = ("Days for shipment (scheduled)",  "mean"),
        Avg_Sales      = ("Sales",                         "mean"),
        Avg_Profit     = ("Order Profit Per Order",        "mean"),
    ).reset_index()

    for c in ["On_Time_Rate","Late_Risk","SLA_Compliance"]:
        summary[c] = (summary[c] * 100).round(1).astype(str) + "%"
    for c in ["Avg_Delay_Days","Avg_Real_Days","Avg_Sched_Days","Avg_Sales","Avg_Profit"]:
        summary[c] = summary[c].round(2)

    summary.columns = [
        "Market","Region","Shipping Mode","Segment","Shipments",
        "On-Time %","Late Risk %","SLA %",
        "Avg Delay (d)","Avg Actual (d)","Avg Scheduled (d)",
        "Avg Sales $","Avg Profit $",
    ]

    # Live search filter
    search = st.text_input(
        "🔍  Filter table (search any column):",
        placeholder="e.g. LATAM, First Class, Consumer…",
    )
    if search:
        mask = summary.apply(
            lambda col: col.astype(str).str.contains(search, case=False)
        ).any(axis=1)
        tbl_show = summary[mask]
    else:
        tbl_show = summary

    st.dataframe(
        tbl_show.sort_values("Shipments", ascending=False),
        use_container_width=True,
        height=360,
        hide_index=True,
    )

    col_dl1, col_dl2, _ = st.columns([1, 1, 3])
    with col_dl1:
        st.download_button(
            "⬇️  Download Summary CSV",
            summary.to_csv(index=False).encode("utf-8"),
            "apl_summary.csv", "text/csv",
        )
    with col_dl2:
        raw_cols = [
            "Market","Order Region","Shipping Mode","Customer Segment",
            "Delivery Performance","Delivery Status","Late_delivery_risk",
            "Delivery Gap","Days for shipping (real)","Days for shipment (scheduled)",
            "Sales","Order Profit Per Order","Quarter",
        ]
        st.download_button(
            "⬇️  Download Filtered Raw Data",
            df[raw_cols].to_csv(index=False).encode("utf-8"),
            "apl_filtered.csv", "text/csv",
        )

    # Quick numeric stats
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-hdr"><div>
      <h3>📈 Quick Statistical Summary</h3>
      <p>Numeric column statistics for the filtered dataset</p>
    </div></div>""", unsafe_allow_html=True)

    num_cols = [
        "Days for shipping (real)","Days for shipment (scheduled)",
        "Delivery Gap","Sales","Order Profit Per Order","Order Item Quantity",
    ]
    st.dataframe(df[num_cols].describe().round(3), use_container_width=True, height=280)


# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="
  border-top: 1px solid {COLORS['border']};
  padding: 16px 0 4px;
  text-align: center;
  font-size: .78rem;
  color: {COLORS['muted']};
">
  APL Logistics Supply Chain Intelligence Dashboard v2.1 &nbsp;·&nbsp;
  Displaying <strong style='color:{COLORS['text']};'>{N:,}</strong> of
  <strong style='color:{COLORS['text']};'>{TOTAL_RECORDS:,}</strong> shipments
  &nbsp;·&nbsp; 5 Modules &nbsp;·&nbsp; Built with Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
