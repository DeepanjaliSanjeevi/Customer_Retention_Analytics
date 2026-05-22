import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Customer Retention Dashboard",
    layout="wide"
)

# TITLE
st.title("🏦 Customer Retention Analytics Dashboard")

st.markdown("### Customer Engagement & Product Utilization Analytics")

# LOAD DATA
df = pd.read_csv("data/churn.csv")

# CREATE ENGAGEMENT PROFILE
def engagement_profile(row):

    if row['IsActiveMember'] == 1 and row['NumOfProducts'] >= 2:
        return "Highly Engaged"

    elif row['IsActiveMember'] == 0 and row['Balance'] > 100000:
        return "High Value Disengaged"

    elif row['NumOfProducts'] == 1:
        return "Low Product User"

    else:
        return "Moderate"

df['EngagementProfile'] = df.apply(engagement_profile, axis=1)

# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

# Geography Filter
selected_country = st.sidebar.multiselect(
    "Select Geography",
    options=df['Geography'].unique(),
    default=df['Geography'].unique()
)

# Product Filter
selected_products = st.sidebar.slider(
    "Select Number of Products",
    min_value=int(df['NumOfProducts'].min()),
    max_value=int(df['NumOfProducts'].max()),
    value=(1, 4)
)

# Balance Filter
selected_balance = st.sidebar.slider(
    "Select Balance Range",
    min_value=float(df['Balance'].min()),
    max_value=float(df['Balance'].max()),
    value=(
        float(df['Balance'].min()),
        float(df['Balance'].max())
    )
)

# APPLY FILTERS
filtered_df = df[
    (df['Geography'].isin(selected_country)) &
    (df['NumOfProducts'].between(
        selected_products[0],
        selected_products[1]
    )) &
    (df['Balance'].between(
        selected_balance[0],
        selected_balance[1]
    ))
]

# KPI CALCULATIONS
total_customers = df.shape[0]

churn_rate = (df['Exited'].sum() / total_customers) * 100

active_customers = df['IsActiveMember'].sum()

high_risk_customers = df[
    (df['IsActiveMember'] == 0) &
    (df['Balance'] > 100000)
].shape[0]

# KPI CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)

col2.metric("Churn Rate", f"{round(churn_rate,2)}%")

col3.metric("Active Customers", active_customers)

col4.metric("High Risk Customers", high_risk_customers)

st.divider()

# GRAPH 1 — CHURN DISTRIBUTION
fig1 = px.histogram(
    filtered_df,
    x='Exited',
    color='Exited',
    title='Customer Churn Distribution',
    text_auto=True,
    template='plotly_dark'
)

st.plotly_chart(fig1, use_container_width=True)

# GRAPH 2 — ENGAGEMENT VS CHURN
fig2 = px.histogram(
    filtered_df,
    x='IsActiveMember',
    color='Exited',
    barmode='group',
    title='Customer Engagement vs Churn',
    text_auto=True,
    template='plotly_dark'
)

st.plotly_chart(fig2, use_container_width=True)

# GRAPH 3 — PRODUCTS VS CHURN
fig3 = px.histogram(
    filtered_df,
    x='NumOfProducts',
    color='Exited',
    barmode='group',
    title='Product Utilization vs Churn',
    text_auto=True,
    template='plotly_dark'
)

st.plotly_chart(fig3, use_container_width=True)

# GRAPH 4 — GEOGRAPHY ANALYSIS
fig4 = px.histogram(
    filtered_df,
    x='Geography',
    color='Exited',
    barmode='group',
    title='Geography-wise Churn Analysis',
    text_auto=True,
    template='plotly_dark'
)

st.plotly_chart(fig4, use_container_width=True)

# GRAPH 5 — BALANCE VS CHURN
fig5 = px.box(
    filtered_df,
    x='Exited',
    y='Balance',
    color='Exited',
    title='Balance vs Customer Churn',
    template='plotly_dark'
)

st.plotly_chart(fig5, use_container_width=True)

# GRAPH 6 — ENGAGEMENT PROFILE
fig6 = px.histogram(
    filtered_df,
    y='EngagementProfile',
    color='EngagementProfile',
    title='Customer Engagement Profiles',
    text_auto=True,
    template='plotly_dark'
)

st.plotly_chart(fig6, use_container_width=True)

# HIGH RISK CUSTOMER DETECTOR
st.subheader("⚠ High-Risk Customer Detector")

high_risk_df = filtered_df[
    (filtered_df['IsActiveMember'] == 0) &
    (filtered_df['Balance'] > 100000) &
    (filtered_df['NumOfProducts'] <= 2)
]

st.write(
    "Customers with high balance, low engagement, and limited product usage."
)

st.dataframe(
    high_risk_df[
        [
            'CustomerId',
            'Geography',
            'Balance',
            'NumOfProducts',
            'EstimatedSalary',
            'EngagementProfile'
        ]
    ].head(20)
)

# BUSINESS INSIGHTS
st.subheader("📌 Business Insights & Recommendations")

st.markdown("""
### Key Insights

- Inactive customers show significantly higher churn rates.

- Customers using only one product are more likely to leave the bank.

- High-balance inactive customers represent premium churn risk.

- Customers with higher engagement and multiple products show stronger retention.

- Product utilization plays a major role in customer loyalty.

### Recommendations

✅ Improve engagement campaigns for inactive users.

✅ Encourage multi-product adoption through bundled offers.

✅ Create loyalty programs for high-balance customers.

✅ Monitor disengaged premium customers proactively.

✅ Strengthen customer relationship management strategies.
""")