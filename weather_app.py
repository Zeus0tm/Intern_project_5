import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = # Give your API Key "
BASE_URL = "https://api.openweathermap.org/data/2.5"
CACHE_SECONDS = 600
REQUEST_TIMEOUT = 15

# In-memory cache: {city_key: (saved_timestamp, weather_result)}
weather_cache = {}


class WeatherError(Exception):
    """Raised when weather data cannot be retrieved or parsed."""


def request_json(endpoint, params):
    """Request an OpenWeather endpoint and return its JSON response."""
    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 401:
            raise WeatherError(
                "API key rejected (401). Check your key; a newly created key "
                "may take a little time to activate."
            )
        if response.status_code == 404:
            raise WeatherError("City not found. Check the spelling and try again.")
        if response.status_code == 429:
            raise WeatherError("API request limit reached. Please try again later.")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        raise WeatherError("The weather service took too long to respond.")
    except requests.exceptions.HTTPError as error:
        raise WeatherError(f"HTTP error from weather service: {error}")
    except requests.exceptions.RequestException as error:
        raise WeatherError(f"Network error: {error}")
    except ValueError:
        raise WeatherError("The server returned invalid JSON.")


def get_weather(city):
    """Get current conditions and the next forecast period for a city."""
    if not API_KEY:
        raise WeatherError(
            "API key is missing. Create a .env file and set "
            "OPENWEATHER_API_KEY=your_key_here."
        )

    cache_key = city.strip().casefold()
    now = time.time()

    if cache_key in weather_cache:
        saved_at, cached_result = weather_cache[cache_key]
        if now - saved_at < CACHE_SECONDS:
            return cached_result, True

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    current = request_json("weather", params)
    forecast = request_json("forecast", params)

    try:
        current_weather = current["weather"][0]
        forecast_item = forecast["list"][0]
        forecast_weather = forecast_item["weather"][0]

        result = {
            "city": current["name"],
            "country": current["sys"].get("country", ""),
            "temperature": current["main"]["temp"],
            "feels_like": current["main"]["feels_like"],
            "humidity": current["main"]["humidity"],
            "condition": current_weather["description"].capitalize(),
            "forecast_time": datetime.fromtimestamp(
                forecast_item["dt"]
            ).strftime("%Y-%m-%d %H:%M"),
            "forecast": forecast_weather["description"].capitalize(),
            "forecast_temp": forecast_item["main"]["temp"],
        }
    except (KeyError, IndexError, TypeError) as error:
        raise WeatherError(f"Unexpected JSON response structure: {error}")

    weather_cache[cache_key] = (now, result)
    return result, False


def display_weather(data, from_cache=False):
    """Print weather information in a readable terminal layout."""
    location = f'{data["city"]}, {data["country"]}'.strip(", ")
    print("\n" + "=" * 42)
    print(f" WEATHER REPORT: {location}")
    print("=" * 42)
    print(f'Temperature : {data["temperature"]:.1f} °C')
    print(f'Feels like  : {data["feels_like"]:.1f} °C')
    print(f'Humidity    : {data["humidity"]}%')
    print(f'Now         : {data["condition"]}')
    print("-" * 42)
    print(f'Next forecast ({data["forecast_time"]})')
    print(f'Forecast    : {data["forecast"]}')
    print(f'Temperature : {data["forecast_temp"]:.1f} °C')
    if from_cache:
        print("\n[Cached result — refreshed within 10 minutes]")
    print("=" * 42)


def main():
    print("PYTHON WEATHER CHECKER")
    print("Type a city name, or 'quit' to exit.")

    while True:
        city = input("\nCity: ").strip()

        if city.casefold() in {"quit", "exit"}:
            print("Goodbye!")
            break
        if not city:
            print("Please enter a city name.")
            continue

        try:
            weather, from_cache = get_weather(city)
            display_weather(weather, from_cache)
        except WeatherError as error:
            print(f"\nWeather error: {error}")


if __name__ == "__main__":
    main()
