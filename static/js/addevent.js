document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        const price = document.getElementById("price").value;
        const numPeople = document.getElementById("num_people").value;

        if (price < 0 || numPeople < 1) {
            alert("Price must be 0 or more and Number of People must be at least 1.");
            event.preventDefault();
        }
    });
});


function searchClub(query) {
    const datalist = document.getElementById("club-list");
    const options = datalist.querySelectorAll("option");

    options.forEach(option => {
        if (option.value.toLowerCase().includes(query.toLowerCase())) {
            option.style.display = "";
        } else {
            option.style.display = "none";
        }
    });
}
