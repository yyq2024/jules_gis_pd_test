import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np # For unpacking data if needed

# Attempt to import data generation for testing, optional
try:
    from pd_data_simulation import generate_prpd_data
except ImportError:
    print("Note: pd_data_simulation.py not found. Test data will be manually created.")
    generate_prpd_data = None


class PRPDWidget(QWidget):
    """
    A PyQt Widget that uses Matplotlib to display PRPD (Phase Resolved Partial Discharge) data.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a Matplotlib Figure and a Canvas
        self.figure = Figure(figsize=(5, 4), dpi=100) # Adjust figsize and dpi as needed
        self.canvas = FigureCanvas(self.figure)
        
        # Add an Axes object to the Figure for the PRPD plot
        self.ax = self.figure.add_subplot(111)

        # Set up a basic layout for the widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initialize with an empty plot
        self.clear_plot()

    def plot_data(self, prpd_data):
        """
        Plots the PRPD data on the Matplotlib canvas.

        Args:
            prpd_data (list): A list of tuples, where each tuple is (phase_angle, magnitude).
        """
        self.ax.clear() # Clear any existing plot

        if prpd_data and len(prpd_data) > 0:
            # Extract phase angles and magnitudes
            # Assuming prpd_data is list of (phase, magnitude) tuples
            phase_angles, magnitudes = zip(*prpd_data)
            
            # Create a 2D scatter plot
            self.ax.scatter(phase_angles, magnitudes, s=5, alpha=0.7) # s is size, alpha is transparency

            self.ax.set_xlabel("Phase Angle (degrees)")
            self.ax.set_ylabel("Magnitude (a.u.)")
            self.ax.set_title("PRPD Diagram")
            self.ax.set_xlim(0, 360)
            self.ax.set_ylim(bottom=0) # Ensure y-axis starts at 0 or auto-adjusts if all magnitudes are high
            self.ax.grid(True, linestyle='--', alpha=0.6)
        else:
            self.ax.text(0.5, 0.5, "No data to display", 
                         horizontalalignment='center', verticalalignment='center', 
                         transform=self.ax.transAxes, fontsize=12)
            # Still set labels and title for consistency, even if empty
            self.ax.set_xlabel("Phase Angle (degrees)")
            self.ax.set_ylabel("Magnitude (a.u.)")
            self.ax.set_title("PRPD Diagram")
            self.ax.set_xlim(0, 360)
            self.ax.set_ylim(0, 100) # Default y limit for empty plot

        self.canvas.draw() # Redraw the canvas

    def clear_plot(self):
        """
        Clears the plot and displays a "No data to display" message.
        """
        self.ax.clear()
        self.ax.text(0.5, 0.5, "No data to display", 
                     horizontalalignment='center', verticalalignment='center', 
                     transform=self.ax.transAxes, fontsize=12)
        self.ax.set_xlabel("Phase Angle (degrees)")
        self.ax.set_ylabel("Magnitude (a.u.)")
        self.ax.set_title("PRPD Diagram")
        self.ax.set_xlim(0, 360)
        self.ax.set_ylim(0, 100) # Default y limit for empty plot
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Main window to test the widget
    main_window = QWidget()
    main_window.setWindowTitle("PRPD Widget Test")
    main_window.setGeometry(100, 100, 600, 500)
    
    layout = QVBoxLayout(main_window)
    
    prpd_plot_widget = PRPDWidget(main_window)
    layout.addWidget(prpd_plot_widget)
    
    # Example: Plot some test data
    # If pd_data_simulation is available, use it
    if generate_prpd_data:
        print("Generating test data using pd_data_simulation.py...")
        # test_data = generate_prpd_data(200, 'corona')
        # test_data = generate_prpd_data(0, 'random') # Test empty data
        test_data = generate_prpd_data(300, 'internal_void')
    else:
        # Fallback manual data if generator is not found
        print("Using manual fallback test data.")
        # test_data = [(45, 50), (90, 70), (200, 30), (270, 60), (30, 80)]
        test_data = [] # Test empty data
        # test_data = [(np.random.uniform(0,360),np.random.uniform(0,100)) for _ in range(100)]

    prpd_plot_widget.plot_data(test_data)
    
    # You could add buttons or other controls here to test clear_plot or plot different data
    
    main_window.show()
    sys.exit(app.exec_())
