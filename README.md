# RoleScout

A Flask web application for searching job listings from Reed and Adzuna in one place.

## Overview

RoleScout brings multiple job sources into a single search interface. Users can search by keyword and location, select job sources, and revisit recent searches.

The project started as a small job-scraping exercise and developed into an API-based job search application.

## Features

- Search jobs by keyword and location.
- Select Reed, Adzuna, or both for UK searches.
- Search US jobs through Adzuna.
- Automatically disable Reed when the United States is selected.
- Display up to 10 jobs per page.
- Save the 10 most recent searches in the browser.
- Click a recent search to run it again.
- Clear search history or reset the search form.
- Open original job listings.
- Responsive layout for desktop and mobile screens.

## Tech Stack

- Python
- Flask and Jinja2
- HTML, CSS and JavaScript
- Requests
- python-dotenv
- Browser localStorage
- Reed and Adzuna APIs

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Brittany1203/role-scout.git
cd role-scout
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.env` file in the project root:

```dotenv
REED_API_KEY=your_reed_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

Use your own credentials. Keep `.env` excluded from Git.

### 5. Start the application

```bash
python app.py
```

Open http://127.0.0.1:5001 in your browser.

The HTML templates must be served through Flask.

## Search History

Search history stores search criteria, including keywords, location, country and selected sources.

Clicking a history entry runs a new search. It does not restore a saved copy of previous results.

History is stored in the current browser using localStorage. It is not synced across devices and can be removed by clearing browser data.

## Current Limitations

- The application currently supports UK and US searches.
- Reed is enabled for UK searches only.
- Each search retrieves up to 20 jobs per selected source.
- Pagination displays the retrieved subset, not every available match.
- Changing result pages currently requests the APIs again.
- Duplicate listings across sources are not yet removed.
- Job descriptions may be shortened by the source API.
- Job level and work arrangement are not currently classified automatically.
- API availability and credentials affect whether results can be retrieved.

## Possible Improvements

- Remove duplicate listings across sources.
- Cache searches to reduce repeated API requests.
- Add salary and job-type filters.
- Add saved jobs.
- Improve source-specific pagination.

## Data Sources

- [Reed Developer API](https://www.reed.co.uk/developers/jobseeker)
- [Adzuna Developer API](https://developer.adzuna.com/)

Job listing content belongs to its respective providers and employers.