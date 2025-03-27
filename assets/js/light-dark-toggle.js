document.addEventListener('DOMContentLoaded', function() {
  const modeToggle = document.getElementById('mode-toggle');
  const root = document.documentElement;
  const body = document.body;

  // Function to switch to light mode
  function enableLightMode() {
    root.classList.remove('dark-mode');
    body.classList.remove('dark');
    document.body.setAttribute('data-theme', 'light');
    document.documentElement.style.backgroundColor = '';
    document.body.style.backgroundColor = '';
    modeToggle.classList.remove('dark');
    modeToggle.querySelector('.toggle-icon').textContent = '🌙';
    localStorage.setItem('theme', 'light');
  }

  // Function to switch to dark mode
  function enableDarkMode() {
    root.classList.add('dark-mode');
    body.classList.add('dark');
    document.body.setAttribute('data-theme', 'dark');
    document.documentElement.style.backgroundColor = '#000000';
    document.body.style.backgroundColor = '#000000';
    modeToggle.classList.add('dark');
    modeToggle.querySelector('.toggle-icon').textContent = '☀️';
    localStorage.setItem('theme', 'dark');
  }

  // Check for saved theme preference on page load
  const savedTheme = localStorage.getItem('theme');
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
