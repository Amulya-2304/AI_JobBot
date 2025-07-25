import requests
import os

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def fetch_jobs(keyword="", location="", job_type="", sort_by="relevant", page=1):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{keyword} {job_type}".strip(),
        "page": str(page),
        "num_pages": "5",
        "location": location,
        "remote_jobs_only": "false"
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        print("\n📡 API REQUEST SENT:", response.url)
        print("📦 STATUS CODE:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("📊 RESPONSE DATA KEYS:", list(data.keys()))
            print("🔍 Total Jobs Fetched:", len(data.get("data", [])))
            return data.get("data", [])
        else:
            print("❌ ERROR RESPONSE BODY:", response.text)
            return []

    except Exception as e:
        print("🔥 EXCEPTION DURING API CALL:", e)
        return []