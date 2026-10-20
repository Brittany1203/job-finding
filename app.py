import requests
from reed_api import search_reed

import csv
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

SOURCE_OPTIONS = ["Reed", "Indeed", "Other job sources"]


def load_jobs():
    csv_path = BASE_DIR / "data" / "jobs.csv"

    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        jobs = list(csv.DictReader(file))

    # use the main URL to determine the source, avoiding mixing reference sites into the source filter
    for job in jobs:
        hostname = urlparse(job["Link"]).hostname or ""

        if hostname == "reed.co.uk" or hostname.endswith(".reed.co.uk"):
            job["Search Source"] = "Reed"
        elif hostname == "indeed.com" or hostname.endswith(".indeed.com"):
            job["Search Source"] = "Indeed"
        else:
            job["Search Source"] = "Other job sources"

    return jobs


@app.route("/")
def index():
    searched = (
        request.args.get("search") == "1"
        and request.args.get("reset") != "1"
    )

    keyword = ""
    location = ""
    selected_sources = SOURCE_OPTIONS.copy()
    results = []
    error_message = ""

    if searched:
        keyword = request.args.get("keyword", "").strip()
        location = request.args.get("location", "").strip()
        selected_sources = request.args.getlist("source")

        # Indeed and other sources temporarily search CSV
        for job in load_jobs():
            if job["Search Source"] == "Reed":
                continue

            searchable_text = " ".join([
                job["Job Title"],
                job["Company"],
                job["Job Description"],
                job["Skills"],
            ]).casefold()

            matches_keyword = keyword.casefold() in searchable_text
            matches_location = (
                location.casefold() in job["Location"].casefold()
            )
            matches_source = job["Search Source"] in selected_sources

            if matches_keyword and matches_location and matches_source:
                results.append(job)

        # Reed using API
        if "Reed" in selected_sources:
            try:
                results.extend(search_reed(keyword, location))

            except requests.exceptions.Timeout:
                error_message = (
                    "Reed took too long to respond. Please try again."
                )

            except requests.exceptions.RequestException:
                error_message = (
                    "Could not load Reed jobs. Please try again."
                )

            except ValueError:
                error_message = (
                    "Check your Reed API key or response format."
                )

    # 10 results per page, calculate total pages and current page
    per_page = 10
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page

    page = request.args.get("page", default=1, type=int) or 1
    page = max(1, min(page, max(1, total_pages)))

    start = (page - 1) * per_page
    page_jobs = results[start:start + per_page]

    # Page links retain keyword, location, and multiple sources
    page_links = [
        {
            "number": number,
            "url": url_for(
                "index",
                search="1",
                keyword=keyword,
                location=location,
                source=selected_sources,
                page=number,
            ),
        }
        for number in range(1, total_pages + 1)
    ]

    return render_template(
        "index.html",
        jobs=page_jobs,
        keyword=keyword,
        location=location,
        source_options=SOURCE_OPTIONS,
        selected_sources=selected_sources,
        error_message=error_message,
        searched=searched,
        total_results=total_results,
        total_pages=total_pages,
        page=page,
        page_links=page_links,
    )


if __name__ == "__main__":
    app.run(port=5001, debug=True)