document.addEventListener('DOMContentLoaded', function() {
  // JavaScript function to call Python script when the invite button is clicked
  document.getElementById('inviteButton').addEventListener('click', function() {
    // Send a request to the Python script
    fetch('http://127.0.0.1:8001/invite', { method: 'POST' })
      .then(function(response) {
        if (response.ok) {
          console.log('Python script called successfully.');
          // Handle the response from the Python script if needed
        } else {
          console.error('Failed to call Python script.');
        }
      })
      .catch(function(error) {
        console.error('An error occurred while calling the Python script:', error);
      });
  });
});

  