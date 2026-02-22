import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY")

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}"
    r = requests.get(url).json()

    return {
        "temp": r["current"]["temp_f"],
        "precipitation": r["current"]["precip_in"]
    }