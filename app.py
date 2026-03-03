import streamlit as st
import pandas as pd
from openai import OpenAI

# -------------------------------------------------
# 기본 설정
# -------------------------------------------------
st.set_page_config(
    page_title="Minister AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 기본 메뉴 숨김
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# OpenAI 연결
# -------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------------------------
# DB 로드
# -------------------------------------------------
@st.cache_data
def load_db():
    return pd.read_csv("minister_DB.csv")

db = load_db()

# -------------------------------------------------
# 스타일
# -------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B132B 0%, #111827 100%);
}

.gold {
    color: #D4AF37;
    font-weight: 800;
}

.subtitle {
    color: #9CA3AF;
    font-size: 18px;
}

.stButton>button {
    background-color: #D4AF37;
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 14px 20px;
}

.stButton>button:hover {
    background-color: #b8932f;
    color: white;
}

textarea {
    border-radius: 12px !important;
    border: 1px solid #2D3748 !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 세션 상태
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

# -------------------------------------------------
# 사이드바 버튼 메뉴
# -------------------------------------------------
with st.sidebar:
    st.markdown("## 🌿 Minister AI")
    st.markdown("---")

    if st.button("🏠 Main", use_container_width=True):
        st.session_state.page = "main"

    if st.button("📖 플랫폼 소개", use_container_width=True):
        st.session_state.page = "platform"

    if st.button("✨ 브랜드 스토리", use_container_width=True):
        st.session_state.page = "brand"

    if st.button("📊 관리자 통계", use_container_width=True):
        st.session_state.page = "admin"

# -------------------------------------------------
# 페이지 분기
# -------------------------------------------------

# ===========================
# MAIN
# ===========================
if st.session_state.page == "main":

    st.markdown("<h1 class='gold'>MINISTER AI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>교회 사역 매칭 & 행사 기획 플랫폼</div>", unsafe_allow_html=True)

    st.divider()

    st.subheader("행사 내용을 입력하세요")

    event = st.text_area(
        "",
        placeholder="예: 창립 30주년 기념 부흥회, 서울 지역, 말씀 중심"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("AI 추천 받기", use_container_width=True):

        if event.strip() == "":
            st.warning("행사 내용을 입력해주세요.")
        else:
            with st.spinner("기도하며 추천 생성 중입니다..."):

                prompt = f"""
                당신은 한국교회 행사 기획을 돕는 전문가입니다.
                아래 행사 내용에 맞는 강사 유형과 설교 방향을 제시해주세요.

                행사 내용:
                {event}

                형식:
                1. 추천 강사 유형
                2. 추천 설교 스타일
                3. 기대 효과
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "당신은 신학적으로 균형잡힌 한국교회 사역 전문가입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content

                st.markdown("### 🔎 AI 전략 추천")
                st.write(result)

                # --------------------------
                # 🔥 DB 자동 매칭 로직
                # --------------------------
                st.markdown("### 📋 사역자 DB 매칭 결과")

                keywords = ["말씀", "부흥", "청년", "선교", "치유"]

                matched = db.copy()

                for word in keywords:
                    if word in event:
                        matched = matched[matched["사역유형"].str.contains(word, na=False)]

                if len(matched) == 0:
                    st.info("조건에 정확히 맞는 사역자가 없습니다. 전체 목록 일부를 표시합니다.")
                    st.dataframe(db.head(5))
                else:
                    st.dataframe(matched.head(5))

# ===========================
# 플랫폼 소개
# ===========================
elif st.session_state.page == "platform":

    st.markdown("<h2 class='gold'>플랫폼 소개</h2>", unsafe_allow_html=True)

    st.write("""
    Minister AI는 교회의 기도와 분별을 돕기 위해 만들어졌습니다.
    
    ✔ AI 전략 추천  
    ✔ 사역자 DB 기반 매칭  
    ✔ 행사 기획 보조  
    ✔ 사역자 존중 구조
    """)

# ===========================
# 브랜드 스토리
# ===========================
elif st.session_state.page == "brand":

    st.markdown("<h2 class='gold'>브랜드 스토리</h2>", unsafe_allow_html=True)

    st.write("""
    우리는 연결을 거래하지 않습니다.
    기도의 결정을 대신하지 않습니다.
    사역자를 순위로 세우지 않습니다.
    
    Minister AI는 분별을 돕는 도구입니다.
    """)

# ===========================
# 관리자 통계
# ===========================
elif st.session_state.page == "admin":

    st.markdown("<h2 class='gold'>관리자 통계</h2>", unsafe_allow_html=True)

    st.metric("총 등록 사역자 수", len(db))

    st.markdown("### 지역별 분포")
    st.bar_chart(db["지역"].value_counts())
