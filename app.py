import csv
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

SOURCE_OPTIONS = ["Reed", "Indeed", "其他招聘來源"]


def load_jobs():
    csv_path = BASE_DIR / "data" / "jobs.csv"

    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        jobs = list(csv.DictReader(file))

    # 按主要連結判斷來源，避免將參考網站混入來源篩選
    for job in jobs:
        hostname = urlparse(job["Link"]).hostname or ""

        if hostname == "reed.co.uk" or hostname.endswith(".reed.co.uk"):
            job["Search Source"] = "Reed"
        elif hostname == "indeed.com" or hostname.endswith(".indeed.com"):
            job["Search Source"] = "Indeed"
        else:
            job["Search Source"] = "其他招聘來源"

    return jobs


@app.route("/")
def index():
    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()

    # 初次開頁面時，預設選取全部來源
    if "search" in request.args:
        selected_sources = request.args.getlist("source")
    else:
        selected_sources = SOURCE_OPTIONS.copy()

    results = []

    for job in load_jobs():
        searchable_text = " ".join([
            job["Job Title"],
            job["Company"],
            job["Job Description"],
            job["Skills"],
        ]).casefold()

        matches_keyword = keyword.casefold() in searchable_text
        matches_location = location.casefold() in job["Location"].casefold()
        matches_source = job["Search Source"] in selected_sources

        if matches_keyword and matches_location and matches_source:
            results.append(job)

    return render_template(
        "index.html",
        jobs=results,
        keyword=keyword,
        location=location,
        source_options=SOURCE_OPTIONS,
        selected_sources=selected_sources,
    )


if __name__ == "__main__":
    app.run(port=5001, debug=True)