import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("📊 Sales Dashboard")

# 데이터 생성
def generate_sales_data():
    st.toast("📦 데이터를 새로 생성 중입니다...")
    date_range = pd.date_range("2024-01-01", periods=365)
    df = pd.DataFrame({
        "date": np.random.choice(date_range, 20000),
        "region": np.random.choice(["North", "South", "East", "West"], 20000),
        "sales": np.random.randint(100000, 1000000, 20000)
    })
    df["date"] = pd.to_datetime(df["date"])
    return df

if "sales_df" not in st.session_state:
    st.session_state.sales_df = generate_sales_data()

if st.sidebar.button("🔁 데이터 리프레시"):
    st.session_state.sales_df = generate_sales_data()

df = st.session_state.sales_df

# 필터
st.sidebar.header("📌 필터")
selected_region = st.sidebar.multiselect("지역 선택", options=df["region"].unique(), default=df["region"].unique())
start_date = st.sidebar.date_input("시작일", df["date"].min())
end_date = st.sidebar.date_input("종료일", df["date"].max())

# 필터 적용
filtered_df = df[
    (df["region"].isin(selected_region)) &
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

total_sales = filtered_df["sales"].sum()
avg_sales = filtered_df["sales"].mean()

col1, col2 = st.columns(2)
col1.metric("💰 총 매출", f"{total_sales:,.0f} 원")
col2.metric("📈 평균 매출", f"{avg_sales:,.0f} 원")

# 매출 추이 그래프
sales_trend = filtered_df.groupby("date")["sales"].sum().reset_index()
fig = px.line(sales_trend, x="date", y="sales", title="📅 날짜별 매출 추이", markers=True)
st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(filtered_df.sort_values("date"))
