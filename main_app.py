import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QLabel, QSpinBox, QComboBox, QPushButton, 
                             QTabWidget, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt

# Import custom modules
try:
    from pd_data_simulation import generate_prpd_data, generate_prps_data
    SIMULATION_MODULE_FOUND = True
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    SIMULATION_MODULE_FOUND = False
    # Define dummy functions if module not found, so app can start with error message
    def generate_prpd_data(*args, **kwargs):
        raise ImportError("pd_data_simulation module not found or failed to import.")
    def generate_prps_data(*args, **kwargs):
        raise ImportError("pd_data_simulation module not found or failed to import.")

try:
    from prpd_display import PRPDWidget
    PRPD_WIDGET_FOUND = True
except ImportError as e:
    print(f"Error importing PRPDWidget: {e}")
    PRPD_WIDGET_FOUND = False
    class PRPDWidget(QWidget): # Dummy widget
        def __init__(self, parent=None): super().__init__(parent); self.setLayout(QVBoxLayout()); self.layout().addWidget(QLabel("Error: PRPDWidget not loaded."))
        def plot_data(self, data): pass
        def clear_plot(self): pass


try:
    from prps_display import PRPSWidget
    PRPS_WIDGET_FOUND = True
except ImportError as e:
    print(f"Error importing PRPSWidget: {e}")
    PRPS_WIDGET_FOUND = False
    class PRPSWidget(QWidget): # Dummy widget
        def __init__(self, parent=None): super().__init__(parent); self.setLayout(QVBoxLayout()); self.layout().addWidget(QLabel("Error: PRPSWidget not loaded."))
        def plot_data(self, data): pass
        def clear_plot(self): pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Portable GIS Partial Discharge Detector")
        self.setGeometry(100, 100, 900, 700) # Adjusted size for better layout

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- Simulation Controls ---
        self.controls_groupbox = QGroupBox("Simulation Controls")
        self.controls_layout = QVBoxLayout() # Main layout for controls

        # Number of Points/Events
        num_points_layout = QHBoxLayout()
        self.num_points_label = QLabel("Number of Points/Events:")
        self.num_points_spinbox = QSpinBox()
        self.num_points_spinbox.setRange(10, 100000)
        self.num_points_spinbox.setValue(1000)
        self.num_points_spinbox.setToolTip("Number of data points for PRPD or events for PRPS.")
        num_points_layout.addWidget(self.num_points_label)
        num_points_layout.addWidget(self.num_points_spinbox)
        self.controls_layout.addLayout(num_points_layout)

        # Discharge Type
        discharge_type_layout = QHBoxLayout()
        self.discharge_type_label = QLabel("Discharge Type:")
        self.discharge_type_combobox = QComboBox()
        self.discharge_type_combobox.addItems(['Random', 'Corona', 'Internal Void', 'Surface Discharge'])
        self.discharge_type_combobox.setToolTip("Select the type of partial discharge to simulate.")
        discharge_type_layout.addWidget(self.discharge_type_label)
        discharge_type_layout.addWidget(self.discharge_type_combobox)
        self.controls_layout.addLayout(discharge_type_layout)
        
        # Duration (for PRPS)
        duration_layout = QHBoxLayout()
        self.duration_label = QLabel("Duration (seconds for PRPS):")
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 3600)
        self.duration_spinbox.setValue(10)
        self.duration_spinbox.setToolTip("Duration of the PRPS data sequence in seconds.")
        duration_layout.addWidget(self.duration_label)
        duration_layout.addWidget(self.duration_spinbox)
        self.controls_layout.addLayout(duration_layout)

        # Generate Data Button
        self.generate_button = QPushButton("Generate Data")
        self.generate_button.setToolTip("Generate and plot new PRPD and PRPS data.")
        self.controls_layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)
        
        self.controls_groupbox.setLayout(self.controls_layout)
        # Allow the groupbox to expand vertically but not too much initially
        self.controls_groupbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        # --- Display Area ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setToolTip("Displays PRPD and PRPS plots.")

        if PRPD_WIDGET_FOUND:
            self.prpd_widget = PRPDWidget()
        else:
            self.prpd_widget = PRPDWidget() # This will be the dummy widget
            QMessageBox.critical(self, "Module Error", "PRPDWidget could not be loaded. Please check the console for errors.")


        if PRPS_WIDGET_FOUND:
            self.prps_widget = PRPSWidget()
        else:
            self.prps_widget = PRPSWidget() # This will be the dummy widget
            QMessageBox.critical(self, "Module Error", "PRPSWidget could not be loaded. Please check the console for errors.")
            
        self.tab_widget.addTab(self.prpd_widget, "PRPD")
        self.tab_widget.addTab(self.prps_widget, "PRPS")
        # Allow the tab widget to expand significantly
        self.tab_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        # --- Layout Management ---
        self.main_layout.addWidget(self.controls_groupbox)
        self.main_layout.addWidget(self.tab_widget)
        
        # Set stretch factors: plot area takes more space than controls
        self.main_layout.setStretchFactor(self.controls_groupbox, 1) # Smaller part
        self.main_layout.setStretchFactor(self.tab_widget, 5)      # Larger part

        # --- Connect Signals and Slots ---
        self.generate_button.clicked.connect(self.generate_and_plot_data)
        
        # Initial check for simulation module
        if not SIMULATION_MODULE_FOUND:
             QMessageBox.critical(self, "Module Error", 
                                  "The 'pd_data_simulation.py' module was not found or failed to import. Data generation will not work. Please check the console.")
             self.generate_button.setEnabled(False)


    def generate_and_plot_data(self):
        try:
            num_points = self.num_points_spinbox.value()
            # Convert display name to function argument name
            discharge_type_display = self.discharge_type_combobox.currentText()
            discharge_type_map = {
                'Random': 'random',
                'Corona': 'corona',
                'Internal Void': 'internal_void',
                'Surface Discharge': 'surface_discharge'
            }
            discharge_type_actual = discharge_type_map.get(discharge_type_display, 'random')
            
            duration = self.duration_spinbox.value()

            # Generate and plot PRPD data
            prpd_data = generate_prpd_data(num_points=num_points, discharge_type=discharge_type_actual)
            if PRPD_WIDGET_FOUND:
                print(f"Plotting PRPD data ({len(prpd_data)} points) for type: {discharge_type_actual}")
                self.prpd_widget.plot_data(prpd_data)
            else:
                print("PRPDWidget not available to plot data.")
                QMessageBox.warning(self, "Plot Error", "PRPDWidget is not available to plot data.")


            # Generate and plot PRPS data
            # num_events is same as num_points for this UI
            prps_data = generate_prps_data(num_events=num_points, duration_seconds=duration, discharge_type=discharge_type_actual)
            if PRPS_WIDGET_FOUND:
                print(f"Plotting PRPS data ({len(prps_data)} events) over {duration}s for type: {discharge_type_actual}")
                self.prps_widget.plot_data(prps_data)
            else:
                print("PRPSWidget not available to plot data.")
                QMessageBox.warning(self, "Plot Error", "PRPSWidget is not available to plot data.")

            print("Data generation and plotting complete for this cycle.")

        except ImportError as e: # Specifically for missing simulation module during generation
            print(f"ImportError during data generation: {e}")
            QMessageBox.critical(self, "Runtime Module Error", 
                                 f"A required module for data generation is missing: {e}\nThe application might not have started correctly.")
            self.generate_button.setEnabled(False) # Disable button if error occurs here
        except Exception as e:
            print(f"Exception during data generation/plotting: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred during data generation or plotting: {e}")
            # Optionally, clear plots if error
            if PRPD_WIDGET_FOUND: self.prpd_widget.clear_plot()
            if PRPS_WIDGET_FOUND: self.prps_widget.clear_plot()


if __name__ == '__main__':
    print("Starting application...")
    app = QApplication(sys.argv)
    print("QApplication instance created.")
    main_win = MainWindow()
    print("MainWindow instance created.")
    main_win.show()
    print("MainWindow shown.")

    # --- Simulated UI Interactions for Testing ---
    # This section will run if __name__ == '__main__' in a non-interactive environment
    # It's a way to "script" the tests when a human cannot click buttons.
    
    if not main_win.generate_button.isEnabled():
        print("Generate button is disabled, likely due to import errors. Skipping interaction tests.")
    else:
        print("\n--- Simulating Test Script ---")

        # Test 1: Application Launch & Default State (implicitly done by reaching here)
        print("Test 1 & 2: Application Launch & Default State - Presumed OK if no crashes before this.")
        # TODO: Add checks for initial text in plot widgets if possible non-visually
        
        # Test 3: Data Generation and Display (Default Parameters)
        print("\nTest 3: Default Data Generation")
        main_win.generate_button.click() # Simulate click
        QApplication.processEvents() # Allow Qt to process the click

        # Test 4: Changing Discharge Type
        print("\nTest 4: Changing Discharge Type to Corona")
        main_win.discharge_type_combobox.setCurrentText('Corona')
        QApplication.processEvents()
        main_win.generate_button.click()
        QApplication.processEvents()

        # Test 5: Changing Number of Points
        print("\nTest 5: Changing Number of Points to 500")
        main_win.num_points_spinbox.setValue(500)
        QApplication.processEvents()
        main_win.generate_button.click()
        QApplication.processEvents()

        # Test 6: Changing Duration (for PRPS)
        print("\nTest 6: Changing Duration to 20s")
        main_win.duration_spinbox.setValue(20)
        QApplication.processEvents()
        main_win.generate_button.click()
        QApplication.processEvents()
        
        print("\n--- Test Script Simulation Complete ---")

    # For a real GUI app, app.exec_() would be here.
    # For a scripted test in a non-GUI environment, we might exit or add a short delay.
    # If the environment supports it, app.exec_() would run the event loop.
    # If not, the script will just end after the simulated interactions.
    
    # Attempt to run the event loop for a very short time to catch immediate errors
    # For proper GUI testing, a dedicated framework (like pytest-qt) would be needed.
    # sys.exit(app.exec_()) # This would block if there's no X server.
    
    # Instead, let's process events and then exit if no GUI is expected.
    # If an X server is available, the window would have shown and then closed by this.
    # If not, the print statements are our primary feedback.
    
    print("Processing final events...")
    QApplication.processEvents()
    print("Exiting application (or script if no event loop running).")
    # No sys.exit(app.exec_()) to prevent blocking in non-GUI environment

    # If we want to ensure the app window appears and then closes in a test:
    # from PyQt5.QtCore import QTimer
    # QTimer.singleShot(1000, app.quit) # Quit after 1 second
    # sys.exit(app.exec_())


# Minimal execution for non-interactive environment
# This will allow the print statements from __main__ to run
# and then the script will terminate.
# This part is tricky because `app.exec_()` blocks.
# For automated testing in headless environments, one might need to run the app
# in a separate process or use a virtual framebuffer like Xvfb.

# The code above will simulate clicks and print logs.
# The actual visual verification cannot be done by the agent.
# The agent will rely on the print logs and absence of crashes.
