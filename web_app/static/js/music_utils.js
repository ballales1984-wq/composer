/**
 * MusicUtils - Shared Music Theory Utilities
 * Common functions used across the application
 */

const MusicUtils = {
    // All chromatic notes
    chromaticNotes: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    
    // Note to semitone mapping
    noteToSemitone: {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
        'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    },
    
    // Semitone to note mapping
    semitoneToNote: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    
    // Scale intervals
    scaleIntervals: {
        major: [0, 2, 4, 5, 7, 9, 11],
        minor_natural: [0, 2, 3, 5, 7, 8, 10],
        minor_harmonic: [0, 2, 3, 5, 7, 8, 11],
        minor_melodic: [0, 2, 3, 5, 7, 9, 11],
        dorian: [0, 2, 3, 5, 7, 9, 10],
        phrygian: [0, 1, 3, 5, 7, 8, 10],
        lydian: [0, 2, 4, 6, 7, 9, 11],
        mixolydian: [0, 2, 4, 5, 7, 9, 10],
        locrian: [0, 1, 3, 5, 6, 8, 10],
        pentatonic_major: [0, 2, 4, 7, 9],
        pentatonic_minor: [0, 3, 5, 7, 10],
        blues_minor: [0, 3, 5, 6, 7, 10],
        blues_major: [0, 2, 3, 4, 7, 9],
        bebop_major: [0, 2, 4, 5, 7, 8, 9, 11],
        bebop_dominant: [0, 2, 4, 5, 7, 9, 10, 11],
        spanish_phrygian: [0, 1, 4, 5, 7, 8, 10]
    },
    
    // Chord intervals
    chordIntervals: {
        maj: [0, 4, 7],
        min: [0, 3, 7],
        dim: [0, 3, 6],
        aug: [0, 4, 8],
        maj7: [0, 4, 7, 11],
        min7: [0, 3, 7, 10],
        dom7: [0, 4, 7, 10],
        dim7: [0, 3, 6, 9],
        min7b5: [0, 3, 6, 10],
        maj9: [0, 4, 7, 11, 14],
        min9: [0, 3, 7, 10, 14],
        '9': [0, 4, 7, 10, 14],
        '11': [0, 4, 7, 10, 14, 17],
        '13': [0, 4, 7, 10, 14, 21],
        sus2: [0, 2, 7],
        sus4: [0, 5, 7],
        add9: [0, 4, 7, 14]
    },
    
    // Standard guitar tunings
    tunings: {
        standard: ['E', 'B', 'G', 'D', 'A', 'E'],
        drop_d: ['E', 'B', 'G', 'D', 'A', 'D'],
        open_g: ['D', 'B', 'G', 'D', 'G', 'D'],
        open_d: ['D', 'A', 'D', 'F#', 'A', 'D'],
        half_step: ['Eb', 'Bb', 'Gb', 'Db', 'Ab', 'Eb'],
        full_step: ['D', 'A', 'G', 'C', 'F', 'D']
    },
    
    /**
     * Get note at fret position
     */
    getNoteAtFret(openNote, fret) {
        const openIdx = this.noteToSemitone[openNote] !== undefined 
            ? this.noteToSemitone[openNote] 
            : this.chromaticNotes.indexOf(openNote);
        
        if (openIdx === -1) return openNote;
        
        const noteIdx = (openIdx + fret) % 12;
        return this.semitoneToNote[noteIdx];
    },
    
    /**
     * Get scale notes
     */
    getScaleNotes(root, scaleType) {
        const rootIdx = this.chromaticNotes.indexOf(root);
        const intervals = this.scaleIntervals[scaleType] || this.scaleIntervals.major;
        
        return intervals.map(i => this.chromaticNotes[(rootIdx + i) % 12]);
    },
    
    /**
     * Get chord notes
     */
    getChordNotes(root, quality) {
        const rootIdx = this.chromaticNotes.indexOf(root);
        const intervals = this.chordIntervals[quality] || this.chordIntervals.maj;
        
        return intervals.map(i => this.chromaticNotes[(rootIdx + i) % 12]);
    },
    
    /**
     * Get triads for a root
     */
    getTriads(root) {
        const rootIdx = this.chromaticNotes.indexOf(root);
        
        return {
            major: [root, this.chromaticNotes[(rootIdx + 4) % 12], this.chromaticNotes[(rootIdx + 7) % 12]],
            minor: [root, this.chromaticNotes[(rootIdx + 3) % 12], this.chromaticNotes[(rootIdx + 7) % 12]],
            diminished: [root, this.chromaticNotes[(rootIdx + 3) % 12], this.chromaticNotes[(rootIdx + 6) % 12]],
            augmented: [root, this.chromaticNotes[(rootIdx + 4) % 12], this.chromaticNotes[(rootIdx + 8) % 12]]
        };
    },
    
    /**
     * Get arpeggio patterns
     */
    getArpeggioPatterns() {
        return {
            major: [0, 2, 4],
            minor: [0, 2, 4],  // Same as major but with minor chord
            dominant: [0, 2, 4, 6],
            diminished: [0, 2, 4, 6],
            octave: [0, 7, 12, 19, 24]
        };
    },
    
    /**
     * Get chord positions for guitar
     */
    getChordPositions(root, quality) {
        const notes = this.getChordNotes(root, quality);
        const positions = [];
        
        // Simple position calculation (can be expanded)
        const tuning = this.tunings.standard;
        
        for (let string = 0; string < 6; string++) {
            for (let fret = 0; fret <= 12; fret++) {
                const note = this.getNoteAtFret(tuning[string], fret);
                if (notes.includes(note)) {
                    positions.push({ string, fret, note });
                }
            }
        }
        
        return positions;
    },
    
    /**
     * Detect key from notes
     */
    detectKey(notes) {
        const noteCounts = {};
        notes.forEach(n => {
            const normalized = this.normalizeNote(n);
            noteCounts[normalized] = (noteCounts[normalized] || 0) + 1;
        });
        
        // Simple key detection based on most common notes
        const majorKeyWeights = {
            'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
            'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
            'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
            'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
            'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']
        };
        
        let bestKey = 'C';
        let bestScore = 0;
        
        for (const [key, scaleNotes] of Object.entries(majorKeyWeights)) {
            let score = 0;
            scaleNotes.forEach(n => {
                if (noteCounts[n]) score += noteCounts[n];
            });
            if (score > bestScore) {
                bestScore = score;
                bestKey = key;
            }
        }
        
        return { key: bestKey, confidence: bestScore / notes.length };
    },
    
    /**
     * Normalize note (flats to sharps)
     */
    normalizeNote(note) {
        const flatToSharp = {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
        };
        return flatToSharp[note] || note;
    },
    
    /**
     * Get interval name
     */
    getIntervalName(semitones) {
        const intervals = [
            'Unison', 'Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd',
            'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th',
            'Minor 7th', 'Major 7th', 'Octave'
        ];
        return intervals[semitones % 12] || `${semitones} semitones`;
    },
    
    /**
     * Get scale degrees
     */
    getScaleDegrees(scaleType) {
        const degrees = {
            major: ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'],
            minor_natural: ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii'],
            minor_harmonic: ['i', 'ii', 'iii+', 'iv', 'V', 'vi', 'VII'],
            dorian: ['i', 'ii', 'III', 'IV', 'v', 'vi', 'VII'],
            phrygian: ['i', 'II', 'III', 'iv', 'v', 'VI', 'vii'],
            lydian: ['I', 'II', 'III', '#IV', 'V', 'VI', 'VII'],
            mixolydian: ['I', 'II', 'iii', 'IV', 'v', 'vi', 'VII'],
            locrian: ['i', 'II', 'iii', 'iv', 'V', 'vi', 'vii']
        };
        return degrees[scaleType] || degrees.major;
    }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MusicUtils;
}

