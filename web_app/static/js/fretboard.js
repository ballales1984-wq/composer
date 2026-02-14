/**
 * Guitar Fretboard Visualization Library
 * Professional fretboard rendering with SVG
 */

class GuitarFretboard {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            numFrets: options.numFrets || 15,
            tuning: options.tuning || 'standard',
            showFretNumbers: options.showFretNumbers !== false,
            showStringNames: options.showStringNames !== false,
            showFretMarkers: options.showFretMarkers !== false,
            onNoteClick: options.onNoteClick || null,
            colorRoot: options.colorRoot || '#ec4899',
            colorScale: options.colorScale || '#6366f1',
            colorChord: options.colorChord || '#10b981',
            width: options.width || 900,
            height: options.height || 280,
            ...options
        };
        
        // Standard tunings
        this.tunings = {
            'standard': ['E', 'A', 'D', 'G', 'B', 'e'],
            'drop_d': ['D', 'A', 'D', 'G', 'B', 'e'],
            'open_g': ['D', 'G', 'D', 'G', 'B', 'D'],
            'open_d': ['D', 'A', 'D', 'F#', 'A', 'D'],
            'half_step': ['Eb', 'Ab', 'Db', 'Gb', 'Bb', 'eb'],
            'full_step': ['D', 'G', 'C', 'F', 'A', 'D']
        };
        
        this.chromaticNotes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        this.currentTuning = this.tunings[this.options.tuning];
        this.activeNotes = new Set();
        this.noteType = {}; // note -> type (root, scale, chord)
        this.render();
    }
    
    setTuning(tuningName) {
        if (this.tunings[tuningName]) {
            this.currentTuning = this.tunings[tuningName];
            this.render();
        }
    }
    
    setNumFrets(numFrets) {
        this.options.numFrets = numFrets;
        this.render();
    }
    
    highlightNotes(notes, type = 'scale') {
        this.activeNotes = new Set(notes);
        this.noteType = {};
        notes.forEach(n => this.noteType[n] = type);
        this.render();
    }
    
    highlightScale(root, scaleType) {
        const intervals = {
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
            blues_major: [0, 2, 3, 4, 7, 9]
        };
        
        const rootIndex = this.chromaticNotes.indexOf(root);
        const scaleIntervals = intervals[scaleType] || intervals.major;
        
        const notes = scaleIntervals.map(i => this.chromaticNotes[(rootIndex + i) % 12]);
        this.highlightNotes(notes, 'scale');
        
        // Mark root separately
        this.noteType[root] = 'root';
        this.activeNotes.add(root);
    }
    
    highlightChord(root, quality) {
        const intervals = {
            maj: [0, 4, 7],
            min: [0, 3, 7],
            dim: [0, 3, 6],
            aug: [0, 4, 8],
            dom7: [0, 4, 7, 10],
            maj7: [0, 4, 7, 11],
            min7: [0, 3, 7, 10],
            dim7: [0, 3, 6, 9],
            min7b5: [0, 3, 6, 10],
            '9': [0, 4, 7, 10, 14],
            maj9: [0, 4, 7, 11, 14],
            min9: [0, 3, 7, 10, 14],
            '11': [0, 4, 7, 10, 14, 17],
            '13': [0, 4, 7, 10, 14, 21]
        };
        
        const rootIndex = this.chromaticNotes.indexOf(root);
        const chordIntervals = intervals[quality] || intervals.maj;
        
        const notes = chordIntervals.map(i => this.chromaticNotes[(rootIndex + i) % 12]);
        this.highlightNotes(notes, 'chord');
        
        // Mark root separately
        this.noteType[root] = 'root';
        this.activeNotes.add(root);
    }
    
    // NEW: Highlight both scale and chord simultaneously
    highlightScaleAndChord(scaleRoot, scaleType, chordRoot, chordQuality) {
        // Get scale notes
        const scaleIntervals = {
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
            blues_major: [0, 2, 3, 4, 7, 9]
        };
        
        // Get chord intervals
        const chordIntervals = {
            maj: [0, 4, 7],
            min: [0, 3, 7],
            dim: [0, 3, 6],
            aug: [0, 4, 8],
            dom7: [0, 4, 7, 10],
            maj7: [0, 4, 7, 11],
            min7: [0, 3, 7, 10],
            dim7: [0, 3, 6, 9],
            min7b5: [0, 3, 6, 10],
            '9': [0, 4, 7, 10, 14],
            maj9: [0, 4, 7, 11, 14],
            min9: [0, 3, 7, 10, 14],
            '11': [0, 4, 7, 10, 14, 17],
            '13': [0, 4, 7, 10, 14, 21]
        };
        
        const scaleRootIdx = this.chromaticNotes.indexOf(scaleRoot);
        const chordRootIdx = this.chromaticNotes.indexOf(chordRoot);
        
        const scaleInterv = scaleIntervals[scaleType] || scaleIntervals.major;
        const chordInterv = chordIntervals[chordQuality] || chordIntervals.maj;
        
        const scaleNotes = scaleInterv.map(i => this.chromaticNotes[(scaleRootIdx + i) % 12]);
        const chordNotes = chordInterv.map(i => this.chromaticNotes[(chordRootIdx + i) % 12]);
        
        // Find common notes
        const commonNotes = scaleNotes.filter(n => chordNotes.includes(n));
        
        // Set up active notes with types
        this.activeNotes = new Set();
        this.noteType = {};
        
        // Mark scale notes (not in chord)
        scaleNotes.forEach(n => {
            if (!commonNotes.includes(n)) {
                this.activeNotes.add(n);
                this.noteType[n] = 'scale';
            }
        });
        
        // Mark chord notes (not in common)
        chordNotes.forEach(n => {
            if (!commonNotes.includes(n)) {
                this.activeNotes.add(n);
                this.noteType[n] = 'chord';
            }
        });
        
        // Mark common notes
        commonNotes.forEach(n => {
            this.activeNotes.add(n);
            this.noteType[n] = 'common';
        });
        
        // Mark roots
        this.noteType[scaleRoot] = 'root';
        this.noteType[chordRoot] = 'root';
        this.activeNotes.add(scaleRoot);
        this.activeNotes.add(chordRoot);
        
        // Store info for legend
        this.currentScaleNotes = scaleNotes;
        this.currentChordNotes = chordNotes;
        this.currentCommonNotes = commonNotes;
        
        this.render();
    }
    
    // Get info about current display for legend
    getDisplayInfo() {
        return {
            scale: this.currentScaleNotes || [],
            chord: this.currentChordNotes || [],
            common: this.currentCommonNotes || []
        };
    }
    
    clearNotes() {
        this.activeNotes = new Set();
        this.noteType = {};
        this.render();
    }
    
    getNoteAtPosition(stringIndex, fret) {
        const openNote = this.currentTuning[stringIndex];
        let openIndex = this.chromaticNotes.indexOf(openNote);
        
        // Handle flats
        if (openIndex === -1) {
            const flatMap = { 'Eb': 'D#', 'Ab': 'G#', 'Bb': 'A#', 'Db': 'C#', 'Gb': 'F#' };
            if (flatMap[openNote]) {
                openIndex = this.chromaticNotes.indexOf(flatMap[openNote]);
            }
        }
        
        const noteIndex = (openIndex + fret) % 12;
        return this.chromaticNotes[noteIndex];
    }
    
    render() {
        const { numFrets, showFretNumbers, showStringNames, showFretMarkers, 
                width, height, colorRoot, colorScale, colorChord } = this.options;
        
        const stringLabelWidth = showStringNames ? 40 : 0;
        const numFret = numFrets;
        const fretWidth = (width - stringLabelWidth - 40) / numFret;
        const stringHeight = (height - 60) / 6;
        
        let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" 
                   style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">`;
        
        // Background
        svg += `<defs>
            <linearGradient id="fretboardBg" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#2d1810"/>
                <stop offset="100%" style="stop-color:#1a0f0a"/>
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
            </filter>
        </defs>`;
        
        svg += `<rect x="0" y="0" width="${width}" height="${height}" fill="url(#fretboardBg)" rx="8"/>`;
        
        // Fret markers (position dots)
        if (showFretMarkers) {
            const markerFrets = [3, 5, 7, 9, 12, 15, 17, 19, 21];
            markerFrets.forEach(fret => {
                if (fret <= numFrets) {
                    const x = stringLabelWidth + (fret - 0.5) * fretWidth;
                    const isDouble = fret === 12;
                    const y1 = height / 2 - (isDouble ? 15 : 0);
                    const y2 = height / 2 + (isDouble ? 15 : 0);
                    
                    if (isDouble) {
                        svg += `<circle cx="${x}" cy="${y1}" r="5" fill="rgba(255,255,255,0.25)"/>`;
                        svg += `<circle cx="${x}" cy="${y2}" r="5" fill="rgba(255,255,255,0.25)"/>`;
                    } else {
                        svg += `<circle cx="${x}" cy="${height/2}" r="5" fill="rgba(255,255,255,0.25)"/>`;
                    }
                }
            });
        }
        
        // Strings (from top = high e to bottom = low E for correct guitar diagram view)
        // In guitar diagrams: high e string is at TOP, low E is at BOTTOM
        const stringThicknesses = [0.8, 1, 1.5, 2, 2.5, 3]; // High e thin, low E thick
        for (let i = 0; i < 6; i++) {
            // Invert the y position: i=0 (high e) -> top, i=5 (low E) -> bottom
            const y = 40 + (5 - i) * stringHeight;
            const thickness = stringThicknesses[i];
            svg += `<line x1="${stringLabelWidth}" y1="${y}" x2="${width-20}" y2="${y}" 
                    stroke="url(#stringGradient)" stroke-width="${thickness}" 
                    opacity="0.9"/>`;
        }
        
        // String gradient
        svg += `<defs>
            <linearGradient id="stringGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#666"/>
                <stop offset="50%" style="stop-color:#aaa"/>
                <stop offset="100%" style="stop-color:#666"/>
            </linearGradient>
        </defs>`;
        
        // Frets (vertical lines)
        for (let i = 0; i <= numFrets; i++) {
            const x = stringLabelWidth + i * fretWidth;
            const isNut = i === 0;
            const fretColor = isNut ? '#d4af37' : '#555';
            const fretWidthAttr = isNut ? 4 : 2;
            
            svg += `<line x1="${x}" y1="30" x2="${x}" y2="${height-30}" 
                    stroke="${fretColor}" stroke-width="${fretWidthAttr}"/>`;
        }
        
        // String names (left side) - now correctly showing high e at top, low E at bottom
        if (showStringNames) {
            for (let i = 0; i < 6; i++) {
                const y = 40 + (5 - i) * stringHeight;
                svg += `<text x="${stringLabelWidth/2}" y="${y+5}" 
                        text-anchor="middle" fill="#888" font-size="14" font-weight="bold">
                        ${this.currentTuning[i]}</text>`;
            }
        }
        
        // Fret numbers (horizontal, below fretboard)
        if (showFretNumbers) {
            for (let i = 0; i <= numFrets; i++) {
                const x = stringLabelWidth + (i === 0 ? 20 : (i - 0.5) * fretWidth);
                svg += `<text x="${x}" y="${height-8}" text-anchor="middle" 
                        fill="#666" font-size="11">${i === 0 ? 'O' : i}</text>`;
            }
        }
        
        // Notes - render at correct positions matching the inverted string layout
        for (let stringIdx = 0; stringIdx < 6; stringIdx++) {
            const y = 40 + (5 - stringIdx) * stringHeight;
            
            for (let fret = 0; fret <= numFrets; fret++) {
                const note = this.getNoteAtPosition(stringIdx, fret);
                
                if (this.activeNotes.has(note)) {
                    const x = stringLabelWidth + (fret === 0 ? 20 : (fret - 0.5) * fretWidth);
                    const type = this.noteType[note] || 'scale';
                    
                    let color;
                    if (type === 'root') color = colorRoot;
                    else if (type === 'chord') color = colorChord;
                    else if (type === 'common') color = '#fbbf24';  // Gold for common notes
                    else color = colorScale;
                    
                    // Note circle with shadow
                    svg += `<circle cx="${x}" cy="${y}" r="14" fill="${color}" 
                            filter="url(#shadow)" opacity="0.9"/>`;
                    
                    // Note text
                    svg += `<text x="${x}" y="${y+4}" text-anchor="middle" 
                            fill="white" font-size="10" font-weight="bold">${note}</text>`;
                }
            }
        }
        
        svg += '</svg>';
        
        // Add click handler
        this.container.innerHTML = svg;
        this.container.style.cursor = 'pointer';
        
        // Add note click events
        this.container.querySelectorAll('circle').forEach(circle => {
            circle.addEventListener('click', (e) => {
                if (this.options.onNoteClick) {
                    const cx = parseFloat(circle.getAttribute('cx'));
                    const cy = parseFloat(circle.getAttribute('cy'));
                    
                    // Calculate string and fret from position
                    // Note: y position is inverted for display, so we need to convert back
                    const visualStringIdx = Math.round((cy - 40) / stringHeight);
                    const stringIdx = 5 - visualStringIdx; // Convert visual position to actual string index
                    const fret = Math.round((cx - stringLabelWidth) / fretWidth);
                    
                    if (stringIdx >= 0 && stringIdx < 6 && fret >= 0 && fret <= numFrets) {
                        const note = this.getNoteAtPosition(stringIdx, fret);
                        this.options.onNoteClick(note, stringIdx, fret);
                    }
                }
            });
        });
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GuitarFretboard;
}

