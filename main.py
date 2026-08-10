import os
import certifi
import requests
from langchain.tools import tool

from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.agents import create_react_agent, AgentExecutor

# Load environment variables from .env file
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_FORECAST_API_KEY")

#create a search tool using TavilySearchResults
search_tool = TavilySearchResults(max_results=3)

result = search_tool.invoke("What is the captial of Frence ")
print(result)

#Creating a function to get weather information

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather information for a given city using the Weatherstack API.

    Args:
        city (str): The name of the city to get weather information for.

    Returns:
        str: A human-readable current weather report.
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

        # Convert response to JSON first
        data = response.json()

        # Weatherstack API-level error
        if "error" in data:
            error = data["error"]

            error_code = error.get("code", "Unknown")
            error_info = error.get("info", "Unknown Weatherstack error")

            return (
                f"Weatherstack API error.\n"
                f"Error code: {error_code}\n"
                f"Message: {error_info}"
            )

        # HTTP-level error
        if response.status_code != 200:
            return (
                f"Weather API request failed.\n"
                f"HTTP status: {response.status_code}"
            )

        # Extract location information
        location = data.get("location", {})
        current = data.get("current", {})

        city_name = location.get("name", city)
        country = location.get("country", "")

        # Extract weather information
        temperature = current.get("temperature")
        feels_like = current.get("feelslike")
        humidity = current.get("humidity")
        condition = current.get(
            "weather_descriptions",
            ["Unknown"]
        )[0]

        wind_speed = current.get("wind_speed")
        wind_direction = current.get("wind_dir")

        pressure = current.get("pressure")
        visibility = current.get("visibility")
        precipitation = current.get("precip")

        return (
            f"Weather Report for {city_name}, {country}\n"
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
        return "Could not connect to the Weatherstack API."

    except requests.exceptions.RequestException as e:
        return f"Weather API request failed: {str(e)}"

    except ValueError:
        return "Weatherstack returned an invalid JSON response."

    except Exception as e:
        return f"Unexpected error while getting weather: {str(e)}"

#creating a llm using ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)

response = llm.invoke("What year is it?, and what is the date today?, and latest news about gen z protest at jantar mantar")
print(response.content())

#tools include the search tool
tools = [search_tool]

#creating a prompt using hub.pull
prompt = hub.pull("hwchase17/react")
print(prompt)

#creating an agent using create_react_agent
agent = create_react_agent(
    llm = llm, 
    tools = tools, 
    prompt = prompt)

#Creating an agent executor using AgentExecutor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True
    )

#invoking the agent executor with a query
response = agent_executor.invoke({
    "input" : ("What is the captial of Frence, and what is the date today?,"
               " and latest news about gen z protest at jantar mantar"
               "and what is the weather in New Delhi, India today?"
               )
    })

print(response["output"])