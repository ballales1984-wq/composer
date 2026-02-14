#!/usr/bin/env python3
"""
Basic usage examples for the Music Theory Engine.

This file demonstrates the fundamental features of the music engine
for guitarists and musicians.
"""

from ..core import notes, scales, chords, arpeggios, progressions
from ..models import Note, Chord, Scale, Arpeggio, Progression


def demo_notes():
    """Demonstrate note operations."""
    print("🎵 Note System Demo")
    print("=" * 50)

    # Create notes
    c = Note('C')
    f_sharp = Note('F#')
    b_flat = Note('Bb')

    print(f"C note: {c}")
    print(f"F# note: {f_sharp}")
    print(f"Bb note: {b_flat}")
    print()

    # Note properties
    print(f"C semitone: {c.semitone}")
    print(f"F# enharmonic: {f_sharp.enharmonic_equivalent()}")
    print(f"Bb is flat: {b_flat.is_flat}")
    print()

    # Chromatic scale
    chromatic = notes.chromatic_scale('C', octaves=2)
    print(f"Chromatic scale: {[n.name for n in chromatic[:12]]}")
    print()

    # Circle of fifths
    fifths = notes.circle_of_fifths('C')
    print(f"Circle of fifths: {[n.name for n in fifths]}")
    print()


def demo_scales():
    """Demonstrate scale construction."""
    print("🎼 Scale Construction Demo")
    print("=" * 50)

    # Major scale
    c_major = scales.major('C')
    print(f"C Major: {[n.name for n in c_major.notes]}")

    # Minor scales
    a_minor = scales.minor('A', 'natural')
    print(f"A Natural Minor: {[n.name for n in a_minor.notes]}")

    a_harmonic = scales.minor('A', 'harmonic')
    print(f"A Harmonic Minor: {[n.name for n in a_harmonic.notes]}")

    # Modal scales
    d_dorian = scales.dorian('D')
    print(f"D Dorian: {[n.name for n in d_dorian.notes]}")

    e_phrygian = scales.phrygian('E')
    print(f"E Phrygian: {[n.name for n in e_phrygian.notes]}")

    # Pentatonic scales
    a_pent_minor = scales.pentatonic_minor('A')
    print(f"A Minor Pentatonic: {[n.name for n in a_pent_minor.notes]}")

    c_pent_major = scales.pentatonic_major('C')
    print(f"C Major Pentatonic: {[n.name for n in c_pent_major.notes]}")

    # Blues scales
    a_blues = scales.blues_minor('A')
    print(f"A Minor Blues: {[n.name for n in a_blues.notes]}")
    print()


def demo_chords():
    """Demonstrate chord construction."""
    print("🎸 Chord Construction Demo")
    print("=" * 50)

    # Triads
    c_major = chords.major('C')
    print(f"C Major: {[n.name for n in c_major.notes]}")

    d_minor = chords.minor('D')
    print(f"D Minor: {[n.name for n in d_minor.notes]}")

    e_dim = chords.diminished('E')
    print(f"E Diminished: {[n.name for n in e_dim.notes]}")

    # Seventh chords
    g_dom7 = chords.dominant7('G')
    print(f"G Dominant 7: {[n.name for n in g_dom7.notes]}")

    f_maj7 = chords.major7('F')
    print(f"F Major 7: {[n.name for n in f_maj7.notes]}")

    a_min7 = chords.minor7('A')
    print(f"A Minor 7: {[n.name for n in a_min7.notes]}")

    b_dim7 = chords.diminished7('B')
    print(f"B Diminished 7: {[n.name for n in b_dim7.notes]}")

    # Extended chords
    c_dom9 = chords.dom9('C')
    print(f"C Dominant 9: {[n.name for n in c_dom9.notes]}")

    d_min11 = chords.min11('D')
    print(f"D Minor 11: {[n.name for n in d_min11.notes]}")
    print()


def demo_arpeggios():
    """Demonstrate arpeggio construction."""
    print("🎶 Arpeggio Construction Demo")
    print("=" * 50)

    # Triad arpeggios
    c_maj_arp = arpeggios.major_triad('C', 'up')
    print(f"C Major triad arpeggio: {[n.name for n in c_maj_arp.notes]}")

    d_min_arp = arpeggios.minor_triad('D', 'up_down')
    print(f"D Minor triad arpeggio (up-down): {[n.name for n in d_min_arp.notes]}")

    # Seventh arpeggios
    g_dom7_arp = arpeggios.dominant7('G', 'up')
    print(f"G7 arpeggio: {[n.name for n in g_dom7_arp.notes]}")

    # Scale arpeggios
    a_minor_scale_arp = arpeggios.minor_scale('A', 'up')
    print(f"A Minor scale arpeggio: {[n.name for n in a_minor_scale_arp.notes[:8]]}...")

    c_blues_arp = arpeggios.blues_scale('C', 'down')
    print(f"C Blues scale arpeggio (down): {[n.name for n in c_blues_arp.notes[:8]]}...")
    print()


def demo_progressions():
    """Demonstrate progression analysis."""
    print("🎼 Progression Analysis Demo")
    print("=" * 50)

    # Create a simple progression
    progression_chords = ['C', 'F', 'G', 'C']  # I - IV - V - I
    prog = progressions.analyze(progression_chords)

    print(f"Progression: {prog}")
    print(f"All notes: {sorted([n.name for n in prog.all_notes])}")

    # Find compatible scales
    compatible_scales = progressions.find_scales(progression_chords)
    print("Compatible scales:")
    for scale in compatible_scales[:5]:  # Show first 5
        print(f"  - {scale}")

    # Scale suggestions for improvisation
    suggestions = progressions.suggest_scales(progression_chords, 3)
    print("\nScale suggestions for improvisation:")
    for scale in suggestions:
        print(f"  - {scale}")
    print()


def demo_advanced_features():
    """Demonstrate advanced features."""
    print("🚀 Advanced Features Demo")
    print("=" * 50)

    # Custom scale
    custom_intervals = [0, 2, 4, 6, 8]  # Whole tone scale
    custom_scale = scales.from_intervals('C', custom_intervals, 'Custom Whole Tone')
    print(f"Custom whole tone scale: {[n.name for n in custom_scale.notes]}")

    # Chord inversions
    c_maj = chords.major('C')
    c_maj_inv1 = c_maj.get_inversion(1)  # First inversion
    print(f"C Major first inversion: {c_maj_inv1}")

    # Transposition
    d_major = scales.major('D')
    d_to_f = d_major.transpose(3)  # Up a minor third
    print(f"D Major transposed up M3: {d_to_f}")

    # Complex progression
    complex_prog = ['Cmaj7', 'Dm7', 'G7', 'Cmaj7']
    analysis = progressions.analyze(complex_prog)
    print(f"Complex progression: {analysis}")
    print(f"Detected complexity: {progressions.get_progression_complexity(complex_prog)}")


def main():
    """Run all demos."""
    print("🎵 MUSIC THEORY ENGINE - DEMO")
    print("=" * 60)
    print()

    demo_notes()
    demo_scales()
    demo_chords()
    demo_arpeggios()
    demo_progressions()
    demo_advanced_features()

    print("✅ Demo completed!")
    print("\n💡 Tip: Check the documentation for more advanced features!")


if __name__ == "__main__":
    main()
