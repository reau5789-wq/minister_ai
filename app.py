import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Minister AI 4.0", page_icon="🙏", layout="wide")

# ==============================
# 세션 초기화
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ==============================
# 로그 저장 함수
# ==============================
def save_log(email, event_text, feature_type):
    log_file = "usage_log.csv"

    new_data = pd.DataFrame([{
        "email": email,
        "event_text": event_text,
        "feature": feature_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    if os.path.exists(log_file):
        old_data = pd.read_csv(log_file)
        updated = pd.concat([old_data, new_data], ignore_index=True)
    else:
        updated = new_data

    updated.to_csv(log_file, index=False)

# ==============================
# 로그인
# ==============================
st.title("🙏 Minister AI 4.0")

if not st.session_state.logged_in:

    email = st.text_input("이메일 로그인")

    if st.button("로그인"):
        if email.strip() != "":
            st.session_state.logged_in = True
            st.session_state.user_email = email

            if email.endswith("@minister.ai"):
                st.session_state.is_premium = True

            st.rerun()

else:
    st.success(f"로그인됨: {st.session_state.user_email}")

    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.is_premium = False
        st.rerun()

st.divider()

df = pd.read_csv("minister_DB.csv")

user_input = st.text_area("행사 내용 입력")

# ==============================
# 기본 추천
# ==============================
if st.session_state.logged_in:

    if st.button("🔎 강사 추천"):
        if user_input.strip() != "":
            with st.spinner("분석 중..."):

                prompt = f"""
                행사 내용: {user_input}

                아래 강사 목록 중 가장 적합한 3명을 추천하세요.

                {df.to_string(index=False)}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "교회 행사 강사 매칭 전문가"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content

            st.info(result)

            # 🔥 로그 저장
            save_log(st.session_state.user_email, user_input, "강사추천")

    st.divider()

    # ==============================
    # 프리미엄 기능
    # ==============================
    if st.button("✨ 행사 기획안 생성"):
        if user_input.strip() != "":
            with st.spinner("기획안 작성 중..."):

                prompt = f"""
                행사 내용: {user_input}

                1. 행사 주제
                2. 전체 흐름
                3. 설교 방향
                4. 찬양 구성
                5. 홍보 문구
                6. 기대 효과
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "교회 행사 기획 전문가"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )

                premium_result = response.choices[0].message.content

            if st.session_state.is_premium:
                st.success(premium_result)
                save_log(st.session_state.user_email, user_input, "기획안생성")
            else:
                st.warning("프리미엄 전용 기능입니다.")
                preview = premium_result[:500]
                st.info(preview)

else:
    st.info("로그인 후 사용 가능합니다.")
