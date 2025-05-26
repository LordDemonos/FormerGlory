document.addEventListener('DOMContentLoaded', function() {
    // Find all copy buttons
    const copyButtons = document.querySelectorAll('.copy-button');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            // Find the associated text content
            const container = this.closest('.copy-text-container');
            const textContent = container.querySelector('.copy-text-content');
            
            try {
                // Copy the text to clipboard
                await navigator.clipboard.writeText(textContent.textContent);
                
                // Visual feedback
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.classList.add('copied');
                this.blur();
                
                // Reset button after 2 seconds
                setTimeout(() => {
                    this.textContent = originalText;
                    this.classList.remove('copied');
                }, 2000);
                
            } catch (err) {
                console.error('Failed to copy text: ', err);
                
                // Fallback for older browsers
                try {
                    // Create a temporary textarea
                    const textArea = document.createElement('textarea');
                    textArea.value = textContent.textContent;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-999999px';
                    textArea.style.top = '-999999px';
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    
                    const successful = document.execCommand('copy');
                    document.body.removeChild(textArea);
                    
                    if (successful) {
                        // Visual feedback for successful fallback
                        const originalText = this.textContent;
                        this.textContent = 'Copied!';
                        this.classList.add('copied');
                        this.blur();
                        
                        setTimeout(() => {
                            this.textContent = originalText;
                            this.classList.remove('copied');
                        }, 2000);
                    } else {
                        throw new Error('Fallback copy failed');
                    }
                } catch (fallbackErr) {
                    console.error('Fallback copy failed: ', fallbackErr);
                    this.textContent = 'Failed to copy';
                    this.classList.add('error');
                    
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.classList.remove('error');
                    }, 2000);
                }
            }
        });
    });
});

function copyText(elementId) {
    const textElement = document.getElementById(elementId);
    const text = textElement.textContent.trim();
    
    try {
        navigator.clipboard.writeText(text).then(() => {
            const button = textElement.nextElementSibling;
            const originalText = button.textContent;
            button.textContent = 'Copied!';
            button.classList.add('copied');
            button.blur();
            
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        });
    } catch (err) {
        console.error('Failed to copy text: ', err);
        
        // Fallback for older browsers
        try {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            const successful = document.execCommand('copy');
            document.body.removeChild(textArea);
            
            if (successful) {
                const button = textElement.nextElementSibling;
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.classList.add('copied');
                button.blur();
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            } else {
                throw new Error('Fallback copy failed');
            }
        } catch (fallbackErr) {
            console.error('Fallback copy failed: ', fallbackErr);
            const button = textElement.nextElementSibling;
            const originalText = button.textContent;
            button.textContent = 'Failed to copy';
            button.classList.add('error');
            
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('error');
            }, 2000);
        }
    }
} 