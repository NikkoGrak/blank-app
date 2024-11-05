import streamlit as st
import pandas as pd
import numpy as np
import random
from geopy.distance import geodesic

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
st.title("🎈 Traveling Salesman Problem Solver")
st.write("Upload data lokasi dan sesuaikan parameter untuk algoritma TSP menggunakan GA, ACO, dan PSO")

# Input untuk mengunggah file Excel
uploaded_file = st.file_uploader("Unggah file Excel berisi data lokasi", type=["xlsx"])

if uploaded_file is not None:
    # Membaca file Excel dan menampilkan data
    data = read_excel(uploaded_file)
    st.write("Data Lokasi:")
    st.write(data)

    # Menampilkan parameter untuk setiap algoritma

    # Parameter untuk Genetic Algorithm
    st.subheader("Genetic Algorithm Parameters")
    pop_size = st.number_input("Population Size", min_value=10, max_value=500, value=50, step=10)
    elite_size = st.number_input("Elite Size", min_value=1, max_value=100, value=10, step=1)
    mutation_rate = st.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.01, step=0.01)
    generations = st.number_input("Generations", min_value=10, max_value=1000, value=100, step=10)

    # Parameter untuk Ant Colony Optimization
    st.subheader("Ant Colony Optimization Parameters")
    n_ants = st.number_input("Number of Ants", min_value=5, max_value=100, value=10, step=1)
    n_iterations = st.number_input("Iterations", min_value=10, max_value=1000, value=100, step=10)
    alpha = st.number_input("Alpha (pheromone influence)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    beta = st.number_input("Beta (distance influence)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    decay = st.slider("Pheromone Decay", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

    # Parameter untuk Particle Swarm Optimization
    st.subheader("Particle Swarm Optimization Parameters")
    num_particles = st.number_input("Number of Particles", min_value=5, max_value=100, value=10, step=1)
    num_iterations = st.number_input("Iterations", min_value=10, max_value=1000, value=100, step=10)
    w = st.number_input("Inertia Weight", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    c1 = st.number_input("Cognitive Coefficient (c1)", min_value=0.1, max_value=2.0, value=1.5, step=0.1)
    c2 = st.number_input("Social Coefficient (c2)", min_value=0.1, max_value=2.0, value=1.5, step=0.1)

    # Tombol untuk menjalankan algoritma
    if st.button("Run Genetic Algorithm"):
        ga_route, ga_distance = run_genetic_algorithm(data, pop_size, elite_size, mutation_rate, generations)
        st.write("**Genetic Algorithm Result:**")
        st.write(f"Optimal Route: {ga_route}")
        st.write(f"Total Distance: {ga_distance}")

    if st.button("Run Ant Colony Optimization"):
        aco_route, aco_distance = run_ant_colony_optimization(data, n_ants, n_iterations, alpha, beta, decay)
        st.write("**Ant Colony Optimization Result:**")
        st.write(f"Optimal Route: {aco_route}")
        st.write(f"Total Distance: {aco_distance}")

    if st.button("Run Particle Swarm Optimization"):
        pso_route, pso_distance = run_particle_swarm_optimization(data, num_particles, num_iterations, w, c1, c2)
        st.write("**Particle Swarm Optimization Result:**")
        st.write(f"Optimal Route: {pso_route}")
        st.write(f"Total Distance: {pso_distance}")

else:
    st.write("Silakan unggah file Excel untuk memulai.")
