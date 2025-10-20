import os

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

st.title("Study Assistant Chatbot")


def get_api_key_input():
    """Minta user untuk masukkan google api key."""
    # Inisiasi api key di session state
    if "GOOGLE_API_KEY" not in st.session_state:
        st.session_state["GOOGLE_API_KEY"] = ""

    # Jangan tampilkan input jika sudah ada key yang dimasukkan
    if st.session_state["GOOGLE_API_KEY"]:
        return

    st.write("Enter Google API Key")

    # Form untuk masukkan API key
    col1, col2 = st.columns((80, 20))
    with col1:
        api_key = st.text_input("", label_visibility="collapsed", type="password")

    with col2:
        is_submit_pressed = st.button("Submit")
        if is_submit_pressed:
            st.session_state["GOOGLE_API_KEY"] = api_key

    # Set key sebagain env variable, agar bisa diakses langchain
    os.environ["GOOGLE_API_KEY"] = st.session_state["GOOGLE_API_KEY"]

    # Jangan tampilkan apapun (kolom chat) sebelum ada API key yang dimasukkan
    if not st.session_state["GOOGLE_API_KEY"]:
        st.stop()
    st.rerun()


def load_llm():
    """Dapatkan LLM dari LangChain."""
    if "llm" not in st.session_state:
        st.session_state["llm"] = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    return st.session_state["llm"]


def get_chat_history():
    """Dapatkan chat history."""
    if "chat_history" not in st.session_state:
        # Add system message defining chatbot role
        st.session_state["chat_history"] = [
            SystemMessage(
                content=(
                    "You are a helpful and knowledgeable Study Assistant chatbot. "
                    "Your job is to help students understand lessons, explain difficult concepts, "
                    "summarize academic topics, and provide clear, concise educational answers. "
                    "Always respond in a friendly, encouraging tone suitable for learners."
                )
            )
        ]
    return st.session_state["chat_history"]


def display_chat_message(message):
    """Display satu chat di kolom chat."""
    if type(message) is HumanMessage:
        role = "User"
    elif type(message) is AIMessage:
        role = "AI"
    else:
        role = "Unknown"
    with st.chat_message(role):
        st.markdown(message.content)


def display_chat_history(chat_history):
    """Display seluruh chat history saat ini di kolom chat."""
    for chat in chat_history:
        if type(chat) is not SystemMessage:  # hide system message from UI
            display_chat_message(chat)


def user_query_to_llm(llm, chat_history):
    """Minta input query dari user, dan request ke LLM."""
    prompt = st.chat_input("Ask your Study Assistant...")
    if not prompt:
        st.stop()
    chat_history.append(HumanMessage(content=prompt))
    display_chat_message(chat_history[-1])

    response = llm.invoke(chat_history)
    chat_history.append(response)
    display_chat_message(chat_history[-1])


def main():
    """Bagian utama program."""
    get_api_key_input()
    llm = load_llm()
    chat_history = get_chat_history()
    display_chat_history(chat_history)
    user_query_to_llm(llm, chat_history)


# Jalankan bagian utama.
main()
