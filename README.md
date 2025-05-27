# Portable GIS Partial Discharge Detector Software

## Purpose

This project is a host computer software designed for the detection and analysis of Partial Discharge (PD) in Gas Insulated Switchgear (GIS). It provides tools for visualizing PD data through PRPD (Phase Resolved Partial Discharge) and PRPS (Phase Resolved Pulse Sequence) diagrams. The software uses simulated data that mimics the characteristics of real-world partial discharge events.

## Features

-   **PRPD (Phase Resolved Partial Discharge) Display:** Visualizes PD magnitude against the phase angle of the AC cycle.
-   **PRPS (Phase Resolved Pulse Sequence) Display:** Shows PD magnitude over time, with pulses colored by their phase angle.
-   **Data Simulation:** Generates simulated PD data for various types of discharges:
    -   Random
    -   Corona
    -   Internal Void
    -   Surface Discharge
-   **Interactive UI:** Allows users to select discharge type, number of PD events, and duration for simulation, and view the corresponding plots.

## Project Structure

The project consists of the following key files:

-   `main_app.py`: The main application script that launches the PyQt-based GUI. It handles user interactions and integrates the other modules.
-   `pd_data_simulation.py`: Contains functions for generating simulated PRPD and PRPS data, mimicking different types of partial discharges.
-   `prpd_display.py`: A PyQt widget that uses Matplotlib to render the PRPD diagram.
-   `prps_display.py`: A PyQt widget that uses Matplotlib to render the PRPS diagram.
-   `requirements.txt`: Lists the Python dependencies required for the project.
-   `test_pd_data_simulation.py`: Unit tests for the data simulation module.
-   `test_prpd_display.py`: Unit tests for the PRPD display widget.
-   `test_prps_display.py`: Unit tests for the PRPS display widget.

## Setup Instructions

1.  **Create a Virtual Environment (Recommended):**
    Open your terminal or command prompt and navigate to the project directory. Create a virtual environment by running:
    ```bash
    python -m venv venv
    ```

2.  **Activate the Virtual Environment:**
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    With the virtual environment activated, install the required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Usage Instructions

1.  **Run the Application:**
    Ensure your virtual environment is activated and you are in the project's root directory. Launch the application by running:
    ```bash
    python main_app.py
    ```

2.  **Using the Interface:**
    -   The main window will display "Simulation Controls" on the left and a tabbed area for "PRPD" and "PRPS" plots on the right.
    -   **Simulation Controls:**
        -   **Number of Points/Events:** Set the desired number of PD events to simulate.
        -   **Discharge Type:** Select the type of partial discharge to simulate from the dropdown menu (Random, Corona, Internal Void, Surface Discharge).
        -   **Duration (seconds for PRPS):** Set the time duration over which the PRPS events will be generated.
        -   **Generate Data Button:** Click this button to generate new data based on the selected parameters. The PRPD and PRPS plots will update accordingly.
    -   **Plots:**
        -   Click on the "PRPD" or "PRPS" tabs to view the respective diagrams.

## Running Unit Tests

To run the automated unit tests, ensure your virtual environment is activated and all dependencies are installed. Navigate to the project's root directory in your terminal and run:

```bash
python -m unittest discover
```
This command will automatically find and execute all tests within the `test_*.py` files.
