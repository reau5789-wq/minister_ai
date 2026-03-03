import streamlit as st

# ----------------------------
# 기본 설정
# ----------------------------
st.set_page_config(
    page_title="Minister AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 브랜드 CSS
# ----------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1 {
    font-weight: 700;
}

.gold {
    color: #D4AF37;
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
    padding: 12px 20px;
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

# ----------------------------
# 세션 상태
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

# ----------------------------
# 왼쪽 버튼형 메뉴
# ----------------------------
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

# ----------------------------
# 메인 페이지
# ----------------------------
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
            st.success("추천 기능은 다음 단계에서 연결됩니다.")

# ----------------------------
# 플랫폼 소개
# ----------------------------
elif st.session_state.page == "platform":

    st.markdown("<h2 class='gold'>플랫폼 소개</h2>", unsafe_allow_html=True)

    st.write("""
    Minister AI는 교회의 기도와 분별을 돕기 위해 만들어졌습니다.
    
    우리는 사역자를 순위로 세우지 않습니다.
    우리는 연결을 거래하지 않습니다.
    우리는 교회의 결정을 대신하지 않습니다.
    
    단지 더 질서있고 투명한 분별을 돕습니다.
    """)

# ----------------------------
# 브랜드 스토리
# ----------------------------
elif st.session_state.page == "brand":

    st.markdown("<h2 class='gold'>브랜드 스토리</h2>", unsafe_allow_html=True)

    st.write("""
    교회는 늘 사람을 찾습니다.
    그러나 선택의 순간은 쉽지 않습니다.
    
    Minister AI는 그 분별의 과정을 조용히 돕기 위해 시작되었습니다.
    
    “모든 것을 품위있게 하고 질서 있게 하라.” (고린도전서 14:40)
    
    우리는 기술보다 마음을 먼저 생각합니다.
    """)

# ----------------------------
# 관리자 통계
# ----------------------------
elif st.session_state.page == "admin":

    st.markdown("<h2 class='gold'>관리자 통계</h2>", unsafe_allow_html=True)
    st.info("관리자 전용 영역입니다.")
