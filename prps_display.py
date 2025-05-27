import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.cm as cm
import numpy as np

# Attempt to import data generation for testing, optional
try:
    from pd_data_simulation import generate_prps_data
except ImportError:
    print("Note: pd_data_simulation.py not found. Test data will be manually created.")
    generate_prps_data = None


class PRPSWidget(QWidget):
    """
    A PyQt Widget that uses Matplotlib to display PRPS (Phase Resolved Pulse Sequence) data.
    The plot shows magnitude vs. time, with points colored by phase angle.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure(figsize=(7, 5), dpi=100) # Adjusted figsize for better PRPS display
        self.canvas = FigureCanvas(self.figure)
        
        # Add an Axes object for the PRPS plot
        self.ax = self.figure.add_subplot(111)
        self.colorbar = None # To keep track of the colorbar object

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.clear_plot()

    def plot_data(self, prps_data):
        """
        Plots the PRPS data on the Matplotlib canvas.
        Magnitude vs. Time, colored by Phase Angle.

        Args:
            prps_data (list): A list of tuples, where each tuple is 
                              (time_stamp, phase_angle, magnitude).
        """
        self.ax.clear() # Clear any existing plot
        # After clearing the axes, the old colorbar is no longer relevant or might be invalid.
        # Simply reset the reference. A new one will be created if data is plotted.
        self.colorbar = None

        if prps_data and len(prps_data) > 0:
            time_stamps, phase_angles, magnitudes = zip(*prps_data)
            
            time_stamps = np.array(time_stamps)
            phase_angles = np.array(phase_angles)
            magnitudes = np.array(magnitudes)

            # Create a scatter plot: Magnitude vs. Time, colored by Phase Angle
            scatter = self.ax.scatter(time_stamps, magnitudes, c=phase_angles, 
                                      cmap='hsv', # 'hsv' is good for cyclical data like phase
                                      s=10, alpha=0.7, vmin=0, vmax=360)
            
            # Add a colorbar to show the phase angle mapping
            self.colorbar = self.figure.colorbar(scatter, ax=self.ax, label='Phase Angle (degrees)')
            
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Magnitude (a.u.)")
            self.ax.set_title("PRPS Diagram - Magnitude vs. Time")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            if len(time_stamps) > 0:
                 self.ax.set_xlim(left=min(time_stamps), right=max(time_stamps) if max(time_stamps) > min(time_stamps) else min(time_stamps) + 1) # Handle single point case
            self.ax.set_ylim(bottom=0) # Ensure y-axis starts at 0
        else:
            self.ax.text(0.5, 0.5, "No data to display", 
                         horizontalalignment='center', verticalalignment='center', 
                         transform=self.ax.transAxes, fontsize=12)
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Magnitude (a.u.)")
            self.ax.set_title("PRPS Diagram - Magnitude vs. Time")
            self.ax.set_xlim(0, 1) # Default time limit for empty plot
            self.ax.set_ylim(0, 100) # Default y limit for empty plot
            self.ax.grid(True, linestyle='--', alpha=0.6)


        self.canvas.draw()

    def clear_plot(self):
        """
        Clears the plot and displays a "No data to display" message.
        """
        self.ax.clear()
        # After clearing the axes, the old colorbar is no longer relevant or might be invalid.
        self.colorbar = None

        self.ax.text(0.5, 0.5, "No data to display", 
                     horizontalalignment='center', verticalalignment='center', 
                     transform=self.ax.transAxes, fontsize=12)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Magnitude (a.u.)")
        self.ax.set_title("PRPS Diagram - Magnitude vs. Time")
        self.ax.set_xlim(0, 1) # Default time limit for empty plot
        self.ax.set_ylim(0, 100) # Default y limit for empty plot
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = QWidget()
    main_window.setWindowTitle("PRPS Widget Test")
    main_window.setGeometry(100, 100, 800, 600) # Slightly larger window for PRPS
    
    layout = QVBoxLayout(main_window)
    
    prps_plot_widget = PRPSWidget(main_window)
    layout.addWidget(prps_plot_widget)
    
    if generate_prps_data:
        print("Generating test data using pd_data_simulation.py...")
        # test_data = generate_prps_data(num_events=200, duration_seconds=60, discharge_type='corona')
        # test_data = generate_prps_data(num_events=0, duration_seconds=60, discharge_type='random') # Test empty
        test_data = generate_prps_data(num_events=500, duration_seconds=30, discharge_type='surface_discharge')
        # test_data = generate_prps_data(num_events=1, duration_seconds=10, discharge_type='random') # Test single point
    else:
        print("Using manual fallback test data.")
        # test_data = [(i*0.1, (i*20)%360, np.random.uniform(20,80)) for i in range(50)]
        test_data = [] # Test empty
        # test_data = [(0.5, 180, 50)] # Test single point

    prps_plot_widget.plot_data(test_data)
    
    main_window.show()
    sys.exit(app.exec_())
