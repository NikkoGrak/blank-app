import streamlit as st
import pandas as pd
import numpy as np
import random
from geopy.distance import geodesic

from data_utils import read_waypoints_from_excel
from ant_colony import AntColony
from genetic import GA_TSP
from particle_swarm import PSO_TSP
from visualization import plot_route_with_satelite
import time

# Fungsi untuk membaca data dari file excel
def read_excel(file):
    df = pd.read_excel(file)
    return df

# Fungsi jarak antara dua titik untuk TSP
def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers

# TSP Algoritma Genetika, ACO, dan PSO (dummy functions)
def run_genetic_algorithm(data, pop_size, elite_size, mutation_rate, generations):
    # Dummy function untuk contoh, masukkan implementasi TSP GA yang sesuai di sini
    return "Optimal Route by Genetic Algorithm", "Total Distance GA"

def run_ant_colony_optimization(data, n_ants, n_iterations, alpha, beta, decay):
    # Dummy function untuk contoh, masukkan implementasi TSP ACO yang sesuai di sini
    return "Optimal Route by Ant Colony Optimization", "Total Distance ACO"

def run_particle_swarm_optimization(data, num_particles, num_iterations, w, c1, c2):
    # Dummy function untuk contoh, masukkan implementasi TSP PSO yang sesuai di sini
    return "Optimal Route by Particle Swarm Optimization", "Total Distance PSO"



# Streamlit UI
st.title("📍 Traveling Salesman Problem Solver 🛵")
st.write("Upload data lokasi dan sesuaikan parameter untuk algoritma TSP menggunakan GA, ACO, dan PSO")

# Input untuk mengunggah file Excel
uploaded_file = st.file_uploader("Unggah file Excel berisi data lokasi", type=["xlsx"])




if uploaded_file is not None:
    # Inisiasi titik awal dan titik akhir (lat, lon)
    start_point = (-6.192649980767408, 106.83733906793265)
    end_point = (-6.192649980767408, 106.83733906793265)
    # Membaca file Excel dan menampilkan data
    data = read_excel(uploaded_file)
    st.write("Data Lokasi:")
    st.write(data)

    
    #column for widget AG, ACO and PSO
    col1,coldiv1, col2 ,coldiv2, col3 = st.columns([2, 1, 2, 1, 2])
    
# Menampilkan parameter untuk setiap algoritma

    # Parameter untuk Genetic Algorithm
    col1.subheader("Genetic Algorithm Parameters")
    pop_size = col1.number_input("Population Size", min_value=10, max_value=500, value=50, step=10)
    elite_size = col1.number_input("Elite Size", min_value=1, max_value=100, value=10, step=1)
    mutation_rate = col1.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.01, step=0.01)
    generations = col1.number_input("Generations", min_value=10, max_value=1000, value=100, step=10)

    
    st.markdown("""
    <style>
    .vertical-divider {
        height: 500px;
        border-left: 2px solid #ddd;
        margin: 0 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    coldiv1.markdown('<div class="vertical-divider"></div>', unsafe_allow_html=True)
    
    # Parameter untuk Ant Colony Optimization
    col2.subheader("Ant Colony Optimization Parameters")
    n_ants = col2.number_input("Number of Ants", min_value=5, max_value=100, value=10, step=1)
    # Input untuk n_best, dengan maksimal sama dengan n_ants
    n_best = col2.number_input("Number of Best Ants", min_value=1, max_value=n_ants, value=min(5, n_ants), step=1)
    n_iterations = col2.number_input("IterationsN", min_value=10, max_value=1000, value=100, step=10)
    alpha = col2.number_input("Alpha (pheromone influence)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    beta = col2.number_input("Beta (distance influence)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    decay = col2.slider("Pheromone Decay", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

    
    st.markdown("""
    <style>
    .vertical-divider {
        height: 500px;
        border-left: 2px solid #ddd;
        margin: 0 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    coldiv2.markdown('<div class="vertical-divider"></div>', unsafe_allow_html=True)
    
    # Parameter untuk Particle Swarm Optimization
    col3.subheader("Particle Swarm Optimization Parameters")
    num_particles = col3.number_input("Number of Particles", min_value=5, max_value=100, value=10, step=1)
    num_iterations = col3.number_input("IterationsNUM", min_value=10, max_value=1000, value=100, step=10)
    w = col3.number_input("Inertia Weight", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    c1 = col3.number_input("Cognitive Coefficient (c1)", min_value=0.1, max_value=2.0, value=1.5, step=0.1)
    c2 = col3.number_input("Social Coefficient (c2)", min_value=0.1, max_value=2.0, value=1.5, step=0.1)

    # Tombol untuk menjalankan algoritma
    if col1.button("Run Genetic Algorithm"):
        start_time = time.time()
        ga_route, ga_distance = run_genetic_algorithm(data, pop_size, elite_size, mutation_rate, generations)
        col1.write("**Genetic Algorithm Result:**")
        col1.write(f"Optimal Route: {ga_route}")
        col1.write(f"Total Distance: {ga_distance}")
        waypoints = read_waypoints_from_excel(uploaded_file)
        waypoints_coordinates = [(item.latitude, item.longitude) for item in waypoints]

        ga_tsp = GA_TSP(waypoints_coordinates, start_point, end_point, pop_size, elite_size, mutation_rate, generations)
        best_route_indices, best_distance = ga_tsp.optimize()

        best_route_coordinates = [waypoints_coordinates[i] for i in best_route_indices]
        
        col1.write(f"Optimal Route: {best_route_indices}")
        col1.write(f"Total Distance: {best_distance} km")

        end_time = time.time()
        computation_time = end_time - start_time
        col1.write(f"Waktu komputasi: {computation_time:.2f} detik")

        plot_route_with_satelite(best_route_indices, waypoints_coordinates, start_point, end_point)

    

    if col2.button("Run Ant Colony Optimization"):
        # aco_route, aco_distance = run_ant_colony_optimization(data, n_ants, n_iterations, alpha, beta, decay)
        # Membaca waypoint dari file Excel
        waypoints = read_waypoints_from_excel(uploaded_file)
        waypoints_coordinates = [(item.latitude, item.longitude) for item in waypoints]
        
        
        # Menjalankan algoritma ACO untuk TSP
        aco = AntColony(waypoints_coordinates, start_point, end_point, n_ants, n_best, n_iterations, decay, alpha, beta)
        best_route_indices, best_distance = aco.optimize()
        col2.write("**Ant Colony Optimization Result:**")
        col2.write(f"Optimal Route: {best_route_indices}")
        col2.write(f"Total Distance: {best_distance} km")
        # Menampilkan rute dalam plot
        plot_route_with_satelite(best_route_indices, waypoints_coordinates, start_point, end_point)


    if col3.button("Run Particle Swarm Optimization"):
        pso_route, pso_distance = run_particle_swarm_optimization(data, num_particles, num_iterations, w, c1, c2)
        col3.write("**Particle Swarm Optimization Result:**")
        # Membaca waypoint dari file Excel
        waypoints = read_waypoints_from_excel(uploaded_file)
        waypoints_coordinates = [(item.latitude, item.longitude) for item in waypoints]

        pso_tsp = PSO_TSP(waypoints_coordinates, start_point, end_point)
        best_route_indices, best_distance = pso_tsp.optimize()
        
        col3.write(f"Optimal Route: {best_route_indices}")
        col3.write(f"Total Distance: {best_distance}")
        plot_route_with_satelite(best_route_indices, waypoints_coordinates, start_point, end_point)

else:
    st.write("Silakan unggah file Excel untuk memulai.")
