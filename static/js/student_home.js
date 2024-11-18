document.addEventListener("DOMContentLoaded", () => {
    const registeredEventsList = document.getElementById("registered-events-list");
    const availableEventsList = document.getElementById("available-events-list");
    const registerModal = document.getElementById("register-modal");
    const confirmRegisterButton = document.getElementById("confirm-register");
    const cancelRegisterButton = document.getElementById("cancel-register");

    let selectedEventId = null;


    // Fetch and display available events
    fetch("/get_available_events")
        .then(response => response.json())
        .then(events => {
            events.forEach(event => {
                const eventElement = document.createElement("div");
                eventElement.innerHTML = `<p>Event: ${event.name}</p><p>Date: ${event.date}</p><p>Location: ${event.location}</p>
                <button onclick="openRegisterModal(${event.id})">Register</button>`;
                availableEventsList.appendChild(eventElement);
            });
        })
        .catch(error => console.error("Error loading available events:", error));

    // Show register modal
    window.openRegisterModal = (eventId) => {
        selectedEventId = eventId;
        registerModal.style.display = "block";
    };


    // Cancel registration modal
    cancelRegisterButton.addEventListener("click", () => {
        registerModal.style.display = "none";
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const availableEventsList = document.getElementById("available-events-list");

    // Fetch available events from the server
    fetch('/events')  // Replace with your actual route for fetching events
        .then(response => response.json())
        .then(events => {
            if (events.length > 0) {
                events.forEach(event => {
                    const eventItem = document.createElement("div");
                    eventItem.className = "event-item";
                    eventItem.innerHTML = `
                        <h3>${event.title}</h3>
                        <p>${event.description}</p>
                        <button onclick="registerForEvent('${event.id}')">Register</button>
                    `;
                    availableEventsList.appendChild(eventItem);
                });
            } else {
                availableEventsList.innerHTML = "<p>No available events at the moment.</p>";
            }
        })
        .catch(error => console.error("Error fetching events:", error));
});

// Function to show registration modal for selected event
function registerForEvent(eventId) {
    const registerModal = document.getElementById("register-modal");
    registerModal.style.display = "block";

    document.getElementById("confirm-register").onclick = () => {
        // Logic to handle registration
        console.log("User registered for event with ID:", eventId);
        registerModal.style.display = "none";
    };

    document.getElementById("cancel-register").onclick = () => {
        registerModal.style.display = "none";
    };
}

function openModal(eventId) {
    document.getElementById("event_id").value = eventId;
    document.getElementById("registrationModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("registrationModal").style.display = "none";
}

// Close modal if clicked outside of the modal content
window.onclick = function (event) {
    const modal = document.getElementById("registrationModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}


document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (message) {
        alert(message.textContent);  // Displaying the message in an alert box
        message.style.display = 'none';  // Optionally hide the flash message after showing it
    });
});
