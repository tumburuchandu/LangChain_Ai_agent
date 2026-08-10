import os
import certifi
import requests
import streamlit as st
from dotenv import load_dotenv


from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor


# ============================================================
# Configuration
# ============================================================

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

GOOGLE_API_KEY = os.getenv("Google_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_FORECAST_API_KEY")


# ============================================================
# Streamlit Page Configuration
# ============================================================

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# Application Header
# ============================================================

st.title("🤖 AI Agent")
st.write(
    "An AI agent powered by Google Gemini with web search "
    "and weather capabilities."
)


# ============================================================
# Validate API Keys
# ============================================================

missing_keys = []

if not GOOGLE_API_KEY:
    missing_keys.append("Google_API_KEY")

if not TAVILY_API_KEY:
    missing_keys.append("TAVILY_API_KEY")

if not WEATHER_API_KEY:
    missing_keys.append("WEATHER_FORECAST_API_KEY")


if missing_keys:
    st.error(
        "Missing API keys: " +
        ", ".join(missing_keys)
    )
    st.stop()


# ============================================================
# Weather Tool
# ============================================================

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather information for a given city
    using the Weatherstack API.
    """

    if not WEATHER_API_KEY:
        return "Weatherstack API key is not configured."

    url = "https://api.weatherstack.com/current"

    params = {
        "access_key": WEATHER_API_KEY,
        "query": city
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        # Weatherstack API error
        if "error" in data:

            error = data["error"]

            error_code = error.get(
                "code",
                "Unknown"
            )

            error_info = error.get(
                "info",
                "Unknown Weatherstack error"
            )

            return (
                f"Weatherstack API error.\n"
                f"Error code: {error_code}\n"
                f"Message: {error_info}"
            )

        # HTTP error
        if response.status_code != 200:

            return (
                f"Weather API request failed.\n"
                f"HTTP status: {response.status_code}"
            )

        location = data.get(
            "location",
            {}
        )

        current = data.get(
            "current",
            {}
        )

        city_name = location.get(
            "name",
            city
        )

        country = location.get(
            "country",
            ""
        )

        temperature = current.get(
            "temperature"
        )

        feels_like = current.get(
            "feelslike"
        )

        humidity = current.get(
            "humidity"
        )

        condition = current.get(
            "weather_descriptions",
            ["Unknown"]
        )[0]

        wind_speed = current.get(
            "wind_speed"
        )

        wind_direction = current.get(
            "wind_dir"
        )

        pressure = current.get(
            "pressure"
        )

        visibility = current.get(
            "visibility"
        )

        precipitation = current.get(
            "precip"
        )

        return (
            f"Weather Report for "
            f"{city_name}, {country}\n"
            f"Condition: {condition}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind speed: {wind_speed} km/h\n"
            f"Wind direction: {wind_direction}\n"
            f"Pressure: {pressure} mb\n"
            f"Visibility: {visibility} km\n"
            f"Precipitation: {precipitation} mm"
        )

    except requests.exceptions.Timeout:

        return "Weather API request timed out."

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to the "
            "Weatherstack API."
        )

    except requests.exceptions.RequestException as e:

        return (
            f"Weather API request failed: {str(e)}"
        )

    except ValueError:

        return (
            "Weatherstack returned an "
            "invalid JSON response."
        )

    except Exception as e:

        return (
            f"Unexpected weather error: {str(e)}"
        )


# ============================================================
# Tavily Search Tool
# ============================================================

search_tool = TavilySearchResults(
    max_results=3
)


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)


# ============================================================
# Tools
# ============================================================

tools = [
    search_tool,
    get_weather
]


# ============================================================
# Agent Prompt
# ============================================================

prompt = hub.pull(
    "hwchase17/react"
)


# ============================================================
# Create Agent
# ============================================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# ============================================================
# Agent Executor
# ============================================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)


# ============================================================
# User Interface
# ============================================================

st.subheader("Ask the AI Agent")

user_input = st.text_area(
    "Enter your question:",
    placeholder=(
        "Example: What is the weather in New Delhi "
        "and what are the latest news about Gen Z protests?"
    ),
    height=120
)


# ============================================================
# Run Agent
# ============================================================

if st.button("🚀 Ask Agent", type="primary"):

    if not user_input.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Agent is thinking and using tools..."
        ):

            try:

                response = agent_executor.invoke(
                    {
                        "input": user_input
                    }
                )

                output = response.get(
                    "output",
                    "No response generated."
                )

                st.success("Agent Response")

                st.write(output)

            except Exception as e:

                st.error(
                    f"Agent execution failed: {str(e)}"
                )


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("🛠️ Available Tools")

    st.write(
        "### 🔎 Tavily Search"
    )

    st.write(
        "Searches the web for current information, "
        "news and facts."
    )

    st.write(
        "### 🌤️ Weatherstack"
    )

    st.write(
        "Retrieves current weather information "
        "for a city."
    )

    st.divider()

    st.caption(
        "Powered by LangChain + Gemini + Tavily + Weatherstack"
    )