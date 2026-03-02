import streamlit as st
import pandas as pd
import os
import random
import openai

# ===============================
# 🔐 OpenAI API Key
# ===============================
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# 🎨 교회용 디자인
# ===============================
st.set_page_config(page_title="Minister AI 4.0", layout="wide")

st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
h1 {
    color: #1f4e79;
}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🙏 Minister AI 4.0 - 교회 행사 강사 추천 시스템")

# ===============================
# 📂 CSV 불러오기
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "minister_DB.csv")

if not os.path.exists(CSV_PATH):
    st.error("minister_DB.csv 파일이 없습니다.")
    st.stop()

df = pd.read_csv(CSV_PATH)

# ===============================
# 컬럼 자동 생성
# ===============================
if "설교스타일" not in df.columns:
    styles = ["은혜형", "도전형", "회복형", "말씀중심형"]
    df["설교스타일"] = [random.choice(styles) for _ in range(len(df))]

if "전문행사" not in df.columns:
    events = ["창립기념", "초청행사", "수련회", "부흥회"]
    df["전문행사"] = [random.choice(events) for _ in range(len(df))]

if "사례비" not in df.columns:
    fees = ["30~50", "50~70", "70~100", "100이상"]
    df["사례비"] = [random.choice(fees) for _ in range(len(df))]

# ===============================
# 행사 유형 분석
# ===============================
def detect_event_type(question):
    if "창립" in question:
        return "창립기념"
    elif "초청" in question or "전도" in question:
        return "초청행사"
    elif "수련회" in question:
        return "수련회"
    elif "부흥" in question:
        return "부흥회"
    else:
        return "일반집회"

# ===============================
# 점수 계산
# ===============================
def calculate_score(row, question, event_type):
    score = 0
    ministries = str(row["사역유형"]).split(",")

    for keyword in ["말씀", "찬양", "간증", "전도"]:
        if keyword in question and keyword in ministries:
            score += 25

    if row["전문행사"] == event_type:
        score += 20

    if row["지역"] in question:
        score += 20

    return score

# ===============================
# 사용자 입력
# ===============================
question = st.text_input("행사 내용을 자세히 입력해주세요 (예: 창립 30주년 기념 부흥회, 서울 지역, 은혜로운 말씀 중심)")

if st.button("🔍 AI 추천 받기"):

    if question.strip() == "":
        st.warning("행사 내용을 입력해주세요.")
        st.stop()

    event_type = detect_event_type(question)

    df["점수"] = df.apply(lambda row: calculate_score(row, question, event_type), axis=1)
    sorted_df = df.sort_values(by="점수", ascending=False)

    top = sorted_df.iloc[0]

    st.subheader("📊 추천 점수 분석 결과")
    st.dataframe(sorted_df, use_container_width=True)

    if top["점수"] == 0:
        st.error("조건에 맞는 사역자가 없습니다.")
    else:

        # ===============================
        # 🤖 AI 추천 설명 생성
        # ===============================
        prompt = f"""
사용자 요청:
{question}

추천 목사 정보:
이름: {top['이름']}
사역분야: {top['사역유형']}
설교스타일: {top['설교스타일']}
전문행사: {top['전문행사']}
지역: {top['지역']}
사례비: {top['사례비']}

당신은 20년 경력의 교회 행사 기획 전문가입니다.

1. 실제 교회 추천서처럼 따뜻하고 신뢰감 있게 작성
2. 7~10줄 분량
3. 목회자가 직접 추천하는 느낌
4. 마지막 줄에 핵심 한 문장 요약 포함
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 교회 강사 추천 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        ai_text = response["choices"][0]["message"]["content"]

        st.divider()
        st.subheader("🥇 AI 종합 추천 분석")

        st.markdown(ai_text)

        # ===============================
        # 📝 자동 한 줄 요약 생성
        # ===============================
        summary_prompt = f"""
다음 내용을 한 줄 핵심 문장으로 요약해주세요:

{ai_text}
"""

        summary_response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 핵심만 정리하는 전문가입니다."},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.5
        )

        summary_text = summary_response["choices"][0]["message"]["content"]

        st.subheader("📝 한 줄 핵심 요약")
        st.success(summary_text)