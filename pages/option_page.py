import streamlit as st
from login_sidebar import make_sidebar


make_sidebar()

st.title("Chat Your Way: Text, Documents, or Databases")
st.write("Pick Your Power")

st.write("")
st.write("")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Chat with CONVERSE!")
    if st.button("Convserse", type="primary"):
        st.switch_page("pages/document_chat_page.py")

with col2:
    st.write("CONVERSE with Docs!")
    if st.button("Converse-Docs", type="primary"):
        st.switch_page("pages/document_chat_page.py")

with col3:
    st.write("CONVERSE with Database!")
    if st.button("Convserse-DB", type="primary"):
        st.switch_page("")
    
    
