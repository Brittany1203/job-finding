const countrySelect = document.querySelector("#country");
const reedCheckbox = document.querySelector(
    'input[name="source"][value="Reed"]'
);
const locationInput = document.querySelector("#location");
const searchForm = countrySelect.closest("form");

// Control reed according to country
function updateSources() {
    const isUS = countrySelect.value === "us";

    if (isUS) {
        reedCheckbox.checked = false;
    }

    reedCheckbox.disabled = isUS;
    reedCheckbox.closest("label").classList.toggle(
        "source-disabled",
        isUS
    );

    locationInput.placeholder = isUS
        ? "e.g. New York, Boston"
        : "e.g. London, Manchester";
}

countrySelect.addEventListener("change", updateSources);
window.addEventListener("pageshow", updateSources);
updateSources();


// search history
const HISTORY_KEY = "jobSearchHistory.v1";
const MAX_HISTORY = 10;

const historyList = document.querySelector("#history-list");
const emptyMessage = document.querySelector("#history-empty");
const clearButton = document.querySelector("#clear-history");
const historyMessage = document.querySelector("#history-message");

function readHistory() {
    try {
        const history = JSON.parse(
            localStorage.getItem(HISTORY_KEY) || "[]"
        );

        if (!Array.isArray(history)) {
            return [];
        }

        return history.filter(item =>
            item &&
            typeof item.keyword === "string" &&
            typeof item.location === "string" &&
            ["gb", "us"].includes(item.country) &&
            Array.isArray(item.sources) &&
            item.sources.length > 0 &&
            item.sources.every(source =>
                ["Reed", "Adzuna"].includes(source)
            )
        ).slice(0, MAX_HISTORY);
    } catch {
        return [];
    }
}

function createSearchURL(item) {
    const params = new URLSearchParams();

    params.set("search", "1");
    params.set("keyword", item.keyword);
    params.set("location", item.location);
    params.set("country", item.country);

    item.sources.forEach(source => {
        params.append("source", source);
    });

    return `${searchForm.action.split("?")[0]}?${params}`;
}

function renderHistory() {
    const history = readHistory();

    historyList.replaceChildren();
    emptyMessage.hidden = history.length > 0;
    clearButton.hidden = history.length === 0;

    history.forEach(item => {
        const li = document.createElement("li");
        const link = document.createElement("a");

        const countryName = item.country === "us" ? "US" : "UK";

        // use textContent to show the input content
        link.textContent = [
            item.keyword || "All jobs",
            item.location || "All locations",
            countryName,
            item.sources.join(" + ")
        ].join(" · ");

        link.href = createSearchURL(item);

        li.appendChild(link);
        historyList.appendChild(li);
    });
}

function saveSearch(item) {
    try {
        // use the same format for comparison, ignoring case and source order
        function searchKey(search) {
            return JSON.stringify([
                search.keyword.toLowerCase(),
                search.location.toLowerCase(),
                search.country,
                [...search.sources].sort()
            ]);
        }

        const history = readHistory().filter(
            oldItem => searchKey(oldItem) !== searchKey(item)
        );

        history.unshift(item);

        localStorage.setItem(
            HISTORY_KEY,
            JSON.stringify(history.slice(0, MAX_HISTORY))
        );
    } catch {
        // save failed but won't stop normal search
    }
}

searchForm.addEventListener("submit", () => {
    updateSources();

    const formData = new FormData(searchForm);

    const item = {
        keyword: String(formData.get("keyword") || "").trim(),
        location: String(formData.get("location") || "").trim(),
        country: countrySelect.value,
        sources: formData.getAll("source").map(String)
    };

    if (item.sources.length > 0) {
        saveSearch(item);
    }
});

clearButton.addEventListener("click", () => {
    try {
        localStorage.removeItem(HISTORY_KEY);
        renderHistory();
        historyMessage.textContent = "Search history cleared.";
    } catch {
        historyMessage.textContent =
            "Could not clear history. Check your browser settings.";
    }
});

// click search history items to move them to the top
historyList.addEventListener("click", event => {
    const link = event.target.closest("a");

    if (!link) {
        return;
    }

    const params = new URL(link.href).searchParams;

    saveSearch({
        keyword: params.get("keyword") || "",
        location: params.get("location") || "",
        country: params.get("country"),
        sources: params.getAll("source")
    });
});

window.addEventListener("pageshow", renderHistory);
renderHistory();