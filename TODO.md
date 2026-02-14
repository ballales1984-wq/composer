# TODO - Integrazione music21 e mingus

## Fase 1: Aggiornamento Dipendenze
- [x] Aggiornare requirements.txt con music21 e mingus

## Fase 2: Creazione Struttura Integrazione
- [x] Creare directory music_engine/integrations/
- [x] Creare music_engine/integrations/__init__.py
- [x] Creare music_engine/integrations/music21_adapter.py
- [x] Creare music_engine/integrations/mingus_adapter.py
- [x] Creare music_engine/integrations/factory.py

## Fase 3: Aggiornamento Modelli
- [x] Aggiungere metodi to_music21() e from_music21() a Note
- [x] Aggiungere metodi to_mingus() e from_mingus() a Note
- [x] Aggiungere metodi di conversione a Chord
- [x] Aggiungere metodi di conversione a Scale
- [x] Aggiungere metodi di conversione a Progression

## Fase 4: Aggiornamento __init__.py
- [x] Aggiornare models/__init__.py
- [x] Aggiornare music_engine/__init__.py

## Fase 5: Test
- [ ] Verificare installazione dipendenze
- [ ] Testare conversione Note
- [ ] Testare conversione Chord
- [ ] Testare conversione Scale
- [ ] Testare conversione Progression

