import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_critical_speed(distance_3min, distance_12min):
    """
    Calculate critical speed based on 3-minute and 12-minute time trials.
    
    Parameters:
    distance_3min (float): Distance covered in 3 minutes (meters)
    distance_12min (float): Distance covered in 12 minutes (meters)
    
    Returns:
    tuple: (critical_speed_ms, critical_speed_kmh, critical_speed_minkm)
    """
    # Time in seconds
    time_3min = 180
    time_12min = 720
    
    # Calculate critical speed (m/s)
    critical_speed_ms = (distance_12min - distance_3min) / (time_12min - time_3min)
    
    # Convert to km/h
    critical_speed_kmh = critical_speed_ms * 3.6
    # Convert to min/km
    critical_speed_minkm = 1000 / critical_speed_ms / 60
    
    return critical_speed_ms, critical_speed_kmh, critical_speed_minkm

def format_pace(min_per_km):
    minutes = int(min_per_km)
    seconds = int(round((min_per_km - minutes) * 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d} min/km"

def main():
    st.title("Critical Running Speed Calculator")
    st.write("Calculate your critical speed based on 3-minute and 12-minute time trials")
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        distance_3min = st.number_input(
            "Distance covered in 3 minutes (meters)", 
            min_value=0.0, 
            max_value=5000.0, 
            value=1000.0,
            step=1.0
        )
    
    with col2:
        distance_12min = st.number_input(
            "Distance covered in 12 minutes (meters)", 
            min_value=0.0, 
            max_value=10000.0, 
            value=3000.0,
            step=1.0
        )
    
    if st.button("Calculate Critical Speed"):
        if distance_12min <= distance_3min:
            st.error("12-minute distance must be greater than 3-minute distance")
        else:
            cs_ms, cs_kmh, cs_minkm = calculate_critical_speed(distance_3min, distance_12min)
            
            # Display results
            st.subheader("Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Critical Speed (m/s)", f"{cs_ms:.2f} m/s")
            
            with col2:
                st.metric("Critical Speed (km/h)", f"{cs_kmh:.2f} km/h")
            
            with col3:
                st.metric("Critical Speed Pace", format_pace(cs_minkm))
            
            # Additional information
            st.subheader("Interpretation")
            st.write(f"""
            **Critical Speed**: {cs_kmh:.2f} km/h (or {format_pace(cs_minkm)}) represents your theoretical maximum sustainable pace.\n
            This is the highest intensity you can maintain without accumulating fatigue.\n
            **Note**: These calculations are based on established critical speed theory from 
            exercise physiology research. Results should be used as guidance alongside 
            other training metrics and professional advice.
            """)

if __name__ == "__main__":
    main()
