function checkPassword() {
  const password = document.getElementById('password').value;
  fetch('/get-password')
    .then(response => response.json())
    .then(data => {
      if (password === data.password) {
        window.location.href = '../host-options';
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