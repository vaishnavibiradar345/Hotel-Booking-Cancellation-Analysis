import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hotel Booking Analysis",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="metric-container"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] { font-size: 13px; color: #64748b; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; }
    h2 { font-size: 16px !important; color: #1e293b; margin-bottom: 4px; }
    .insight-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        font-size: 13px;
        color: #1e40af;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking.csv")

    # Cleaning
    df['company']  = df['company'].fillna(0)
    df['agent']    = df['agent'].fillna(0)
    df['country']  = df['country'].fillna('Unknown')
    df['children'] = df['children'].fillna(0)
    df.drop_duplicates(inplace=True)
    df = df.drop(columns=['name', 'email', 'phone-number', 'credit_card'], errors='ignore')
    df = df[df['adr'] <= 520]
    df = df[~((df['adults'] == 0) & (df['children'] == 0) & (df['babies'] == 0))]
    df = df[~((df['adults'] == 0) & ((df['children'] != 0) | (df['babies'] != 0)))]
    df = df[df['adr'] >= 0]

    # Feature engineering
    df['total_stay_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['total_guests']      = df['adults'] + df['children'] + df['babies']
    df['is_family']         = ((df['children'] > 0) | (df['babies'] > 0)).astype(int)

    intervals = [0, 7, 30, 90, 300, 700]
    labels    = ['0–7', '8–30', '31–90', '91–300', '301+']
    df['lead_time_bin'] = pd.cut(df['lead_time'], bins=intervals, labels=labels)

    month_order = [
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ]
    df['arrival_date_month'] = pd.Categorical(
        df['arrival_date_month'], categories=month_order, ordered=True
    )
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏨 Hotel Booking")
    st.caption("EDA Dashboard")
    st.divider()

    hotel_opts = list(df['hotel'].unique())
    hotel_filter = st.multiselect("Hotel Type", options=hotel_opts, default=hotel_opts)

    year_opts = sorted(df['arrival_date_year'].unique())
    year_filter = st.multiselect("Year", options=year_opts, default=year_opts)

    st.divider()
    st.caption("Data: Hotel Booking Demand Dataset (Kaggle)\n\n[📓 View Notebook](https://github.com/)")

fdf = df[df['hotel'].isin(hotel_filter) & df['arrival_date_year'].isin(year_filter)]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Hotel Booking")

st.divider()

# ── KPI row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Bookings",    f"{len(fdf):,}")
c2.metric("Cancellation Rate", f"{fdf['is_canceled'].mean():.1%}")
c3.metric("Avg Daily Rate",    f"€{fdf['adr'].mean():.0f}")
c4.metric("Avg Stay",          f"{fdf['total_stay_nights'].mean():.1f} nights")
c5.metric("Avg Lead Time",     f"{fdf['lead_time'].mean():.0f} days")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 — Lead Time + Top Countries
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cancellation Rate by Lead Time")
    lt = fdf.groupby('lead_time_bin', observed=True)['is_canceled'].mean().reset_index()
    lt['label'] = lt['is_canceled'].apply(lambda x: f'{x:.0%}')
    fig = px.bar(
        lt, x='lead_time_bin', y='is_canceled', text='label',
        labels={'lead_time_bin': 'Lead Time (Days)', 'is_canceled': 'Cancellation Rate'},
        color='is_canceled', color_continuous_scale='Blues',
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(coloraxis_showscale=False, height=340, margin=dict(t=10, b=0))
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">📌 Cancellation risk climbs steadily with lead time — 301+ day bookings cancel at 43–75% depending on hotel type.</div>', unsafe_allow_html=True)

with col2:
    st.subheader("Top 10 Guest Countries")
    top_c = fdf['country'].value_counts().head(10).reset_index()
    top_c.columns = ['country', 'bookings']
    fig = px.bar(
        top_c, x='bookings', y='country', orientation='h',
        labels={'bookings': 'Number of Bookings', 'country': ''},
        color='bookings', color_continuous_scale='Blues'
    )
    fig.update_layout(coloraxis_showscale=False, height=340, margin=dict(t=10, b=0),
                      yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">📌 Portugal accounts for nearly 4× more bookings than any other country. Top 5 are all European.</div>', unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — Hotel Type Comparison + Monthly Pattern
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    st.subheader("City vs Resort Hotel — Key Metrics")
    kpis = fdf.groupby('hotel').agg(
        avg_adr=('adr', 'mean'),
        avg_stay=('total_stay_nights', 'mean'),
        avg_lead=('lead_time', 'mean'),
        cancel_rate=('is_canceled', 'mean')
    ).reset_index()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Avg Daily Rate (€)', 'Avg Stay (Nights)',
                        'Avg Lead Time (Days)', 'Cancellation Rate'],
        vertical_spacing=0.18, horizontal_spacing=0.12
    )
    colors = ['#1d4ed8', '#0891b2']
    for i, col_name in enumerate(['avg_adr', 'avg_stay', 'avg_lead', 'cancel_rate']):
        r, c = (i // 2) + 1, (i % 2) + 1
        fig.add_trace(go.Bar(
            x=kpis['hotel'], y=kpis[col_name],
            marker_color=colors, showlegend=False,
            text=[f"{v:.1f}" for v in kpis[col_name]],
            textposition='outside'
        ), row=r, col=c)

    fig.update_layout(height=370, margin=dict(t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">📌 City Hotel has higher ADR but 42% cancellation vs Resort\'s 28%. Resort guests stay 45% longer on average.</div>', unsafe_allow_html=True)

with col2:
    st.subheader("Monthly Cancellation Rate by Hotel")
    monthly = (
        fdf.groupby(['arrival_date_month', 'hotel'], observed=True)['is_canceled']
        .mean().reset_index()
    )
    fig = px.line(
        monthly, x='arrival_date_month', y='is_canceled', color='hotel',
        markers=True,
        labels={'arrival_date_month': '', 'is_canceled': 'Cancellation Rate', 'hotel': 'Hotel'},
        color_discrete_sequence=['#1d4ed8', '#0891b2']
    )
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(tickformat='.0%')
    fig.update_layout(height=370, margin=dict(t=10, b=0), legend=dict(x=0.01, y=0.99))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">📌 City Hotel consistently outpaces Resort Hotel in cancellations every month — this is structural, not seasonal.</div>', unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Market Segment + Special Requests
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cancellation Rate by Market Segment")
    seg = (fdf.groupby('market_segment')['is_canceled']
              .mean().sort_values(ascending=False).reset_index())
    seg = seg[seg['market_segment'] != 'Undefined']
    fig = px.bar(
        seg, x='market_segment', y='is_canceled',
        labels={'market_segment': '', 'is_canceled': 'Cancellation Rate'},
        color='is_canceled', color_continuous_scale='Reds',
        text=seg['is_canceled'].apply(lambda x: f'{x:.0%}')
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(coloraxis_showscale=False, height=340, margin=dict(t=10, b=0))
    fig.update_xaxes(tickangle=30)
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">📌 Groups (61%) and Online TA (37%) are highest risk. Direct (15%) and Corporate (19%) are most reliable.</div>', unsafe_allow_html=True)

with col2:
    st.subheader("Special Requests vs Cancellation Rate")
    sr = (fdf.groupby('total_of_special_requests')['is_canceled']
             .mean().reset_index())
    fig = px.bar(
        sr, x='total_of_special_requests', y='is_canceled',
        labels={'total_of_special_requests': 'Number of Special Requests', 'is_canceled': 'Cancellation Rate'},
        color='is_canceled', color_continuous_scale='Blues_r',
        text=sr['is_canceled'].apply(lambda x: f'{x:.0%}')
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(coloraxis_showscale=False, height=340, margin=dict(t=10, b=0))
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">📌 Every additional special request is associated with a lower cancellation rate — a clear signal of guest commitment.</div>', unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 4 — Customer Type + Repeat Guest
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cancellation Rate by Customer Type")
    ct = (fdf.groupby('customer_type')['is_canceled']
             .mean().sort_values(ascending=False).reset_index())
    fig = px.bar(
        ct, x='customer_type', y='is_canceled',
        labels={'customer_type': '', 'is_canceled': 'Cancellation Rate'},
        color='is_canceled', color_continuous_scale='Blues',
        text=ct['is_canceled'].apply(lambda x: f'{x:.0%}')
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(coloraxis_showscale=False, height=320, margin=dict(t=10, b=0))
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("New vs Repeat Guest Cancellation Rate")
    rg = fdf.groupby('is_repeated_guest')['is_canceled'].mean().reset_index()
    rg['Guest Type'] = rg['is_repeated_guest'].map({0: 'New Guest', 1: 'Repeat Guest'})
    fig = px.bar(
        rg, x='Guest Type', y='is_canceled',
        labels={'is_canceled': 'Cancellation Rate'},
        color='Guest Type',
        color_discrete_map={'New Guest': '#1d4ed8', 'Repeat Guest': '#0891b2'},
        text=rg['is_canceled'].apply(lambda x: f'{x:.0%}')
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, height=320, margin=dict(t=10, b=0))
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="insight-box">📌 Repeat guests cancel at just 15% vs 38% for new guests. Direct booking and loyalty investment have a measurable impact on cancellation rates.</div>', unsafe_allow_html=True)

st.divider()
st.caption("Built with Streamlit · Python · Plotly · Pandas | EDA Notebook: `HotelBookingDA_Enhanced.ipynb`")
