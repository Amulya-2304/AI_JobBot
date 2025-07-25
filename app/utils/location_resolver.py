import requests
import os

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def resolve_location(city_input):
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"

    querystring = {
        "namePrefix": city_input,
        "limit": "1",
        "types": "CITY"
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                city = data["data"][0]["city"]
                country = data["data"][0]["country"]
                return f"{city}, {country}"
    except Exception as e:
        print("🌍 Location resolver error:", e)

    return city_input  # fallback to original