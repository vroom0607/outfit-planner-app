import requests

API_KEY = "YOUR_OPENWEATHER_API_KEY"

def get_weather(city="Pullman"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "imperial"}
    data = requests.get(url, params=params).json()

    """
    return {
        "temp": data.get("main", {}).get("temp", 70),
        "rain": "rain" in data.get("weather", [{}])[0].get("main", "").lower()
    }
    """
    #temporary
    return {
        "temp": 70,
        "rain": False
    }