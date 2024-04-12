import google.generativeai as genai
import google.ai.generativelanguage as glm
import json

from populate_db import PopulateDB


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


def generate_gemini_response(user_question):

    model = genai.GenerativeModel(
        "gemini-pro", tools=[list_tables, get_table_schema, sql_query]
    )

    chat = model.start_chat()
    response = chat.send_message(user_question)

    response = response.candidates[0].content.parts[0]

    api_requests_and_responses = []

    function_calling_in_process = True
    while function_calling_in_process:
        try:
            params = {}
            for key, value in response.function_call.args.items():
                params[key] = value

            print("Function call name: ", response.function_call.name)
            print("Params: ", params)

            if response.function_call.name == "multiply":
                api_response = multiply_func(params["a"], params["b"])
                api_requests_and_responses.append(
                    [response.function_call.name, params, api_response]
                )

            if response.function_call.name == "list_tables":
                api_response = list_tables_func()
                api_requests_and_responses.append(
                    [response.function_call.name, params, api_response]
                )

            if response.function_call.name == "get_table_schema":
                api_response = get_table_schema_func(params["table_name"])
                api_requests_and_responses.append(
                    [response.function_call.name, params, api_response]
                )

            if response.function_call.name == "sql_query":
                api_response = sql_query_func(params["query"])
                api_requests_and_responses.append(
                    [response.function_call.name, params, api_response]
                )

            response = chat.send_message(
                glm.Content(
                    parts=[
                        glm.Part(
                            function_response=glm.FunctionResponse(
                                name=response.function_call.name,
                                response={"content": api_response},
                            )
                        )
                    ]
                )
            )

            response = response.candidates[0].content.parts[0]

        except AttributeError:
            function_calling_in_process = False

    for content in chat.history:
        part = content.parts[0]
        print(content.role, "->", type(part).to_dict(part))
        print("-" * 80)

    print("Response: ", response.text)
    return response.text
