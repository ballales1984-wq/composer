/**
 * Shared Music Theory Components
 * Reusable components for the Music Theory Engine
 */

// Export all components
window.MusicComponents = {
    // Components will be loaded from individual files
    AudioManager: window.AudioManager
};

// Initialize components when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Music Components loaded');
});

