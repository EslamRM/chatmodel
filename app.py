import utils.session
import streamlit as st
from openai import OpenAI

st.title("🐋 Chat DeepSeek 🐋")
st.subheader("🤖 DeepSeek Chatbot prototype 🤖", divider="blue")


# ======= Sidebar UI =========


# ===== API Client =========
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["DEEPSEEK_API_KEY"]
)


# ====== Chat History =======
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def render_chat_history_messages():
    if len(st.session_state.chat_history) > 0:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])


render_chat_history_messages()


if prompt := st.chat_input():
    try:
        # append the prompt to the chat history
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )

        # display the user's prompt/message
        with st.chat_message("user"):
            st.markdown(prompt)

        # display the llm message
        with st.chat_message("assistant"):
            # placeholder for the llm response
            placeholder = st.empty()

        chat_completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "user", "content": prompt}
            ] + st.session_state.chat_history,
            stream=True,
        )

        full_response = ""

        for chunk in chat_completion:
            full_response += chunk.choices[0].delta.content or ""
            placeholder.write(full_response)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response}
        )

    except Exception as e:
        print("something went wrong: ", e)
