# TODO - Scale + Chord Combined Display on Fretboard

## Obiettivo
Visualizzare simultaneamente le note della scala E dell'accordo sul manico della chitarra.

## Passi di Implementazione

- [x] 1. Modificare fretboard.js - aggiungere metodo per visualizzazione combinata
- [x] 2. Modificare fretboard.html - aggiungere opzione "Scale + Chord" 
- [ ] 3. Modificare scales.html - aggiungere pulsante "View on Fretboard"
- [ ] 4. Modificare chords.html - aggiungere pulsante "View on Fretboard"
- [x] 5. Testare navigazione e visualizzazione

## Dettagli Tecnici

### Colori:
- Scala: Blu (#6366f1)
- Accordo: Verde (#10b981)  
- Note in comune: Oro (#fbbf24)

### Parametri URL:
- /fretboard?root=C&scale=major&chord=G&chord_quality=dom7
- /fretboard?mode=scale_chord&root=C&scale=major&chord_root=G&chord_quality=dom7

