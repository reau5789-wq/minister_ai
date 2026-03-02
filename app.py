import streamlit as st
import pandas as pd
from openai import OpenAI

# ==============================
# 🔐 OpenAI API 설정
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 🎨 페이지 설정
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
h1, h2, h3 {
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
# 🌟 히어로 섹션
# ==============================
st.markdown("""
<div style='text-align:center; padding: 40px 0;'>
    <h1 style='font-size:48px;'>🙏 Minister AI 4.0</h1>
    <h2 style='color:#D4AF37;'>교회 행사 강사 추천 플랫폼</h2>
    <p style='font-size:18px; color:#CCCCCC;'>
        사역의 분별을 돕는 도구<br>
        기도 위에 기술을 더합니다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================
# 📂 데이터 로드
# ==============================
df = pd.read_csv("minister_DB.csv")

# ==============================
# 📝 사용자 입력
# ==============================
st.markdown("### 📌 행사 내용을 자세히 입력해주세요")
user_input = st.text_area("행사 내용 입력", height=120)

# ==============================
# 🔍 기본 추천 기능
# ==============================
if st.button("🔎 AI 강사 추천 받기"):

    if user_input.strip() == "":
        st.warning("행사 내용을 입력해주세요.")
    else:
        with st.spinner("AI가 분석 중입니다..."):

            prompt = f"""
            교회 행사 내용: {user_input}

            아래 강사 데이터 중 가장 적합한 3명을 추천하고
            각각의 추천 이유를 설명하세요.

            강사 목록:
            {df.to_string(index=False)}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 교회 행사 강사 매칭 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content

        st.markdown("### 📊 AI 추천 결과")
        st.markdown(f"""
        <div style='background-color:#1C2A3A; padding:25px; border-radius:15px;'>
        {result}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================
# 📄 프리미엄 기능 — 행사 기획안 자동 생성
# ==============================
st.markdown("## 📄 행사 기획안 자동 생성 (프리미엄 기능)")
st.caption("※ 현재 베타 체험 제공 중")

if st.button("✨ 행사 기획안 생성하기"):

    if user_input.strip() == "":
        st.warning("행사 내용을 먼저 입력해주세요.")
    else:
        with st.spinner("AI가 행사 기획안을 작성 중입니다..."):

            premium_prompt = f"""
            교회 행사 내용: {user_input}

            아래 형식으로 행사 기획안을 작성하세요:

            1. 행사 주제 제안
            2. 전체 행사 흐름
            3. 설교 방향 제안
            4. 찬양 구성 제안
            5. 홍보 문구 초안
            6. 기대 효과
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 교회 행사 기획 전문가입니다."},
                    {"role": "user", "content": premium_prompt}
                ],
                temperature=0.8
            )

            premium_result = response.choices[0].message.content

        st.markdown("### ✨ 행사 기획안 초안")
        st.markdown(f"""
        <div style='background-color:#152233; padding:30px; border-radius:15px;'>
        {premium_result}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================
# 🌿 사역 철학
# ==============================
st.markdown("""
### 🌿 Minister AI의 사역 철학

Minister AI는 교회를 대신하지 않습니다.

강단의 능력은 알고리즘에서 나오지 않습니다.  
그러나 하나님은 시대의 도구를 사용하십니다.

이 플랫폼은 기도 위에 기술을 더하는 작은 도구입니다.

이곳에서 발생하는 수익은  
다시 사역자를 섬기는 일에 사용됩니다.
""")
