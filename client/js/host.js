function checkPassword() {
  const password = document.getElementById('password').value;
  fetch('/api/get-password')
    .then(response => response.json())
    .then(data => {
      if (password === data.password) {
        window.location.href = '/host-options.w';
      } else {
        alert("Incorrect password. Please try again.");
      }
    })
    .catch(err => {
      console.error('Error fetching password:', err);
      alert('Something went wrong. Please try again later.');
    });
}

function executeAction(url) {
  fetch(url)
    .then(response => response.text())
    .then(message => {
      alert(message);
    })
    .catch(error => {
      alert("An error occurred: " + error);
    });
} 