from smart_inventory_bot.components.graph_components.states import State
import instructor
from cohere import Client
from smart_inventory_bot.components import function_schema
from smart_inventory_bot.components.sqlite_utils import sqlite_exc
from smart_inventory_bot.app_properties.constant import DATABASE_SCHEMA
from smart_inventory_bot.components.cohere_utils import cohere_text_generation
from dotenv import load_dotenv
import os
load_dotenv()



client = instructor.from_cohere(Client())

def where_to_go(state: State):
    resp = client.chat.completions.create(
        response_model=function_schema.semantic_routing,
        messages=[
            {
                "role": "user",
                "content": state["messages"][0].content,
            }
        ],
    )

    print(resp)
    return resp.path


def llm_ai(state: State):
    resp = client.chat.completions.create(
        response_model=function_schema.prompt_generator,
        messages=[
            {
                "role": "user",
                "content": state["messages"][0].content,
            }
        ],
    )

    return {"messages": resp.final_ans}


def sql_query_gen(state: State):
    resp = client.chat.completions.create(
        response_model=function_schema.sql_query_generator,
        messages=[
            {
                "role": "user",
                "content": state["messages"][0].content,
            }
        ],
    )

    print(resp.sql_query)
    return {"sql_query": resp.sql_query}


def sql_agent(state: State):
    data = sqlite_exc(state["sql_query"])
    print(data)
    return {'data' : data}


def where_to_go_if_error(state: State):
    if state['data'] == "error":
        return 'error_in_fetching'
    else:
        return 'llm_final_response'
    

def error_in_fetching(state: State):
    return {"messages": "Couldn't fetch the data. Kindly provide more descriptive query"}


def llm_final_response(state: State):
    prompt = f"""
    Based on the user question, SQL query and SQL response, generate a clear and concise natural language response that directly answers the question without referencing the database schema or SQL process.
    {DATABASE_SCHEMA}
    Question: {state['messages'][0].content}
    SQL Response: {state['data']}
    SQL query: {state['sql_query']}
    """

    generated_text = cohere_text_generation(prompt, temperature=0.5)
    return {"messages": generated_text}


