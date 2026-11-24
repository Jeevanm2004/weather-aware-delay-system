# AI Log — Weather-Aware Order Delay System

This document lists the AI prompts used while building the two
key technical components: Parallel Fetching and Error Handling.

---

## Prompt 1 — Parallel Fetching

**Goal:** Fetch weather data for multiple cities at the same time, not one by one.

**Prompt used:**
> "Write an async Python function using `aiohttp` and `asyncio.gather` that
> fetches weather data for a list of cities concurrently from the
> OpenWeatherMap API and returns all results together, without blocking on
> each individual request."

**What it produced:**
The core pattern in `main.py` where all `fetch_weather()` coroutines are
created as a list of tasks and passed to `asyncio.gather()` together,
so all HTTP requests fire simultaneously instead of sequentially.

```python
tasks = [fetch_weather(session, order["city"], api_key) for order in orders]
results = await asyncio.gather(*tasks, return_exceptions=True)
```

---

## Prompt 2 — Error Handling (Invalid City)

**Goal:** Make the script survive a bad city name without crashing.

**Prompt used:**
> "How do I use `asyncio.gather` so that if one of the async tasks raises
> an exception (like a 404 city-not-found error), the other tasks still
> complete normally and the script does not crash?"

**What it produced:**
The `return_exceptions=True` flag on `asyncio.gather`. With this flag,
exceptions are returned as values in the results list instead of being
raised immediately, so a single failure does not cancel the whole batch.

```python
results = await asyncio.gather(*tasks, return_exceptions=True)

for order, result in zip(orders, results):
    if isinstance(result, CityNotFoundError):
        print(f"[ERROR] City not found: {order['city']} — skipping.")
        continue
    # ... process valid results
```

---

## Prompt 3 — Weather-Aware Apology (AI Challenge)

**Goal:** Generate a personalised, human-friendly delay message per customer.

**Prompt used:**
> "Write a Python function that takes a customer name, city, and an
> OpenWeatherMap weather condition string (like 'Rain' or 'Snow') and
> returns a personalised delivery delay apology message in the format:
> 'Hi {first_name}, your order to {city} is delayed due to {reason}.
> We appreciate your patience!'"

**What it produced:**
The `generate_apology()` function in `apology.py` with a lookup table
(`WEATHER_PHRASES`) that maps OWM condition strings to natural language
phrases, and uses only the customer's first name for a friendly tone.

```python
def generate_apology(customer: str, city: str, condition: str) -> str:
    first_name = customer.split()[0]
    phrase = WEATHER_PHRASES.get(condition, "extreme weather conditions")
    return (
        f"Hi {first_name}, your order to {city} is delayed due to {phrase}. "
        f"We appreciate your patience!"
    )
```
