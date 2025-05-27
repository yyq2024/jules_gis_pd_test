import unittest
import numpy as np # For potential use if checking types, not strictly required by problem
from pd_data_simulation import generate_prpd_data, generate_prps_data

class TestPDDataSimulation(unittest.TestCase):

    def test_generate_prpd_data_random(self):
        num_points = 100
        data = generate_prpd_data(num_points, 'random')
        self.assertEqual(len(data), num_points)
        for phase, magnitude in data:
            self.assertTrue(0 <= phase <= 360)
            self.assertTrue(0 <= magnitude <= 100) # As defined in simulation

    def test_generate_prpd_data_other_types(self):
        num_points = 50
        discharge_types = ['corona', 'internal_void', 'surface_discharge']
        for dtype in discharge_types:
            with self.subTest(discharge_type=dtype):
                data = generate_prpd_data(num_points, dtype)
                self.assertEqual(len(data), num_points)
                if num_points > 0: # Only check ranges if data is expected
                    for phase, magnitude in data:
                        self.assertTrue(0 <= phase <= 360, f"Phase {phase} out of range for {dtype}")
                        self.assertTrue(0 <= magnitude <= 100, f"Magnitude {magnitude} out of range for {dtype}")
                else:
                    self.assertEqual(len(data),0)


    def test_generate_prpd_data_zero_points(self):
        data = generate_prpd_data(0, 'random')
        self.assertEqual(len(data), 0)

    def test_generate_prpd_data_invalid_type(self):
        with self.assertRaises(ValueError):
            generate_prpd_data(10, 'invalid_type')

    def test_generate_prps_data_random(self):
        num_events = 100
        duration_seconds = 10
        data = generate_prps_data(num_events, duration_seconds, 'random')
        self.assertEqual(len(data), num_events)
        if num_events > 0:
            for timestamp, phase, magnitude in data:
                self.assertTrue(0 <= timestamp <= duration_seconds, f"Timestamp {timestamp} out of range 0-{duration_seconds}")
                self.assertTrue(0 <= phase <= 360)
                self.assertTrue(0 <= magnitude <= 100)

    def test_generate_prps_data_other_types(self):
        num_events = 50
        duration_seconds = 5
        discharge_types = ['corona', 'internal_void', 'surface_discharge']
        for dtype in discharge_types:
            with self.subTest(discharge_type=dtype):
                data = generate_prps_data(num_events, duration_seconds, dtype)
                self.assertEqual(len(data), num_events)
                if num_events > 0:
                    for timestamp, phase, magnitude in data:
                        self.assertTrue(0 <= timestamp <= duration_seconds, f"Timestamp {timestamp} out of range for {dtype}")
                        self.assertTrue(0 <= phase <= 360, f"Phase {phase} out of range for {dtype}")
                        self.assertTrue(0 <= magnitude <= 100, f"Magnitude {magnitude} out of range for {dtype}")

    def test_generate_prps_data_zero_events(self):
        data = generate_prps_data(0, 10, 'random')
        self.assertEqual(len(data), 0)

    def test_generate_prps_data_zero_duration(self):
        num_events = 100
        # With duration 0, timestamps should all be 0.
        data = generate_prps_data(num_events, 0, 'random')
        self.assertEqual(len(data), num_events)
        if num_events > 0:
            for timestamp, phase, magnitude in data:
                self.assertEqual(timestamp, 0)
                self.assertTrue(0 <= phase <= 360)
                self.assertTrue(0 <= magnitude <= 100)
    
    def test_generate_prps_data_zero_events_zero_duration(self):
        data = generate_prps_data(0, 0, 'random')
        self.assertEqual(len(data), 0)

    def test_generate_prps_data_invalid_type(self):
        with self.assertRaises(ValueError):
            generate_prps_data(10, 10, 'invalid_type')

if __name__ == '__main__':
    unittest.main()
