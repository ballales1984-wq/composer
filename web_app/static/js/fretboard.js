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
        
        // Standard tunings (from highest pitch at TOP to lowest at BOTTOM)
        this.tunings = {
            'standard': ['E', 'B', 'G', 'D', 'A', 'E'],  // High E at top, low E at bottom
            'drop_d': ['E', 'B', 'G', 'D', 'A', 'D'],  // Drop D tuning
            'open_g': ['D', 'B', 'G', 'D', 'G', 'D'],  // Open G (D G D G B D)
            'open_d': ['D', 'A', 'F#', 'D', 'A', 'D'],  // Open D (D A D F# A D) - FIXED: high to low
            'half_step': ['Eb', 'Bb', 'Gb', 'Db', 'Ab', 'Eb'],  // Half step down (Eb Ab Db Gb Bb eb)
            'full_step': ['D', 'A', 'F', 'C', 'G', 'D']  // Full step down (D G C F A D) - FIXED: high to low
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
    
    // Highlight a note temporarily (for play scale animation) - now with MIDI for precise position
    highlightNoteTemporary(noteName, duration, midiNote = null) {
        // Store original active notes
        const originalActiveNotes = new Set(this.activeNotes);
        const originalNoteType = {...this.noteType};
        
        // Determine which specific position(s) to highlight based on MIDI note
        if (midiNote !== null) {
            // If we have MIDI, highlight only that specific position
            this.tempHighlightMidi = midiNote;
        } else {
            this.tempHighlightMidi = null;
        }
        
        // Keep current notes visible and add playing note highlight
        // (don't clear - this.activeNotes already has the scale/chord notes)
        // The scale/chord stays visible, and we add a "playing" highlight on top
        // Just mark the playing note without clearing other note types
        this.activeNotes.add(noteName);
        this.noteType[noteName] = 'playing';
        
        // Re-render with ONLY the highlighted note
        this.render();
        
        // After duration, restore original notes
        setTimeout(() => {
            this.tempHighlightMidi = null;
            this.activeNotes = originalActiveNotes;
            this.noteType = originalNoteType;
            this.render();
        }, duration);
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
        const noteName = this.chromaticNotes[noteIndex];
        
        // Standard guitar tuning MIDI notes (low E = 40, high e = 64)
        // String 0 (high e): E4 = 64, String 5 (low E): E2 = 40
        const stringBaseMidi = [64, 59, 55, 50, 45, 40]; // E4, B3, G3, D3, A2, E2
        
        // Calculate MIDI note: base MIDI + fret
        const midiNote = stringBaseMidi[stringIndex] + fret;
        
        // Calculate octave from MIDI (MIDI 60 = C4)
        const octave = Math.floor(midiNote / 12) - 1;
        
        return { note: noteName, octave: octave, midi: midiNote };
    }
    
    render() {
        const { numFrets, showFretNumbers, showStringNames, showFretMarkers, 
                width, height, colorRoot, colorScale, colorChord } = this.options;
        
        const stringLabelWidth = showStringNames ? 40 : 0;
        const numFret = numFrets;
        const fretWidth = (width - stringLabelWidth - 40) / numFret;
        const stringHeight = (height - 60) / 6;
        
        // Note circle radius - made larger for easier clicking
        const noteRadius = 18;
        
        let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" 
                   style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">`;
        
        // Background and definitions
        svg += `<defs>
            <linearGradient id="fretboardBg" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#2d1810"/>
                <stop offset="100%" style="stop-color:#1a0f0a"/>
            </linearGradient>
            <linearGradient id="stringGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#666"/>
                <stop offset="50%" style="stop-color:#aaa"/>
                <stop offset="100%" style="stop-color:#666"/>
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
        // thickness array: index 0 = first string (top), index 5 = last string (bottom)
        const stringThicknesses = [1.5, 2, 2.5, 3, 3.5, 4.5]; // High e thin at TOP, low E thick at BOTTOM
        for (let i = 0; i < 6; i++) {
            // i=0 is high e (top), i=5 is low E (bottom)
            const y = 40 + i * stringHeight;
            const thickness = stringThicknesses[i];
            svg += `<line x1="${stringLabelWidth}" y1="${y}" x2="${width-20}" y2="${y}" 
                    stroke="#cccccc" stroke-width="${thickness}" 
                    opacity="1.0"/>`;
        }
        
        // Frets (vertical lines)
        for (let i = 0; i <= numFrets; i++) {
            const x = stringLabelWidth + i * fretWidth;
            const isNut = i === 0;
            const fretColor = isNut ? '#d4af37' : '#555';
            const fretWidthAttr = isNut ? 4 : 2;
            
            svg += `<line x1="${x}" y1="30" x2="${x}" y2="${height-30}" 
                    stroke="${fretColor}" stroke-width="${fretWidthAttr}"/>`;
        }
        
        // String names (left side) - high e at top, low E at bottom
        if (showStringNames) {
            for (let i = 0; i < 6; i++) {
                const y = 40 + i * stringHeight;
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
        
        // Notes - render at correct positions (skip fret 0 as it's shown as string names)
        // Check if we have a temporary highlight (playing animation)
        const hasTempHighlight = this.tempHighlightMidi !== null && this.tempHighlightMidi !== undefined;
        
        for (let stringIdx = 0; stringIdx < 6; stringIdx++) {
            const y = 40 + stringIdx * stringHeight;
            
            // Start from fret 1 (skip open strings which are shown as labels)
            for (let fret = 1; fret <= numFrets; fret++) {
                const noteInfo = this.getNoteAtPosition(stringIdx, fret);
                const note = noteInfo.note;
                const octave = noteInfo.octave;
                const midiNote = noteInfo.midi;
                
                // Check if this note should be rendered
                let shouldRender = false;
                let type = 'scale';
                
                if (hasTempHighlight) {
                    // If this is the specific highlighted note (by MIDI), show it in cyan
                    if (midiNote === this.tempHighlightMidi) {
                        const x = stringLabelWidth + (fret - 0.5) * fretWidth;
                        svg += `<circle cx="${x}" cy="${y}" r="${noteRadius+4}" fill="#00ffff" filter="url(#shadow)" opacity="1.0"/>`;
                        const displayNote = fret > 12 ? `${note}${octave}` : note;
                        svg += `<text x="${x}" y="${y+4}" text-anchor="middle" fill="black" font-size="10" font-weight="bold">${displayNote}</text>`;
                        svg += `<circle cx="${x}" cy="${y}" r="${noteRadius+12}" fill="transparent" data-string="${stringIdx}" data-fret="${fret}" class="note-click-area"/>`;
                    }
                    // Also render normal active notes (scale/chord) - they stay visible!
                    else if (this.activeNotes.has(note)) {
                        const x = stringLabelWidth + (fret - 0.5) * fretWidth;
                        const noteType = this.noteType[note] || 'scale';
                        let color;
                        if (noteType === 'root') color = colorRoot;
                        else if (noteType === 'chord') color = colorChord;
                        else if (noteType === 'common') color = '#fbbf24';
                        else color = colorScale;
                        svg += `<circle cx="${x}" cy="${y}" r="${noteRadius}" fill="${color}" filter="url(#shadow)" opacity="0.9"/>`;
                        const displayNote = fret > 12 ? `${note}${octave}` : note;
                        svg += `<text x="${x}" y="${y+4}" text-anchor="middle" fill="white" font-size="10" font-weight="bold">${displayNote}</text>`;
                        svg += `<circle cx="${x}" cy="${y}" r="${noteRadius + 8}" fill="transparent" data-string="${stringIdx}" data-fret="${fret}" class="note-click-area"/>`;
                    }
                } else {
                    // Normal rendering: check if this note is in activeNotes
                    shouldRender = this.activeNotes.has(note);
                    type = this.noteType[note] || 'scale';
                }
                
                if (shouldRender) {
                    const x = stringLabelWidth + (fret === 0 ? 20 : (fret - 0.5) * fretWidth);
                    
                    let color;
                    if (type === 'root') color = colorRoot;
                    else if (type === 'chord') color = colorChord;
                    else if (type === 'common') color = '#fbbf24';  // Gold for common notes
                    else if (type === 'playing') color = '#00ffff';  // Cyan for playing note
                    else color = colorScale;
                    
                    // Note circle with shadow - using larger radius for easier clicking
                    // Add extra glow for playing notes
                    if (type === 'playing') {
                        svg += `<circle cx="${x}" cy="${y}" r="${noteRadius + 4}" fill="${color}" 
                                opacity="1.0"/>`;
                    }
                    svg += `<circle cx="${x}" cy="${y}" r="${noteRadius}" fill="${color}" 
                            filter="url(#shadow)" opacity="0.9"/>`;
                    
                    // Note text with octave for frets > 12, otherwise just note name
                    const displayNote = fret > 12 ? `${note}${octave}` : note;
                    const textColor = (type === 'playing') ? 'black' : 'white';
                    svg += `<text x="${x}" y="${y+4}" text-anchor="middle" 
                            fill="${textColor}" font-size="${fret > 12 ? '8' : '10'}" font-weight="bold">${displayNote}</text>`;
                    
                    // Invisible larger clickable area for easier clicking
                    svg += `<circle cx="${x}" cy="${y}" r="${noteRadius + 8}" fill="transparent" 
                            data-string="${stringIdx}" data-fret="${fret}" class="note-click-area"/>`;
                }
            }
        }
        
        svg += '</svg>';
        
        // Add click handler
        this.container.innerHTML = svg;
        this.container.style.cursor = 'pointer';
        
        // Add note click events - use the invisible click areas
        this.container.querySelectorAll('.note-click-area').forEach(area => {
            area.addEventListener('click', (e) => {
                if (this.options.onNoteClick) {
                    const stringIdx = parseInt(area.getAttribute('data-string'));
                    const fret = parseInt(area.getAttribute('data-fret'));
                    
                    if (stringIdx >= 0 && stringIdx < 6 && fret >= 0 && fret <= numFrets) {
                        const note = this.getNoteAtPosition(stringIdx, fret);
                        this.options.onNoteClick(note, stringIdx, fret);
                    }
                }
            });
            
            // Also add hover effect
            area.addEventListener('mouseenter', () => {
                area.style.cursor = 'pointer';
            });
        });
        
        // Also handle click on visible circles as fallback
        this.container.querySelectorAll('circle:not(.note-click-area)').forEach(circle => {
            circle.style.pointerEvents = 'none'; // Let clicks pass through to click areas
        });
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GuitarFretboard;
}

