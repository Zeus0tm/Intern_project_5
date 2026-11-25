# Python Weather Checker

A command-line weather app that calls the OpenWeather REST API, parses its JSON response, and displays current temperature, humidity, conditions, and the next available forecast period for a city.

## Features

- Requests current weather and 5-day / 3-hour forecast data.
- Displays temperature in Celsius (`units=metric`), feels-like temperature, humidity, and a short forecast.
- Handles unknown cities, rejected API keys, rate limits, timeouts, HTTP errors, and invalid JSON.
- Caches successful results in memory for 10 minutes to reduce repeat requests.
- Reads the API key from an environment variable / `.env` file. No key is included in this repository.

## Files

- `weather_app.py` — application source.
- `.env.example` — environment variable template (contains no real key).
- `.gitignore` — excludes `.env`, Python caches, and local files.
- `requirements.txt` — dependencies.

## 1. Get an API key

Create an account at [OpenWeather](https://openweathermap.org/) and generate an API key. New keys may take some time to activate.

## 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 3. Configure your key

Copy `.env.example` to a new file named `.env`, then replace the placeholder:

```env
OPENWEATHER_API_KEY=put_your_real_key_here
```

Never paste your real key into `weather_app.py`, README, screenshots, or a public GitHub repository. Keep `.env` untracked.

## 4. Run

```bash
python weather_app.py
```

Enter a city such as `Sivakasi,IN`, `Chennai,IN`, or `London,GB`. Type `quit` to close the program.

## API endpoints

- Current weather: `https://api.openweathermap.org/data/2.5/weather`
- 5-day / 3-hour forecast: `https://api.openweathermap.org/data/2.5/forecast`

Both requests send `q`, `appid`, and `units=metric`. OpenWeather returns JSON; the app reads nested fields such as `main.temp`, `main.humidity`, `weather[0].description`, and `list[0].weather[0].description`.

## API key protection

The key is stored locally in `.env` and loaded with `python-dotenv`. `.gitignore` excludes `.env` so it is not committed. The `.env.example` file contains only a placeholder. If a key is accidentally published, revoke it in the OpenWeather account and create a replacement.

## Cache behavior

Successful city results are cached in memory for 10 minutes. Restarting the program clears the cache. OpenWeather recommends avoiding repeated requests for the same location more frequently than once every 10 minutes; see its API care recommendations.

## Screenshot / real result

A real screenshot requires your own active API key. After configuring `.env`, run the program and capture the terminal after a successful city lookup. Do not show the key in the screenshot. No live result is fabricated or included in this starter project.
