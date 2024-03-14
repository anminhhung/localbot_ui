import streamlit as st 
import requests
from src import utils

def send_query(text):
    resp = requests.post("http://localhost:8000/api/stream?query={}".format(text), stream=True)

    return resp

def run_app():    
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    st.set_page_config(page_title="localbot", page_icon="🧑‍💼", layout="wide")

    st.title("💬 Chatbot")
    st.caption("🚀 I'm a Local Bot")
    

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Tôi có thể giúp gì được cho bạn?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        
    # Initialize the QA system using caching
    # translater = Translation(from_lang="en", to_lang='vi', mode='translate') 
    if query := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").write(query)
        
        # Add spinner
        with st.spinner("Thinking..."):
            res = send_query(query)
            res.raise_for_status()

            answer = res
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
            for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            

        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # save_qa
        utils.log_to_csv(query, answer)
        st.chat_message("assistant").write(answer)

if __name__ == "__main__":
    run_app()