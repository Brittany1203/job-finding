import requests
from flask import Flask, render_template, request, url_for

from reed_api import search_reed
from adzuna_api import search_adzuna

app = Flask(__name__)

SOURCE_OPTIONS = ["Reed", "Adzuna"]


@app.route("/")
def index():
    searched = (
        request.args.get("search") == "1"
        and request.args.get("reset") != "1"
    )

    keyword = ""
    location = ""
    country = "gb"
    selected_sources = SOURCE_OPTIONS.copy()
    results = []
    messages = []

    if searched:
        keyword = request.args.get("keyword", "").strip()
        location = request.args.get("location", "").strip()
        country = request.args.get("country", "gb")

        selected_sources = [
            source
            for source in request.args.getlist("source")
            if source in SOURCE_OPTIONS
        ]

        if country not in {"gb", "us"}:
            messages.append("Please select a supported country.")

        elif not selected_sources:
            messages.append("Please select at least one job source.")

        else:
            if "Reed" in selected_sources:
                if country == "gb":
                    try:
                        results.extend(
                            search_reed(keyword, location)
                        )
                    except (requests.exceptions.RequestException, ValueError):
                        messages.append(
                            "Could not load Reed results. "
                            "Check your connection and API credentials."
                        )
                else:
                    messages.append(
                        "Reed was skipped: this app uses Reed "
                        "for UK searches only. Select Adzuna for US jobs."
                    )

            if "Adzuna" in selected_sources:
                try:
                    results.extend(
                        search_adzuna(keyword, location, country)
                    )
                except (requests.exceptions.RequestException, ValueError):
                    messages.append(
                        "Could not load Adzuna results. "
                        "Check your connection and API credentials."
                    )

    # 每頁顯示 10 筆
    per_page = 10
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page

    page = request.args.get("page", default=1, type=int) or 1
    page = max(1, min(page, max(1, total_pages)))

    start = (page - 1) * per_page
    page_jobs = results[start:start + per_page]

    page_links = [
        {
            "number": number,
            "url": url_for(
                "index",
                search="1",
                keyword=keyword,
                location=location,
                country=country,
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
        country=country,
        source_options=SOURCE_OPTIONS,
        selected_sources=selected_sources,
        error_message=" ".join(messages),
        searched=searched,
        total_results=total_results,
        total_pages=total_pages,
        page=page,
        page_links=page_links,
    )


if __name__ == "__main__":
    app.run(port=5001, debug=True)