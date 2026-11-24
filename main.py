"""
main.py
Entry point for the Weather-Aware Order Delay System.

Flow:
  1. Load orders from orders.json
  2. Load API key from .env
  3. Fetch weather for ALL cities concurrently (asyncio.gather)
  4. Flag delayed orders, generate apology messages
  5. Handle errors gracefully (no crash on invalid cities)
  6. Write updated orders back to orders.json
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

from apology import generate_apology
from weather import CityNotFoundError, WeatherFetchError, classify_weather, fetch_weather

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR   = Path(__file__).parent
ORDERS_FILE = BASE_DIR / "orders.json"
ENV_FILE    = BASE_DIR / ".env"

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_orders() -> list[dict]:
    """Read orders from orders.json."""
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)


def save_orders(orders: list[dict]) -> None:
    """Write updated orders back to orders.json (pretty-printed)."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)


def print_banner() -> None:
    print("\n" + "=" * 60)
    print("   🌦️  Weather-Aware Order Delay System")
    print("=" * 60 + "\n")


def print_summary(orders: list[dict]) -> None:
    print("\n" + "-" * 60)
    print("📦  Final Order Summary")
    print("-" * 60)
    for o in orders:
        icon = "🔴" if o["status"] == "Delayed" else "🟢"
        print(f"  {icon}  Order {o['order_id']} | {o['customer']:<20} | "
              f"{o['city']:<15} | {o['status']}")
    print("-" * 60 + "\n")


# ── Core async logic ──────────────────────────────────────────────────────────

async def process_orders(orders: list[dict], api_key: str) -> None:
    """
    Fetch weather for all cities concurrently and update order statuses.

    Key: asyncio.gather(..., return_exceptions=True) ensures one failed
    city (like InvalidCity123) does NOT cancel the other API calls.
    """
    async with aiohttp.ClientSession() as session:

        # Fire all API calls at the same time — parallel fetching
        tasks = [
            fetch_weather(session, order["city"], api_key)
            for order in orders
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process each result paired with its order
    for order, result in zip(orders, results):
        city     = order["city"]
        customer = order["customer"]

        # ── Error cases ───────────────────────────────────────────────────────
        if isinstance(result, CityNotFoundError):
            print(f"  ❌  [ERROR] {result} — skipping, other orders unaffected.")
            continue

        if isinstance(result, Exception):
            print(f"  ⚠️   [ERROR] Could not fetch weather for '{city}': {result}")
            continue

        # ── Happy path ────────────────────────────────────────────────────────
        is_delayed, condition = classify_weather(result)
        description = result["weather"][0]["description"].capitalize()

        if is_delayed:
            order["status"] = "Delayed"
            apology = generate_apology(customer, city, condition)
            print(f"  🔴  [DELAYED] {city} — {description}")
            print(f"       💬  {apology}\n")
        else:
            print(f"  🟢  [OK]      {city} — {description}. No delays expected.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    print_banner()

    # Load environment variables
    load_dotenv(ENV_FILE)
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("❌  OPENWEATHER_API_KEY not found in .env — aborting.")
        sys.exit(1)

    # Load orders
    orders = load_orders()
    print(f"📋  Loaded {len(orders)} orders from orders.json\n")
    print("🌐  Fetching weather for all cities concurrently...\n")

    # Run async processing
    asyncio.run(process_orders(orders, api_key))

    # Save results
    save_orders(orders)
    print(f"💾  orders.json updated.\n")

    # Print final summary table
    print_summary(orders)


if __name__ == "__main__":
    main()
