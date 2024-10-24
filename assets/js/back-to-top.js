document.addEventListener('DOMContentLoaded', function() {
  const backToTopBtn = document.getElementById('back-to-top-btn');

  // Always display the button
  backToTopBtn.style.display = 'flex';

  // Set initial state based on the current scroll position
  if (window.pageYOffset === 0) {
    backToTopBtn.textContent = '🔽'; // Down arrow emoji
  } else {
    backToTopBtn.textContent = '🔼'; // Up arrow emoji
  }

  window.onscroll = function() {
    if (window.pageYOffset === 0) {
      backToTopBtn.textContent = '🔽'; // Down arrow emoji
    } else {
      backToTopBtn.textContent = '🔼'; // Up arrow emoji
    }
  };

  backToTopBtn.addEventListener('click', function(e) {
    e.preventDefault();
    if (window.pageYOffset === 0) {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
});
