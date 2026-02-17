/**
 * Chord Box Diagram Library
 * Renders standard chord diagrams with finger numbers (like in music textbooks)
 */

class ChordBoxDiagram {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            width: options.width || 120,
            height: options.height || 140,
            stringSpacing: options.stringSpacing || 16,
            fretSpacing: options.fretSpacing || 20,
            stringColor: options.stringColor || '#333',
            fretColor: options.fretColor || '#333',
            fingerColor: options.fingerColor || '#2d3748',
            fingerTextColor: options.fingerTextColor || '#fff',
            mutedColor: options.mutedColor || '#718096',
            openColor: options.openColor || '#2d3748',
            ...options
        };
        
        this.currentChord = null;
    }
    
    /**
     * Draw a chord diagram
     * @param {Object} chordData - { root: 'C', quality: 'maj', fingers: [0,1,2,2,3,0], frets: [null,3,2,0,1,0], barre: null }
     */
    draw(chordData) {
        this.currentChord = chordData;
        
        const { width, height, stringSpacing, fretSpacing } = this.options;
        const numStrings = 6;
        const numFrets = 5;
        
        // Calculate dimensions
        const padding = 20;
        const titleHeight = 20;
        const xStart = padding;
        const yStart = padding + titleHeight;
        
        const diagramWidth = (numStrings - 1) * stringSpacing + padding * 2;
        const diagramHeight = numFrets * fretSpacing + padding * 2;
        
        let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${diagramWidth}" height="${diagramHeight + titleHeight}" 
                   style="font-family: 'Arial', sans-serif;">`;
        
        // Title
        const chordName = this.getChordName(chordData.root, chordData.quality);
        svg += `<text x="${diagramWidth/2}" y="15" text-anchor="middle" font-size="14" font-weight="bold" fill="#1a202c">
                ${chordName}</text>`;
        
        // Draw nut (thick bar at top)
        const nutHeight = 4;
        svg += `<rect x="${xStart - 3}" y="${yStart}" width="${diagramWidth - padding + 6}" height="${nutHeight}" 
                fill="#1a202c" rx="2"/>`;
        
        // Draw frets
        for (let i = 0; i <= numFrets; i++) {
            const y = yStart + nutHeight + i * fretSpacing;
            const lineWidth = i === 0 ? 3 : 1;
            const color = i === 0 ? '#1a202c' : '#a0aec0';
            svg += `<line x1="${xStart}" y1="${y}" x2="${xStart + (numStrings - 1) * stringSpacing}" y2="${y}" 
                    stroke="${color}" stroke-width="${lineWidth}"/>`;
        }
        
        // Draw strings (vertical lines)
        for (let i = 0; i < numStrings; i++) {
            const x = xStart + i * stringSpacing;
            const thickness = 1 + (numStrings - i) * 0.3; // Thicker on low strings
            svg += `<line x1="${x}" y1="${yStart}" x2="${x}" y2="${yStart + numFrets * fretSpacing}" 
                    stroke="${this.options.stringColor}" stroke-width="${thickness}"/>`;
        }
        
        // Draw finger positions
        const frets = chordData.frets || [];
        const fingers = chordData.fingers || [];
        
        for (let stringIdx = 0; stringIdx < numStrings; stringIdx++) {
            const x = xStart + stringIdx * stringSpacing;
            const fret = frets[stringIdx];
            const finger = fingers[stringIdx];
            
            if (fret === null || fret === 'x') {
                // Muted string
                svg += `<text x="${x}" y="${yStart - 5}" text-anchor="middle" font-size="14" font-weight="bold" 
                        fill="${this.options.mutedColor}">×</text>`;
            } else if (fret === 0) {
                // Open string
                svg += `<circle cx="${x}" cy="${yStart + nutHeight/2}" r="4" fill="none" 
                        stroke="${this.options.openColor}" stroke-width="2"/>`;
                // Show finger number if provided
                if (finger > 0) {
                    svg += `<text x="${x}" y="${yStart + nutHeight/2 + 4}" text-anchor="middle" font-size="8" 
                            fill="${this.options.openColor}">${finger}</text>`;
                }
            } else {
                // Fretted note
                const y = yStart + nutHeight + (fret - 0.5) * fretSpacing;
                svg += `<circle cx="${x}" cy="${y}" r="7" fill="${this.options.fingerColor}"/>`;
                
                // Finger number
                if (finger > 0) {
                    svg += `<text x="${x}" y="${y + 3}" text-anchor="middle" font-size="9" font-weight="bold" 
                            fill="${this.options.fingerTextColor}">${finger}</text>`;
                }
            }
        }
        
        // Draw barre if present
        if (chordData.barre) {
            const { fret, fromString, toString } = chordData.barre;
            const x1 = xStart + fromString * stringSpacing;
            const x2 = xStart + toString * stringSpacing;
            const y = yStart + nutHeight + (fret - 0.5) * fretSpacing;
            
            svg += `<rect x="${x1 - 7}" y="${y - 7}" width="${x2 - x1 + 14}" height="14" rx="7" 
                    fill="${this.options.fingerColor}" opacity="0.9"/>`;
            
            // Barre finger number
            svg += `<text x="${(x1 + x2) / 2}" y="${y + 3}" text-anchor="middle" font-size="9" font-weight="bold" 
                    fill="${this.options.fingerTextColor}">${chordData.barre.finger || 1}</text>`;
        }
        
        // Draw string labels at bottom (6th string left → 1st string right: E A D G B e)
        const stringLabels = ['E', 'A', 'D', 'G', 'B', 'E'];
        for (let i = 0; i < numStrings; i++) {
            const x = xStart + i * stringSpacing;
            svg += `<text x="${x}" y="${yStart + numFrets * fretSpacing + 15}" text-anchor="middle" 
                    font-size="10" fill="#718096">${stringLabels[i]}</text>`;
        }
        
        svg += '</svg>';
        
        this.container.innerHTML = svg;
    }
    
    getChordName(root, quality) {
        const qualityNames = {
            'maj': '',
            'min': 'm',
            'dim': 'dim',
            'aug': 'aug',
            'dom7': '7',
            'maj7': 'maj7',
            'min7': 'm7',
            'dim7': 'dim7',
            'min7b5': 'm7♭5',
            'sus2': 'sus2',
            'sus4': 'sus4',
            '7sus4': '7sus4',
            '6': '6',
            'min6': 'm6',
            '6/9': '6/9',
            '9': '9',
            'maj9': 'maj9',
            'min9': 'm9',
            '11': '11',
            '13': '13'
        };
        
        return root + (qualityNames[quality] || '');
    }
    
    clear() {
        this.container.innerHTML = '';
        this.currentChord = null;
    }
}

/**
 * Chord Diagram Grid - displays multiple chord diagrams in a grid
 */
class ChordDiagramGrid {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            columns: options.columns || 3,
            diagramWidth: options.diagramWidth || 120,
            diagramHeight: options.diagramHeight || 140,
            ...options
        };
        
        this.diagrams = [];
    }
    
    /**
     * Draw multiple chord diagrams
     * @param {Array} chords - Array of chordData objects
     */
    draw(chords) {
        if (!chords || chords.length === 0) {
            this.container.innerHTML = '<p style="color: var(--gray);">No chords to display</p>';
            return;
        }
        
        let html = `<div style="display: grid; grid-template-columns: repeat(${this.options.columns}, 1fr); 
                    gap: 1rem; align-items: start;">`;
        
        chords.forEach((chordData, index) => {
            const diagramId = `chord-diagram-${index}`;
            html += `<div id="${diagramId}" class="chord-diagram-item"></div>`;
        });
        
        html += '</div>';
        
        this.container.innerHTML = html;
        
        // Draw each diagram
        chords.forEach((chordData, index) => {
            const diagram = new ChordBoxDiagram(`chord-diagram-${index}`, {
                width: this.options.diagramWidth,
                height: this.options.diagramHeight
            });
            diagram.draw(chordData);
            this.diagrams.push(diagram);
        });
    }
    
    clear() {
        this.container.innerHTML = '';
        this.diagrams = [];
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChordBoxDiagram, ChordDiagramGrid };
}

