document.addEventListener("DOMContentLoaded", () => {
    const classContainer = document.getElementById("class-container");
    const bookingForm = document.getElementById("booking-form");
    const classSelect = document.getElementById("class-select");

    if (classContainer) {  // Module 1: Load classes into Home Page
        fetch('/api/classes')
            .then(res => res.json())
            .then(data => {
                classContainer.innerHTML = "";
                if (data.length === 0) {
                    classContainer.innerHTML = "<li>No active sessions found.</li>";
                    return;
                }
                data.forEach(c => {
                    const li = document.createElement("li");
                    li.textContent = `${c.name} with ${c.instructor} - Time: ${c.time} (${c.spots} slots remaining)`;
                    classContainer.appendChild(li);
                });
            })
            .catch(err => {
                classContainer.innerHTML = "<li>Failed to load schedule from server.</li>";
            });
    }

