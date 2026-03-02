import streamlit as st
import pandas as pd
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import tempfile
import os

# ==============================
# 🔐 OpenAI API 설정
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="Minister AI 4.0",
    page_icon="🙏",
    layout="wide",
)

st.title("🙏 Minister AI 4.0")
st.subheader("교회 행사 강사 추천 & 기획 플랫폼")

st.divider()

# ==============================
# 📂 데이터 로드
# ==============================
df = pd.read_csv("minister_DB.csv")

# ==============================
# 📝 사용자 입력
# ==============================
st.markdown("### 📌 행사 내용을 입력하세요")
user_input = st.text_area("행사 내용", height=120)

# ==============================
# 🔎 기본 추천
# ==============================
if st.button("🔎 AI 강사 추천"):
    if user_input.strip() == "":
        st.warning("행사 내용을 입력해주세요.")
    else:
        with st.spinner("분석 중..."):
            prompt = f"""
            교회 행사 내용: {user_input}

            아래 강사 목록 중 가장 적합한 3명을 추천하고
            추천 이유를 설명하세요.

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
st.markdown("## 💎 행사 기획안 자동 생성 (프리미엄)")

premium_code = st.text_input("프리미엄 코드 입력", type="password")

if st.button("✨ 행사 기획안 생성"):

    if user_input.strip() == "":
        st.warning("행사 내용을 먼저 입력해주세요.")
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

        if premium_code == "MINISTER2026":

            st.success("✅ 프리미엄 인증 완료")
            st.markdown("### ✨ 전체 기획안")
            st.success(premium_result)

            # ==============================
            # 📄 PDF 생성
            # ==============================
            pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            doc = SimpleDocTemplate(pdf_file.name, pagesize=A4)

            styles = getSampleStyleSheet()
            custom_style = ParagraphStyle(
                name='Custom',
                parent=styles['Normal'],
                fontSize=12,
                leading=18,
            )

            story = []
            for line in premium_result.split("\n"):
                story.append(Paragraph(line, custom_style))
                story.append(Spacer(1, 8))

            doc.build(story)

            with open(pdf_file.name, "rb") as f:
                st.download_button(
                    label="📥 PDF 다운로드",
                    data=f,
                    file_name="Minister_AI_기획안.pdf",
                    mime="application/pdf"
                )

            os.unlink(pdf_file.name)

        else:
            st.warning("🔒 프리미엄 기능입니다.")
            preview = premium_result[:500]
            st.info(preview + "...\n\n(전체 내용은 프리미엄에서 확인 가능합니다)")
