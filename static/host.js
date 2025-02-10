function checkPassword() {
  const password = document.getElementById('password').value;
  fetch('/get-password')
    .then(response => response.json())
    .then(data => {
      if (password === data.password) {
        document.getElementById('admin-buttons').classList.remove('hidden');
        document.getElementById('password-section').classList.add('hidden');
      } else {
        alert("Incorrect password. Please try again.");
      }
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