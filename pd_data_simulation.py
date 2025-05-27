import numpy as np
import random

def generate_prpd_data(num_points, discharge_type='random'):
    """
    Generates Phase Resolved Partial Discharge (PRPD) data.

    Args:
        num_points (int): The number of data points to generate.
        discharge_type (str): Type of discharge ('random', 'corona', 
                                'internal_void', 'surface_discharge').

    Returns:
        list: A list of tuples, where each tuple is (phase_angle, magnitude).
    """
    prpd_data = []
    
    if discharge_type == 'random':
        # Generate phase angles uniformly between 0 and 360 degrees
        phase_angles = np.random.uniform(0, 360, num_points)
        # Generate magnitudes uniformly between 0 and 100
        magnitudes = np.random.uniform(0, 100, num_points)
    
    elif discharge_type == 'corona':
        # Corona discharges typically cluster at 0-90 and 180-270 degrees
        # We'll use a von Mises distribution for phase, centered at 45 and 225 degrees
        # and a normal distribution for magnitude
        kappa = 10 # Concentration parameter for von Mises
        loc1, loc2 = np.deg2rad(45), np.deg2rad(225) # Centers for phase
        
        # Generate points in two clusters
        num_points_cluster1 = num_points // 2
        num_points_cluster2 = num_points - num_points_cluster1
        
        phase_angles1 = np.random.vonmises(loc1, kappa, num_points_cluster1)
        phase_angles2 = np.random.vonmises(loc2, kappa, num_points_cluster2)
        phase_angles = np.concatenate((phase_angles1, phase_angles2))
        
        # Convert phase angles from radians to degrees and normalize to 0-360
        phase_angles = np.rad2deg(phase_angles) % 360
        
        magnitudes = np.random.normal(50, 15, num_points) # Mean 50, Std 15
        magnitudes = np.clip(magnitudes, 0, 100) # Clip to 0-100 range

    elif discharge_type == 'internal_void':
        # Internal void discharges often form symmetrical clusters around AC peaks
        # (e.g., 60-120 and 240-300 degrees)
        # We'll use a von Mises distribution for phase, centered at 90 and 270 degrees
        # and a wider normal distribution for magnitude
        kappa = 5 # Concentration parameter for von Mises
        loc1, loc2 = np.deg2rad(90), np.deg2rad(270) # Centers for phase

        # Generate points in two clusters
        num_points_cluster1 = num_points // 2
        num_points_cluster2 = num_points - num_points_cluster1

        phase_angles1 = np.random.vonmises(loc1, kappa, num_points_cluster1)
        phase_angles2 = np.random.vonmises(loc2, kappa, num_points_cluster2)
        phase_angles = np.concatenate((phase_angles1, phase_angles2))

        # Convert phase angles from radians to degrees and normalize to 0-360
        phase_angles = np.rad2deg(phase_angles) % 360
        
        magnitudes = np.random.normal(60, 25, num_points) # Mean 60, Std 25 (wider spread)
        magnitudes = np.clip(magnitudes, 0, 100) # Clip to 0-100 range

    elif discharge_type == 'surface_discharge':
        # Surface discharges can be scattered, often skewed to one half of the AC cycle
        # We'll use a von Mises distribution for phase, centered at 180 degrees (one half)
        # and a beta distribution for magnitude to create a skewed distribution
        kappa = 2 # Lower concentration for more scatter
        loc = np.deg2rad(180) # Center for phase

        phase_angles = np.random.vonmises(loc, kappa, num_points)
        phase_angles = np.rad2deg(phase_angles) % 360
        
        # Beta distribution for skewed magnitudes (e.g., more lower magnitude events)
        magnitudes = np.random.beta(2, 5, num_points) * 100 
        magnitudes = np.clip(magnitudes, 0, 100)

    else:
        raise ValueError(f"Unknown discharge_type: {discharge_type}")

    prpd_data = list(zip(phase_angles, magnitudes))
    return prpd_data


def generate_prps_data(num_events, duration_seconds, discharge_type='random'):
    """
    Generates Phase Resolved Pulse Sequence (PRPS) data.

    Args:
        num_events (int): The total number of PD events to simulate.
        duration_seconds (int): The total duration over which the events occur.
        discharge_type (str): Type of discharge, influencing phase and magnitude.

    Returns:
        list: A list of tuples, where each tuple is (time_stamp, phase_angle, magnitude).
    """
    prps_data = []

    # Generate timestamps
    # Using a Poisson process for event arrival times (more realistic for some PD phenomena)
    # The rate lambda is num_events / duration_seconds
    if duration_seconds > 0 and num_events > 0:
        event_rate = num_events / duration_seconds
        inter_arrival_times = np.random.exponential(1/event_rate, num_events)
        time_stamps = np.cumsum(inter_arrival_times)
        # Ensure timestamps are within the duration and we have the correct number of events
        time_stamps = time_stamps[time_stamps <= duration_seconds]
        # If not enough events due to time limit, fill with uniform random or regenerate
        while len(time_stamps) < num_events:
             # simple fill with random for remaining, could be more sophisticated
            additional_stamps = np.random.uniform(0, duration_seconds, num_events - len(time_stamps))
            time_stamps = np.concatenate((time_stamps, additional_stamps))
            time_stamps = np.sort(time_stamps[:num_events]) # ensure sorted and correct count

    elif num_events > 0 : # if duration is zero, place all events at t=0
        time_stamps = np.zeros(num_events)
    else: # No events
        time_stamps = np.array([])


    # Generate phase and magnitude using the PRPD function logic
    # We call generate_prpd_data to get the phase and magnitude pairs
    # This is a simplification; in reality, each pulse in PRPS is an independent event
    # but their collective distribution over phase/magnitude follows PRPD patterns.
    
    if num_events > 0:
        # Get phase and magnitude for each event
        # We need to pass num_events to generate_prpd_data
        phase_magnitude_data = generate_prpd_data(num_events, discharge_type)
        
        for i in range(len(time_stamps)): # Iterate up to the number of valid timestamps
            if i < len(phase_magnitude_data): # Check if phase_magnitude_data has enough elements
                 phase_angle, magnitude = phase_magnitude_data[i]
                 prps_data.append((time_stamps[i], phase_angle, magnitude))
            else: # Fallback if phase_magnitude_data is shorter (should not happen with current logic)
                # Generate random phase/magnitude as a fallback
                phase_angle = np.random.uniform(0,360)
                magnitude = np.random.uniform(0,100)
                prps_data.append((time_stamps[i], phase_angle, magnitude))

    return prps_data

if __name__ == '__main__':
    # Example usage:
    # PRPD Data
    random_prpd = generate_prpd_data(500, 'random')
    print(f"Generated {len(random_prpd)} random PRPD points.")
    # print(random_prpd[:5])

    corona_prpd = generate_prpd_data(500, 'corona')
    print(f"Generated {len(corona_prpd)} corona PRPD points.")
    # print(corona_prpd[:5])

    internal_void_prpd = generate_prpd_data(500, 'internal_void')
    print(f"Generated {len(internal_void_prpd)} internal void PRPD points.")
    # print(internal_void_prpd[:5])

    surface_discharge_prpd = generate_prpd_data(500, 'surface_discharge')
    print(f"Generated {len(surface_discharge_prpd)} surface discharge PRPD points.")
    # print(surface_discharge_prpd[:5])

    # PRPS Data
    random_prps = generate_prps_data(100, 60, 'random') # 100 events in 60 seconds
    print(f"Generated {len(random_prps)} random PRPS points.")
    # print(random_prps[:5])
    
    corona_prps = generate_prps_data(100, 60, 'corona')
    print(f"Generated {len(corona_prps)} corona PRPS points.")
    # print(corona_prps[:5])

    # Test with zero duration
    zero_duration_prps = generate_prps_data(50, 0, 'corona')
    print(f"Generated {len(zero_duration_prps)} PRPS points with zero duration.")
    # print(zero_duration_prps[:5])
    
    # Test with zero events
    zero_events_prps = generate_prps_data(0, 60, 'random')
    print(f"Generated {len(zero_events_prps)} PRPS points with zero events.")
    # print(zero_events_prps)

    # Test with more events than can typically fit if inter_arrival_times are too large
    # This tests the refill logic for timestamps
    many_events_short_duration_prps = generate_prps_data(1000, 10, 'random')
    print(f"Generated {len(many_events_short_duration_prps)} PRPS points for many events in short duration.")
    # print(many_events_short_duration_prps[:5])

    # Test error case for generate_prpd_data
    try:
        error_prpd = generate_prpd_data(100, 'unknown_type')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test error case for generate_prps_data (via generate_prpd_data)
    try:
        error_prps = generate_prps_data(100, 60, 'unknown_type')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("Example usage complete.")
