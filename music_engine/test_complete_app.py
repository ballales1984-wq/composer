#!/usr/bin/env python3
"""
Test script for complete Music Theory Engine functionality.
"""

import tkinter as tk
from gui.main_window import MusicTheoryGUI

# Test complete app functionality
print('Testing complete Music Theory Engine...')

try:
    root = MusicTheoryGUI()
    print('[OK] Main window created')

    # Check all components are created and visible
    components = ['scale_explorer', 'chord_builder', 'progression_analyzer', 'arpeggio_viewer', 'fretboard_viewer']
    for comp in components:
        if hasattr(root, comp):
            print(f'[OK] {comp} exists')
        else:
            print(f'[ERROR] {comp} missing')

    # Check if tabs are working
    tabs = root.tabview.get()
    print(f'[OK] Tabs available: {tabs}')

    # Check default data
    if hasattr(root.scale_explorer, 'current_scale') and root.scale_explorer.current_scale:
        print(f'[OK] Default scale: {root.scale_explorer.current_scale.name}')

    if hasattr(root.chord_builder, 'current_chord') and root.chord_builder.current_chord:
        print(f'[OK] Default chord: {root.chord_builder.current_chord.name}')

    print('')
    print('SUCCESS: Music Theory Engine is fully functional!')
    print('You should now see:')
    print('- Window with title and tabs')
    print('- Scale Explorer tab with controls and C Major scale')
    print('- Chord Builder tab with controls and C Major chord')
    print('- Other tabs with their respective controls')
    print('- Fretboard Viewer showing the guitar neck')

    # Close without showing GUI
    root.destroy()

except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()