function showModal() {
    // Show the modal asking for the current admin's password
    document.getElementById('authModal').style.display = 'block';
}

function closeModal() {
    // Close the modal without doing anything
    document.getElementById('authModal').style.display = 'none';
}

function authorize() {
    var currentPassword = document.getElementById('currentAdminPasswordInput').value;

    // Send an AJAX request to verify the current admin password
    fetch('/verify_admin_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: currentPassword })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If authorization is successful, submit the form
                document.getElementById('currentAdminPassword').value = currentPassword;
                document.querySelector('form').submit();
            } else {
                alert('Authorization failed! Incorrect current password.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

