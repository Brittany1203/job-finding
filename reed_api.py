import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def search_reed(keyword, location):
    api_key = os.getenv("REED_API_KEY")

    if not api_key:
        raise ValueError("Missing REED_API_KEY. Check your .env file.")

    response = requests.get(
        "https://www.reed.co.uk/api/1.0/search",
        params={
            "keywords": keyword,
            "locationName": location,
            "resultsToTake": 20,
        },
        auth=(api_key, ""),
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    # let column reed be the source of truth for the Reed jobs, so we can filter them out of the CSV results
    jobs = []

    for item in data.get("results", []):
        jobs.append({
            "Job Title": item.get("jobTitle", ""),
            "Company": item.get("employerName", ""),
            "Location": item.get("locationName", ""),
            "Job Description": item.get("jobDescription", ""),
            "Job Level": "Not classified",
            "Remote/On-site": "Not specified",
            "Skills": "Not extracted",
            "Search Source": "Reed",
            "Listing Status": "Retrieved from Reed API",
            "Link": item.get("jobUrl", ""),
        })

    return jobs