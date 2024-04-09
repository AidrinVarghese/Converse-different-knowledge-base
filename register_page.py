from config.streamlit_config import authenticator

# authenticator.login()

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = (
        authenticator.register_user(pre_authorization=False)
    )
    if email_of_registered_user:
        # st.success("User registered successfully")
        st.page_link("pages/login_page.py", label="Login Page")
except Exception as e:
    st.error(e)
