import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# read .env of the same directory as this script
load_dotenv(Path(__file__).resolve().parent / ".env")

api_key = os.getenv("REED_API_KEY")

if not api_key:
    raise SystemExit("Missing REED_API_KEY. Check your .env file.")

url = "https://www.reed.co.uk/api/1.0/search"

params = {
    "keywords": "Data Analyst",
    "locationName": "London",
    "resultsToTake": 5,
}

try:
    response = requests.get(
        url,
        params=params,
        auth=(api_key, ""),
        timeout=20,
    )

    print("HTTP status:", response.status_code)
    response.raise_for_status()

    data = response.json()
    jobs = data.get("results", [])

    print(f"Found {len(jobs)} jobs\n")

    for job in jobs:
        print("Title:", job.get("jobTitle"))
        print("Company:", job.get("employerName"))
        print("Location:", job.get("locationName"))
        print("Link:", job.get("jobUrl"))
        print("-" * 40)

except requests.exceptions.RequestException as error:
    print("Request failed:", error)

except ValueError:
    print("The response could not be read as JSON.")