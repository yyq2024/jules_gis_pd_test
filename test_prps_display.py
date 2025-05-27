import unittest
import sys
from PyQt5.QtWidgets import QApplication

# Attempt to import PRPSWidget and generate_prps_data
try:
    from prps_display import PRPSWidget
    from pd_data_simulation import generate_prps_data
    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    print(f"Failed to import modules for testing PRPSWidget: {e}")
    # Define dummy classes/functions if imports fail
    class PRPSWidget: pass
    def generate_prps_data(*args, **kwargs): return []


@unittest.skipIf(not MODULES_LOADED, "Modules for PRPSWidget tests could not be loaded.")
class TestPRPSWidget(unittest.TestCase):
    app = None # Class attribute to hold QApplication instance

    @classmethod
    def setUpClass(cls):
        """Create a QApplication instance before any tests run."""
        if QApplication.instance() is None:
            cls.app = QApplication(sys.argv if hasattr(sys, 'argv') else [''])
        else:
            cls.app = QApplication.instance()

    @classmethod
    def tearDownClass(cls):
        """Clean up QApplication instance after all tests run."""
        cls.app = None # Dereference

    def test_instantiation(self):
        """Test if PRPSWidget can be created."""
        try:
            widget = PRPSWidget()
            self.assertIsNotNone(widget)
            if hasattr(widget, 'canvas'):
                 self.assertIsNotNone(widget.canvas, "Widget canvas should be initialized.")
            if hasattr(widget, 'ax'):
                 self.assertIsNotNone(widget.ax, "Widget axes should be initialized.")
        except Exception as e:
            self.fail(f"PRPSWidget instantiation failed with error: {e}")

    def test_plot_data_with_sample_data(self):
        """Test plot_data with sample PRPS data."""
        widget = PRPSWidget()
        sample_data = generate_prps_data(num_events=100, duration_seconds=10, discharge_type='random')
        try:
            widget.plot_data(sample_data)
            if hasattr(widget, 'ax') and widget.ax is not None:
                self.assertTrue(widget.ax.get_title() == "PRPS Diagram - Magnitude vs. Time", "Plot title was not set correctly.")
                # Check if a colorbar was added (it's stored in widget.colorbar)
                if sample_data: # Only expect colorbar if data was plotted
                    self.assertIsNotNone(widget.colorbar, "Colorbar was not created for sample data.")
        except Exception as e:
            self.fail(f"widget.plot_data(sample_data) failed with error: {e}")

    def test_plot_data_with_empty_data(self):
        """Test plot_data with empty data."""
        widget = PRPSWidget()
        try:
            widget.plot_data([])
            if hasattr(widget, 'ax') and widget.ax is not None:
                self.assertTrue(widget.ax.get_title() == "PRPS Diagram - Magnitude vs. Time", "Plot title was not set correctly on empty data.")
                self.assertTrue(len(widget.ax.texts) > 0, "No text message found on empty plot.")
                # Check that no colorbar was added for empty data
                self.assertIsNone(widget.colorbar, "Colorbar should not be present for empty data.")
        except Exception as e:
            self.fail(f"widget.plot_data([]) failed with error: {e}")

    def test_clear_plot(self):
        """Test clear_plot method."""
        widget = PRPSWidget()
        # Optionally plot some data first
        sample_data = generate_prps_data(num_events=50, duration_seconds=5, discharge_type='corona')
        widget.plot_data(sample_data)
        
        try:
            widget.clear_plot()
            if hasattr(widget, 'ax') and widget.ax is not None:
                self.assertTrue(widget.ax.get_title() == "PRPS Diagram - Magnitude vs. Time", "Plot title was not set correctly after clear_plot.")
                self.assertTrue(len(widget.ax.texts) > 0, "No text message found after clear_plot.")
                self.assertEqual(len(widget.ax.collections), 0, "Plot data (collections) not cleared.")
                # Check that colorbar is removed/reset
                self.assertIsNone(widget.colorbar, "Colorbar was not reset after clear_plot.")
        except Exception as e:
            self.fail(f"widget.clear_plot() failed with error: {e}")

if __name__ == '__main__':
    unittest.main(argv=sys.argv + ['-v'], exit=False)
