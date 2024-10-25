from pydantic import BaseModel, Field
from smart_inventory_bot.app_properties.constant import DATABASE_SCHEMA
from typing import Literal


class prompt_generator(BaseModel):
    """This function answer for natural language questions like a inventory manager"""
    final_ans : str = Field(..., description=f"""
        You are an AI trained model that answers natural language questions like a inventory manager.
    """)


class semantic_routing(BaseModel):
    """This function determines the appropriate path to use based on the user question"""
    path: Literal['llm_ai', 'sql_query_gen'] = Field(..., description=f"""
        You are an AI trained to determine the appropriate path to use based on a given user question. 
        If you think that the user question is related to Database schema and the tables and columns mentioned in the schema are enough to answer, then return 'sql_query_gen' otherwise return 'llm_ai' 
        Below is the schema description of the databases:
        {DATABASE_SCHEMA}
    """)


class sql_query_generator(BaseModel):
    """This function generates fully formed SQL query for the given user question and database schema"""
    sql_query: str = Field(..., description=f"""
        You are an AI trained to convert natural language questions into Sqlite queries based on a given database schema. Below is the schema description of the database you will be querying:
        {DATABASE_SCHEMA}
        The query should be returned in plain text, not in JSON. The query should be without using placeholders like <value>. The goal is to list out all the results directly without specifying any placeholder. When writing the SELECT query add the limit of 10
    """)

