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

# -----------------------------
# MAIN
# -----------------------------
if st.session_state.page == "main":

    st.markdown("<h1 class='gold'>MINISTER AI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>교회 사역 매칭 & 행사 기획 플랫폼</div>", unsafe_allow_html=True)
    st.divider()

    # 로그인 영역 (선택형)
    with st.expander("🔐 로그인 (선택)"):
        email = st.text_input("이메일")

        if st.button("로그인"):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("로그인 완료")
            else:
                st.warning("이메일 입력")

    # 로그인 상태 표시
    if st.session_state.logged_in:
        st.success(f"현재 로그인: {st.session_state.user_email}")

    # 프리미엄 판단
    is_premium = False
    if st.session_state.logged_in:
        is_premium = "premium" in st.session_state.user_email.lower()

    if is_premium:
        st.success("⭐ 프리미엄 사용자 모드 (10명 추천 + 연락처 공개)")
    else:
        st.info("Free 모드 (상위 3명 추천 / 연락처 비공개)")

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

            limit = 10 if is_premium else 3
            matched = db.head(limit)

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

                        if st.session_state.open_detail == idx:
                            st.session_state.open_detail = None
                        else:
                            st.session_state.open_detail = idx

                if st.session_state.open_detail == idx:

                    phone_info = row['연락처'] if is_premium else "🔒 프리미엄 사용자만 열람 가능"

                    st.markdown(f"""
                    <div class="card">
                    <h4>📖 상세 프로필</h4>
                    이름: {row['이름']}<br>
                    사역유형: {row['사역유형']}<br>
                    지역: {row['지역']}<br>
                    설교스타일: {row['설교스타일']}<br>
                    연락처: {phone_info}
                    </div>
                    """, unsafe_allow_html=True)
