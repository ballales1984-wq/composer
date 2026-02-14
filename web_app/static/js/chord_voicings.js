/**
 * Guitar Chord Voicings Data
 * Common chord positions for standard tuning (EADGBe)
 */

const GUITAR_CHORD_VOICINGS = {
    // Major chords
    'C': {
        'maj': [
            { frets: [null, 3, 2, 0, 1, 0], fingers: [null, 3, 2, 0, 1, 0], barre: null, position: 'Open C' },
            { frets: [null, 3, 5, 5, 5, 3], fingers: [null, 1, 2, 3, 4, 1], barre: { fret: 3, fromString: 0, toString: 5, finger: 1 }, position: 'Barre C' },
            { frets: [8, 10, 10, 9, 8, 8], fingers: [1, 3, 4, 2, 1, 1], barre: { fret: 8, fromString: 0, toString: 5, finger: 1 }, position: 'Barre C (8th fret)' }
        ]
    },
    'D': {
        'maj': [
            { frets: [null, null, 0, 2, 3, 2], fingers: [null, null, 0, 1, 3, 2], barre: null, position: 'Open D' },
            { frets: [null, null, 10, 9, 8, 7], fingers: [null, null, 4, 3, 2, 1], barre: null, position: 'Barre D (7th fret)' }
        ]
    },
    'E': {
        'maj': [
            { frets: [0, 2, 2, 1, 0, 0], fingers: [0, 2, 3, 1, 0, 0], barre: null, position: 'Open E' },
            { frets: [7, 9, 9, 8, 7, 7], fingers: [1, 3, 4, 2, 1, 1], barre: { fret: 7, fromString: 0, toString: 5, finger: 1 }, position: 'Barre E' }
        ]
    },
    'F': {
        'maj': [
            { frets: [1, 3, 3, 2, 1, 1], fingers: [1, 3, 4, 2, 1, 1], barre: { fret: 1, fromString: 0, toString: 5, finger: 1 }, position: 'Barre F' },
            { frets: [null, 3, 5, 5, 5, 3], fingers: [null, 1, 2, 3, 4, 1], barre: { fret: 3, fromString: 0, toString: 5, finger: 1 }, position: 'Barre F (3rd fret)' }
        ]
    },
    'G': {
        'maj': [
            { frets: [3, 2, 0, 0, 0, 3], fingers: [2, 1, 0, 0, 0, 3], barre: null, position: 'Open G' },
            { frets: [3, 5, 5, 4, 3, 3], fingers: [1, 3, 4, 2, 1, 1], barre: { fret: 3, fromString: 0, toString: 5, finger: 1 }, position: 'Barre G' }
        ]
    },
    'A': {
        'maj': [
            { frets: [null, 0, 2, 2, 2, 0], fingers: [null, 0, 1, 2, 3, 0], barre: null, position: 'Open A' },
            { frets: [5, 7, 7, 6, 5, 5], fingers: [1, 3, 4, 2, 1, 1], barre: { fret: 5, fromString: 0, toString: 5, finger: 1 }, position: 'Barre A' }
        ]
    },
    'B': {
        'maj': [
            { frets: [null, 2, 4, 4, 4, 2], fingers: [null, 1, 2, 3, 4, 1], barre: { fret: 2, fromString: 0, toString: 5, finger: 1 }, position: 'Barre B' },
            { frets: [7, 9, 9, 8, 7, 7], fingers: [1, 3, 4, 2, 1, 1], barre: { fret: 7, fromString: 0, toString: 5, finger: 1 }, position: 'Barre B (7th fret)' }
        ]
    },
    
    // Minor chords
    'C': {
        'min': [
            { frets: [null, 3, 5, 5, 4, 3], fingers: [null, 1, 3, 4, 2, 1], barre: { fret: 3, fromString: 0, toString: 5, finger: 1 }, position: 'Barre Cm' }
        ]
    },
    'D': {
        'min': [
            { frets: [null, null, 0, 2, 3, 1], fingers: [null, null, 0, 2, 3, 1], barre: null, position: 'Open Dm' }
        ]
    },
    'E': {
        'min': [
            { frets: [0, 2, 2, 0, 0, 0], fingers: [0, 2, 3, 0, 0, 0], barre: null, position: 'Open Em' },
            { frets: [7, 9, 9, 7, 7, 7], fingers: [1, 3, 4, 1, 1, 1], barre: { fret: 7, fromString: 0, toString: 5, finger: 1 }, position: 'Barre Em' }
        ]
    },
    'F': {
        'min': [
            { frets: [1, 3, 3, 1, 1, 1], fingers: [1, 3, 4, 1, 1, 1], barre: { fret: 1, fromString: 0, toString: 5, finger: 1 }, position: 'Barre Fm' }
        ]
    },
    'G': {
        'min': [
            { frets: [3, 5, 5, 3, 3, 3], fingers: [1, 3, 4, 1, 1, 1], barre: { fret: 3, fromString: 0, toString: 5, finger: 1 }, position: 'Barre Gm' }
        ]
    },
    'A': {
        'min': [
            { frets: [null, 0, 2, 2, 1, 0], fingers: [null, 0, 2, 3, 1, 0], barre: null, position: 'Open Am' },
            { frets: [5, 7, 7, 5, 5, 5], fingers: [1, 3, 4, 1, 1, 1], barre: { fret: 5, fromString: 0, toString: 5, finger: 1 }, position: 'Barre Am' }
        ]
    },
    'B': {
        'min': [
            { frets: [null, 2, 4, 4, 3, 2], fingers: [null, 1, 3, 4, 2, 1], barre: { fret: 2, fromString: 0, toString: 5, finger: 1 }, position: 'Barre Bm' }
        ]
    },
    
    // Seventh chords
    'C': {
        'dom7': [
            { frets: [null, 3, 2, 3, 1, 0], fingers: [null, 3, 2, 4, 1, 0], barre: null, position: 'Open C7' }
        ]
    },
    'D': {
        'dom7': [
            { frets: [null, null, 0, 2, 1, 2], fingers: [null, null, 0, 2, 1, 3], barre: null, position: 'Open D7' }
        ]
    },
    'E': {
        'dom7': [
            { frets: [0, 2, 0, 1, 0, 0], fingers: [0, 2, 0, 1, 0, 0], barre: null, position: 'Open E7' }
        ]
    },
    'G': {
        'dom7': [
            { frets: [3, 2, 0, 0, 0, 1], fingers: [2, 1, 0, 0, 0, 3], barre: null, position: 'Open G7' },
            { frets: [3, 5, 3, 4, 3, 3], fingers: [1, 3, 1, 4, 1, 1], barre: { fret: 3, fromString: 0, toString: 5, finger: 1 }, position: 'Barre G7' }
        ]
    },
    'A': {
        'dom7': [
            { frets: [null, 0, 2, 0, 2, 0], fingers: [null, 0, 1, 0, 2, 0], barre: null, position: 'Open A7' }
        ]
    },
    'B': {
        'dom7': [
            { frets: [null, 2, 1, 2, 0, 2], fingers: [null, 3, 1, 4, 0, 2], barre: null, position: 'Open B7' }
        ]
    },
    
    // Major 7th
    'C': {
        'maj7': [
            { frets: [null, 3, 2, 0, 0, 0], fingers: [null, 3, 2, 0, 0, 0], barre: null, position: 'Open Cmaj7' }
        ]
    },
    'D': {
        'maj7': [
            { frets: [null, null, 0, 2, 2, 2], fingers: [null, null, 0, 1, 2, 3], barre: null, position: 'Open Dmaj7' }
        ]
    },
    'G': {
        'maj7': [
            { frets: [3, 2, 0, 0, 0, 2], fingers: [2, 1, 0, 0, 0, 3], barre: null, position: 'Open Gmaj7' }
        ]
    },
    
    // Minor 7th
    'A': {
        'min7': [
            { frets: [null, 0, 2, 0, 2, 0], fingers: [null, 0, 1, 0, 2, 0], barre: null, position: 'Open Am7' }
        ]
    },
    'E': {
        'min7': [
            { frets: [0, 2, 0, 0, 0, 0], fingers: [0, 2, 0, 0, 0, 0], barre: null, position: 'Open Em7' }
        ]
    }
};

// Helper function to get chord positions
function getChordPositions(root, quality) {
    const key = root.replace('#', 's').replace('b', 'b');
    const qualityKey = quality || 'maj';
    
    if (GUITAR_CHORD_VOICINGS[key] && GUITAR_CHORD_VOICINGS[key][qualityKey]) {
        return GUITAR_CHORD_VOICINGS[key][qualityKey].map(v => ({
            root: root,
            quality: quality,
            frets: v.frets,
            fingers: v.fingers,
            barre: v.barre,
            position: v.position
        }));
    }
    
    return [];
}

// Get all chords for a key (diatonic chords)
function getDiatonicChords(key, mode = 'major') {
    const majorScale = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'];
    const minorScale = ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII'];
    
    const scale = mode === 'minor' ? minorScale : majorScale;
    const roots = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const keyIndex = roots.indexOf(key);
    
    const chords = [];
    const intervals = [0, 2, 4, 5, 7, 9, 11]; // Major scale intervals
    
    for (let i = 0; i < 7; i++) {
        const rootNote = roots[(keyIndex + intervals[i]) % 12];
        let quality = '';
        
        if (mode === 'major') {
            if (i === 0 || i === 3 || i === 4) quality = 'maj';
            else if (i === 6) quality = 'dim';
            else quality = 'min';
        } else {
            if (i === 0 || i === 3 || i === 5) quality = 'min';
            else if (i === 1 || i === 4) quality = 'dim';
            else quality = 'maj';
        }
        
        chords.push({
            numeral: scale[i],
            root: rootNote,
            quality: quality,
            degree: i + 1
        });
    }
    
    return chords;
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GUITAR_CHORD_VOICINGS, getChordPositions, getDiatonicChords };
}

