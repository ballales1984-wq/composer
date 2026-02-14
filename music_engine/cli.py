"""
Command Line Interface for Music Theory Engine.

This module provides a CLI for interacting with the music theory engine
directly from the terminal. It allows users to:
- Build and analyze chords
- Explore scales
- Work with progressions
- Transpose notes and chords
- Analyze harmonic content

Usage:
    music-engine chord Cmaj7
    music-engine scale C major
    music-engine analyze "C F G C"
    music-engine transpose C 5

Author: AI Music Engineer
"""

import sys
import os
from typing import Optional, List

# Ensure the package is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Import core modules
from music_engine.models.chord import Chord, CHORD_INTERVALS, CHORD_NAMES
from music_engine.models.scale import Scale, SCALE_INTERVALS, SCALE_NAMES
from music_engine.models.note import Note
from music_engine.models.progression import Progression

console = Console()


# ==================== Version ====================

@click.group()
@click.option('--version', is_flag=True, help='Show version information')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def main(ctx: click.Context, version: bool, verbose: bool) -> None:
    """
    Music Theory Engine - A comprehensive music theory analysis engine.
    
    Use this CLI to build chords, explore scales, analyze progressions,
    and more - all from the command line.
    """
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    
    if version:
        console.print("[bold blue]Music Theory Engine[/bold blue] v1.0.0")
        console.print("A comprehensive music theory analysis engine")
        console.print("https://github.com/yourusername/music-theory-engine")
        sys.exit(0)


# ==================== Chord Commands ====================

@main.group()
def chord() -> None:
    """Work with musical chords."""
    pass


@chord.command('show')
@click.argument('root')
@click.argument('quality', default='maj')
@click.option('--inversion', '-i', type=int, default=0, help='Show specific inversion (0-3)')
@click.option('--voicing', is_flag=True, help='Show guitar-friendly voicing')
def chord_show(root: str, quality: str, inversion: int, voicing: bool) -> None:
    """
    Show chord information.
    
    ROOT: Root note (e.g., C, D, Eb, F#)
    QUALITY: Chord quality (e.g., maj, min, 7, maj7, dim, aug)
    
    Examples:
        music-engine chord show C maj
        music-engineb chord show B 7
        music-engine chord show F# min7
    """
    try:
        c = Chord(root, quality)
        
        if inversion > 0:
            c = c.get_inversion(inversion)
        
        # Display chord information
        console.print(f"\n[bold cyan]Chord:[/bold cyan] {c.name}")
        console.print(f"[bold cyan]Quality:[/bold cyan] {CHORD_NAMES.get(quality, quality)}")
        
        # Notes
        notes_table = Table(title="Notes", show_header=True)
        notes_table.add_column("Note", style="cyan")
        notes_table.add_column("Semitone", style="green")
        
        for note in c.notes:
            notes_table.add_row(note.name, str(note.semitone))
        
        console.print(notes_table)
        
        # Intervals
        intervals_table = Table(title="Intervals (semitones)", show_header=True)
        intervals_table.add_column("Position", style="cyan")
        intervals_table.add_column("Interval", style="green")
        
        for i, interval in enumerate(c.intervals):
            intervals_table.add_row(str(i + 1), str(interval))
        
        console.print(intervals_table)
        
        # Voicing info
        if voicing:
            guitar_voicing = c.get_voicing(octave=4, spread=True)
            voicing_table = Table(title="Guitar Voicing (EADGBE)", show_header=True)
            voicing_table.add_column("String", style="cyan")
            voicing_table.add_column("Note", style="green")
            voicing_table.add_column("Octave", style="yellow")
            
            strings = ["E (low)", "A", "D", "G", "B", "E (high)"]
            for i, (note, octave) in enumerate(guitar_voicing[:6]):
                if i < len(strings):
                    voicing_table.add_row(strings[i], note.name, str(octave))
            
            console.print(voicing_table)
        
        # Inversions
        if inversion == 0 and len(c.notes) > 1:
            inversions_table = Table(title="Available Inversions", show_header=True)
            inversions_table.add_column("Position", style="cyan")
            inversions_table.add_column("Notes", style="green")
            
            for inv in c.get_all_inversions():
                notes_str = " - ".join([n.name for n in inv.notes])
                bass = " (bass)" if inv.is_inverted else ""
                inversions_table.add_row(str(inv.get_all_inversions().index(inv)), notes_str + bass)
            
            console.print(inversions_table)
        
        console.print()
        
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        console.print(f"\nValid chord qualities: {', '.join(sorted(CHORD_INTERVALS.keys()))}")
        sys.exit(1)


@chord.command('list')
@click.option('--type', 'chord_type', type=click.Choice(['triads', 'seventh', 'extended', 'all']), default='all')
def chord_list(chord_type: str) -> None:
    """
    List all available chord types.
    
    TYPE: Type of chords to list (triads, seventh, extended, all)
    """
    table = Table(title=f"Available Chord Types ({chord_type})", show_header=True)
    table.add_column("Quality", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Intervals", style="yellow")
    
    quality_map = {
        'triads': ['maj', 'min', 'dim', 'aug', 'sus2', 'sus4', '5'],
        'seventh': ['maj7', 'dom7', 'min7', 'dim7', 'min7b5', 'maj7b5', '7sus4', '7b9'],
        'extended': ['9', 'min9', 'maj9', '11', 'min11', 'maj11', '13', 'min13', 'maj13'],
    }
    
    if chord_type == 'all':
        qualities = sorted(CHORD_INTERVALS.keys())
    else:
        qualities = quality_map.get(chord_type, [])
    
    for q in qualities:
        if q in CHORD_INTERVALS:
            intervals = " - ".join(map(str, CHORD_INTERVALS[q]))
            table.add_row(q, CHORD_NAMES.get(q, q.title()), intervals)
    
    console.print(table)


@chord.command('compare')
@click.argument('root')
@click.argument('qualities', nargs=-1, required=True)
def chord_compare(root: str, qualities: tuple) -> None:
    """
    Compare multiple chord qualities for the same root.
    
    ROOT: Root note
    QUALITIES: List of chord qualities to compare
    
    Examples:
        music-engine chord compare C maj min dim aug
    """
    table = Table(title=f"Chord Comparison: {root}", show_header=True)
    table.add_column("Quality", style="cyan")
    table.add_column("Notes", style="green")
    table.add_column("Intervals", style="yellow")
    
    for quality in qualities:
        try:
            c = Chord(root, quality)
            notes = " - ".join([n.name for n in c.notes])
            intervals = " - ".join(map(str, c.intervals))
            table.add_row(quality, notes, intervals)
        except ValueError as e:
            table.add_row(quality, f"[red]Error: {e}[/red]", "")
    
    console.print(table)


# ==================== Scale Commands ====================

@main.group()
def scale() -> None:
    """Work with musical scales."""
    pass


@scale.command('show')
@click.argument('root')
@click.argument('scale_type', default='major')
@click.option('--octaves', '-o', type=int, default=1, help='Number of octaves')
@click.option('--degrees', is_flag=True, help='Show scale degrees')
def scale_show(root: str, scale_type: str, octaves: int, degrees: bool) -> None:
    """
    Show scale information.
    
    ROOT: Root note (e.g., C, D, Eb, F#)
    SCALE_TYPE: Type of scale (major, minor_natural, dorian, etc.)
    
    Examples:
        music-engine scale show C major
        music-engine scale show A minor_natural
        music-engine scale show D dorian --octaves 2
    """
    try:
        s = Scale(root, scale_type, octaves)
        
        # Display scale information
        console.print(f"\n[bold cyan]Scale:[/bold cyan] {s.name}")
        console.print(f"[bold cyan]Type:[/bold cyan] {SCALE_NAMES.get(scale_type, scale_type)}")
        
        # Notes
        notes_table = Table(title="Notes", show_header=True)
        notes_table.add_column("Degree", style="cyan")
        notes_table.add_column("Note", style="green")
        notes_table.add_column("Semitone", style="yellow")
        
        for i, note in enumerate(s.notes):
            degree = str(i + 1) if not degrees else f"{_get_degree_name(i + 1)} ({i + 1})"
            notes_table.add_row(degree, note.name, str(note.semitone))
        
        console.print(notes_table)
        
        # Intervals
        intervals_table = Table(title="Intervals (semitones from root)", show_header=True)
        intervals_table.add_column("Position", style="cyan")
        intervals_table.add_column("Interval", style="green")
        
        for i, interval in enumerate(s.intervals):
            intervals_table.add_row(str(i + 1), str(interval))
        
        console.print(intervals_table)
        
        # Diatonic chords
        chords_table = Table(title=f"Diatonic Chords (in {root} {scale_type})", show_header=True)
        chords_table.add_column("Degree", style="cyan")
        chords_table.add_column("Chord", style="green")
        
        try:
            for degree in range(1, 8):
                triad = s.get_triad(degree)
                chords_table.add_row(str(degree), triad.name)
            console.print(chords_table)
        except Exception:
            pass  # Skip if diatonic chords not available
        
        console.print()
        
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        console.print(f"\nValid scale types: {', '.join(sorted(SCALE_INTERVALS.keys()))}")
        sys.exit(1)


@scale.command('list')
@click.option('--type', 'scale_cat', type=click.Choice(['major', 'minor', 'modal', 'pentatonic', 'blues', 'other', 'all']), default='all')
def scale_list(scale_cat: str) -> None:
    """
    List all available scale types.
    
    TYPE: Category of scales to list
    """
    categories = {
        'major': ['major', 'ionian'],
        'minor': ['minor_natural', 'minor_harmonic', 'minor_melodic', 'aeolian'],
        'modal': ['dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian'],
        'pentatonic': ['pentatonic_major', 'pentatonic_minor', 'pentatonic_blues'],
        'blues': ['blues_major', 'blues_minor'],
        'other': ['whole_tone', 'chromatic', 'diminished', 'augmented'],
    }
    
    table = Table(title=f"Available Scale Types ({scale_cat})", show_header=True)
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Intervals", style="yellow")
    
    if scale_cat == 'all':
        types = sorted(SCALE_INTERVALS.keys())
    else:
        types = categories.get(scale_cat, [])
    
    for t in types:
        if t in SCALE_INTERVALS:
            intervals = " - ".join(map(str, SCALE_INTERVALS[t]))
            table.add_row(t, SCALE_NAMES.get(t, t.title()), intervals)
    
    console.print(table)


@scale.command('modes')
@click.argument('root')
@click.argument('scale_type', default='major')
def scale_modes(root: str, scale_type: str) -> None:
    """
    Show all modes of a scale.
    
    ROOT: Root note
    SCALE_TYPE: Base scale type
    
    Examples:
        music-engine scale modes C major
    """
    try:
        s = Scale(root, scale_type)
        
        table = Table(title=f"Modes of {root} {scale_type}", show_header=True)
        table.add_column("Mode", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Notes", style="yellow")
        
        mode_names = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
        
        for i in range(1, 8):
            try:
                mode = s.get_mode(i)
                notes = " - ".join([n.name for n in mode.notes[:7]])
                table.add_row(f"Mode {i}", mode_names[i-1], notes)
            except Exception:
                pass
        
        console.print(table)
        
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@scale.command('chords')
@click.argument('root')
@click.argument('scale_type', default='major')
def scale_chords(root: str, scale_type: str) -> None:
    """
    Show all diatonic chords in a scale.
    
    ROOT: Root note
    SCALE_TYPE: Scale type
    
    Examples:
        music-engine scale chords C major
    """
    try:
        s = Scale(root, scale_type)
        
        table = Table(title=f"Diatonic Chords in {root} {scale_type}", show_header=True)
        table.add_column("Degree", style="cyan")
        table.add_column("Roman", style="green")
        table.add_column("Quality", style="yellow")
        table.add_column("Notes", style="magenta")
        
        roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        
        for degree in range(1, 8):
            try:
                triad = s.get_triad(degree)
                quality = CHORD_NAMES.get(triad.quality, triad.quality)
                notes = " - ".join([n.name for n in triad.notes])
                roman = roman_numerals[degree - 1]
                if quality.lower() in ['minor', 'diminished']:
                    roman = roman.lower()
                    if 'dim' in quality.lower():
                        roman += "°"
                table.add_row(str(degree), roman, quality, notes)
            except Exception as e:
                table.add_row(str(degree), "?", str(e), "")
        
        console.print(table)
        
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


# ==================== Progression Commands ====================

@main.group()
def progression() -> None:
    """Work with chord progressions."""
    pass


@progression.command('analyze')
@click.argument('chords', nargs=-1, required=True)
@click.option('--key', '-k', help='Key for analysis (e.g., C, Am)')
def progression_analyze(chords: tuple, key: Optional[str]) -> None:
    """
    Analyze a chord progression.
    
    CHORDS: List of chords (e.g., C F G C)
    
    Examples:
        music-engine progression analyze C F G C
        music-engine progression analyze Am7 Dm7 G7 Cmaj7 --key Am
    """
    try:
        # Build progression from chord strings
        chord_list = []
        for c_str in chords:
            # Parse chord string (e.g., "Cmaj7", "Dm", "G7")
            import re
            pattern = r'^([A-G])([#b]?)(.*)$'
            match = re.match(pattern, c_str.strip(), re.IGNORECASE)
            
            if not match:
                console.print(f"[red]Invalid chord: {c_str}[/red]")
                continue
            
            root = match.group(1).upper() + (match.group(2).lower() if match.group(2) else '')
            quality = match.group(3).lower() or 'maj'
            
            # Map quality
            quality_map = {'': 'maj', 'm': 'min', 'maj': 'maj', '7': 'dom7',
                         'm7': 'min7', 'maj7': 'maj7', 'dim': 'dim'}
            quality = quality_map.get(quality, quality)
            
            chord_list.append(Chord(root, quality))
        
        if not chord_list:
            console.print("[red]No valid chords provided[/red]")
            return
        
        # Display progression
        console.print(f"\n[bold cyan]Progression:[/bold cyan] {' - '.join([c.name for c in chord_list])}")
        
        if key:
            console.print(f"[bold cyan]Key:[/bold cyan] {key}")
            
            # Show roman numeral analysis
            root_note = Note(key.strip()[0])
            roman_table = Table(title=f"Roman Numeral Analysis (in {key})", show_header=True)
            roman_table.add_column("Chord", style="cyan")
            roman_table.add_column("Degree", style="green")
            roman_table.add_column("Function", style="yellow")
            
            functions = {1: 'Tonic', 2: 'Supertonic', 3: 'Mediant', 4: 'Subdominant',
                        5: 'Dominant', 6: 'Submediant', 7: 'Leading Tone'}
            
            for i, c in enumerate(chord_list):
                degree = (i % 7) + 1
                func = functions.get(degree, '?')
                roman = str(degree)
                if c.quality == 'min':
                    roman = roman.lower()
                elif c.quality == 'dim':
                    roman = roman.lower() + "°"
                elif c.quality == 'dom7':
                    roman += "7"
                roman_table.add_row(c.name, roman, func)
            
            console.print(roman_table)
        
        # Find compatible scales
        console.print(f"\n[bold cyan]Compatible Scales:[/bold cyan]")
        
        # Common compatible scales
        compatible = []
        root = chord_list[0].root.note_name
        
        for scale_type in ['major', 'minor_natural', 'dorian', 'mixolydian']:
            try:
                s = Scale(root, scale_type)
                compatible.append(f"{root} {SCALE_NAMES.get(scale_type, scale_type)}")
            except:
                pass
        
        for sc in compatible:
            console.print(f"  • {sc}")
        
        console.print()
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        import traceback
        if '--verbose' in sys.argv or '-v' in sys.argv:
            traceback.print_exc()
        sys.exit(1)


@progression.command('common')
@click.argument('key')
@click.option('--type', 'prog_type', type=click.Choice(['jazz', 'pop', 'classical', 'blues']), default='pop')
def progression_common(key: str, prog_type: str) -> None:
    """
    Show common progressions in a key.
    
    KEY: Root key (e.g., C, Am)
    TYPE: Type of progressions
    
    Examples:
        music-engine progression common C jazz
        music-engine progression common Am pop
    """
    progressions = {
        'jazz': [
            ('ii-V-I', 'Dm7 - G7 - Cmaj7'),
            ('I-vi-ii-V', 'Cmaj7 - Am7 - Dm7 - G7'),
            ('iii-VI-ii-V', 'Em7 - Am7 - Dm7 - G7'),
            ('vi-V-I', 'Am7 - Dm7 - G7 - Cmaj7'),
        ],
        'pop': [
            ('I-IV-V-I', 'C - F - G - C'),
            ('I-V-vi-IV', 'C - G - Am - F'),
            ('I-vi-IV-V', 'C - Am - F - G'),
            ('vi-IV-I-V', 'Am - F - C - G'),
        ],
        'classical': [
            ('I-IV-V-I', 'C - F - G - C'),
            ('i-iv-v-i', 'Am - Dm - Em - Am'),
            ('I-V-vi-IV', 'C - G - Am - F'),
            ('I-vi-IV-V', 'C - Am - F - G'),
        ],
        'blues': [
            ('12-bar blues', 'I7 - IV7 - I7 - V7 - IV7 - I7 - V7 - IV7 - I7'),
        ],
    }
    
    table = Table(title=f"Common Progressions in {key}", show_header=True)
    table.add_column("Name", style="cyan")
    table.add_column("Progression", style="green")
    table.add_column("Roman", style="yellow")
    
    name_map = {
        'jazz': {'I': key.upper(), 'ii': f'{key.lower()}m7', 'iii': f'{chr(ord(key[0])+2)}m7',
                'IV': f'{chr(ord(key[0])+3)}', 'V': f'{chr(ord(key[0])+4)}7',
                'VI': f'{chr(ord(key[0])+5)}m7', 'vi': f'{key.lower()}m7'},
        'pop': {'I': key.upper(), 'ii': f'{key.lower()}m', 'iii': f'{chr(ord(key[0])+2)}m',
               'IV': f'{chr(ord(key[0])+3)}', 'V': f'{chr(ord(key[0])+4)}',
               'vi': f'{key.lower()}m', 'VI': f'{key.upper()}m'}
    }
    
    for name, prog in progressions.get(prog_type, []):
        # Simple roman mapping
        if 'jazz' in prog_type:
            roman = name
        else:
            roman = name.replace('I', key.upper()).replace('i', key.lower())
        
        table.add_row(name, prog, roman)
    
    console.print(table)


# ==================== Utility Commands ====================

@main.group()
def util() -> None:
    """Utility functions."""
    pass


@util.command('transpose')
@click.argument('note')
@click.argument('semitones', type=int)
def util_transpose(note: str, semitones: int) -> None:
    """
    Transpose a note by a number of semitones.
    
    NOTE: Note to transpose (e.g., C, Eb, F#)
    SEMITONES: Number of semitones (positive = up, negative = down)
    
    Examples:
        music-engine util transpose C 5     # C -> F#
        music-engine util transpose G -2    # G -> F
        music-engine util transpose A 12    # A -> A (octave)
    """
    try:
        n = Note(note)
        transposed = n.transpose(semitones)
        
        console.print(f"\n[bold cyan]Original:[/bold cyan] {n.name}")
        console.print(f"[bold cyan]Transposed:[/bold cyan] {transposed.name}")
        console.print(f"[bold cyan]Interval:[/bold cyan] {semitones} semitones")
        
        # Show interval name
        intervals = ['Unison', 'Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd',
                    'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th',
                    'Minor 7th', 'Major 7th', 'Octave']
        
        abs_semitones = abs(semitones) % 12
        direction = "up" if semitones > 0 else "down" if semitones < 0 else "same"
        
        console.print(f"[bold cyan]Interval Name:[/bold cyan] {intervals[abs_semitones]} {direction}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@util.command('intervals')
@click.argument('note1')
@click.argument('note2')
def util_intervals(note1: str, note2: str) -> None:
    """
    Calculate the interval between two notes.
    
    NOTE1: First note
    NOTE2: Second note
    
    Examples:
        music-engine util intervals C E      # Major 3rd
        music-engine util intervals C Gb     # Tritone
    """
    try:
        n1 = Note(note1)
        n2 = Note(note2)
        
        # Calculate interval
        diff = (n2.semitone - n1.semitone) % 12
        
        intervals = [
            ('Unison', 0),
            ('Minor 2nd', 1),
            ('Major 2nd', 2),
            ('Minor 3rd', 3),
            ('Major 3rd', 4),
            ('Perfect 4th', 5),
            ('Tritone', 6),
            ('Perfect 5th', 7),
            ('Minor 6th', 8),
            ('Major 6th', 9),
            ('Minor 7th', 10),
            ('Major 7th', 11),
            ('Octave', 12),
        ]
        
        interval_name = "Unknown"
        for name, sems in intervals:
            if sems == diff:
                interval_name = name
                break
        
        console.print(f"\n[bold cyan]Note 1:[/bold cyan] {n1.name} (semitone: {n1.semitone})")
        console.print(f"[bold cyan]Note 2:[/bold cyan] {n2.name} (semitone: {n2.semitone})")
        console.print(f"[bold cyan]Interval:[/bold cyan] {interval_name} ({diff} semitones)")
        
        # Show inverse
        inverse_diff = (n1.semitone - n2.semitone) % 12
        inverse_name = intervals[inverse_diff][0] if inverse_diff < len(intervals) else "Unknown"
        console.print(f"[bold cyan]Inverse:[/bold cyan] {inverse_name}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@util.command('circle')
@click.option('--key', default='C', help='Key for circle of fifths')
def util_circle(key: str) -> None:
    """
    Display the circle of fifths.
    
    KEY: Starting key (default: C)
    """
    # Circle of fifths keys
    keys_sharp = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    keys_flat = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    
    console.print(f"\n[bold cyan]Circle of Fifths (Key: {key})[/bold cyan]\n")
    
    table = Table(show_header=False)
    table.add_column("Key", style="cyan")
    table.add_column("Relation", style="green")
    table.add_column("Relative Minor", style="yellow")
    
    for i, k in enumerate(keys_sharp):
        relation = _get_relation(i)
        rel_minor = _get_relative_minor(k)
        table.add_row(k, relation, rel_minor)
    
    console.print(table)


# ==================== Helper Functions ====================

def _get_degree_name(degree: int) -> str:
    """Get the name of a scale degree."""
    names = ['Tonic', 'Supertonic', 'Mediant', 'Subdominant', 
             'Dominant', 'Submediant', 'Leading Tone']
    return names[degree - 1] if 1 <= degree <= 7 else str(degree)


def _get_relation(index: int) -> str:
    """Get the relationship name for circle of fifths position."""
    relations = [
        'Perfect Unison', 'Perfect Fifth', 'Major Second', 'Major Sixth',
        'Major Third', 'Major Seventh', 'Tritone', 'Minor Fourth'
    ]
    return relations[index % 8]


def _get_relative_minor(key: str) -> str:
    """Get the relative minor of a major key."""
    # Simple relative minor calculation (3 semitones down)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    try:
        idx = notes.index(key.replace('b', '#').replace('Bb', 'A#').replace('Eb', 'D#').replace('Ab', 'G#').replace('Db', 'C#').replace('Gb', 'F#'))
        minor_idx = (idx - 3) % 12
        return notes[minor_idx] + 'm'
    except:
        return '?'


# ==================== Entry Point ====================

if __name__ == '__main__':
    main(obj={})

