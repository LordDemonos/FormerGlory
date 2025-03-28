document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers to all resize-img images
    document.querySelectorAll('.resize-img').forEach(img => {
        img.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('full-size');
            
            // If image is now full size, scroll it into view
            if (this.classList.contains('full-size')) {
                this.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}); 