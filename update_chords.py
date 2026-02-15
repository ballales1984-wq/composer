# Script to update chords.html with VexChord integration
import os

# Read the file
input_file = 'web_app/templates/chords.html'
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Old function to find and replace
old_func = """async function fetchVoicing(root, quality) {
    try {
        const response = await fetch(`/api/chords/voicing?root=${root}&quality=${quality}`);
        const data = await response.json();
        
        if (data.success) {
            const voicingHtml = data.voicing.map(v => `
                <div class="voicing-item">
                    <span class="voicing-note">${v.note}</span>
                    <span>Octave ${v.octave}</span>
                </div>
            `).join('');
            document.getElementById('voicing-result').innerHTML = `
                <div class="voicing-list">${voicingHtml}</div>
            `;
        }
    } catch (error) {
        console.error('Error fetching voicing:', error);
    }
}"""

# New function with VexChord integration
new_func = """async function fetchVoicing(root, quality) {
    try {
        const response = await fetch(`/api/chords/voicing?root=${root}&quality=${quality}`);
        const data = await response.json();
        
        if (data.success) {
            const voicingHtml = data.voicing.map(v => `
                <div class="voicing-item">
                    <span class="voicing-note">${v.note}</span>
                    <span>Octave ${v.octave}</span>
                </div>
            `).join('');
            document.getElementById('voicing-result').innerHTML = `
                <div class="voicing-list">${voicingHtml}</div>
            `;
        }
    } catch (error) {
        console.error('Error fetching voicing:', error);
    }
    
    // Render chord diagram with VexChord
    mostraAccordo(root, quality);
}

// Funzione per mostrare il diagramma dell'accordo con VexChord
async function mostraAccordo(root, quality) {
    const container = document.getElementById('chord-diagrams-result');
    if (!container) return;
    
    try {
        const res = await fetch(`/api/chords/positions?root=${root}&quality=${quality}`);
        const data = await res.json();
        
        if (!data.success) {
            container.innerHTML = '<p>Select a chord to see chord diagrams</p>';
            return;
        }
        
        const voicing = data.voicings && data.voicings[0] ? data.voicings[0] : null;
        if (!voicing) {
            container.innerHTML = '<p>No chord diagram available</p>';
            return;
        }
        
        const frets = voicing.frets;
        const vexFrets = frets.slice().reverse().map(f => {
            if (f === -1) return 'X';
            if (f === 0) return 'O';
            return f;
        });
        
        const qualityMap = {
            'maj': '', 'min': 'm', 'dom7': '7', 
            'maj7': 'maj7', 'min7': 'm7', 'dim': 'dim',
            'aug': 'aug', 'sus2': 'sus2', 'sus4': 'sus4',
            'dim7': 'dim7', 'min7b5': 'm7b5'
        };
        const q = qualityMap[quality] || quality;
        const chordName = root + q;
        
        if (typeof Vexchord !== 'undefined') {
            container.innerHTML = '<div id="vexchord-diagram" style="display:flex;justify-content:center;padding:20px;"></div>';
            const chord = new Vexchord.Chord(root, { position: vexFrets });
            chord.addModifier("title", chordName);
            chord.draw("#vexchord-diagram");
        } else {
            container.innerHTML = '<div style="text-align:center;padding:20px;"><h4>' + chordName + '</h4><p>Frets: ' + frets.join(' - ') + '</p><p style="color:gray;font-size:0.875rem;">VexChord loading...</p></div>';
        }
    } catch (error) {
        console.error('Error showing chord diagram:', error);
        container.innerHTML = '<p>Error loading chord diagram</p>';
    }
}"""

# Replace
new_content = content.replace(old_func, new_func)

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('File updated successfully')

