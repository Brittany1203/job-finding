import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

if not app_id or not app_key:
    raise SystemExit(
        "Missing ADZUNA_APP_ID or ADZUNA_APP_KEY. Check your .env file."
    )

# us = united states, test with New York
url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

params = {
    "app_id": app_id,
    "app_key": app_key,
    "what": "Data Analyst",
    "where": "New York",
    "results_per_page": 5,
}

try:
    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        timeout=20,
    )

    print("HTTP status:", response.status_code)

    if response.ok:
        data = response.json()
        jobs = data.get("results", [])

        print(f"Retrieved {len(jobs)} jobs\n")

        for job in jobs:
            print("Title:", job.get("title"))
            print("Company:", (job.get("company") or {}).get("display_name"))
            print("Location:", (job.get("location") or {}).get("display_name"))
            print("-" * 40)
    else:
        print("Adzuna request failed. Check credentials and account access.")

except requests.exceptions.RequestException:
    print("Connection failed or timed out. Please try again.")

except ValueError:
    print("Adzuna did not return valid JSON.")