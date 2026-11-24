# 🌦️ Weather-Aware Order Delay System

A Python CLI tool that checks live weather for each order's city using the **OpenWeatherMap API** and automatically flags deliveries as `Delayed` when severe weather (Rain, Snow, or Extreme conditions) is detected.

---

## 📋 Features

- **Concurrent API calls** — fetches weather for all cities simultaneously using `asyncio.gather`
- **Smart delay classification** — flags Rain, Snow, Thunderstorm, Tornado, Squall conditions
- **Personalized apology messages** — generates customer-specific delay notifications
- **Graceful error handling** — invalid cities are logged without crashing the script
- **Secure** — API key stored in `.env`, never hardcoded

---

## 🗂️ Project Structure

```
weather-aware-delay-system/
├── main.py          # Entry point — orchestrates the full flow
├── weather.py       # Async weather fetcher + delay classifier
├── apology.py       # Weather-aware apology message generator
├── orders.json      # Order data (statuses updated after each run)
├── ai_log.md        # AI prompts used to build this project
├── .env.example     # API key template (safe to commit)
├── .gitignore       # Excludes .env from git
└── requirements.txt # Python dependencies
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/Jeevanm2004/weather-aware-delay-system.git
cd weather-aware-delay-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
```bash
cp .env.example .env
```
Then open `.env` and replace the placeholder with your [OpenWeatherMap API key](https://openweathermap.org/api):
```
OPENWEATHER_API_KEY=your_actual_key_here
```

### 4. Run the script
```bash
python3 main.py
```

---

## 🚀 Example Output

```
============================================================
   🌦️  Weather-Aware Order Delay System
============================================================

📋  Loaded 4 orders from orders.json

🌐  Fetching weather for all cities concurrently...

  🔴  [DELAYED] New York — Heavy rain
       💬  Hi Alice, your order to New York is delayed due to heavy rain. We appreciate your patience!

  🟢  [OK]      Mumbai — Clear sky. No delays expected.
  🟢  [OK]      London — Overcast clouds. No delays expected.
  ❌  [ERROR]   City not found: 'InvalidCity123' — skipping, other orders unaffected.

💾  orders.json updated.

------------------------------------------------------------
📦  Final Order Summary
------------------------------------------------------------
  🔴  Order 1001 | Alice Smith          | New York        | Delayed
  🟢  Order 1002 | Bob Jones            | Mumbai          | Pending
  🟢  Order 1003 | Charlie Green        | London          | Pending
  🟢  Order 1004 | InvalidCity123       | InvalidCity123  | Pending
------------------------------------------------------------
```

---

## 🌩️ Delay Conditions

| OWM Condition | Triggers Delay |
|---|---|
| `Rain` | ✅ |
| `Drizzle` | ✅ |
| `Snow` | ✅ |
| `Thunderstorm` | ✅ |
| `Tornado` | ✅ |
| `Squall` | ✅ |
| `Clear`, `Clouds`, `Mist`, etc. | ❌ |

---

## 🔐 Security

- API key is loaded from `.env` via `python-dotenv`
- `.env` is listed in `.gitignore` and is **never committed**
- Use `.env.example` as a safe template for collaborators

---

## 📦 Dependencies

```
aiohttp
python-dotenv
```

---

## 📄 API Used

[OpenWeatherMap Current Weather API](https://openweathermap.org/current) (Free Tier)
