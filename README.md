# 🤖 LangChain AI Agent

A practical **Agentic AI application** built with **LangChain, Google Gemini, Tavily Search, Weatherstack, and Streamlit**.

The application demonstrates how an LLM-powered agent can understand a user's request, decide when external tools are required, invoke the appropriate tool, and generate a final response based on the tool results.

## 🚀 Features

* **LLM-powered AI Agent** using Google Gemini
* **ReAct Agent architecture** using LangChain
* **Web Search** using Tavily
* **Real-time Weather Information** using Weatherstack
* **Tool Calling** — the agent can select the appropriate tool based on the user's query
* **Streamlit Web Interface**
* **Environment-based API key management**
* Error handling for external API failures
* Interactive agent execution through a browser UI

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              Streamlit Interface
                     │
                     ▼
                LangChain Agent
                     │
                     ▼
                Google Gemini
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    Tavily Search          Weather Tool
          │                     │
          ▼                     ▼
    Web Search API        Weatherstack API
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
                Agent Response
                     │
                     ▼
              Streamlit UI
```

## 🛠️ Tech Stack

### Programming Language

* Python

### AI / LLM

* Google Gemini
* LangChain
* ReAct Agent

### Tools / APIs

* Tavily Search API
* Weatherstack API

### Application

* Streamlit

### Supporting Libraries

* Requests
* python-dotenv
* Certifi

## 📂 Project Structure

```text
LangChain_Ai_agent/
│
├── app.py
├── main..py
├── requirements.txt
├── .gitignore
│
└── research/
    └── agent_demo.ipynb
```

## ⚙️ How It Works

The application receives a natural-language request from the user.

For example:

```text
What is the weather in New Delhi and what are the latest news about Gen Z protests?
```

The agent analyzes the request and determines which tools are required.

For this example:

```text
User Query
    │
    ▼
Google Gemini
    │
    ├── Weather information
    │       ↓
    │   Weatherstack
    │
    └── Latest news
            ↓
        Tavily Search
    │
    ▼
Final Response
```

The important concept demonstrated by this project is that the **LLM is not directly providing all information itself**. It can use external tools when current or external information is required.

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/tumburuchandu/LangChain_Ai_agent.git
```

### 2. Navigate to the project

```bash
cd LangChain_Ai_agent
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Configuration

Create a `.env` file in the project root:

```env
Google_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHER_FORECAST_API_KEY=your_weatherstack_api_key
```

### Important

Never commit your `.env` file or expose API keys publicly.

The `.gitignore` file is configured to prevent `.env` and the virtual environment from being committed.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can interact with the AI agent.

## 💬 Example Queries

### General Information

```text
What is the capital of France?
```

The agent can use the web search tool when appropriate.

### Current Information

```text
What are the latest technology news?
```

The agent can use Tavily to search the web.

### Weather

```text
What is the weather in Bangalore today?
```

The agent can use the Weatherstack tool.

### Multiple Tools

```text
What is the weather in New Delhi and what are the latest news about Gen Z protests?
```

The agent can use both Weatherstack and Tavily to answer the request.

## 🎯 Learning Objectives

This project was developed to understand the fundamentals of building tool-using AI agents with LangChain.

Key concepts demonstrated:

* Large Language Model integration
* Agent architecture
* ReAct prompting
* Tool creation
* External API integration
* Tool selection by an LLM
* Environment variable management
* API error handling
* Streamlit application development

## 🔮 Future Improvements

Possible improvements include:

* Add conversation memory
* Add persistent chat history
* Add additional tools
* Improve tool error handling
* Add structured tool outputs
* Add authentication
* Add LangSmith tracing and monitoring
* Deploy the application to a cloud platform
* Add more specialized agents
* Implement a multi-agent architecture

## ⚠️ Current Limitations

This project is primarily a learning and demonstration application.

It currently uses a relatively simple ReAct agent architecture and a small set of external tools. It is not intended to represent a production-grade autonomous agent system.

## 👨‍💻 Author

**Tumburu Chandu**

GitHub:
https://github.com/tumburuchandu

---

⭐ If you found this project useful, consider giving the repository a star.
