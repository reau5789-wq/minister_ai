import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import os

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="Minister AI", page_icon="🌿", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
body {background-color:#0E1117;}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0B132B 0%,#111827 100%);
}

.gold {color:#D4AF37;font-weight:800;}
.subtitle {color:#9CA3AF;font-size:18px;}

.stButton>button {
    background-color:#D4AF37;
    color:black;
    font-weight:bold;
    border-radius:10px;
    padding:10px;
}

.card {
    background:#1F2937;
    padding:20px;
    border-radius:12px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 세션 초기화
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "open_detail" not in st.session_state:
    st.session_state.open_detail = None

# -----------------------------
# OpenAI
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# DB
# -----------------------------
@st.cache_data
def load_db():
    return pd.read_csv("minister_DB.csv")

db = load_db()

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("## 🌿 Minister AI")
    st.markdown("---")

    if st.button("🏠 Main", use_container_width=True):
        st.session_state.page = "main"

    if st.button("📖 플랫폼 소개", use_container_width=True):
        st.session_state.page = "platform"

    if st.button("✨ 브랜드 스토리", use_container_width=True):
        st.session_state.page = "brand"

    if st.button("📊 관리자", use_container_width=True):
        st.session_state.page = "admin"

    if st.button("📢 프리젠테이션 모드", use_container_width=True):
        st.session_state.page = "presentation"

# -----------------------------
# MAIN
# -----------------------------
if st.session_state.page == "main":

    st.markdown("<h1 class='gold'>MINISTER AI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>교회 사역 매칭 & 행사 기획 플랫폼</div>", unsafe_allow_html=True)
    st.divider()

    st.info("Free 모드 (상위 3명 추천)")

    st.subheader("행사 내용을 입력하세요")
    event = st.text_area("")

    if st.button("AI 추천 받기", use_container_width=True):

        if not event.strip():
            st.warning("행사 내용을 입력하세요.")
        else:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"신학적으로 균형잡힌 한국교회 전문가"},
                    {"role":"user","content":event}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content

            st.markdown("## 🔎 AI 전략 추천")
            st.write(result)

            st.markdown("## 📋 추천 사역자")

            matched = db.head(3)

            for idx, row in matched.iterrows():

                col1, col2 = st.columns([4,1])

                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <b>{row['이름']}</b><br>
                        사역유형: {row['사역유형']}<br>
                        지역: {row['지역']}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    if st.button("상세보기", key=f"detail_{idx}"):

                        # 토글 구조
                        if st.session_state.open_detail == idx:
                            st.session_state.open_detail = None
                        else:
                            st.session_state.open_detail = idx

                # 상세 표시
                if st.session_state.open_detail == idx:
                    st.markdown(f"""
                    <div class="card">
                    <h4>📖 상세 프로필</h4>
                    이름: {row['이름']}<br>
                    사역유형: {row['사역유형']}<br>
                    지역: {row['지역']}<br>
                    설교스타일: {row['설교스타일']}<br>
                    연락처: {row['연락처']}
                    </div>
                    """, unsafe_allow_html=True)

# -----------------------------
# 기타 페이지
# -----------------------------
elif st.session_state.page == "platform":
    st.write("플랫폼 소개")

elif st.session_state.page == "brand":
    st.write("브랜드 스토리")

elif st.session_state.page == "admin":
    st.write("관리자 페이지")

elif st.session_state.page == "presentation":
    st.write("프리젠테이션 모드")
