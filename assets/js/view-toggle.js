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

    // If on spoilers page, modify internal links to point to strategy
    if (document.body.classList.contains('spoilers-page')) {
        document.querySelectorAll('.card-container a').forEach(link => {
            // Check if this is an internal link (no target="_blank" and no external domain)
            if (!link.hasAttribute('target') && !link.href.includes('pqdi.cc')) {
                // Get just the last part of the href (the filename)
                const href = link.getAttribute('href');
                // Make sure we're not duplicating /strategy/
                if (!href.startsWith('/strategy/')) {
                    link.href = '/strategy/' + href;
                }
                console.log('Modified link:', link.href); // Debug log
            }
        });
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