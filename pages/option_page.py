import streamlit as st
from login_sidebar import make_sidebar

make_sidebar()

if st.button("Go back", type="secondary"):
    st.session_state.logged_in = False
    st.switch_page("starter.py")

st.title("Chat Your Way: Text, Documents, or Databases")
st.write("")
st.write("Pick Your Power")

st.write("")
    
col1, col2, col3 = st.columns(3)

with col1:
    st.write("CONVERSING TIME!")
    if st.button("START", type="primary"):
        st.switch_page("pages/chat_bot.py")

with col2:
    st.write("CONVERSE WITH DOCS!")
    if st.button("CONV-DOC", type="primary"):
        st.switch_page("pages/document_chat_page.py")

with col3:
    st.write("CONVERSE WITH DATABASE!")
    if st.button("CONV-DB", type="primary"):
        st.switch_page("")
    
    
