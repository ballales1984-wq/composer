# Leggi il file
with open('web_app/templates/chords.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Trova e sostituisci la funzione vuota
old_code = '''async function mostraAccordo(root, quality) {
}'''

new_code = '''async function mostraAccordo(root, quality) {

    const chordName = root + quality;
    const container = document.getElementById("chord-diagrams-result");
    container.innerHTML = "<p>Caricamento...</p>";

    try {

        const data = await fetchVoicing(chordName);

        if (!data || !data.voicing || data.voicing.length === 0) {
            container.innerHTML = "<p>Nessun voicing trovato</p>";
            return;
        }

        // Prendi il primo voicing
        const voicing = data.voicing[0];
        
        // Costruisci i fret dal voicing
        const frets = [];
        for (let i = 0; i < 6; i++) {
            if (voicing.frets && voicing.frets[i] !== undefined) {
                frets.push(voicing.frets[i]);
            } else {
                frets.push(-1);
            }
        }

        // Converti nel formato corretto per VexChord
        const vexFrets = frets.map(f => {
            if (f === -1) return 'x';
            if (f === 0) return '0';
            return String(f);
        });

        if (typeof Vexchord !== 'undefined') {

            container.innerHTML = \`
                <div id="vexchord-diagram" 
                     style="display:flex;justify-content:center;padding:20px;">
                </div>
            \`;

            new Vexchord('#vexchord-diagram', {
                chord: vexFrets,
                position: 1,
                title: chordName,
                tuning: ['E','A','D','G','B','E']
            });

        } else {
            container.innerHTML = "<p>Errore: VexChord non caricato</p>";
        }

    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Errore nel caricamento accordo</p>";
    }
}'''

# Applica la sostituzione
if old_code in content:
    content = content.replace(old_code, new_code)
    with open('web_app/templates/chords.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fix applicato!")
else:
    print("Codice non trovato")
