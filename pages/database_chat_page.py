import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm

from populate_db import PopulateDB
from database_sql_talk_gemini import generate_gemini_response


GOOGLE_API_KEY = "AIzaSyDTzAF3jNsbktskJLC_EIBz0_QKPFdnHds"
genai.configure(api_key=GOOGLE_API_KEY, transport="rest")

postgres_db = PopulateDB()
print(postgres_db.list_tables())

multiply = {
    "function_declarations": [
        {
            "name": "multiply",
            "description": "Returns the product of two numbers.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {"a": {"type_": "NUMBER"}, "b": {"type_": "NUMBER"}},
                "required": ["a", "b"],
            },
        }
    ]
}

list_tables = {
    "function_declarations": [
        {
            "name": "list_tables",
            "description": "This will list the tables that will help answer the user's question",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        }
    ]
}

get_table_schema = {
    "function_declarations": [
        {
            "name": "get_table_schema",
            "description": "This will give the schema of a table",
            "parameters": {
                "type_": "OBJECT",
                "properties": {"table_name": {"type_": "STRING"}},
                "required": ["table_name"],
            },
        }
    ]
}

sql_query = {
    "function_declarations": [
        {
            "name": "sql_query",
            "description": "Get information from data in Postgresql using SQL queries",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query on a single line that will help give quantitative answers to the user's question when run on a PostgreSQL database and table. In the SQL query, always use the fully qualified table names.",
                    }
                },
                "required": [
                    "query",
                ],
            },
        }
    ]
}


def multiply_func(a: float, b: float):
    return a * b


def list_tables_func():
    return postgres_db.list_tables()


def get_table_schema_func(table_name: str):
    return postgres_db.get_table_info(table_name)


def sql_query_func(query: str):
    return postgres_db.execute_sql_query(query)


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "upload some pdfs and ask me a question"}
    ]


def main():
    st.set_page_config(page_title="Database Chatbot", page_icon="")

    if st.button("Go back", type="secondary"):
        st.session_state.logged_in = False
        st.switch_page("pages/option_page.py")

    st.title("Ask me anything from the database")
    st.write("Welcome to the chat!")
    st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "throw your doubts here"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_gemini_response(prompt)
                placeholder = st.empty()
                # full_response = ""
                # for item in response["output_text"]:
                #     full_response += item
                #     placeholder.markdown(full_response)
                placeholder.markdown(response)
        if response is not None:
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
