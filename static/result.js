function checkPassword() {
  const password = document.getElementById('password').value;
  if (password === "uw data science - goated events") {
    document.getElementById('admin-buttons').classList.remove('hidden');
  } else {
    alert("Incorrect password. Please try again.");
  }
}

// Add floating names animation with varied starting positions and directions
const names = JSON.parse('{{ names|tojson|safe }}').filter(name => name !== 'dummy');
const container = document.querySelector('div[style*="height: 80vh"]');

const startPositions = [
  {left: '10%', top: '10%'},
  {left: '80%', top: '20%'},
  {left: '30%', top: '70%'},
  {left: '70%', top: '60%'},
  {left: '20%', top: '40%'},
  {left: '60%', top: '15%'},
  {left: '40%', top: '80%'},
  {left: '90%', top: '50%'}
];

names.forEach((name, index) => {
  const nameElement = document.createElement('div');
  nameElement.className = 'floating-name';
  nameElement.textContent = name;
  nameElement.style.left = startPositions[index].left;
  nameElement.style.top = startPositions[index].top;
  
  // Generate random movement pattern
  const randomAngle = Math.random() * 360;
  const randomDistance = 50 + Math.random() * 150;
  const dx = Math.cos(randomAngle * Math.PI / 180) * randomDistance;
  const dy = Math.sin(randomAngle * Math.PI / 180) * randomDistance;
  
  // Apply custom animation with longer duration (25-35s instead of 15-25s)
  nameElement.style.animation = `float-${index} ${25 + Math.random() * 10}s infinite ease-in-out`;
  
  // Create keyframe animation
  const keyframes = `
    @keyframes float-${index} {
      0%, 100% { transform: translate(0, 0); }
      25% { transform: translate(${dx}px, ${dy}px); }
      50% { transform: translate(${-dy}px, ${dx}px); }
      75% { transform: translate(${-dx}px, ${-dy}px); }
    }
  `;
  
  // Add keyframes to document
  const styleSheet = document.createElement('style');
  styleSheet.textContent = keyframes;
  document.head.appendChild(styleSheet);
  
  container.appendChild(nameElement);
});