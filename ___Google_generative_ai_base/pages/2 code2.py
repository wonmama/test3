import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
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

st.title("원소 정보 검색기 🔍")

atom_name = st.text_input("원소 이름을 한글로 입력하세요")

if atom_name:
    prompt = f"""
    원소 이름: {atom_name}
    이 원소의 다음 정보를 알려줘:
    - 원자기호
    - 원자번호
    - 원자량
    - 지구상의 존재비율
    - 끓는점
    - 어는점
    - 밀도
    - 실온에서의 상태
    - 화학적 성질
    - 화학반응 생성물
    - 사용사례 1가지
    """
    result = try_generate_content(api_key, prompt)
    if result:
        st.markdown(to_markdown(result))
    else:
        st.error("정보를 가져오는데 실패했습니다. 다시 시도해주세요.")
