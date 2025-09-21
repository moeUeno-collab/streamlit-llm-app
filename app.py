from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain_poenai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def get_system_message_by_role(role: str) -> str:
    if role == "医者":
        return "あなたは優秀な医者です。医学的な知識をもとに丁寧に回答してください。"
    elif role == "弁護士":
        return "あなたは経験豊富な弁護士です。法律に基づいて正確に回答してください。"
    elif role == "エンジニア":
        return "あなたは熟練したエンジニアです。技術的な観点から詳しく説明してください。"
    else:
        return "あなたは有能なアシスタントです。"
    
    def get_llm_response(role: str, user_input: str) -> str:
        system_message = get_system_message_by_role(role)
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_input)
        ]
        response = llm(messages)
        return response.content 
    get_llm_response = get_llm_response
st.set_page_config(page_title="専門家チャットアプリ", layout="centered")

st.title("専門家チャットアプリ")
st.write("""
このアプリでは、あなたの質問に対して、選択した専門家（医者・弁護士・エンジニア）が回答してくれます。
以下のフォームに質問を入力し、専門家の種類を選んで「送信」ボタンを押してください。
""")

with st.form("qa_form"):
    user_input = st.text_area("質問を入力してください:", height=100)
    expert_role = st.radio("専門家の種類を選んでください:", ("医者", "弁護士", "エンジニア"))
    submitted = st.form_submit_button("送信")

if submitted and user_input.strip():
    with st.spinner("専門家が回答を考えています..."):
        response = get_llm_response(expert_role, user_input)
    st.markdown("### 回答:")
    st.write(response)
