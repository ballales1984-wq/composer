"""
Chord Shapes Database - Real Guitar Chord Shapes
CAGED-based chord shapes with correct string ordering
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ChordShape:
    """Represents a guitar chord shape."""
    name: str
    quality: str
    frets: List[Optional[int]]  # [string_6, string_5, string_4, string_3, string_2, string_1]
    fingers: List[Optional[int]]  # 0=open/X, 1=index, 2=middle, 3=ring, 4=pinky
    base_fret: int = 1
    is_barre: bool = False
    root_string: int = 6
    position_name: str = ""


# Standard guitar tuning (low to high): E2 A2 D3 G3 B3 E4
# String indices: [0]=Low E(6), [1]=A(5), [2]=D(4), [3]=G(3), [4]=B(2), [5]=High E(1)

OPEN_CHORDS = {
    # Major chords - OPEN POSITIONS
    'C_maj': ChordShape("Open C", "maj", [None, 3, 2, 0, 1, 0], [None, 3, 2, 0, 1, 0], position_name="Open C"),
    'D_maj': ChordShape("Open D", "maj", [None, None, 0, 2, 3, 2], [None, None, 0, 1, 3, 2], position_name="Open D"),
    'E_maj': ChordShape("Open E", "maj", [0, 2, 2, 1, 0, 0], [0, 2, 3, 1, 0, 0], position_name="Open E"),
    'G_maj': ChordShape("Open G", "maj", [3, 2, 0, 0, 0, 3], [2, 1, 0, 0, 0, 3], position_name="Open G"),
    'A_maj': ChordShape("Open A", "maj", [None, 0, 2, 2, 2, 0], [None, 0, 1, 2, 3, 0], position_name="Open A"),
    'F_maj': ChordShape("F Major", "maj", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], is_barre=True, base_fret=1, position_name="Barre F"),
    
    # Minor chords - OPEN
    'C_min': ChordShape("C Minor", "min", [None, 3, 5, 5, 4, 3], [None, 1, 3, 4, 2, 1], position_name="C Minor"),
    'D_min': ChordShape("D Minor", "min", [None, None, 0, 2, 3, 1], [None, None, 0, 2, 3, 1], position_name="D Minor"),
    'E_min': ChordShape("E Minor", "min", [0, 2, 2, 0, 0, 0], [0, 2, 3, 0, 0, 0], position_name="E Minor"),
    'A_min': ChordShape("A Minor", "min", [None, 0, 2, 2, 1, 0], [None, 0, 2, 3, 1, 0], position_name="A Minor"),
    
    # Seventh chords - OPEN
    'C_dom7': ChordShape("C7", "dom7", [None, 3, 2, 3, 1, 0], [None, 3, 2, 4, 1, 0], position_name="C7"),
    'D_dom7': ChordShape("D7", "dom7", [None, None, 0, 2, 1, 2], [None, None, 0, 2, 1, 3], position_name="D7"),
    'E_dom7': ChordShape("E7", "dom7", [0, 2, 0, 1, 0, 0], [0, 2, 0, 1, 0, 0], position_name="E7"),
    'G_dom7': ChordShape("G7", "dom7", [3, 1, 0, 0, 0, 1], [3, 1, 0, 0, 0, 2], position_name="G7"),
    'A_dom7': ChordShape("A7", "dom7", [None, 0, 2, 0, 2, 0], [None, 0, 1, 0, 2, 0], position_name="A7"),
    
    # Major 7th - OPEN
    'C_maj7': ChordShape("Cmaj7", "maj7", [None, 3, 2, 0, 0, 0], [None, 3, 2, 0, 0, 0], position_name="Cmaj7"),
    'A_maj7': ChordShape("Amaj7", "maj7", [None, 0, 2, 1, 2, 0], [None, 0, 2, 1, 3, 0], position_name="Amaj7"),
    
    # Minor 7th - OPEN
    'C_min7': ChordShape("Cmin7", "min7", [None, 3, 5, 3, 4, 3], [None, 1, 3, 1, 4, 2], position_name="Cmin7"),
    'A_min7': ChordShape("Amin7", "min7", [None, 0, 2, 0, 1, 0], [None, 0, 2, 0, 1, 0], position_name="Amin7"),
}

BARRE_CHORDS = {
    # E-shape barre (root on string 6)
    'E_maj_barre': ChordShape("Barre E-Shape Major", "maj", [None, 3, 5, 5, 5, 3], [None, 1, 3, 4, 4, 1], is_barre=True, base_fret=1, root_string=6, position_name="Barre E-Shape"),
    'E_min_barre': ChordShape("Barre E-Shape Minor", "min", [None, 3, 5, 5, 4, 3], [None, 1, 3, 4, 2, 1], is_barre=True, base_fret=1, root_string=6, position_name="Barre E-Shape"),
    'E_dom7_barre': ChordShape("Barre E-Shape 7th", "dom7", [None, 3, 3, 3, 3, 3], [None, 1, 1, 1, 1, 1], is_barre=True, base_fret=1, root_string=6, position_name="Barre E-Shape"),
    'E_maj7_barre': ChordShape("Barre E-Shape Maj7", "maj7", [None, 3, 5, 4, 5, 3], [None, 1, 3, 2, 4, 1], is_barre=True, base_fret=1, root_string=6, position_name="Barre E-Shape"),
    'E_min7_barre': ChordShape("Barre E-Shape Min7", "min7", [None, 3, 5, 3, 4, 3], [None, 1, 3, 1, 2, 1], is_barre=True, base_fret=1, root_string=6, position_name="Barre E-Shape"),
    
    # A-shape barre (root on string 5)
    'A_maj_barre': ChordShape("Barre A-Shape Major", "maj", [None, 5, 7, 7, 7, 5], [None, 1, 3, 4, 4, 1], is_barre=True, base_fret=5, root_string=5, position_name="Barre A-Shape"),
    'A_min_barre': ChordShape("Barre A-Shape Minor", "min", [None, 5, 7, 7, 6, 5], [None, 1, 3, 4, 2, 1], is_barre=True, base_fret=5, root_string=5, position_name="Barre A-Shape"),
    'A_dom7_barre': ChordShape("Barre A-Shape 7th", "dom7", [None, 5, 7, 5, 7, 5], [None, 1, 3, 1, 4, 1], is_barre=True, base_fret=5, root_string=5, position_name="Barre A-Shape"),
    'A_maj7_barre': ChordShape("Barre A-Shape Maj7", "maj7", [None, 5, 7, 6, 7, 5], [None, 1, 3, 2, 4, 1], is_barre=True, base_fret=5, root_string=5, position_name="Barre A-Shape"),
    'A_min7_barre': ChordShape("Barre A-Shape Min7", "min7", [None, 5, 7, 5, 6, 5], [None, 1, 3, 1, 2, 1], is_barre=True, base_fret=5, root_string=5, position_name="Barre A-Shape"),
}

TRIAD_SHAPES = {
    'maj_root_E': ChordShape("Major Triad", "maj", [None, None, 0, 2, 3, 2], [None, None, 0, 1, 3, 2], root_string=4, position_name="Triad Root"),
    'maj_root_A': ChordShape("Major Triad", "maj", [None, 0, 2, 2, 1, 0], [None, 0, 2, 3, 1, 0], root_string=5, position_name="Triad Root"),
    'maj_root_D': ChordShape("Major Triad", "maj", [None, None, 0, 2, 3, 0], [None, None, 0, 1, 3, 0], root_string=4, position_name="Triad Root"),
    'maj_1st': ChordShape("Major Triad 1st", "maj", [None, 0, 0, 2, 3, 2], [None, 0, 0, 1, 3, 2], position_name="Triad 1st Inv"),
    'maj_2nd': ChordShape("Major Triad 2nd", "maj", [0, 0, 2, 2, 1, 0], [0, 0, 2, 3, 1, 0], position_name="Triad 2nd Inv"),
    'min_root_E': ChordShape("Minor Triad", "min", [None, None, 0, 2, 3, 1], [None, None, 0, 2, 3, 1], root_string=4, position_name="Minor Triad"),
    'min_root_A': ChordShape("Minor Triad", "min", [None, 0, 2, 2, 1, 0], [None, 0, 2, 3, 1, 0], root_string=5, position_name="Minor Triad"),
    'min_1st': ChordShape("Minor Triad 1st", "min", [None, 0, 0, 2, 3, 1], [None, 0, 0, 2, 3, 1], position_name="Minor 1st Inv"),
    'min_2nd': ChordShape("Minor Triad 2nd", "min", [0, 0, 2, 2, 1, 1], [0, 0, 2, 3, 1, 1], position_name="Minor 2nd Inv"),
    'dim_root': ChordShape("Diminished", "dim", [None, None, 0, 1, 3, 1], [None, None, 0, 1, 3, 2], position_name="Diminished"),
    'aug_root': ChordShape("Augmented", "aug", [None, None, 0, 3, 3, 1], [None, None, 0, 2, 3, 1], position_name="Augmented"),
}

SEVENTH_CHORDS = {
    'dom7_root': ChordShape("Dom7 Root", "dom7", [None, 3, 2, 3, 1, 0], [None, 3, 2, 4, 1, 0], position_name="Dom7 Root"),
    'dom7_1st': ChordShape("Dom7 1st", "dom7", [None, 3, 1, 3, 2, 0], [None, 2, 1, 4, 3, 0], position_name="Dom7 1st Inv"),
    'dom7_2nd': ChordShape("Dom7 2nd", "dom7", [None, 2, 1, 2, 1, 2], [None, 2, 1, 3, 1, 4], position_name="Dom7 2nd Inv"),
    'maj7_root': ChordShape("Maj7 Root", "maj7", [None, 3, 2, 0, 0, 0], [None, 3, 2, 0, 0, 0], position_name="Maj7 Root"),
    'maj7_1st': ChordShape("Maj7 1st", "maj7", [None, 2, 0, 2, 2, 0], [None, 1, 0, 2, 3, 0], position_name="Maj7 1st Inv"),
    'maj7_2nd': ChordShape("Maj7 2nd", "maj7", [None, 0, 2, 0, 2, 0], [None, 0, 2, 0, 3, 0], position_name="Maj7 2nd Inv"),
    'min7_root': ChordShape("Min7 Root", "min7", [None, 3, 5, 3, 4, 3], [None, 1, 3, 1, 4, 2], position_name="Min7 Root"),
    'min7_1st': ChordShape("Min7 1st", "min7", [None, 3, 3, 3, 4, 3], [None, 1, 1, 1, 4, 2], position_name="Min7 1st Inv"),
    'min7_2nd': ChordShape("Min7 2nd", "min7", [None, 2, 3, 2, 3, 2], [None, 1, 3, 1, 4, 2], position_name="Min7 2nd Inv"),
    'm7b5_root': ChordShape("m7b5 Root", "min7b5", [None, 3, 4, 3, 4, 3], [None, 1, 3, 2, 4, 1], position_name="m7b5 Root"),
    'dim7_root': ChordShape("Dim7 Root", "dim7", [None, 3, 4, 3, 4, 3], [None, 1, 3, 2, 4, 1], position_name="Dim7 Root"),
}

EXTENDED_CHORDS = {
    'dom9_root': ChordShape("Dom9", "9", [None, 3, 2, 3, 3, 3], [None, 2, 1, 3, 4, 4], position_name="Dom9"),
    'maj9_root': ChordShape("Maj9", "maj9", [None, 2, 2, 1, 2, 2], [None, 1, 2, 1, 3, 4], position_name="Maj9"),
    'min9_root': ChordShape("Min9", "min9", [None, 3, 5, 3, 4, 3], [None, 1, 3, 1, 4, 2], position_name="Min9"),
    'dom11_root': ChordShape("Dom11", "11", [None, 3, 3, 3, 3, 3], [None, 1, 1, 1, 1, 1], position_name="Dom11"),
    'dom13_root': ChordShape("Dom13", "13", [None, 2, 2, 2, 2, 2], [None, 1, 1, 1, 1, 1], position_name="Dom13"),
}

NOTE_TO_FRET = {
    'C': 1, 'C#': 2, 'DB': 2, 'D': 3, 'D#': 4, 'EB': 4,
    'E': 5, 'F': 6, 'F#': 7, 'GB': 7, 'G': 8, 'G#': 9,
    'AB': 9, 'A': 10, 'A#': 11, 'BB': 11, 'B': 12
}

QUALITY_ALIASES = {
    'm': 'min', 'min': 'min', 'maj': 'maj', 'major': 'maj',
    '7': 'dom7', 'dom': 'dom7', 'dom7': 'dom7',
    'maj7': 'maj7', 'major7': 'maj7',
    'min7': 'min7', 'm7': 'min7',
    'dim7': 'dim7', 'm7b5': 'min7b5', 'min7b5': 'min7b5',
    '9': '9', 'maj9': 'maj9', 'min9': 'min9',
    '11': '11', '13': '13',
}


def get_chord_shape(root: str, quality: str) -> List[ChordShape]:
    """Get all available chord shapes for a given root and quality."""
    shapes = []
    root_upper = root.upper()
    
    # Normalize quality
    quality_norm = quality.lower()
    if quality_norm in QUALITY_ALIASES:
        quality_norm = QUALITY_ALIASES[quality_norm]
    
    # Get open chord if available
    key = f"{root_upper}_{quality_norm}"
    if key in OPEN_CHORDS:
        shapes.append(OPEN_CHORDS[key])
    
    # Get barre chords
    for barre_key, barre_shape in BARRE_CHORDS.items():
        if barre_shape.quality == quality_norm:
            if root_upper in NOTE_TO_FRET:
                transposed = transpose_shape(barre_shape, NOTE_TO_FRET[root_upper])
                shapes.append(transposed)
            else:
                shapes.append(barre_shape)
    
    # Get triad shapes
    for triad_key, triad_shape in TRIAD_SHAPES.items():
        if triad_shape.quality == quality_norm:
            shapes.append(triad_shape)
    
    # Get seventh shapes
    for sev_key, sev_shape in SEVENTH_CHORDS.items():
        if sev_shape.quality == quality_norm:
            shapes.append(sev_shape)
    
    # Get extended shapes
    for ext_key, ext_shape in EXTENDED_CHORDS.items():
        if ext_shape.quality == quality_norm:
            shapes.append(ext_shape)
    
    return shapes


def transpose_shape(shape: ChordShape, target_fret: int) -> ChordShape:
    """Transpose a barre chord to a different fret position."""
    if not shape.is_barre:
        return shape
    
    base_diff = target_fret - shape.base_fret
    new_frets = []
    for f in shape.frets:
        if f is None:
            new_frets.append(None)
        elif f == 0:
            new_frets.append(0)
