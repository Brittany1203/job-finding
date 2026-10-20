import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def search_adzuna(keyword, location, country):
    if country not in {"gb", "us"}:
        raise ValueError("Unsupported country.")

    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError("Missing Adzuna credentials.")

    response = requests.get(
        f"https://api.adzuna.com/v1/api/jobs/{country}/search/1",
        params={
            "app_id": app_id,
            "app_key": app_key,
            "what": keyword,
            "where": location,
            "results_per_page": 20,
        },
        headers={"Accept": "application/json"},
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()
    jobs = []

    for item in data.get("results", []):
        jobs.append({
            "Job Title": item.get("title", ""),
            "Company": (
                item.get("company") or {}
            ).get("display_name", "Not specified"),
            "Location": (
                item.get("location") or {}
            ).get("display_name", ""),
            "Job Description": item.get("description", ""),
            "Job Level": "Not classified",
            "Remote/On-site": "Not specified",
            "Skills": "Not extracted",
            "Search Source": "Adzuna",
            "Listing Status": "Retrieved from Adzuna API",
            "Link": item.get("redirect_url", ""),
        })

    return jobs