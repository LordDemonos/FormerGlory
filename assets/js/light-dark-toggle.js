document.addEventListener('DOMContentLoaded', function() {
  const modeToggle = document.getElementById('mode-toggle');
  const root = document.documentElement;

  // Function to switch to light mode
  function enableLightMode() {
    root.classList.remove('dark-mode');
    modeToggle.classList.remove('dark'); // Remove dark class
    modeToggle.querySelector('.toggle-icon').textContent = '🌙'; // Moon emoji
    sessionStorage.setItem('theme', 'light'); // Save preference
  }

  // Function to switch to dark mode
  function enableDarkMode() {
    root.classList.add('dark-mode');
    modeToggle.classList.add('dark'); // Add dark class
    modeToggle.querySelector('.toggle-icon').textContent = '☀️'; // Sun emoji
    sessionStorage.setItem('theme', 'dark'); // Save preference
  }

  // Check for saved theme preference on page load
  const savedTheme = sessionStorage.getItem('theme');
  if (savedTheme === 'dark') {
    enableDarkMode();
  } else {
    enableLightMode();
  }

  // Toggle between light and dark modes
  modeToggle.addEventListener('click', function() {
    if (root.classList.contains('dark-mode')) {
      enableLightMode();
    } else {
      enableDarkMode();
    }
  });
});
