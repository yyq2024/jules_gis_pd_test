import unittest
import sys
from PyQt5.QtWidgets import QApplication

# Attempt to import PRPDWidget and generate_prpd_data
# This structure helps in environments where these might not be immediately on PYTHONPATH
# or if there are issues with dependencies needed for these modules but not for tests themselves.
try:
    from prpd_display import PRPDWidget
    from pd_data_simulation import generate_prpd_data
    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    print(f"Failed to import modules for testing PRPDWidget: {e}")
    # Define dummy classes/functions if imports fail, so tests can be discovered
    # but will likely fail or be skipped, indicating the problem.
    class PRPDWidget: pass 
    def generate_prpd_data(*args, **kwargs): return []


@unittest.skipIf(not MODULES_LOADED, "Modules for PRPDWidget tests could not be loaded.")
class TestPRPDWidget(unittest.TestCase):
    app = None # Class attribute to hold QApplication instance

    @classmethod
    def setUpClass(cls):
        """Create a QApplication instance before any tests run."""
        # QApplication expects sys.argv, at least with the program name
        if QApplication.instance() is None: # Check if an instance already exists
            cls.app = QApplication(sys.argv if hasattr(sys, 'argv') else ['']) 
        else: # Use existing instance
            cls.app = QApplication.instance()


    @classmethod
    def tearDownClass(cls):
        """Clean up QApplication instance after all tests run."""
        # This might not be strictly necessary for all environments,
        # but good practice for explicit cleanup.
        # cls.app.quit() # This can sometimes cause issues depending on test runner
        cls.app = None # Dereference

    def test_instantiation(self):
        """Test if PRPDWidget can be created."""
        try:
            widget = PRPDWidget()
            self.assertIsNotNone(widget)
            # If the widget has a canvas, check it too
            if hasattr(widget, 'canvas'):
                 self.assertIsNotNone(widget.canvas, "Widget canvas should be initialized.")
            if hasattr(widget, 'ax'):
                 self.assertIsNotNone(widget.ax, "Widget axes should be initialized.")
        except Exception as e:
            self.fail(f"PRPDWidget instantiation failed with error: {e}")

    def test_plot_data_with_sample_data(self):
        """Test plot_data with sample PRPD data."""
        widget = PRPDWidget()
        sample_data = generate_prpd_data(100, 'random') # Generate 100 random points
        try:
            widget.plot_data(sample_data)
            # Basic check: ensure axes have some content (e.g., title is set)
            # More specific checks would require inspecting the plot elements (hard without GUI interaction)
            if hasattr(widget, 'ax') and widget.ax is not None:
                self.assertTrue(widget.ax.get_title() == "PRPD Diagram", "Plot title was not set correctly.")
        except Exception as e:
            self.fail(f"widget.plot_data(sample_data) failed with error: {e}")

    def test_plot_data_with_empty_data(self):
        """Test plot_data with empty data."""
        widget = PRPDWidget()
        try:
            widget.plot_data([])
            # Check for "No data to display" text or similar indication
            # This is a bit tricky as it involves checking text elements on a Matplotlib Axes
            # For simplicity, we'll just check that it runs without error and title is standard.
            if hasattr(widget, 'ax') and widget.ax is not None:
                self.assertTrue(widget.ax.get_title() == "PRPD Diagram", "Plot title was not set correctly on empty data.")
                # A more robust test might check for a specific text artist.
                # Example: any(isinstance(artist, plt.Text) and artist.get_text() == "No data to display" for artist in widget.ax.artists)
                # This requires importing matplotlib.pyplot as plt
                # For now, ensuring no crash and correct title is a good start.
                # Let's check if there are any text elements on the axes, one of them should be the message.
                self.assertTrue(len(widget.ax.texts) > 0, "No text message found on empty plot.")


        except Exception as e:
            self.fail(f"widget.plot_data([]) failed with error: {e}")

    def test_clear_plot(self):
        """Test clear_plot method."""
        widget = PRPDWidget()
        # Optionally plot some data first
        sample_data = generate_prpd_data(50, 'corona')
        widget.plot_data(sample_data)
        
        try:
            widget.clear_plot()
            if hasattr(widget, 'ax') and widget.ax is not None:
                self.assertTrue(widget.ax.get_title() == "PRPD Diagram", "Plot title was not set correctly after clear_plot.")
                self.assertTrue(len(widget.ax.texts) > 0, "No text message found after clear_plot.")
                # Check if data is cleared (e.g., no scatter points)
                # Scatter points are typically stored in ax.collections
                self.assertEqual(len(widget.ax.collections), 0, "Plot data (collections) not cleared.")

        except Exception as e:
            self.fail(f"widget.clear_plot() failed with error: {e}")

if __name__ == '__main__':
    # This allows running the tests directly from this file
    unittest.main(argv=sys.argv + ['-v'], exit=False)
