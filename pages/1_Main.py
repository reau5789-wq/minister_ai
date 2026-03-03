import streamlit as st
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(layout="wide")

# ============================
# 🎨 상단 로고
# ============================
st.image("logo.png", width=200)
st.markdown("""
<div style='text-align:center; padding:20px;'>
    <h1 style='color:#D4AF37; font-size:42px;'>MINISTER AI</h1>
    <p style='color:gray;'>교회 사역 매칭 & 행사 기획 플랫폼</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================
# 🎯 상단 버튼 네비게이션
# ============================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Main"):
        st.switch_page("pages/1_Main.py")

with col2:
    if st.button("📖 브랜드 스토리"):
        st.switch_page("pages/2_브랜드스토리.py")

with col3:
    if st.button("📊 관리자"):
        st.switch_page("pages/3_관리자통계.py")

st.divider()

# ============================
# 📂 데이터
# ============================
df = pd.read_csv("minister_DB.csv")

st.subheader("행사 내용을 입력하세요")

user_input = st.text_area("행사 내용", height=120)

if st.button("🔎 AI 추천"):
    if user_input.strip() != "":
        with st.spinner("분석 중..."):
            prompt = f"""
            행사 내용: {user_input}

            아래 강사 중 가장 적합한 3명을 추천하세요.

            {df.to_string(index=False)}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "교회 행사 강사 매칭 전문가"},
                    {"role": "user", "content": prompt}
                ]
            )

            st.success(response.choices[0].message.content)
