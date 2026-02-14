/**
 * Loading Spinner Utility
 * Aggiunge un indicatore di caricamento moderno
 */

const LoadingSpinner = {
    // Create a spinner element
    create: function(options = {}) {
        const {
            size = 'medium',  // small, medium, large
            color = 'primary', // primary, white
            text = ''
        } = options;

        const sizeMap = {
            small: '20px',
            medium: '40px',
            large: '60px'
        };

        const spinnerSize = sizeMap[size] || sizeMap.medium;
        
        const container = document.createElement('div');
        container.className = 'loading-spinner-container';
        container.innerHTML = `
            <style>
                .loading-spinner-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                    gap: 15px;
                }
                .loading-spinner {
                    width: ${spinnerSize};
                    height: ${spinnerSize};
                    border: 3px solid rgba(99, 102, 241, 0.1);
                    border-top-color: #6366f1;
                    border-radius: 50%;
                    animation: spin 0.8s linear infinite;
                }
                .loading-spinner.white {
                    border-color: rgba(255, 255, 255, 0.1);
                    border-top-color: white;
                }
                .loading-text {
                    color: #64748b;
                    font-size: 14px;
                }
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
                .loading-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 9999;
                }
                .loading-card {
                    background: #1e1e2e;
                    padding: 30px;
                    border-radius: 16px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 15px;
                }
            </style>
            <div class="loading-spinner ${color === 'white' ? 'white' : ''}"></div>
            ${text ? `<span class="loading-text">${text}</span>` : ''}
        `;

        return container;
    },

    // Show full page loading
    show: function(text = 'Caricamento...') {
        // Remove existing overlay if any
        this.hide();

        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.id = 'global-loading';
        
        const card = document.createElement('div');
        card.className = 'loading-card';
        
        const spinner = this.create({ size: 'large', text });
        card.appendChild(spinner);
        overlay.appendChild(card);
        
        document.body.appendChild(overlay);
    },

    // Hide full page loading
    hide: function() {
        const overlay = document.getElementById('global-loading');
        if (overlay) {
            overlay.remove();
        }
    },

    // Wrap a function with loading indicator
    wrap: async function(fn, loadingText = 'Caricamento...') {
        this.show(loadingText);
        try {
            const result = await fn();
            return result;
        } finally {
            this.hide();
        }
    }
};

// Fade in animation for elements
const FadeIn = {
    elements: [],

    init: function() {
        // Find all elements with fade-in class
        this.elements = document.querySelectorAll('.fade-in');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        this.elements.forEach(el => observer.observe(el));
    },

    // Add fade-in class to element
    add: function(element, delay = 0) {
        element.classList.add('fade-in');
        element.style.animationDelay = `${delay}ms`;
    }
};

// Add CSS for fade animations
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }
    .fade-in.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Staggered animation delays */
    .fade-in-delay-1 { animation-delay: 0.1s; }
    .fade-in-delay-2 { animation-delay: 0.2s; }
    .fade-in-delay-3 { animation-delay: 0.3s; }
    .fade-in-delay-4 { animation-delay: 0.4s; }
    .fade-in-delay-5 { animation-delay: 0.5s; }
    
    /* Card hover effects */
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.15);
    }
    
    /* Button hover animation */
    .btn {
        transition: all 0.2s ease;
    }
    .btn:hover {
        transform: translateY(-2px);
    }
    .btn:active {
        transform: translateY(0);
    }
    
    /* Pulse animation for live indicators */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Skeleton loading */
    .skeleton {
        background: linear-gradient(90deg, #1e1e2e 25%, #2a2a3e 50%, #1e1e2e 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s ease-in-out infinite;
    }
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
`;
document.head.appendChild(style);

// Toast notifications
const Toast = {
    show: function(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toast-container') || this.createContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        toast.innerHTML = `
            <style>
                .toast-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 10000;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .toast {
                    padding: 15px 20px;
                    border-radius: 10px;
                    background: #1e1e2e;
                    color: white;
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
                    animation: slideIn 0.3s ease;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .toast-success { border-left: 4px solid #10b981; }
                .toast-error { border-left: 4px solid #ef4444; }
                .toast-warning { border-left: 4px solid #f59e0b; }
                .toast-info { border-left: 4px solid #6366f1; }
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
                .toast.hiding {
                    animation: slideOut 0.3s ease forwards;
                }
            </style>
            <span>${icons[type] || icons.info}</span>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },
    
    createContainer: function() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    },
    
    success: function(message) { this.show(message, 'success'); },
    error: function(message) { this.show(message, 'error'); },
    warning: function(message) { this.show(message, 'warning'); },
    info: function(message) { this.show(message, 'info'); }
};

// Export for use
window.LoadingSpinner = LoadingSpinner;
window.FadeIn = FadeIn;
window.Toast = Toast;

