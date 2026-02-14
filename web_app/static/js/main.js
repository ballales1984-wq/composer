/**
 * Music Theory Engine - Web App Main JavaScript
 */

// Utility functions
const api = {
    async get(url) {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('API Error: - main.js:12', error);
            return { success: false, error: error.message };
        }
    },
    
    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API Error: - main.js:26', error);
            return { success: false, error: error.message };
        }
    }
};

// Note utilities
const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

// Scale types
const scaleTypes = {
    major: { name: 'Major', intervals: [0, 2, 4, 5, 7, 9, 11] },
    minor_natural: { name: 'Natural Minor', intervals: [0, 2, 3, 5, 7, 8, 10] },
    minor_harmonic: { name: 'Harmonic Minor', intervals: [0, 2, 3, 5, 7, 8, 11] },
    minor_melodic: { name: 'Melodic Minor', intervals: [0, 2, 3, 5, 7, 9, 11] },
    dorian: { name: 'Dorian', intervals: [0, 2, 3, 5, 7, 9, 10] },
    phrygian: { name: 'Phrygian', intervals: [0, 1, 3, 5, 7, 8, 10] },
    lydian: { name: 'Lydian', intervals: [0, 2, 4, 6, 7, 9, 11] },
    mixolydian: { name: 'Mixolydian', intervals: [0, 2, 4, 5, 7, 9, 10] },
    locrian: { name: 'Locrian', intervals: [0, 1, 3, 5, 6, 8, 10] },
    pentatonic_major: { name: 'Major Pentatonic', intervals: [0, 2, 4, 7, 9] },
    pentatonic_minor: { name: 'Minor Pentatonic', intervals: [0, 3, 5, 7, 10] },
    blues_minor: { name: 'Minor Blues', intervals: [0, 3, 5, 6, 7, 10] }
};

// Chord qualities
const chordQualities = {
    maj: { name: 'Major', intervals: [0, 4, 7] },
    min: { name: 'Minor', intervals: [0, 3, 7] },
    dim: { name: 'Diminished', intervals: [0, 3, 6] },
    aug: { name: 'Augmented', intervals: [0, 4, 8] },
    sus2: { name: 'Sus2', intervals: [0, 2, 7] },
    sus4: { name: 'Sus4', intervals: [0, 5, 7] },
    maj7: { name: 'Major 7th', intervals: [0, 4, 7, 11] },
    dom7: { name: 'Dominant 7th', intervals: [0, 4, 7, 10] },
    min7: { name: 'Minor 7th', intervals: [0, 3, 7, 10] },
    dim7: { name: 'Diminished 7th', intervals: [0, 3, 6, 9] },
    min7b5: { name: 'Half-Diminished', intervals: [0, 3, 6, 10] }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Music Theory Engine Web App loaded - main.js:68');
});

