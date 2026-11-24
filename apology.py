"""
apology.py
Generates personalised "Weather-Aware Apology" messages for delayed orders.
This satisfies the AI Challenge requirement from the assignment.
"""

# ── Human-readable phrases per OWM condition ─────────────────────────────────

WEATHER_PHRASES: dict[str, str] = {
    "Rain":         "heavy rain",
    "Drizzle":      "heavy drizzle",
    "Snow":         "heavy snowfall",
    "Thunderstorm": "thunderstorms",
    "Tornado":      "a tornado warning",
    "Squall":       "severe squalls",
}


# ── Apology generator ─────────────────────────────────────────────────────────

def generate_apology(customer: str, city: str, condition: str) -> str:
    """
    Generate a personalised delivery delay apology message.

    Args:
        customer:  Customer's full name (e.g. "Alice Smith").
        city:      Destination city (e.g. "New York").
        condition: OWM weather condition string (e.g. "Rain").

    Returns:
        A human-friendly apology string.

    Example:
        "Hi Alice, your order to New York is delayed due to heavy rain.
         We appreciate your patience!"
    """
    # Use only the first name for a friendlier tone
    first_name = customer.split()[0]
    phrase = WEATHER_PHRASES.get(condition, "extreme weather conditions")

    return (
        f"Hi {first_name}, your order to {city} is delayed due to {phrase}. "
        f"We appreciate your patience!"
    )
