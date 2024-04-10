import streamlit as st
from time import sleep
import streamlit_authenticator as stauth
from login_sidebar import make_sidebar

make_sidebar()

st.title("Unlock the Conversation ")
st.write("Ready to Talk? Login Now")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if username == "aidrin" and password == "aidrin":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/option_page.py")
    else:
        st.error("Incorrect username or password")

st.write("")
st.write("")

st.write("New User? Register here")
if st.button("Register", type="secondary"):
    st.session_state.logged_in = False
    st.switch_page("pages/register_page.py")
