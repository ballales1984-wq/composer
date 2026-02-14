# TODO - Music Composer Project

## Correzioni effettuate (2025-01-26)
- [x] Corretto parsing accordi in `ChordBuilder.parse_chord_string()` - ora gestisce correttamente "Am", "Cm", etc.
- [x] Corretto nome accordi in `Chord.name` - ora usa `note_name` invece di `name` per evitare "C4Major"
- [x] Testato e verificato Progression con chord strings "C", "G", "Am", "F"
- [x] Testato tutti gli API endpoints del web app

## Fase 1: Core Modules - [COMPLETED]
- [x] Interval class - music_engine/core/intervals.py
- [x] HarmonyEngine class - music_engine/core/harmony.py
  - [x] Tonal compatibility
  - [x] Modal compatibility
  - [x] find_compatible_scales()
  - [x] find_compatible_chords()

## Fase 2: API Endpoints - [COMPLETED]
- [x] /api/analyzer - Unified endpoint
- [x] /api/analyzer/chord - Chord analysis
- [x] /api/analyzer/scale - Scale analysis
- [x] /api/analyzer/compatibility - Check compatibility

## Fase 3: UI Templates - [COMPLETED]
- [x] analyzer.html - Unified analyzer page
- [x] Index page updated with new feature
- [x] Fretboard visualization

## Fase 4: Orchestrator Module - [COMPLETED] ✅
- [x] controller.py - InputController, OutputFormatter, Coordinator
- [x] solver.py - ScaleSolver, ChordSolver, ConflictResolver
- [x] expansion.py - ProgressionExpander, ContinuationGenerator, SubstitutionHandler
- [x] genre_rules.py - GenreDetector, JazzRules, PopRules, RockRules, BluesRules
- [x] API endpoints - /api/orchestrator/*

## Fase 5: Orchestrator API - [COMPLETED] ✅
- [x] /api/orchestrator/suggest - Get suggestions
- [x] /api/orchestrator/expand - Expand progressions
- [x] /api/orchestrator/next-chords - Get next chord suggestions
- [x] /api/orchestrator/compatible-scales - Get compatible scales
- [x] /api/orchestrator/genre/detect - Detect genre
- [x] /api/orchestrator/genre/progressions - Get genre progressions
- [x] /api/orchestrator/substitute/tritone - Get tritone substitute
- [x] /api/orchestrator/continuation - Get continuation suggestions

## Prossimi passi - Sviluppo Step-by-Step
1. ~~Real-time analysis - MIDI/keyboard input~~ ✅ COMPLETATO
2. **Progression generation** - Generate listenable progressions (Phase 3) ✅ COMPLETATO
   - [x] `/api/orchestrator/expand` - Expand short progressions
   - [x] `/api/orchestrator/continuation` - Get continuation suggestions
   - [x] Frontend integration in progressions.html
3. **Visualization enhancements** - Keyboard, diagrams, tablature (Phase 4)
4. **Exercises & Metronome** - Practice tools (Phase 5)
5. **IA Integration** - Ollama integration (Phase 6)
6. **Genre Templates** - Jazz, Pop, Rock templates (Phase 7)

---

*Ultimo aggiornamento: 2026-02-14*

## Real-time Analysis - COMPLETATO ✅
- [x] `/api/analyzer/realtime/analyze` - Analisi completa in tempo reale
- [x] `/api/analyzer/realtime/chord-detect` - Rilevamento accordi
- [x] `/api/analyzer/realtime/scale-suggest` - Suggerimento scale
- [x] Pagina `/realtime` con tastiera virtuale
- [x] Supporto Web MIDI API per controller esterni
- [x] Tastiera virtuale 2 ottave (C3-C5)
- [x] Keyboard shortcuts (a-k keys)
- [x] Algoritmo rilevamento accordi con inversioni
- [x] Nota.from_midi() e proprietà midi, frequency

