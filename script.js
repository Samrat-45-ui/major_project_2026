document.addEventListener("DOMContentLoaded", () => {
    const classContainer = document.getElementById("class-container") || document.getElementById("class-list");
    const bookingForm = document.getElementById("booking-form");
    const classSelect = document.getElementById("class-select");

    function showClasses(classes) {
        classContainer.innerHTML = "";

        if (!classes.length) {
            classContainer.innerHTML = "<li>No active sessions found.</li>";
            return;
        }

        classes.forEach((session) => {
            const item = document.createElement("li");
            item.textContent = `${session.name} with ${session.instructor} - Time: ${session.time} (${session.spots} slots remaining)`;
            classContainer.appendChild(item);
        });
    }

    function fillClassOptions(classes) {
        classSelect.innerHTML = '<option value="">-- Choose a Training Session --</option>';

        classes.forEach((session) => {
            const option = document.createElement("option");
            option.value = session.id;
            option.textContent = `${session.name} (${session.spots} left) at ${session.time}`;

            if (session.spots <= 0) {
                option.disabled = true;
            }

            classSelect.appendChild(option);
        });
    }

    if (classContainer) {
        fetch("/api/classes")
            .then((response) => response.json())
            .then(showClasses)
            .catch(() => {
                classContainer.innerHTML = "<li>Failed to load schedule from server.</li>";
            });
    }

    if (bookingForm && classSelect) {
        fetch("/api/classes")
            .then((response) => response.json())
            .then(fillClassOptions);

        bookingForm.addEventListener("submit", (event) => {
            event.preventDefault();

            const usernameInput = document.getElementById("username");
            const feedbackBanner = document.getElementById("feedback-banner");

            const data = {
                username: usernameInput.value.trim(),
                class_id: Number(classSelect.value)
            };

            fetch("/api/book", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
                .then((response) => response.json())
                .then((result) => {
                    if (result.success) {
                        feedbackBanner.style.color = "green";
                        feedbackBanner.textContent = result.success;
                        bookingForm.reset();
                        setTimeout(() => window.location.reload(), 1500);
                    } else {
                        feedbackBanner.style.color = "red";
                        feedbackBanner.textContent = result.error;
                    }
                })
                .catch(() => {
                    feedbackBanner.textContent = "Server is currently unavailable.";
                });
        });
    }
});