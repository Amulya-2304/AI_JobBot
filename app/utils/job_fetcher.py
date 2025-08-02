import os
import requests

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")


def fetch_jobs(keyword="", location="", job_type="", sort_by="", page=1):
    """
    Fetch jobs from RapidAPI JSearch first.
    If no jobs are returned (common for European cities), fallback to Adzuna API.
    Supports manual pagination (10 jobs/page).
    """
    keyword = keyword.strip()
    location = location.strip()
    query = f"{keyword} {location}".strip()

    jobs = []
    results_per_page = 10
    max_pages = 10  # Fetch up to 100 jobs

    # ----------------------------
    # 1️⃣ Primary: RapidAPI JSearch
    # ----------------------------
    try:
        for p in range(1, max_pages + 1):
            querystring = {
                "query": query,
                "page": str(p),
                "num_pages": "1",
                "date_posted": "all",
            }
            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": RAPIDAPI_HOST
            }

            response = requests.get("https://jsearch.p.rapidapi.com/search",
                                    headers=headers, params=querystring)
            print("📡 RapidAPI REQUEST:", response.url)

            if response.status_code == 200:
                data = response.json()
                data_jobs = data.get("data", [])
                if not data_jobs:
                    break

                for item in data_jobs:
                    jobs.append({
                        "job_title": item.get("job_title", "N/A"),
                        "employer_name": item.get("employer_name", "N/A"),
                        "job_type": item.get("job_employment_type", "N/A"),
                        "posted_date": item.get("job_posted_at_datetime_utc", "N/A"),
                        "description": item.get("job_description", "No description provided."),
                        "apply_link": item.get("job_apply_link", "#"),
                        "job_url": item.get("job_apply_link", "#"),
                        "job_city": item.get("job_city", "N/A"),
                        "job_country": item.get("job_country", "N/A")
                    })

                if len(data_jobs) < results_per_page:
                    break
            else:
                print("⚠️ RapidAPI error:", response.text)
                break

    except Exception as e:
        print("❌ RapidAPI fetch error:", e)

    # ----------------------------
    # 2️⃣ Fallback: Adzuna API
    # ----------------------------
    if len(jobs) == 0 and ADZUNA_APP_ID and ADZUNA_APP_KEY:
        try:
            country = "de" if "germany" in location.lower() or "berlin" in location.lower() else "gb"
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "results_per_page": 50,
                "what": keyword,
                "where": location,
                "content-type": "application/json"
            }
            response = requests.get(url, params=params)
            print("🌐 Adzuna REQUEST:", response.url)

            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", []):
                    jobs.append({
                        "job_title": item.get("title", "N/A"),
                        "employer_name": item.get("company", {}).get("display_name", "N/A"),
                        "job_type": item.get("contract_time", "N/A"),
                        "posted_date": item.get("created", "N/A"),
                        "description": item.get("description", "No description provided."),
                        "apply_link": item.get("redirect_url", "#"),
                        "job_url": item.get("redirect_url", "#"),
                        "job_city": item.get("location", {}).get("area", ["N/A"])[-1],
                        "job_country": country.upper()
                    })
        except Exception as e:
            print("❌ Adzuna fetch error:", e)

    # ----------------------------
    # Manual Pagination
    # ----------------------------
    start_index = (page - 1) * results_per_page
    end_index = start_index + results_per_page
    paginated_jobs = jobs[start_index:end_index]

    print(f"✅ Total jobs fetched: {len(jobs)} | Showing {len(paginated_jobs)} for page {page}")
    return paginated_jobs