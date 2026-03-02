import streamlit as st
import pandas as pd
from openai import OpenAI

# ==============================
# 🔐 OpenAI API 설정
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 🎨 페이지 기본 설정
# ==============================
st.set_page_config(
    page_title="Minister AI 4.0",
    page_icon="🙏",
    layout="wide",
)

# ==============================
# 🎨 디자인 스타일
# ==============================
st.markdown("""
<style>
body {
    background-color: #0E1A2B;
}
h1, h2, h3, h4 {
    color: #F5F5F5;
}
.stButton>button {
    background-color: #1E3A5F;
    color: white;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #D4AF37;
    color: black;
}
div.stTextArea textarea {
    background-color: #1C2A3A;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🙏 메인 타이틀
# ==============================
st.title("🙏 Minister AI 4.0 - 교회 행사 강사 추천 시스템")

st.markdown("행사 내용을 자세히 입력해주세요 (예: 창립 30주년 기념 부흥회, 서울 지역, 은혜로운 말씀 중심)")

# ==============================
# 📂 데이터 로드
# ==============================
try:
    df = pd.read_csv("minister_DB.csv")
except:
    st.error("minister_DB.csv 파일을 찾을 수 없습니다.")
    st.stop()

# ==============================
# 📝 사용자 입력
# ==============================
user_input = st.text_area("행사 내용 입력", height=120)

# ==============================
# 🔍 추천 버튼
# ==============================
if st.button("🔎 AI 추천 받기"):

    if user_input.strip() == "":
        st.warning("행사 내용을 입력해주세요.")
    else:

        with st.spinner("AI가 분석 중입니다..."):

            prompt = f"""
            교회 행사 내용: {user_input}

            아래 강사 데이터 중에서 가장 적합한 3명을 추천하고
            이유를 간단히 설명해 주세요.

            강사 목록:
            {df.to_string(index=False)}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 교회 행사에 적합한 강사를 추천하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content

        st.subheader("📊 AI 추천 결과")
        st.markdown(result)

# ==============================
# 📈 데이터 전체 보기 (투명성 강화)
# ==============================
st.divider()
st.subheader("📋 등록된 강사 데이터")
st.dataframe(df, use_container_width=True)

# ==============================
# 🌱 철학 선언
# ==============================
st.divider()
st.markdown("""
### 🌿 Minister AI의 사역 철학

Minister AI는 **결정을 대신하는 시스템이 아닙니다.**  
교회의 기도와 분별을 돕는 도구입니다.

이 플랫폼에서 발생하는 수익은  
다시 사역자들을 돕는 일에 사용됩니다.
""")
