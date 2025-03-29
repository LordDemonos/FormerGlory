document.addEventListener('DOMContentLoaded', function() {
    // Only run on strategy and spoilers pages
    if (!document.body.classList.contains('strategy-page') && 
        !document.body.classList.contains('spoilers-page')) {
        return;
    }

    // Check localStorage and redirect if needed
    const savedView = localStorage.getItem('viewPreference');
    const savedScrollPosition = localStorage.getItem('scrollPosition');
    
    if (savedView) {
        const currentPage = document.body.classList.contains('strategy-page') ? 'strategy' : 'spoilers';
        if (savedView !== currentPage) {
            window.location.href = savedView === 'strategy' ? '/strategy/' : '/spoilers/';
            return;
        }
    }

    // Restore scroll position if exists
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition));
        localStorage.removeItem('scrollPosition'); // Clear after using
    }

    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.className = 'view-toggle';
    toggleButton.innerHTML = document.body.classList.contains('strategy-page') ? '📖' : '👁️';
    toggleButton.title = 'Toggle View';
    document.body.appendChild(toggleButton);

    // Handle toggle click
    toggleButton.addEventListener('click', function() {
        const currentView = document.body.classList.contains('strategy-page') ? 'strategy' : 'spoilers';
        const newView = currentView === 'strategy' ? 'spoilers' : 'strategy';
        
        // Save current scroll position
        localStorage.setItem('scrollPosition', window.pageYOffset);
        
        // Update view preference
        localStorage.setItem('viewPreference', newView);
        
        // Redirect to the appropriate page
        window.location.href = newView === 'strategy' ? '/strategy/' : '/spoilers/';
    });
}); 