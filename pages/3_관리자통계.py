import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="관리자 통계", page_icon="📊")

st.title("📊 Minister AI 관리자 통계")

log_file = "usage_log.csv"

if not os.path.exists(log_file):
    st.warning("아직 사용 기록이 없습니다.")
    st.stop()

df = pd.read_csv(log_file)

st.subheader("📁 전체 사용 로그")
st.dataframe(df, use_container_width=True)

st.divider()

# ==============================
# 📊 통계 1 — 기능별 사용 횟수
# ==============================
st.subheader("📌 기능별 사용 횟수")

feature_count = df["feature"].value_counts()
st.bar_chart(feature_count)

st.divider()

# ==============================
# 📊 통계 2 — 사용자별 사용 횟수
# ==============================
st.subheader("👤 사용자별 사용 횟수")

user_count = df["email"].value_counts()
st.bar_chart(user_count)

st.divider()

# ==============================
# 📊 통계 3 — 날짜별 사용 추이
# ==============================
st.subheader("📅 날짜별 사용 추이")

df["date"] = pd.to_datetime(df["timestamp"]).dt.date
daily_count = df.groupby("date").size()

st.line_chart(daily_count)

st.divider()

st.success("운영 데이터 분석 완료")
