import streamlit as st
from smart_inventory_bot.components.graph_components.states import State
from smart_inventory_bot.components.graph_components import nodes as Node
from smart_inventory_bot.components.sqlite_utils import sqlite_exc
from smart_inventory_bot.components.cohere_utils import cohere_text_generation
# from rapid_law.components.ollama_utils import ollama_text_generation
# from rapid_law.components.gemini_utils import gemini_text_generation
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
# from openai import OpenAI


graph_builder = StateGraph(State)

graph_builder.add_node("llm_ai", Node.llm_ai)
graph_builder.add_node("sql_query_gen", Node.sql_query_gen)
graph_builder.add_node("sql_agent", Node.sql_agent)
graph_builder.add_node("error_in_fetching", Node.error_in_fetching)
graph_builder.add_node("llm_final_response", Node.llm_final_response)


graph_builder.add_conditional_edges(
    START,
    Node.where_to_go,
    {"llm_ai": "llm_ai", "sql_query_gen": "sql_query_gen"},

)
graph_builder.add_edge("sql_query_gen", "sql_agent")

graph_builder.add_conditional_edges(
    'sql_agent',
    Node.where_to_go_if_error,
    {"error_in_fetching": "error_in_fetching", "llm_final_response": "llm_final_response"},

)

graph_builder.add_edge("llm_ai", END)
graph_builder.add_edge("llm_final_response", END)
graph_builder.add_edge("error_in_fetching", END)

graph = graph_builder.compile()



st.title("💬 Smart Inventory Bot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = graph.invoke({"messages": ("user", str(prompt))})
    # data = sqlite_exc("SELECT Staff.Staff_ID, Staff.First_Name, Staff.Last_Name, COUNT(`Order`.Order_ID) AS Total_Orders, SUM(Order_Detail.Total) AS Total_Revenue FROM Staff LEFT JOIN Customer ON Staff.Staff_ID = Customer.Staff_ID LEFT JOIN `Order` ON Customer.Customer_ID = `Order`.Customer_ID LEFT JOIN Order_Detail ON `Order`.Order_ID = Order_Detail.Order_ID WHERE `Order`.Date_of_Order BETWEEN '2024-08-01' AND '2024-08-31' GROUP BY Staff.Staff_ID, Staff.First_Name, Staff.Last_Name;")
    # st.write(data)
    msg = response['messages'][-1].content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)