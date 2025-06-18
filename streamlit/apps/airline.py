import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    st.toast("📦 데이터를 새로 생성 중입니다...")
    df = pd.read_csv("/app/data/acs4_target_data.csv", parse_dates=["regist_dt"])
    df["regist_day"] = df["regist_dt"].dt.day
    df["regist_year_month"] = df["regist_dt"].dt.strftime("%Y-%m")
    return df

if "data_df" not in st.session_state:
    st.session_state.data_df = load_data()

if st.sidebar.button("🔁 데이터 리프레시"):
    st.session_state.data_df = load_data()

df = st.session_state.data_df

df = df[df['regist_dt'] >= pd.to_datetime("2025-03-01")]

st.title("✈️ acs4 성과 분석 대시보드")

# 필터
st.sidebar.title("필터 조건")
airlines = st.sidebar.multiselect("항공사", options=df["airline"].unique(), default=df["airline"].unique())
sites = st.sidebar.multiselect("판매 사이트", options=df["sales_site"].unique(), default=df["sales_site"].unique())
dates = st.sidebar.date_input("regist_dt", [df["regist_dt"].min(), df["regist_dt"].max()])

# 필터링 적용
filtered_df = df[
    (df["airline"].isin(airlines)) &
    (df["sales_site"].isin(sites)) &
    (df["regist_dt"] >= pd.to_datetime(dates[0])) &
    (df["regist_dt"] <= pd.to_datetime(dates[1]))
]

# 탭 분리
tab1, tab2, tab3 = st.tabs(["✈️ 항공사별 성과", "🛒 판매채널별 성과", "🧾 데이터 테이블"])

# 항공사 기준 일별 집계
with tab1:
    st.subheader("✈️ 항공사별 일별 성과 추이")
    daily_by_airline = filtered_df.groupby(["regist_dt", "airline"]).agg({
        "s_fare": "sum",
        "p": "sum",
        "p_rate": "mean"
    }).reset_index()

    fig1 = px.line(daily_by_airline, x="regist_dt", y="s_fare", color="airline", markers=True, title="일별 s_fare")
    fig2 = px.line(daily_by_airline, x="regist_dt", y="p", color="airline", markers=True, title="일별 p")
    fig3 = px.line(daily_by_airline, x="regist_dt", y="p_rate", color="airline", markers=True, title="일별 p_rate (%)")

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

# 판매채널 기준 일별 집계
with tab2:
    st.subheader("🛒 판매사이트별 일별 성과 추이")
    daily_by_site = filtered_df.groupby(["regist_dt", "sales_site"]).agg({
        "s_fare": "sum",
        "p": "sum",
        "p_rate": "mean"
    }).reset_index()

    fig4 = px.line(daily_by_site, x="regist_dt", y="s_fare", color="sales_site", markers=True, title="일별 s_fare")
    fig5 = px.line(daily_by_site, x="regist_dt", y="p", color="sales_site", markers=True, title="일별 p")
    fig6 = px.line(daily_by_site, x="regist_dt", y="p_rate", color="sales_site", markers=True, title="일별 p_rate (%)")

    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.plotly_chart(fig6, use_container_width=True)

# 데이터 테이블
with tab3:
    st.markdown("### 🧾 필터 적용된 데이터")
    st.dataframe(filtered_df.sort_values("regist_dt"), use_container_width=True)
