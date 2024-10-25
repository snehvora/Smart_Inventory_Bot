# Smart Inventory Bot

---

## Overview

The **Smart Inventory Bot** is an intelligent system designed to handle user queries related to inventory management. The bot efficiently processes natural language questions, routes them through either a SQL query generator or a Large Language Model (LLM), and responds with relevant data or natural language explanations.

### Key functionalities include:
- Converting natural language queries to SQL queries.
- Fetching data from a SQL database based on the queries.
- Generating human-readable responses from both SQL query results and AI-generated answers.
- Error handling to manage cases where queries fail.

The system utilizes AI for understanding context and generating queries or answers, employing structured workflows to ensure that user queries are routed and processed effectively.

---

## Code Modules and Key Components

### 1. StateGraph Definition (`StateGraph`):
   - The `StateGraph` manages different states for processing user queries.
   - It defines multiple nodes, each performing a specific function.
   - The flow is designed to route the query to the correct handler based on its content and structure.

### 2. Class Definitions:
   - **`State`:** 
     This class holds the state of the current operation, such as the user's messages, the generated SQL query, the resulting data, and the prompt being worked on.
   - **`prompt_generator`:** 
     This class defines the schema for generating a final response based on user messages.
   - **`sql_query_generator`:** 
     It generates a SQL query from the user's natural language question using an AI model.
   - **`semantic_routing`:** 
     This class determines whether the question should be routed to the SQL generation module or directly to an LLM.

### 3. Functions:
   - **`llm_ai(state: State)`:** 
     This function uses an AI model to generate natural language responses to user questions that are not schema-related or not easily converted into SQL.
   - **`sql_query_gen(state: State)`:** 
     This function leverages the AI model to generate SQL queries based on the user's question and the database schema.
   - **`where_to_go(state: State)`:** 
     Determines the next step based on the nature of the user's question: either SQL query generation (`sql_query_gen`) or LLM-based generation (`llm_ai`).
   - **`sql_agent(state: State)`:** 
     Executes the generated SQL query on the SQLite database and retrieves data.
   - **`where_to_go_if_error(state: State)`:** 
     Checks if there is an error in fetching the data and directs the flow accordingly.
   - **`llm_final_response(state: State)`:** 
     Creates a natural language response based on the SQL query results and the original user query.

### 4. Graph Construction:
   - The `graph_builder` builds and manages the flow of states and their connections. It compiles the nodes and sets conditions for transitions between them.
   - It invokes functions and handlers for each state based on the user's query and processes the request to generate a final response.

---

## Workflow

1. **Start State:**
   - The process begins when a user submits a query.
   - The initial state holds the user's message.

2. **Routing Decision (`where_to_go`):**
   - Based on the user's query, the system routes the request to one of two paths:
     - **`llm_ai`:** The LLM path is chosen if the query cannot be answered using the database schema.
     - **`sql_query_gen`:** The SQL path is selected if the question pertains to the database schema and can be answered via SQL.

3. **SQL Query Generation and Execution (`sql_query_gen` & `sql_agent`):**
   - If the system routes the query to `sql_query_gen`, it generates a SQL query using the AI model.
   - The `sql_agent` function executes the query on the SQLite database and fetches the result.

4. **Error Handling (`where_to_go_if_error`):**
   - After executing the SQL query, the system checks if there was an error in fetching the data.
   - If an error occurs, the system routes the flow to the `error_in_fetching` state.
   - If no error occurs, the flow proceeds to the next state, `llm_final_response`.

5. **Final Response (`llm_final_response`):**
   - The system generates a user-friendly natural language response based on the SQL query and the fetched data.
   - The response is sent back to the user, and the workflow ends.

6. **Error Handling Path (`error_in_fetching`):**
   - If an error is detected in the process of fetching data, the flow routes to the error handling state.
   - A suitable error message or fallback response is generated, and the workflow ends.

---

## Example Workflow

### Question: *"What is the average discount percentage given in each product category over the past year?"*

1. The user asks a question related to the average discount percentage in product categories over the past year.
2. The system first checks if the question can be answered using the database schema.
3. Since the question pertains to product categories and discounts (which are present in the schema), it routes the query to the `sql_query_gen` function.
4. The SQL query is generated: 
   ```sql
   SELECT category, AVG(discount_percentage) FROM products WHERE date >= DATE('now', '-1 year') GROUP BY category;
5. The `sql_agent` executes the SQL query on the inventory database, fetching the results.
6. If there is no error in fetching, the results are passed to `llm_final_response`, which generates a natural language response, such as:
  - "The average discount percentages for each product category over the past year are as follows: Electronics: 15%, Clothing: 10%, Home Goods: 5%."
7. The workflow ends, and the user receives the response.

## Conclusion

The Smart Inventory Bot is a robust system that leverages AI and structured workflows to handle complex natural language queries related to inventory data. By using a combination of LLM responses and SQL-based data retrieval, the bot can provide accurate and human-friendly answers to a wide range of questions. The system's ability to route queries based on their nature ensures efficient and relevant responses, making it an effective tool for inventory management queries.
