import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role
    

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])


if st.button("Go back", type="secondary"):
    st.session_state.logged_in = False
    st.switch_page("pages/option_page.py")

st.title("Chat with Converse!")

for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input(
    "I possess a well of knowledge. What would you like to know?"
):

    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
