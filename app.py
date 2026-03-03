import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import os

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
# 세션 상태 초기화
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "selected_minister" not in st.session_state:
    st.session_state.selected_minister = None

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
# 추천 저장
# -------------------------------------------------
def save_history(email, event):
    file_name = "recommend_history.csv"
    new_data = pd.DataFrame([{
        "email": email,
        "event": event,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }])

    if os.path.exists(file_name):
        old = pd.read_csv(file_name)
        updated = pd.concat([old, new_data], ignore_index=True)
        updated.to_csv(file_name, index=False)
    else:
        new_data.to_csv(file_name, index=False)

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

    if st.button("📢 프리젠테이션 모드", use_container_width=True):
        st.session_state.page = "presentation"

# -------------------------------------------------
# MAIN 페이지
# -------------------------------------------------
if st.session_state.page == "main":

    st.markdown("<h1 class='gold'>MINISTER AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>교회 사역 매칭 & 행사 기획 플랫폼</div>", unsafe_allow_html=True)
st.divider()

# 로그인 영역 (선택)
with st.expander("🔐 로그인 (선택)"):

    email = st.text_input("이메일")

    if st.button("로그인"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("로그인 완료")
        else:
            st.warning("이메일 입력")

if st.session_state.logged_in:
    st.success(f"현재 로그인: {st.session_state.user_email}")

    is_premium = "premium" in st.session_state.user_email.lower()

    if is_premium:
        st.success("⭐ 프리미엄 사용자 모드")
    else:
        st.info("Free 모드 (상위 3명 추천)")

    st.subheader("행사 내용을 입력하세요")
    event = st.text_area("", placeholder="예: 창립 30주년 기념 부흥회, 서울 지역, 말씀 중심")

    if st.button("AI 추천 받기", use_container_width=True):

        if not event.strip():
            st.warning("행사 내용 입력")
        else:
            save_history(st.session_state.user_email, event)

            with st.spinner("추천 생성 중..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content":"신학적으로 균형잡힌 한국교회 전문가"},
                        {"role":"user","content":event}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content

                st.markdown("### 🔎 AI 전략 추천")
                st.write(result)

                st.markdown("### 📋 추천 사역자")

                limit = 10 if is_premium else 3
                matched = db.head(limit)

                for _, row in matched.iterrows():
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
                        if st.button("상세보기", key=row['이름']):
                            st.session_state.selected_minister = row.to_dict()

                if is_premium:
                    st.markdown("### 🔬 심층 매칭 분석")
                    st.write("행사 성격과 사역자 성향 분석 결과: 높은 적합도")

    if st.session_state.selected_minister:
        m = st.session_state.selected_minister
        st.markdown("## 📖 사역자 상세 프로필")
        st.write(f"이름: {m['이름']}")
        st.write(f"사역유형: {m['사역유형']}")
        st.write(f"지역: {m['지역']}")
        st.write(f"설교스타일: {m['설교스타일']}")
        st.write(f"연락처: {m['연락처']}")

# -------------------------------------------------
# 플랫폼 소개
# -------------------------------------------------
elif st.session_state.page == "platform":
    st.markdown("<h2 class='gold'>플랫폼 소개</h2>", unsafe_allow_html=True)
    st.write("""
Minister AI는 교회의 분별을 돕는 도구입니다.
AI는 사역을 대신하지 않습니다.
그러나 분별을 돕는 도구가 될 수 있습니다.
""")

# -------------------------------------------------
# 브랜드 스토리
# -------------------------------------------------
elif st.session_state.page == "brand":
    st.markdown("<h2 class='gold'>브랜드 스토리</h2>", unsafe_allow_html=True)
    st.write("""
하나님은 시대마다 새로운 도구를 허락하십니다.
그러나 도구를 쓰시는 분은 하나님이십니다.
Minister AI는 분별을 돕는 조용한 도구입니다.
""")

# -------------------------------------------------
# 관리자
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
    st.metric("총 사역자", len(db))

# -------------------------------------------------
# 프리젠테이션 모드
# -------------------------------------------------
elif st.session_state.page == "presentation":

    st.markdown("<h1 class='gold'>Minister AI 4.0</h1>", unsafe_allow_html=True)
    st.markdown("### 한국교회 사역 매칭 플랫폼")
    st.divider()

    st.markdown("## 🎯 왜 필요한가?")
    st.write("""
• 교회는 적합한 강사를 찾기 어렵습니다.  
• 사역자는 자신을 소개할 기회가 제한적입니다.  
• 연결은 비공식적 네트워크에 의존합니다.
""")

    st.markdown("## 🧭 우리가 지키는 원칙")
    st.write("""
✔ 사역자를 순위로 세우지 않습니다.  
✔ 기도의 결정을 대신하지 않습니다.  
✔ 연결을 거래하지 않습니다.  
✔ 수익은 사역자 지원 구조로 환원합니다.
""")

    st.markdown("## 🛡 데이터 보호 구조")
    st.write("""
• 교회 데이터는 외부 공유하지 않습니다.  
• 관리자 승인 기반 운영  
• 추천 기록은 통계 목적 외 사용 금지
""")

    st.markdown("## 💡 사용 시나리오")
    st.write("""
1. 교회 로그인  
2. 행사 입력  
3. AI 전략 추천  
4. DB 매칭  
5. 사역자 상세 검토  
""")

    st.markdown("## 🌱 수익 구조")
    st.write("""
• 기본 추천 무료  
• 프리미엄 매칭 유료  
• 수익 일부는 사역자 지원 기금으로 환원
""")

    st.markdown("## 🚀 비전")
    st.write("""
Minister AI는 한국교회와 사역자를 연결하는
공정하고 신뢰 가능한 플랫폼이 되는 것을 목표로 합니다.
""")


