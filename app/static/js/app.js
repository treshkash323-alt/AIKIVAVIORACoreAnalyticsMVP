function updateClock(id, timezone) {

    const now = new Date();

    const time = now.toLocaleTimeString(
        "ru-RU",
        {
            timeZone: timezone,
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        }
    );

    document.getElementById(id).textContent = time;
}

function updateAllClocks() {

    updateClock("clock-usa", "America/New_York");
    updateClock("clock-uk", "Europe/London");
    updateClock("clock-fin", "Europe/Helsinki");
    updateClock("clock-ger", "Europe/Berlin");
    updateClock("clock-ru", "Europe/Moscow");
}

setInterval(updateAllClocks, 1000);

updateAllClocks();