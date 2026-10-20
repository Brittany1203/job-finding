const countrySelect = document.querySelector("#country");
const reedCheckbox = document.querySelector(
    'input[name="source"][value="Reed"]'
);

function updateSources() {
    const isUS = countrySelect.value === "us";

    if (isUS) {
        reedCheckbox.checked = false;
    }

    reedCheckbox.disabled = isUS;

    const label = reedCheckbox.closest("label");
    label.classList.toggle("source-disabled", isUS);
}

// update sources when country is changed
countrySelect.addEventListener("change", updateSources);

// first load, pagination, or browser back button
window.addEventListener("pageshow", updateSources);
updateSources();