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
    border-radius:12px;
    padding:14px;
}

.stButton>button:hover {
    background-color:#b8932f;
    color:white;
}

.card {
    background:#1F2937;
    padding:20px;
    border-radius:12px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 세션 초기화
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

# -------------------------------------------------
# OpenAI
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
# 사이드바 메뉴
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

    if st.button("📊 관리자", use_container_width=True):
        st.session_state.page = "admin"

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if st.session_state.page == "main":

    st.markdown("<h1 class='gold'>MINISTER AI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>교회 사역 매칭 & 행사 기획 플랫폼</div>", unsafe_allow_html=True)
    st.divider()

    # 로그인 영역
    if not st.session_state.logged_in:
        st.subheader("🔐 로그인")
        email = st.text_input("이메일")
        if st.button("로그인"):
            if email:
                st.session_state.logged_in = True
                st.success("로그인 되었습니다.")
            else:
                st.warning("이메일을 입력하세요.")
        st.stop()

    # 행사 입력
    st.subheader("행사 내용을 입력하세요")
    event = st.text_area("", placeholder="예: 창립 30주년 기념 부흥회, 서울 지역, 말씀 중심")

    if st.button("AI 추천 받기", use_container_width=True):

        if not event.strip():
            st.warning("행사 내용을 입력하세요.")
        else:
            with st.spinner("추천 생성 중..."):

                prompt = f"""
                한국교회 행사에 맞는 강사 방향을 제안하세요.
                행사 내용: {event}

                형식:
                1. 추천 강사 유형
                2. 추천 설교 스타일
                3. 기대 효과
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content":"신학적으로 균형잡힌 한국교회 전문가"},
                        {"role":"user","content":prompt}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content

                st.markdown("### 🔎 AI 전략 추천")
                st.write(result)

                # --------------------------
                # DB 자동 매칭
                # --------------------------
                st.markdown("### 📋 추천 사역자")

                keywords = ["말씀","부흥","청년","선교","치유"]

                matched = db.copy()

                for word in keywords:
                    if word in event:
                        matched = matched[matched["사역유형"].str.contains(word, na=False)]

                if len(matched) == 0:
                    st.info("일치하는 사역자가 없어 전체 일부를 표시합니다.")
                    matched = db.head(3)

                for _, row in matched.head(5).iterrows():
                    st.markdown(f"""
                    <div class="card">
                        <b>{row['이름']}</b><br>
                        사역유형: {row['사역유형']}<br>
                        지역: {row['지역']}<br>
                        설교스타일: {row['설교스타일']}
                    </div>
                    """, unsafe_allow_html=True)

# -------------------------------------------------
# 플랫폼 소개
# -------------------------------------------------
elif st.session_state.page == "platform":

    st.markdown("<h2 class='gold'>플랫폼 소개</h2>", unsafe_allow_html=True)

    st.write("""
    Minister AI는 교회의 분별을 돕는 도구입니다.
    
    • AI 전략 추천  
    • 사역자 DB 기반 매칭  
    • 행사 기획 보조  
    • 사역자 존중 구조  
    """)

# -------------------------------------------------
# 브랜드 스토리
# -------------------------------------------------
elif st.session_state.page == "brand":

    st.markdown("<h2 class='gold'>브랜드 스토리</h2>", unsafe_allow_html=True)

    st.write("""
    하나님은 시대마다 새로운 도구를 허락하십니다.
    그러나 도구를 쓰시는 분은 하나님이십니다.
    
    우리는 사역자를 순위로 세우지 않습니다.
    기도의 결정을 대신하지 않습니다.
    연결을 거래하지 않습니다.
    
    Minister AI는 분별을 돕는 조용한 도구입니다.
    """)

# -------------------------------------------------
# 관리자 모드
# -------------------------------------------------
elif st.session_state.page == "admin":

    if not st.session_state.admin_mode:
        pw = st.text_input("관리자 비밀번호", type="password")
        if st.button("관리자 로그인"):
            if pw == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.admin_mode = True
                st.success("관리자 모드 활성화")
            else:
                st.error("비밀번호 오류")
        st.stop()

    st.markdown("<h2 class='gold'>관리자 통계</h2>", unsafe_allow_html=True)

    st.metric("총 등록 사역자", len(db))
    st.bar_chart(db["지역"].value_counts())
