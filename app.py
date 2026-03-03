import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="Minister AI",
    page_icon="🌿",
    layout="wide"
)

# --------------------------------------------------
# OpenAI 연결
# --------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --------------------------------------------------
# 브랜드 CSS
# --------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B132B 0%, #111827 100%);
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
    padding: 14px 20px;
    font-size: 16px;
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

# --------------------------------------------------
# 사이드바 (단순 브랜드 표시용)
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🌿 Minister AI")
    st.markdown("---")
    st.markdown("교회 사역 매칭 & 행사 기획 플랫폼")

# --------------------------------------------------
# 메인 화면
# --------------------------------------------------
st.markdown("<h1 class='gold'>MINISTER AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>교회 사역 매칭 & 행사 기획 플랫폼</div>", unsafe_allow_html=True)

st.divider()

st.subheader("행사 내용을 입력하세요")

event = st.text_area(
    "",
    placeholder="예: 창립 30주년 기념 부흥회, 서울 지역, 말씀 중심"
)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# AI 추천 기능
# --------------------------------------------------
if st.button("AI 추천 받기", use_container_width=True):

    if event.strip() == "":
        st.warning("행사 내용을 입력해주세요.")
    else:
        with st.spinner("기도하며 추천 생성 중입니다..."):

            prompt = f"""
            당신은 한국교회 행사 기획을 돕는 전문가입니다.
            아래 행사 내용에 맞는 강사 유형과 추천 방향을 제시해주세요.

            행사 내용:
            {event}

            다음 형식으로 답변해주세요:
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

            st.markdown("### 🔎 AI 추천 결과")
            st.write(result)
