import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("Converse")
        st.write("")
        st.write("")

        # if st.session_state.get("logged_in", False):
        #     st.page_link(
        #         "pages/register_page.py",
        #         label="New User? Register here!",
        #         icon=""
        #     )

        #     st.write("")
        #     st.write("")

        # # Improved logic to switch page based on page name
        # elif get_current_page_name() != "starter":
        #     st.switch_page("starter.py")  # Use page name "starter" here
