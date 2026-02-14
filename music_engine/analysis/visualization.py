"""
Visualization module for advanced analytics.

This module provides graphical representations of harmonic analysis results
using Tkinter Canvas for lightweight, integrated visualizations.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Tuple, Optional
import math

# Import with proper path handling
import sys
import os

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.progression import Progression


class AnalyticsVisualizer:
    """
    Creates visual representations of harmonic analysis data.

    Provides charts and graphs for:
    - Tension curves
    - Circle of fifths relationships
    - Functional harmony distribution
    - Complexity metrics
    """

    # Color scheme for visualizations
    COLORS = {
        'tension': '#FF6B6B',
        'release': '#4ECDC4',
        'tonic': '#45B7D1',
        'dominant': '#FFA07A',
        'subdominant': '#98D8C8',
        'other': '#F7DC6F',
        'background': '#F8F9FA',
        'grid': '#E9ECEF',
        'text': '#343A40'
    }

    @staticmethod
    def create_tension_curve(parent, analysis_data: Dict, width: int = 400, height: int = 200) -> tk.Canvas:
        """
        Create a tension curve visualization.

        Args:
            parent: Parent widget
            analysis_data: Analysis results from HarmonicAnalyzer
            width: Canvas width
            height: Canvas height

        Returns:
            Canvas widget with tension curve
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg=AnalyticsVisualizer.COLORS['background'])
        canvas.pack(pady=10)

        tension_data = analysis_data.get('tension_profile', {})
        tension_curve = tension_data.get('tension_curve', [])

        if not tension_curve:
            canvas.create_text(width//2, height//2, text="No tension data available",
                             fill=AnalyticsVisualizer.COLORS['text'])
            return canvas

        # Draw grid
        AnalyticsVisualizer._draw_grid(canvas, width, height, len(tension_curve))

        # Draw tension curve
        points = []
        max_tension = 10  # Tension scale 0-10

        for i, tension in enumerate(tension_curve):
            x = (i / max(1, len(tension_curve) - 1)) * (width - 60) + 30
            y = height - 30 - (tension / max_tension) * (height - 60)
            points.extend([x, y])

        if points:
            canvas.create_line(points, fill=AnalyticsVisualizer.COLORS['tension'],
                             width=3, smooth=True, splinesteps=20)

        # Draw data points
        for i, (x, y) in enumerate(zip(points[::2], points[1::2])):
            canvas.create_oval(x-3, y-3, x+3, y+3, fill=AnalyticsVisualizer.COLORS['tension'])

        # Add labels
        canvas.create_text(width//2, 15, text="Harmonic Tension Curve",
                         fill=AnalyticsVisualizer.COLORS['text'], font=('Arial', 12, 'bold'))
        canvas.create_text(15, height//2, text="Tension", angle=90,
                         fill=AnalyticsVisualizer.COLORS['text'])
        canvas.create_text(width//2, height-10, text="Chord Position",
                         fill=AnalyticsVisualizer.COLORS['text'])

        return canvas

    @staticmethod
    def create_circle_plot(parent, analysis_data: Dict, width: int = 300, height: int = 300) -> tk.Canvas:
        """
        Create a circle of fifths visualization.

        Args:
            parent: Parent widget
            analysis_data: Analysis results from HarmonicAnalyzer
            width: Canvas width
            height: Canvas height

        Returns:
            Canvas widget with circle of fifths plot
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg=AnalyticsVisualizer.COLORS['background'])
        canvas.pack(pady=10)

        cof_data = analysis_data.get('circle_of_fifths', {})
        positions = cof_data.get('circle_positions', [])

        if not positions or all(p == -1 for p in positions):
            canvas.create_text(width//2, height//2, text="No circle data available",
                             fill=AnalyticsVisualizer.COLORS['text'])
            return canvas

        # Circle parameters
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3

        # Draw circle
        canvas.create_oval(center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius,
                         outline=AnalyticsVisualizer.COLORS['grid'], width=2)

        # Major keys around the circle
        major_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#',
                     'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']

        # Plot progression path
        prev_x, prev_y = None, None
        for i, pos in enumerate(positions):
            if pos == -1:  # Unknown position
                continue

            # Calculate position on circle (simplified mapping)
            angle = (pos / 12) * 2 * math.pi - math.pi/2  # Start at top
            x = center_x + radius * 0.7 * math.cos(angle)
            y = center_y + radius * 0.7 * math.sin(angle)

            # Draw point
            color = AnalyticsVisualizer.COLORS['tension'] if i == 0 else AnalyticsVisualizer.COLORS['dominant']
            canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline='black')

            # Draw line to previous point
            if prev_x is not None and prev_y is not None:
                canvas.create_line(prev_x, prev_y, x, y,
                                 fill=AnalyticsVisualizer.COLORS['grid'], width=2)

            prev_x, prev_y = x, y

            # Add chord number
            canvas.create_text(x, y-15, text=str(i+1),
                             fill=AnalyticsVisualizer.COLORS['text'], font=('Arial', 8, 'bold'))

        # Add title
        canvas.create_text(width//2, 20, text="Circle of Fifths Path",
                         fill=AnalyticsVisualizer.COLORS['text'], font=('Arial', 12, 'bold'))

        return canvas

    @staticmethod
    def create_function_distribution(parent, analysis_data: Dict, width: int = 400, height: int = 200) -> tk.Canvas:
        """
        Create a functional harmony distribution chart.

        Args:
            parent: Parent widget
            analysis_data: Analysis results from HarmonicAnalyzer
            width: Canvas width
            height: Canvas height

        Returns:
            Canvas widget with function distribution
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg=AnalyticsVisualizer.COLORS['background'])
        canvas.pack(pady=10)

        functional_data = analysis_data.get('functional_analysis', {})
        distribution = functional_data.get('function_distribution', {})

        if not distribution:
            canvas.create_text(width//2, height//2, text="No functional data available",
                             fill=AnalyticsVisualizer.COLORS['text'])
            return canvas

        # Function colors
        function_colors = {
            'T': AnalyticsVisualizer.COLORS['tonic'],
            'D': AnalyticsVisualizer.COLORS['dominant'],
            'S': AnalyticsVisualizer.COLORS['subdominant'],
            'O': AnalyticsVisualizer.COLORS['other']
        }

        # Calculate bar positions
        total = sum(distribution.values())
        if total == 0:
            return canvas

        bar_width = (width - 60) // len(distribution)
        max_height = height - 80

        x_pos = 30
        for func, count in distribution.items():
            percentage = count / total
            bar_height = percentage * max_height

            # Draw bar
            color = function_colors.get(func, AnalyticsVisualizer.COLORS['other'])
            canvas.create_rectangle(x_pos, height - 50 - bar_height,
                                  x_pos + bar_width - 5, height - 50,
                                  fill=color, outline='black')

            # Draw label
            canvas.create_text(x_pos + bar_width//2, height - 25,
                             text=f"{func}\n{count}",
                             fill=AnalyticsVisualizer.COLORS['text'],
                             font=('Arial', 9, 'bold'))

            x_pos += bar_width

        # Add title and labels
        canvas.create_text(width//2, 15, text="Functional Harmony Distribution",
                         fill=AnalyticsVisualizer.COLORS['text'], font=('Arial', 12, 'bold'))
        canvas.create_text(15, height//2, text="Count", angle=90,
                         fill=AnalyticsVisualizer.COLORS['text'])

        # Legend
        legend_x = width - 100
        legend_y = 40
        for func, color in function_colors.items():
            canvas.create_rectangle(legend_x, legend_y, legend_x+15, legend_y+15,
                                  fill=color, outline='black')
            canvas.create_text(legend_x+25, legend_y+7, text=func,
                             fill=AnalyticsVisualizer.COLORS['text'], anchor='w')
            legend_y += 20

        return canvas

    @staticmethod
    def create_complexity_gauge(parent, analysis_data: Dict, width: int = 200, height: int = 200) -> tk.Canvas:
        """
        Create a complexity gauge visualization.

        Args:
            parent: Parent widget
            analysis_data: Analysis results from HarmonicAnalyzer
            width: Canvas width
            height: Canvas height

        Returns:
            Canvas widget with complexity gauge
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg=AnalyticsVisualizer.COLORS['background'])
        canvas.pack(pady=10)

        complexity_data = analysis_data.get('complexity_metrics', {})
        complexity_score = complexity_data.get('overall_complexity', 0)

        if complexity_score == 0:
            canvas.create_text(width//2, height//2, text="No complexity data",
                             fill=AnalyticsVisualizer.COLORS['text'])
            return canvas

        # Gauge parameters
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3

        # Draw gauge background
        canvas.create_arc(center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        start=0, extent=180, outline=AnalyticsVisualizer.COLORS['grid'],
                        width=10, style='arc')

        # Draw complexity arc
        extent = complexity_score * 180  # 0-180 degrees
        color = AnalyticsVisualizer._get_complexity_color(complexity_score)
        canvas.create_arc(center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        start=0, extent=extent, outline=color, width=10, style='arc')

        # Draw needle
        needle_angle = math.radians(complexity_score * 180 - 90)
        needle_length = radius - 10
        needle_x = center_x + needle_length * math.cos(needle_angle)
        needle_y = center_y + needle_length * math.sin(needle_angle)

        canvas.create_line(center_x, center_y, needle_x, needle_y,
                         fill='red', width=3, arrow='last')

        # Add labels
        canvas.create_text(center_x, center_y + radius + 20,
                         text=".1%", fill=AnalyticsVisualizer.COLORS['text'],
                         font=('Arial', 12, 'bold'))

        desc = complexity_data.get('complexity_description', '')
        canvas.create_text(center_x, height - 20, text=desc,
                         fill=AnalyticsVisualizer.COLORS['text'], font=('Arial', 9))

        canvas.create_text(center_x, 20, text="Harmonic Complexity",
                         fill=AnalyticsVisualizer.COLORS['text'], font=('Arial', 11, 'bold'))

        return canvas

    @staticmethod
    def _draw_grid(canvas: tk.Canvas, width: int, height: int, data_points: int):
        """Draw a grid on the canvas."""
        # Horizontal grid lines
        for i in range(0, 11):  # 0-10 tension scale
            y = height - 30 - (i / 10) * (height - 60)
            canvas.create_line(30, y, width - 30, y,
                             fill=AnalyticsVisualizer.COLORS['grid'], dash=(2, 2))
            canvas.create_text(15, y, text=str(i), fill=AnalyticsVisualizer.COLORS['text'],
                             font=('Arial', 8))

        # Vertical grid lines
        for i in range(data_points):
            x = (i / max(1, data_points - 1)) * (width - 60) + 30
            canvas.create_line(x, 30, x, height - 30,
                             fill=AnalyticsVisualizer.COLORS['grid'], dash=(2, 2))

    @staticmethod
    def _get_complexity_color(score: float) -> str:
        """Get color based on complexity score."""
        if score < 0.3:
            return '#4CAF50'  # Green - Simple
        elif score < 0.5:
            return '#8BC34A'  # Light green
        elif score < 0.7:
            return '#FFC107'  # Yellow - Moderate
        elif score < 0.85:
            return '#FF9800'  # Orange
        else:
            return '#F44336'  # Red - Complex

    @staticmethod
    def create_analytics_dashboard(parent, progression: Progression,
                                 width: int = 800, height: int = 600) -> tk.Frame:
        """
        Create a complete analytics dashboard.

        Args:
            parent: Parent widget
            progression: Progression to analyze
            width: Dashboard width
            height: Dashboard height

        Returns:
            Frame containing the complete analytics dashboard
        """
        from .advanced_analytics import HarmonicAnalyzer

        # Analyze progression
        analysis = HarmonicAnalyzer.analyze_progression(progression)

        # Create main frame
        dashboard = tk.Frame(parent, bg=AnalyticsVisualizer.COLORS['background'])
        dashboard.pack(fill='both', expand=True)

        # Title
        title_label = tk.Label(dashboard,
                             text="🎼 Advanced Harmonic Analysis Dashboard",
                             font=('Arial', 16, 'bold'),
                             bg=AnalyticsVisualizer.COLORS['background'],
                             fg=AnalyticsVisualizer.COLORS['text'])
        title_label.pack(pady=10)

        # Create notebook for different views
        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Overview tab
        overview_frame = tk.Frame(notebook, bg=AnalyticsVisualizer.COLORS['background'])

        # Tension curve
        tension_container = tk.Frame(overview_frame, bg=AnalyticsVisualizer.COLORS['background'])
        tension_container.pack(side='top', fill='x', pady=5)
        tk.Label(tension_container, text="Harmonic Tension Profile",
                font=('Arial', 12, 'bold'),
                bg=AnalyticsVisualizer.COLORS['background']).pack()
        AnalyticsVisualizer.create_tension_curve(tension_container, analysis, width=600, height=150)

        # Bottom row with circle and functions
        bottom_row = tk.Frame(overview_frame, bg=AnalyticsVisualizer.COLORS['background'])
        bottom_row.pack(fill='x')

        # Circle of fifths
        circle_container = tk.Frame(bottom_row, bg=AnalyticsVisualizer.COLORS['background'])
        circle_container.pack(side='left', padx=10)
        tk.Label(circle_container, text="Circle of Fifths",
                font=('Arial', 11, 'bold'),
                bg=AnalyticsVisualizer.COLORS['background']).pack()
        AnalyticsVisualizer.create_circle_plot(circle_container, analysis, width=250, height=250)

        # Functional distribution
        function_container = tk.Frame(bottom_row, bg=AnalyticsVisualizer.COLORS['background'])
        function_container.pack(side='left', padx=10)
        tk.Label(function_container, text="Functional Harmony",
                font=('Arial', 11, 'bold'),
                bg=AnalyticsVisualizer.COLORS['background']).pack()
        AnalyticsVisualizer.create_function_distribution(function_container, analysis, width=300, height=150)

        # Complexity gauge
        complexity_container = tk.Frame(bottom_row, bg=AnalyticsVisualizer.COLORS['background'])
        complexity_container.pack(side='right', padx=10)
        tk.Label(complexity_container, text="Complexity Level",
                font=('Arial', 11, 'bold'),
                bg=AnalyticsVisualizer.COLORS['background']).pack()
        AnalyticsVisualizer.create_complexity_gauge(complexity_container, analysis, width=150, height=150)

        notebook.add(overview_frame, text="Overview")

        # Details tab
        details_frame = tk.Frame(notebook, bg=AnalyticsVisualizer.COLORS['background'])

        # Text summary
        text_frame = tk.Frame(details_frame, bg=AnalyticsVisualizer.COLORS['background'])
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap='word', height=20,
                            bg='white', fg=AnalyticsVisualizer.COLORS['text'])
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Generate summary text
        summary = AnalyticsVisualizer._generate_analysis_summary(analysis)
        text_widget.insert('1.0', summary)
        text_widget.config(state='disabled')

        notebook.add(details_frame, text="Details")

        return dashboard

    @staticmethod
    def _generate_analysis_summary(analysis: Dict) -> str:
        """Generate a text summary of the analysis."""
        summary = "🎼 ADVANCED HARMONIC ANALYSIS REPORT\n"
        summary += "=" * 50 + "\n\n"

        # Basic metrics
        basic = analysis.get('basic_metrics', {})
        if basic:
            summary += "📊 BASIC METRICS:\n"
            summary += f"  • Chords: {basic.get('chord_count', 0)}\n"
            summary += f"  • Unique qualities: {basic.get('unique_qualities', 0)}\n"
            summary += f"  • Unique roots: {basic.get('unique_roots', 0)}\n"
            summary += f"  • Average notes per chord: {basic.get('average_notes_per_chord', 0):.2f}\n"
            summary += "\n"

        # Tension profile
        tension = analysis.get('tension_profile', {})
        if tension:
            summary += "🔥 TENSION ANALYSIS:\n"
            summary += f"  • Average tension: {tension.get('average_tension', 0):.1f}/10\n"
            summary += f"  • Peak tension: {tension.get('peak_tension', 0):.1f}/10\n"
            summary += f"  • Tension range: {tension.get('tension_range', 0):.1f}\n"
            flow_desc = analysis.get('harmonic_flow', {}).get('flow_description', '')
            summary += f"  • Harmonic flow: {flow_desc}\n"
            summary += "\n"

        # Functional analysis
        functional = analysis.get('functional_analysis', {})
        if functional:
            summary += "🎯 FUNCTIONAL HARMONY:\n"
            summary += f"  • Key: {functional.get('detected_key', 'Unknown')}\n"
            summary += f"  • Mode: {'Minor' if functional.get('is_minor', False) else 'Major'}\n"
            distribution = functional.get('function_distribution', {})
            for func, count in distribution.items():
                func_name = {'T': 'Tonic', 'D': 'Dominant', 'S': 'Subdominant', 'O': 'Other'}.get(func, func)
                summary += f"  • {func_name}: {count}\n"
            summary += "\n"

        # Complexity
        complexity = analysis.get('complexity_metrics', {})
        if complexity:
            summary += "🧠 COMPLEXITY ANALYSIS:\n"
            summary += f"  • Overall complexity: {complexity.get('complexity_description', 'Unknown')}\n"
            summary += f"  • Note density: {complexity.get('note_density', 0):.1%}\n"
            summary += f"  • Chord variety: {complexity.get('chord_variety', 0):.1%}\n"
            summary += "\n"

        # Patterns
        patterns = analysis.get('patterns', {})
        if patterns:
            pattern_list = patterns.get('patterns', [])
            if pattern_list:
                summary += "🔍 IDENTIFIED PATTERNS:\n"
                for pattern in pattern_list:
                    summary += f"  • {pattern}\n"
                summary += "\n"
            else:
                summary += "🔍 PATTERNS: No common patterns detected\n\n"

        # Circle of fifths
        cof = analysis.get('circle_of_fifths', {})
        if cof:
            summary += "🎯 CIRCLE OF FIFTHS:\n"
            efficiency = cof.get('circle_efficiency', 0)
            summary += f"  • Circle efficiency: {efficiency:.1%}\n"
            avg_dist = cof.get('average_distance', 0)
            summary += f"  • Average distance: {avg_dist:.1f} steps\n"
            summary += "\n"

        # Voice leading
        voice = analysis.get('voice_leading', {})
        if voice:
            summary += "🎵 VOICE LEADING:\n"
            efficiency = voice.get('voice_leading_efficiency', 0)
            summary += f"  • Voice leading efficiency: {efficiency:.1%}\n"
            smoothness = voice.get('smoothness_score', 0)
            summary += f"  • Smoothness score: {smoothness:.1%}\n"
            summary += "\n"

        summary += "📈 END OF ANALYSIS REPORT"

        return summary