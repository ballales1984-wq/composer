/**
 * VirtualKeyboard - Piano Keyboard Component
 * Clickable piano keyboard for note input
 */

class VirtualKeyboard {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            startOctave: options.startOctave || 3,
            numOctaves: options.numOctaves || 2,
            showLabels: options.showLabels !== false,
            onNoteClick: options.onNoteClick || null,
            width: options.width || 600,
            height: options.height || 160,
            ...options
        };
        
        this.whiteKeyWidth = this.options.width / (this.options.numOctaves * 7);
        this.blackKeyWidth = this.whiteKeyWidth * 0.6;
        this.blackKeyHeight = this.options.height * 0.6;
        
        this.render();
    }
    
    render() {
        const { startOctave, numOctaves, showLabels, width, height } = this.options;
        
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" 
                     style="font-family: 'Inter', -apple-system, sans-serif;">
            <defs>
                <linearGradient id="whiteKeyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#ffffff"/>
                    <stop offset="100%" style="stop-color:#e8e8e8"/>
                </linearGradient>
                <linearGradient id="blackKeyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#333"/>
                    <stop offset="100%" style="stop-color:#111"/>
                </linearGradient>
            </defs>
        </svg>`;
        
        this.container.innerHTML = svg;
        const svgEl = this.container.querySelector('svg');
        
        const whiteKeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
        const blackKeyPositions = { 'C': 0, 'D': 1, 'F': 3, 'G': 4, 'A': 5 }; // Offset from white key
        
        // Draw white keys
        for (let oct = 0; oct < numOctaves; oct++) {
            for (let i = 0; i < 7; i++) {
                const note = whiteKeys[i];
                const x = (oct * 7 + i) * this.whiteKeyWidth;
                
                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('x', x);
                rect.setAttribute('y', 0);
                rect.setAttribute('width', this.whiteKeyWidth - 2);
                rect.setAttribute('height', height);
                rect.setAttribute('fill', 'url(#whiteKeyGrad)');
                rect.setAttribute('stroke', '#ccc');
                rect.setAttribute('stroke-width', '1');
                rect.setAttribute('class', 'white-key');
                rect.setAttribute('data-note', note);
                rect.setAttribute('data-octave', startOctave + oct);
                
                svgEl.appendChild(rect);
                
                // Add label
                if (showLabels) {
                    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    text.setAttribute('x', x + this.whiteKeyWidth / 2);
                    text.setAttribute('y', height - 20);
                    text.setAttribute('text-anchor', 'middle');
                    text.setAttribute('fill', '#666');
                    text.setAttribute('font-size', '12');
                    text.textContent = note + (startOctave + oct);
                    svgEl.appendChild(text);
                }
            }
        }
        
        // Draw black keys
        for (let oct = 0; oct < numOctaves; oct++) {
            for (let i = 0; i < 7; i++) {
                if (blackKeyPositions[i] !== undefined) {
                    const note = whiteKeys[i] + '#';
                    const x = (oct * 7 + i + 0.65) * this.whiteKeyWidth;
                    
                    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                    rect.setAttribute('x', x);
                    rect.setAttribute('y', 0);
                    rect.setAttribute('width', this.blackKeyWidth);
                    rect.setAttribute('height', this.blackKeyHeight);
                    rect.setAttribute('fill', 'url(#blackKeyGrad)');
                    rect.setAttribute('rx', '3');
                    rect.setAttribute('class', 'black-key');
                    rect.setAttribute('data-note', note.replace('#', ''));
                    rect.setAttribute('data-accidental', '#');
                    rect.setAttribute('data-octave', startOctave + oct);
                    
                    svgEl.appendChild(rect);
                }
            }
        }
        
        // Add event listeners
        this.container.querySelectorAll('rect').forEach(rect => {
            rect.addEventListener('click', (e) => {
                const note = rect.getAttribute('data-note');
                const accidental = rect.getAttribute('data-accidental') || '';
                const octave = parseInt(rect.getAttribute('data-octave'));
                const fullNote = note + accidental;
                
                // Visual feedback
                rect.style.fill = rect.classList.contains('white-key') ? '#ddd' : '#555';
                setTimeout(() => {
                    rect.style.fill = '';
                }, 100);
                
                if (this.options.onNoteClick) {
                    this.options.onNoteClick(fullNote, octave);
                }
            });
            
            // Hover effect
            rect.addEventListener('mouseenter', () => {
                rect.style.opacity = '0.8';
            });
            rect.addEventListener('mouseleave', () => {
                rect.style.opacity = '1';
            });
        });
    }
    
    /**
     * Highlight a key
     * @param {string} note - Note name
     * @param {number} octave - Octave
     * @param {string} color - Highlight color
     */
    highlightKey(note, octave, color = '#4CAF50') {
        const key = this.container.querySelector(
            `rect[data-note="${note}"][data-octave="${octave}"]`
        );
        if (key) {
            const originalFill = key.getAttribute('fill');
            key.style.fill = color;
            setTimeout(() => {
                key.style.fill = originalFill;
            }, 300);
        }
    }
    
    /**
     * Set octave range
     */
    setOctaveRange(startOctave, numOctaves) {
        this.options.startOctave = startOctave;
        this.options.numOctaves = numOctaves;
        this.render();
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VirtualKeyboard;
}

