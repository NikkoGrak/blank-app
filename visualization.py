 

import matplotlib.pyplot as plt
import streamlit as st

def plot_route_with_satelite(best_route, waypoints, start_point, end_point):
    latitudes = [start_point[0]] + [waypoints[i][0] for i in best_route] + [end_point[0]]
    longitudes = [start_point[1]] + [waypoints[i][1] for i in best_route] + [end_point[1]]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(longitudes, latitudes, 'o-', markersize=8, label='Route')
    ax.plot(start_point[1], start_point[0], 'ro', markersize=10, label='Start/End Point')
    for i, (lat, lon) in enumerate(zip(latitudes, longitudes)):
        ax.annotate(f'{i}', (lon, lat))
    ax.set_title("Best Route for TSP with Ant Colony Optimize")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    # plt.show()
    st.pyplot(fig)
