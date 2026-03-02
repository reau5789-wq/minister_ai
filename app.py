import streamlit as st
import pandas as pd
from openai import OpenAI

# ==============================
# 🔐 OpenAI 설정
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="Minister AI 4.0",
    page_icon="🙏",
    layout="wide",
)

# ==============================
# 🧠 세션 초기화
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ==============================
# 🌟 타이틀
# ==============================
st.title("🙏 Minister AI 4.0")
st.caption("교회 행사 강사 추천 & 기획 플랫폼")

st.divider()

# ==============================
# 🔐 로그인 영역
# ==============================
if not st.session_state.logged_in:

    st.subheader("🔐 로그인")

    email = st.text_input("이메일 입력")

    if st.button("로그인"):
        if email.strip() == "":
            st.warning("이메일을 입력해주세요.")
        else:
            st.session_state.logged_in = True
            st.session_state.user_email = email

            # 프리미엄 조건 (임시)
            if email.endswith("@minister.ai"):
                st.session_state.is_premium = True

            st.success("로그인 성공!")
            st.rerun()

else:
    st.success(f"로그인됨: {st.session_state.user_email}")

    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.is_premium = False
        st.rerun()

st.divider()

# ==============================
# 📂 데이터 로드
# ==============================
df = pd.read_csv("minister_DB.csv")

# ==============================
# 📝 행사 입력
# ==============================
user_input = st.text_area("행사 내용 입력", height=120)

# ==============================
# 🔎 기본 추천
# ==============================
if st.session_state.logged_in:

    if st.button("🔎 AI 강사 추천"):
        if user_input.strip() == "":
            st.warning("행사 내용을 입력해주세요.")
        else:
            with st.spinner("분석 중..."):

                prompt = f"""
                교회 행사 내용: {user_input}

                아래 강사 목록 중 가장 적합한 3명을 추천하고
                이유를 설명하세요.

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

    st.divider()

    # ==============================
    # 💎 프리미엄 기능
    # ==============================
    st.subheader("💎 행사 기획안 자동 생성")

    if st.button("✨ 기획안 생성"):

        if user_input.strip() == "":
            st.warning("행사 내용을 입력해주세요.")
        else:
            with st.spinner("기획안 작성 중..."):

                premium_prompt = f"""
                교회 행사 내용: {user_input}

                아래 형식으로 작성:
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
                        {"role": "user", "content": premium_prompt}
                    ],
                    temperature=0.8
                )

                premium_result = response.choices[0].message.content

            if st.session_state.is_premium:
                st.success("프리미엄 사용자")
                st.success(premium_result)
            else:
                st.warning("🔒 프리미엄 전용 기능입니다.")
                preview = premium_result[:500]
                st.info(preview + "\n\n(전체 기능은 프리미엄 사용자에게 제공됩니다)")

else:
    st.info("로그인 후 사용 가능합니다.")
