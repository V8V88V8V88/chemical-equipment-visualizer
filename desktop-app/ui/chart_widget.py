"""Matplotlib chart widgets for PyQt5."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


class ChartWidget(QWidget):
    """Base widget for matplotlib charts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor='white')
        self.figure.patch.set_facecolor('white')
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
    
    def clear(self):
        """Clear the chart."""
        self.figure.clear()
        self.canvas.draw()


class TypeDistributionChart(ChartWidget):
    """Bar chart for equipment type distribution."""
    
    def update_chart(self, distribution: dict):
        """Update the chart with new data."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('white')
        
        if not distribution:
            ax.text(0.5, 0.5, "No data", ha='center', va='center', 
                   color='#9ca3af', fontsize=12)
            self.canvas.draw()
            return
        
        types = list(distribution.keys())
        counts = list(distribution.values())
        # Use muted slate colors matching web frontend
        colors = ['#475569', '#64748b', '#94a3b8', '#334155', '#1e293b', 
                 '#475569', '#64748b', '#94a3b8', '#334155', '#1e293b']
        bar_colors = [colors[i % len(colors)] for i in range(len(types))]
        
        bars = ax.bar(types, counts, color=bar_colors, alpha=0.8, edgecolor='white', linewidth=1.5)
        ax.set_xlabel("Equipment Type", fontsize=11, color='#6b7280', fontweight=500)
        ax.set_ylabel("Count", fontsize=11, color='#6b7280', fontweight=500)
        ax.set_title("Equipment Type Distribution", fontsize=13, color='#111827', 
                    fontweight=600, pad=15)
        
        # Clean up tick labels
        ax.tick_params(axis='both', labelsize=9, colors='#6b7280')
        if len(types) > 4:
            ax.set_xticklabels(types, rotation=45, ha='right')
        
        # Remove top and right spines for cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
        
        # Add subtle grid
        ax.grid(True, axis='y', alpha=0.2, linestyle='-', linewidth=0.5, color='#e5e7eb')
        ax.set_axisbelow(True)
        
        self.figure.tight_layout()
        self.canvas.draw()


class ParameterChart(ChartWidget):
    """Line chart for equipment parameters."""
    
    def update_chart(self, equipment: list):
        """Update the chart with new data."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('white')
        
        if not equipment:
            ax.text(0.5, 0.5, "No data", ha='center', va='center',
                   color='#9ca3af', fontsize=12)
            self.canvas.draw()
            return
        
        names = [e["equipment_name"] for e in equipment]
        flowrates = [e["flowrate"] for e in equipment]
        pressures = [e["pressure"] for e in equipment]
        temperatures = [e["temperature"] for e in equipment]
        
        x = range(len(names))
        
        # Use muted colors matching web frontend
        ax.plot(x, flowrates, color='#1e293b', marker='o', label='Flowrate', 
               markersize=5, linewidth=2, markeredgecolor='white', markeredgewidth=1.5)
        ax.plot(x, pressures, color='#94a3b8', marker='s', label='Pressure', 
               markersize=5, linewidth=2, markeredgecolor='white', markeredgewidth=1.5)
        ax.plot(x, temperatures, color='#64748b', marker='^', label='Temperature', 
               markersize=5, linewidth=2, markeredgecolor='white', markeredgewidth=1.5)
        
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9, color='#6b7280')
        ax.set_xlabel("Equipment", fontsize=11, color='#6b7280', fontweight=500)
        ax.set_ylabel("Value", fontsize=11, color='#6b7280', fontweight=500)
        ax.set_title("Equipment Parameters", fontsize=13, color='#111827', 
                    fontweight=600, pad=15)
        
        # Clean legend
        legend = ax.legend(loc='upper right', frameon=True, fancybox=False, 
                          shadow=False, fontsize=9)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('#e5e7eb')
        legend.get_frame().set_linewidth(1)
        
        # Clean up spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
        
        # Subtle grid
        ax.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#e5e7eb')
        ax.set_axisbelow(True)
        
        # Clean tick labels
        ax.tick_params(axis='y', labelsize=9, colors='#6b7280')
        
        self.figure.tight_layout()
        self.canvas.draw()
