import streamlit as st
import pandas as pd
from queries import (
    run_query,
    q1_top_rated_locations,
    q2_oversaturated_locations,
    q3_online_order_vs_rating,
    q4_table_booking_vs_rating,
    q5_price_vs_satisfaction,
    q6_pricing_segment_performance,
    q7_most_common_cuisines,
    q8_top_rated_cuisines,
    q9_niche_cuisine_opportunities,
    q10_cost_vs_rating,
    q11_premium_onboarding_locations,
    q12_high_demand_low_quality,
)

st.set_page_config(
    page_title="Uber Eats Bangalore Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }

    .page-header {
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 1.5rem;
    }
    .page-title {
        font-size: 2rem; font-weight: 700;
        color: #1B263B; margin-bottom: 0.2rem;
    }
    .page-title span { color: #06B6D4; }
    .page-subtitle {
        font-size: 0.88rem; color: #6B7280;
        text-transform: uppercase; letter-spacing: 0.4px;
    }

    .metric-card {
        background: #F8F9FA;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #1B263B; }
    .metric-label {
        font-size: 0.72rem; color: #6B7280;
        text-transform: uppercase; letter-spacing: 0.5px;
    }

    .section-tag {
        font-size: 0.72rem; font-weight: 700; color: #06B6D4;
        text-transform: uppercase; letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    .section-heading {
        font-size: 1.2rem; font-weight: 700;
        color: #1B263B; margin-bottom: 0.8rem;
    }

    .insight-box {
        background: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin-top: 0.8rem;
        font-size: 0.88rem;
        color: #1E3A5F;
    }

    .stButton button {
        background-color: #1B263B;
        color: #FFFFFF;
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }
    .stButton button:hover { background-color: #06B6D4; color: #1B263B; }

    section[data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E5E7EB;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)
def get_locations() -> list:
    """Return sorted list of unique locations from DB"""
    df = run_query(
        "SELECT DISTINCT location FROM restaurants ORDER BY location"
    )
    return df["location"].tolist()


@st.cache_data(ttl=300)
def get_summary_stats() -> dict:
    """Return high-level summary metrics for the header cards."""
    df = run_query("""
        SELECT
            COUNT(*)                             AS total_restaurants,
            COUNT(DISTINCT location)             AS total_locations,
            COUNT(DISTINCT cuisines)             AS total_cuisines,
            ROUND(AVG(rate), 2)                  AS overall_avg_rating,
            SUM(
                   CASE WHEN online_order = 1 THEN 1 ELSE 0 END
            ) AS online_order_count
        FROM restaurants
    """)
    return df.iloc[0].to_dict()


def render_header(title: str, subtitle: str) -> None:
    """Render a consistent page header across all pages."""
    parts = title.split(" ", 1)
    colored = (
        f"<span>{parts[0]}</span> {parts[1]}" if len(parts) > 1 else title
    )

    st.markdown(
        f"""
    <div class="page-header">
        <div class="page-title">{colored}</div>
        <div class="page-subtitle">{subtitle}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_metric_row(stats: dict) -> None:
    """Render the 5 summary metric cards at the top of every page."""
    cols = st.columns(5)
    metrics = [
        (f"{int(stats['total_restaurants']):,}", "Total Restaurants"),
        (int(stats["total_locations"]), "Locations"),
        (int(stats["total_cuisines"]), "Cuisine Types"),
        (stats["overall_avg_rating"], "Avg Rating"),
        (f"{int(stats['online_order_count']):,}", "Online Order Enabled"),
    ]
    for col, (value, label) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def show_dataframe(df: pd.DataFrame, insight: str = "") -> None:
    """Display a DataFrame with an optional business insight below."""
    st.success(f"Query returned {len(df)} rows.")
    st.dataframe(df, width="stretch", hide_index=True)
    if insight:
        st.markdown(
            f"""
            <div class="insight-box">💡
                <strong>Business Insight:</strong> {insight}
            </div>""",
            unsafe_allow_html=True,
        )


page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📊 Business Q&A", "🗄️ Order Analytics"],
)

stats = get_summary_stats()

if page == "🏠 Dashboard":

    render_header(
        "Uber Eats Bangalore Intelligence",
        "SQL-powered restaurant analytics · Tabular insights only",
    )
    render_metric_row(stats)
    st.write("")

    st.sidebar.header("Filters")

    locations = ["All"] + get_locations()
    sel_location = st.sidebar.selectbox("Location", locations)
    sel_segment = st.sidebar.selectbox(
        "Price Segment", ["All", "Low", "Mid", "Premium"]
    )
    sel_online = st.sidebar.selectbox("Online Order", ["All", "Yes", "No"])
    sel_booking = st.sidebar.selectbox("Table Booking", ["All", "Yes", "No"])
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)
    min_votes = st.sidebar.slider("Minimum Votes", 0, 1000, 0, 50)

    conditions = [
        f"rate >= {min_rating}",
        f"votes >= {min_votes}",
    ]
    if sel_location != "All":
        conditions.append(f"location = '{sel_location}'")
    if sel_segment != "All":
        conditions.append(f"price_segment = '{sel_segment}'")
    if sel_online != "All":
        val = 1 if sel_online == "Yes" else 0
        conditions.append(f"online_order = {val}")
    if sel_booking != "All":
        val = 1 if sel_booking == "Yes" else 0
        conditions.append(f"book_table = {val}")

    where_clause = " AND ".join(conditions)

    sql = f"""
        SELECT
            restaurant_name,
            location,
            cuisines,
            rest_type,
            rate,
            votes,
            approx_cost_for_two,
            price_segment,
            rating_category,
            CASE
                WHEN online_order = 1 THEN 'Yes'
                ELSE 'No'
            END AS online_order,
            CASE
                WHEN book_table  = 1 THEN 'Yes'
                ELSE 'No'
            END  AS book_table
        FROM restaurants
        WHERE {where_clause}
        ORDER BY rate DESC, votes DESC
        LIMIT 200
    """

    result_df = run_query(sql)

    st.markdown(
        '<div class="section-tag">Filtered Results</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-heading">Restaurant Explorer</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Matches Found", len(result_df))
    c2.metric(
        "Avg Rating",
        f"{result_df['rate'].mean():.2f}" if len(result_df) else "—",
    )
    c3.metric(
        "Avg Cost (₹)",
        (
            f"{result_df['approx_cost_for_two'].mean():.0f}"
            if len(result_df)
            else "—"
        ),
    )
    c4.metric(
        "Unique Locations",
        result_df["location"].nunique() if len(result_df) else 0,
    )

    st.divider()

    if len(result_df) == 0:
        st.warning(
            "No restaurants match the selected filters."
            "Try relaxing the filters."
        )
    else:
        st.dataframe(result_df, width="stretch", hide_index=True)

    st.divider()
    st.markdown(
        '<div class="section-tag">Breakdown</div>', unsafe_allow_html=True
    )
    st.markdown(
        """<div class="section-heading">Location Summary'
            '(from filtered results)'
        '</div>""",
        unsafe_allow_html=True,
    )

    if len(result_df) > 0:
        location_summary = (
            result_df.groupby("location")
            .agg(
                count=("restaurant_name", "count"),
                avg_rating=("rate", "mean"),
                avg_cost=("approx_cost_for_two", "mean"),
            )
            .round(2)
            .sort_values("avg_rating", ascending=False)
            .reset_index()
        )
        location_summary.columns = [
            "Location",
            "Restaurants",
            "Avg Rating",
            "Avg Cost (₹)",
        ]
        st.dataframe(location_summary, width="stretch", hide_index=True)


elif page == "📊 Business Q&A":

    render_header(
        "Business Q&A Analytics",
        "15 predefined business questions · All answers computed via SQL",
    )
    render_metric_row(stats)
    st.write("")

    qa_map = {
        "Q1  — Which locations have the highest avg ratings?": (
            q1_top_rated_locations,
            "These areas are ideal for onboarding"
            "premium restaurant partners.",
        ),
        "Q2  — Which locations are over-saturated?": (
            q2_oversaturated_locations,
            "Avoid adding more partners in these markets —"
            "competition is already fierce.",
        ),
        "Q3  — Does online ordering improve ratings?": (
            q3_online_order_vs_rating,
            "Online ordering correlates with higher ratings —"
            "encourage adoption.",
        ),
        "Q4  — Does table booking correlate with higher ratings?": (
            q4_table_booking_vs_rating,
            "Table booking restaurants consistently outperform others.",
        ),
        "Q5  — What price range delivers best satisfaction?": (
            q5_price_vs_satisfaction,
            "Mid-range restaurants achieve the"
            "best balance of cost and rating.",
        ),
        "Q6  — How do pricing segments perform overall?": (
            q6_pricing_segment_performance,
            "Use this table to benchmark restaurant"
            "performance by price tier.",
        ),
        "Q7  — Which cuisines are most common in Bangalore?": (
            q7_most_common_cuisines,
            "High-count cuisines signal market saturation —"
            "niche cuisines may be better bets.",
        ),
        "Q8  — Which cuisines receive the highest avg ratings?": (
            q8_top_rated_cuisines,
            "Promote these cuisines on the platform to"
            "drive customer satisfaction.",
        ),
        "Q9  — Which cuisines perform well with fewer restaurants?": (
            q9_niche_cuisine_opportunities,
            "Niche cuisines with high ratings represent"
            "untapped market opportunities.",
        ),
        "Q10 — What is the relationship between cost and rating?": (
            q10_cost_vs_rating,
            "Higher price does not guarantee higher ratings — mid-tier wins.",
        ),
        "Q11 — Which locations are ideal for premium onboarding?": (
            q11_premium_onboarding_locations,
            "These locations combine high ratings with premium pricing power.",
        ),
        "Q12 — Which locations show high demand but low quality?": (
            q12_high_demand_low_quality,
            "Quality improvement programs should"
            "target these locations first.",
        ),
    }

    col_select, col_btn = st.columns([3, 1])
    with col_select:
        selected_q = st.selectbox(
            "Select a business question:", list(qa_map.keys())
        )
    with col_btn:
        st.write("")
        run_one = st.button("Run Selected", width="stretch")

    run_all = st.button("Run All 13 Questions", width="stretch")

    if run_one:
        func, insight = qa_map[selected_q]
        st.markdown(
            f'<div class="section-heading">{selected_q}</div>',
            unsafe_allow_html=True,
        )
        with st.spinner("Running SQL query..."):
            result = func()
        show_dataframe(result, insight)

    if run_all:
        for label, (func, insight) in qa_map.items():
            st.markdown(
                f'<div class="section-heading">{label}</div>',
                unsafe_allow_html=True,
            )
            with st.spinner(f"Running {label[:30]}..."):
                result = func()
            show_dataframe(result, insight)
            st.divider()


elif page == "🗄️ Order Analytics":

    render_header(
        "Order Analytics",
        "Order dataset analysis · SQL-driven tabular insights",
    )

    try:
        order_count_df = run_query("SELECT COUNT(*) AS cnt FROM orders")
        order_count = int(order_count_df.iloc[0]["cnt"])
    except Exception:
        order_count = 0

    if order_count == 0:
        st.warning(
            "No order data found. Run `python database.py` after placing "
            "`orders.json` in the `data/` folder."
        )
        st.stop()

    st.info(f"Orders table loaded — {order_count:,} records available.")
    render_metric_row(stats)
    st.write("")

    order_questions = {
        "Total orders and revenue by restaurant": """
        SELECT
            restaurant_name,
            COUNT(*)                         AS total_orders,
            ROUND(SUM(order_value), 2)       AS total_revenue,
            ROUND(AVG(order_value), 2)       AS avg_order_value
        FROM orders
        GROUP BY restaurant_name
        ORDER BY total_orders DESC
        LIMIT 10
    """,
        "Revenue by payment method": """
        SELECT
            payment_method,
            COUNT(*)                         AS total_orders,
            ROUND(SUM(order_value), 2)       AS total_revenue,
            ROUND(AVG(order_value), 2)       AS avg_order_value
        FROM orders
        GROUP BY payment_method
        ORDER BY total_revenue DESC
    """,
        "Discount usage analysis": """
        SELECT
            discount_used,
            COUNT(*)                         AS total_orders,
            ROUND(SUM(order_value), 2)       AS total_revenue,
            ROUND(AVG(order_value), 2)       AS avg_order_value
        FROM orders
        GROUP BY discount_used
        ORDER BY total_orders DESC
    """,
        "Monthly order trend": """
        SELECT
            SUBSTR(order_date, 1, 7)         AS month,
            COUNT(*)                          AS total_orders,
            ROUND(SUM(order_value), 2)        AS total_revenue,
            ROUND(AVG(order_value), 2)        AS avg_order_value
        FROM orders
        GROUP BY month
        ORDER BY month ASC
    """,
        "Top restaurants by total revenue": """
        SELECT
            restaurant_name,
            COUNT(*)                         AS total_orders,
            ROUND(SUM(order_value), 2)       AS total_revenue,
            ROUND(AVG(order_value), 2)       AS avg_order_value,
            SUM(
                CASE WHEN discount_used = 'Yes' THEN 1 ELSE 0 END
            ) AS discount_orders
        FROM orders
        GROUP BY restaurant_name
        ORDER BY total_revenue DESC
        LIMIT 10
    """,
    }

    col_q, col_run = st.columns([3, 1])
    with col_q:
        selected_order_q = st.selectbox(
            "Select an order analysis:", list(order_questions.keys())
        )
    with col_run:
        st.write("")
        run_order = st.button("Run Analysis", width="stretch")

    if run_order:
        st.markdown(
            f'<div class="section-heading">{selected_order_q}</div>',
            unsafe_allow_html=True,
        )
        with st.spinner("Querying orders table..."):
            result = run_query(order_questions[selected_order_q])
        show_dataframe(result)
