"""
weather.py
Handles all OpenWeatherMap API interactions:
  - Async fetching with aiohttp
  - Custom exceptions for clean error handling
  - Weather classification (delay or no delay)
"""

import aiohttp

# ── Custom Exceptions ────────────────────────────────────────────────────────

class CityNotFoundError(Exception):
    """Raised when OWM returns 404 — city does not exist."""
    pass


class WeatherFetchError(Exception):
    """Raised on any other non-200 HTTP response from OWM."""
    pass


# ── Weather conditions that trigger a delivery delay ─────────────────────────

DELAY_CONDITIONS = {
    "Rain",
    "Drizzle",
    "Snow",
    "Thunderstorm",
    "Tornado",
    "Squall",
}


# ── Async fetch ───────────────────────────────────────────────────────────────

async def fetch_weather(session: aiohttp.ClientSession, city: str, api_key: str) -> dict:
    """
    Fetch current weather for `city` from OpenWeatherMap.

    Returns:
        dict: Parsed JSON response from OWM.

    Raises:
        CityNotFoundError: If the city is not recognised by OWM (HTTP 404).
        WeatherFetchError:  On any other non-200 HTTP status.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    async with session.get(url, params=params) as response:
        if response.status == 404:
            raise CityNotFoundError(f"City not found: '{city}'")
        if response.status != 200:
            raise WeatherFetchError(
                f"HTTP {response.status} while fetching weather for '{city}'"
            )
        return await response.json()


# ── Classifier ────────────────────────────────────────────────────────────────

def classify_weather(weather_data: dict) -> tuple[bool, str]:
    """
    Determine whether the weather warrants a delivery delay.

    Args:
        weather_data: Parsed OWM API response dict.

    Returns:
        (is_delayed: bool, condition: str)
        e.g. (True, "Rain") or (False, "Clear")
    """
    condition = weather_data["weather"][0]["main"]
    return condition in DELAY_CONDITIONS, condition
