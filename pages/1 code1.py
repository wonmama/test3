import textwrap
import google.generativeai as genai
import streamlit as st
import pathlib
import toml

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# 적정기술 목록
appropriate_technologies = [
    "태양열 조리기",
    "바이오가스 발전기",
    "태양열 탈수기",
    "로켓스토브",
    "휴대용 정수기",
    "저비용 생리대",
    "페달 발전기",
    "물저장탱크",
    "태양열 난방기",
    "수동 세탁기",
    "태양열 충전기",
    "빗물 집수 시스템",
    "태양열 펌프",
    "오염된 물 필터",
    "연료 효율적인 난로",
    "태양광 전등",
    "휴대용 의학 키트",
    "작은 바람 터빈",
    "태양광 냉장고",
    "재활용 건축 자재"
]

st.title("적정기술 사례")
selected_tech = st.selectbox("알아보고 싶은 적정기술을 선택하세요", appropriate_technologies)

if st.button("정보 생성"):
    if not api_key:
        st.error("Google API 키를 입력하세요.")
    else:
        prompt = f"적정기술 '{selected_tech}'에 대해 개발 배경, 장점, 단점, 개선점, 사용 국가, 사용 사례, 이미지를 제공하세요."
        content = try_generate_content(api_key, prompt)
        
        if content:
            st.markdown(to_markdown(content))
        else:
            st.error("정보를 생성할 수 없습니다. 나중에 다시 시도하세요.")
