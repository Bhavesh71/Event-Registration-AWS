// adminhome.js

function openEditModal(eventId) {
    // Fetch event details via AJAX and populate the modal fields
    fetch(`/get_event/${eventId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("eventId").value = data.id;
                document.getElementById("eventName").value = data.name;
                document.getElementById("eventDescription").value = data.description;
                document.getElementById("eventDate").value = data.date;
                document.getElementById("eventTime").value = data.time;
                document.getElementById("venue").value = data.venue;
                document.getElementById("price").value = data.price;
                document.getElementById("numPeople").value = data.num_people;
                document.getElementById("editModal").style.display = "block";
            }
        })
        .catch(error => console.error('Error:', error));
}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}

// Submit edited event data
function submitEditEvent(event) {
    event.preventDefault();
    const eventId = document.getElementById('eventId').value;
    const eventData = {
        id: eventId,
        name: document.getElementById('eventName').value,
        description: document.getElementById('eventDescription').value,
        date: document.getElementById('eventDate').value,
        time: document.getElementById('eventTime').value,
        venue: document.getElementById('venue').value,
        price: document.getElementById('price').value,
        num_people: document.getElementById('numPeople').value,
    };

    fetch('/edit_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Event updated successfully!');
                location.reload();
            } else {
                alert(data.error);
            }
        })
        .catch(err => console.error(err));

    closeEditModal();
}

function deleteEvent(eventId) {
    if (confirm("Are you sure you want to delete this event?")) {
        fetch(`/delete_event/${eventId}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Event deleted successfully!");
                    location.reload();
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

// Function to filter clubs in the dropdown based on search input
function filterClubs() {
    let input = document.getElementById("clubSearchInput");
    let filter = input.value.toUpperCase();
    let div = document.getElementsByClassName("clubs-dropdown-content")[0];
    let a = div.getElementsByTagName("a");

    // Loop through all links and hide those that don't match the search query
    for (let i = 0; i < a.length; i++) {
        let txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

// Function to filter events by selected club
function filterEvents(clubName) {
    let eventSections = document.querySelectorAll(".club-section");

    eventSections.forEach(section => {
        let clubTitle = section.querySelector("h3").innerText;

        // Show all clubs if 'All' is selected, or only the matching club's events
        if (clubName === "all" || clubTitle === clubName) {
            section.style.display = "block";
        } else {
            section.style.display = "none";
        }
    });
}
