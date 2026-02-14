/**
 * AudioManager - Centralized Audio Playback System
 * Handles all audio playback across the application
 */

class AudioManager {
    constructor() {
        this.context = null;
        this.masterGain = null;
        this.isInitialized = false;
        
        // Note frequencies (A4 = 440Hz)
        this.noteFrequencies = {
            'C': 261.63, 'C#': 277.18, 'Db': 277.18, 'D': 293.66,
            'D#': 311.13, 'Eb': 311.13, 'E': 329.63, 'F': 349.23,
            'F#': 369.99, 'Gb': 369.99, 'G': 392.00, 'G#': 415.30,
            'Ab': 415.30, 'A': 440.00, 'A#': 466.16, 'Bb': 466.16,
            'B': 493.88
        };
        
        // Initialize on first user interaction
        this.initOnClick();
    }
    
    initOnClick() {
        const initAudio = () => {
            if (!this.isInitialized) {
                this.context = new (window.AudioContext || window.webkitAudioContext)();
                this.masterGain = this.context.createGain();
                this.masterGain.gain.value = 0.5;
                this.masterGain.connect(this.context.destination);
                this.isInitialized = true;
                
                // Remove listeners after initialization
                document.removeEventListener('click', initAudio);
                document.removeEventListener('keydown', initAudio);
            }
        };
        
        document.addEventListener('click', initAudio);
        document.addEventListener('keydown', initAudio);
    }
    
    /**
     * Play a single note
     * @param {string} note - Note name (C, C#, D, etc.)
     * @param {number} octave - Octave number (default: 4)
     * @param {number} duration - Duration in seconds (default: 0.5)
     * @param {string} type - Wave type: 'sine', 'triangle', 'square', 'sawtooth'
     */
    playNote(note, octave = 4, duration = 0.5, type = 'sine') {
        if (!this.isInitialized) {
            this.initOnClick();
            return;
        }
        
        // Normalize note name
        const normalizedNote = this.normalizeNote(note);
        const frequency = this.noteFrequencies[normalizedNote] * Math.pow(2, octave - 4);
        
        const oscillator = this.context.createOscillator();
        const gainNode = this.context.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = type;
        oscillator.frequency.setValueAtTime(frequency, this.context.currentTime);
        
        // Envelope: attack, decay, sustain, release
        gainNode.gain.setValueAtTime(0, this.context.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.6, this.context.currentTime + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.context.currentTime + duration);
        
        oscillator.start(this.context.currentTime);
        oscillator.stop(this.context.currentTime + duration);
    }
    
    /**
     * Play a chord (multiple notes)
     * @param {string[]} notes - Array of note names
     * @param {number} octave - Base octave (default: 4)
     * @param {number} duration - Duration in seconds
     */
    playChord(notes, octave = 4, duration = 1.0) {
        if (!this.isInitialized) {
            this.initOnClick();
            return;
        }
        
        notes.forEach((note, index) => {
            // Stagger the notes slightly for arpeggio effect
            const delay = index * 0.02;
            setTimeout(() => {
                this.playNote(note, octave, duration, 'triangle');
            }, delay);
        });
    }
    
    /**
     * Play an arpeggio
     * @param {string[]} notes - Notes to play in sequence
     * @param {number} octave - Base octave
     * @param {number} noteDuration - Duration of each note
     * @param {number} delay - Delay between notes
     */
    playArpeggio(notes, octave = 4, noteDuration = 0.3, delay = 0.15) {
        notes.forEach((note, index) => {
            setTimeout(() => {
                this.playNote(note, octave, noteDuration, 'sine');
            }, index * delay * 1000);
        });
    }
    
    /**
     * Play a scale
     * @param {string[]} notes - Scale notes
     * @param {number} octave - Base octave
     */
    playScale(notes, octave = 4) {
        this.playArpeggio(notes, octave, 0.25, 0.2);
    }
    
    /**
     * Get frequency for a note
     * @param {string} note - Note name
     * @param {number} octave - Octave
     * @returns {number} Frequency in Hz
     */
    getFrequency(note, octave = 4) {
        const normalizedNote = this.normalizeNote(note);
        return this.noteFrequencies[normalizedNote] * Math.pow(2, octave - 4);
    }
    
    /**
     * Normalize note name (handle flats to sharps)
     * @param {string} note - Note name
     * @returns {string} Normalized note name
     */
    normalizeNote(note) {
        const flatToSharp = {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
        };
        return flatToSharp[note] || note;
    }
    
    /**
     * Set master volume
     * @param {number} volume - Volume level (0-1)
     */
    setVolume(volume) {
        if (this.masterGain) {
            this.masterGain.gain.value = Math.max(0, Math.min(1, volume));
        }
    }
    
    /**
     * Resume audio context (needed for some browsers)
     */
    async resume() {
        if (this.context && this.context.state === 'suspended') {
            await this.context.resume();
        }
    }
}

// Global instance
const audioManager = new AudioManager();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AudioManager;
}

