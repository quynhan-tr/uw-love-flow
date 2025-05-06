document.getElementById('friendship-quiz-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const genres = document.querySelectorAll('input[type="checkbox"][name="movie-genres"]:checked');
  const mbti = document.querySelector('input[name="mbti"]').value.toUpperCase();
  const validMBTIs = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'];
  const relationshipComponents = document.querySelectorAll('input[type="checkbox"][name="relationship-components"]:checked');

  if (relationshipComponents.length !== 3) {
    alert('Please select exactly three components for a good relationship.');
    event.preventDefault();
    return;
  }
  if (!validMBTIs.includes(mbti)) {
    alert('Please enter a valid MBTI type (e.g. INTJ, ENFP, etc).');
    event.preventDefault();
    return;
  }

  if (genres.length !== 3) {
    alert('Please select exactly three movie genres.');
    event.preventDefault();
    return;
  }

  window.location.href = '/waiting.w';
});