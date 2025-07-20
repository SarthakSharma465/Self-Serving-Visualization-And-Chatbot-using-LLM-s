---

# Self-Service Visualizer & Chatbot

A **Streamlit-based LLM application** that enables users to interact with a database using natural language queries. The app integrates **OpenAI GPT models**, **Azure Synapse SQL**, and powerful **Python visualization libraries** to deliver insightful data visualizations and text-based chatbot responses — all via an intuitive web interface.

## 🚀 Project Overview

This application was developed as part of the **DataSonic project** to allow policy-related data querying and visualization from an **Azure Synapse SQL** database. It provides two main functionalities:

* **Data Visualizer**: Converts natural language queries into SQL and visualizes the results.
* **Chatbot**: Answers user questions in natural language based on database content.

---

## 🏗️ Architecture Overview

The system architecture comprises:

1. **Start Node**: App initialization and setup.
2. **SQL DB Connection**: Establishes connection to Azure Synapse SQL via `pyodbc`.
3. **Schema Fetching**:

   * *Presentation Schema* for Visualizer.
   * *Entire Schema* for Chatbot.
4. **Prompt Preparation**: Combines schema and user input.
5. **LLM API Calls**:

   * Generate SQL queries.
   * Generate visualizations or natural language answers.
6. **Execution & Rendering**: Executes queries, handles errors, and displays results.
7. **Streamlit UI**: Dual-tab interface for interaction.
8. **Stop Node**: Closes database connections gracefully.

---

## 📊 Features

### 🧠 LLM Capabilities (Powered by GPT-4o)

* **SQL Query Generation**: Adheres to schema constraints.
* **Visualization Code Generation**: Uses Plotly, Altair, or Matplotlib.
* **Natural Language Explanation**: Translates SQL results into plain English.

### 🔍 Tabs in Streamlit UI

#### 1. Data Visualizer

* Uses only the **presentation schema**.
* Returns **interactive charts**.

#### 2. Chatbot

* Accesses the **entire database schema**.
* Provides **textual insights**.

---

## 🧰 Tech Stack

| Component        | Technology                 |
| ---------------- | -------------------------- |
| LLM Backend      | OpenAI GPT-4o              |
| UI Framework     | Streamlit 1.24.0           |
| Programming Lang | Python 3.13                |
| Database         | Azure Synapse SQL          |
| SQL Driver       | pyodbc + ODBC Driver 17    |
| Visualization    | Plotly, Altair, Matplotlib |

---

## ⚙️ Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-org/self-service-visualizer-chatbot.git
   cd self-service-visualizer-chatbot
   ```

2. **Install Dependencies**

   ```bash
   pip install streamlit openai pyodbc altair plotly matplotlib
   ```

3. **API Key Setup**

   * Create a file `api_key.txt` in the root directory.
   * Paste your OpenAI API key into the file.

4. **Run the App**

   ```bash
   streamlit run app.py
   ```

---

## 🗂️ Application Structure

```text
├── app.py                  # Main Streamlit application
├── api_call.py             # Wrapper for OpenAI API
├── schema_fetch.py         # Schema retrieval logic
├── api_key.txt             # Your OpenAI API Key (not tracked in Git)
└── README.md               # This file
```

---

## 🧮 Database Connection

```python
server = 'adro-data-sonic-ondemand.sql.azuresynapse.net'
database = 'Datasonic_Workflow'
username = 'sqladminuser'
password = 'root@123'
```

Ensure that the above credentials are secured in production via environment variables or secret management systems.

---

## 🧪 Error Handling

* **Rate Limiting (HTTP 429)**: Displays friendly message to retry later.
* **Execution Errors**: Catches API and SQL errors gracefully.

---

## 📈 Data Flow (Data Visualizer)

1. User submits query.
2. App fetches presentation schema.
3. SQL query is generated and executed.
4. Data is passed to the LLM to generate Python code.
5. Visualization is rendered on the UI.

---

## 💬 Chatbot Flow

1. User submits a natural language question.
2. App fetches entire database schema.
3. LLM generates SQL and executes it.
4. Results are interpreted and presented in plain English.

---

## 🔒 Closing the Connection

The application closes all connections on termination to avoid resource leakage.

```python
if 'connection' in locals() and conn.is_connected():
    conn.close()
    cursor.close()
```

---

## 📄 License

This project is part of the **DataSonic initiative** and licensed under [MIT License](LICENSE).

---
