from config.streamlit_config import authenticator
import streamlit as st

# authenticator.login()
if st.button("Go back", type="secondary"):
    st.session_state.logged_in = False
    st.switch_page("starter.py")

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = (
        authenticator.register_user(pre_authorization=False)
    )
    if email_of_registered_user:
        # st.success("User registered successfully")
        st.page_link("login_page.py", label="Login Page")
except Exception as e:
    st.error(e)

