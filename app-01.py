import getpass
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Minta user masukkan API KEY
GOOGLE_API_KEY = getpass.getpass("Enter your API key: ")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Inisiasi client dengan Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Bikin system prompt
chat_history = []
chat_history.append(
    SystemMessage(content="You are a funny assistant that always joking."),
)

while True:
    # Minta user memasukkan promptnya
    prompt = input("User: ")
    chat_history.append(HumanMessage(content=prompt))

    # Masukkan prompt ke LLM, dan print jawabannya
    response = llm.invoke(chat_history)
    print()
    print("AI:", response.content)
    print()
    chat_history.append(response)
