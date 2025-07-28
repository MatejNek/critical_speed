import streamlit as st
import numpy as np

def calculate_critical_speed(distance_3min, distance_12min):
    """
    Calculate critical speed based on 3-minute and 12-minute time trials.

    Returns:
    - critical_speed_ms: m/s
    - critical_speed_kmh: km/h
    - critical_speed_minkm: min/km
    """
    time_3min = 180  # seconds
    time_12min = 720  # seconds

    # Critical speed in m/s
    critical_speed_ms = (distance_12min - distance_3min) / (time_12min - time_3min)
    critical_speed_kmh = critical_speed_ms * 3.6
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

            # Training zone definitions based on percentages of critical speed
            # Your logic: Z1 = slowest (>160%), Z5 = fastest (85–105%)
            zone_percentages = [1.60, 1.40, 1.25, 1.15, 1.05, 0.85]  # descending speed logic
            # We divide CS by percentage to get slower speed at higher %CS
            boundary_speeds_ms = [cs_ms / pct for pct in zone_percentages]
            boundary_paces = [1000 / s / 60 for s in boundary_speeds_ms]  # min/km

            zones = [
                {"Zone": "Z1 (>160%)",        "Pace Range": f"> {format_pace(boundary_paces[0])}"},
                {"Zone": "Z2 (140-160%)",     "Pace Range": f"{format_pace(boundary_paces[1])} - {format_pace(boundary_paces[0])}"},
                {"Zone": "Z3 (125-140%)",     "Pace Range": f"{format_pace(boundary_paces[2])} - {format_pace(boundary_paces[1])}"},
                {"Zone": "Z4 (115-125%)",     "Pace Range": f"{format_pace(boundary_paces[3])} - {format_pace(boundary_paces[2])}"},
                {"Zone": "Z5 (105-115%)",      "Pace Range": f"{format_pace(boundary_paces[4])} - {format_pace(boundary_paces[3])}"},
                {"Zone": "Z6 (85-105%)",      "Pace Range": f"{format_pace(boundary_paces[5])} - {format_pace(boundary_paces[4])}"},
            ]

            st.subheader("Training Zones (based on Critical Speed %)")
            st.table(zones)

            # Explanation
            st.subheader("Interpretation")
            st.write(f"""
            **Critical Speed**: {cs_kmh:.2f} km/h (or {format_pace(cs_minkm)}) is your theoretical maximal sustainable pace.\n
    
            - **Z6 (85–105%)**: Fastest, high-intensity intervals\n
            - **Z5 (105–115%)**: Threshold\n
            - **Z4 (115–125%)**: tempo\n
            - **Z3 (125–140%)**: Aerobic endurance\n
            - **Z2 (140–160%)**: Easy running\n
            - **Z1 (>160%)**: Recovery or very easy pace\n
            """)

if __name__ == "__main__":
    main()
