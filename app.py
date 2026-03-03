import streamlit as st

st.set_page_config(
    page_title="Minister AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 기본 메뉴 숨김
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 세션 상태
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

# -------------------------
# 커스텀 사이드 메뉴
# -------------------------
with st.sidebar:
    st.markdown("## 🌿 Minister AI")

    if st.button("🏠 Main", use_container_width=True):
        st.session_state.page = "main"

    if st.button("📖 플랫폼 소개", use_container_width=True):
        st.session_state.page = "platform"

    if st.button("✨ 브랜드 스토리", use_container_width=True):
        st.session_state.page = "brand"

    if st.button("📊 관리자 통계", use_container_width=True):
        st.session_state.page = "admin"

# -------------------------
# 페이지 렌더링
# -------------------------

if st.session_state.page == "main":

    st.markdown("""
    <h1 style='color:#D4AF37;'>MINISTER AI</h1>
    <h4 style='color:gray;'>교회 사역 매칭 & 행사 기획 플랫폼</h4>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("행사 내용을 입력하세요")
    event = st.text_area("")

    if st.button("AI 추천 받기"):
        st.success("추천 기능은 다음 단계에서 연결됩니다.")

elif st.session_state.page == "platform":

    st.title("플랫폼 소개")
    st.write("Minister AI는 교회의 기도와 분별을 돕는 플랫폼입니다.")

elif st.session_state.page == "brand":

    st.title("브랜드 스토리")
    st.write("우리는 연결을 거래하지 않습니다.")
    st.write("기도의 결정을 대신하지 않습니다.")
    st.write("사역을 돕는 도구가 되기를 원합니다.")

elif st.session_state.page == "admin":

    st.title("관리자 통계")
    st.info("관리자 전용 기능 영역입니다.")
