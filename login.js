document.addEventListener("DOMContentLoaded", function() {
    var loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent form submission

            var username = document.getElementById("username").value;
            var password = document.getElementById("password").value;

            // Read the JSON file
            fetch("login-details.json")
                .then(response => response.json())
                .then(data => {
                    var loginDetails = data;
                    var found = false;

                    // Check if the entered username and password match the JSON data
                    for (var i = 0; i < loginDetails.length; i++) {
                        var user = loginDetails[i];

                        if (user.hasOwnProperty(username) && user[username] === password) {
                            found = true;
                            break;
                        }
                    }

                    // Display login status message
                    var loginStatus = document.getElementById("login-status");
                    if (found) {
                        loginStatus.innerHTML = "Login successful.";
                        loginStatus.style.color = "green";
                    } else {
                        loginStatus.innerHTML = "Invalid username or password.";
                        loginStatus.style.color = "red";
                    }
                })
                .catch(error => console.error(error));
        });
    }
});

