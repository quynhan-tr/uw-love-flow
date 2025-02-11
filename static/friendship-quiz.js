document.getElementById('friendship-quiz-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission

  const genres = document.querySelectorAll('input[type="checkbox"][name="movie-genres"]:checked');
  const mbti = document.querySelector('input[name="mbti"]').value.toUpperCase();
  const validMBTIs = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'];
  const relationshipComponents = document.querySelectorAll('input[type="checkbox"][name="relationship-components"]:checked');

  if (relationshipComponents.length !== 3) {
    alert('Please select exactly three components for a good relationship.');
    return;
  }
  if (!validMBTIs.includes(mbti)) {
    alert('Please enter a valid MBTI type (e.g. INTJ, ENFP, etc).');
    return;
  }

  if (genres.length !== 3) {
    alert('Please select exactly three movie genres.');
    return;
  }

  const formData = new FormData(this);

  fetch('/friendship-quiz', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert(data.error); // Show alert if there's an error
    } else {
      window.location.href = 'waiting.html'; // Redirect if successful
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});