
#particle_swarm.py

import streamlit as st
import pandas as pd
import numpy as np
import random
from geopy.distance import geodesic
from data_utils import read_waypoints_from_excel

# Fungsi untuk menghitung jarak antara dua titik menggunakan geodesic (lat, lon)
def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers

# Fungsi untuk menghitung total jarak dalam rute
def total_distance(route, start_point, end_point):
    distance = distance_between_points(start_point, route[0])
    for i in range(len(route) - 1):
        distance += distance_between_points(route[i], route[i + 1])
    distance += distance_between_points(route[-1], end_point)
    return distance

# Kelas PSO untuk TSP
class PSO_TSP:
    def __init__(self, waypoints, start_point, end_point, num_particles=50, num_iterations=100, alpha=1, beta=2):
        self.waypoints = waypoints
        self.start_point = start_point
        self.end_point = end_point
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.alpha = alpha  # Faktor inersia
        self.beta = beta    # Faktor pembelajaran

        self.distances = self.calculate_distances_matrix()
        self.particles = [random.sample(range(len(waypoints)), len(waypoints)) for _ in range(num_particles)]
        self.p_best = self.particles[:]
        self.g_best = min(self.particles, key=lambda p: self.route_distance(p))
        self.velocities = [random.sample(range(len(waypoints)), len(waypoints)) for _ in range(num_particles)]
    def calculate_distances_matrix(self):
        num_waypoints = len(self.waypoints)
        distances = np.zeros((num_waypoints, num_waypoints))
        for i in range(num_waypoints):
            for j in range(i + 1, num_waypoints):
                distances[i][j] = distance_between_points(self.waypoints[i], self.waypoints[j])
                distances[j][i] = distances[i][j]
        return distances

    def route_distance(self, route):
        waypoints_order = [self.waypoints[i] for i in route]
        return total_distance(waypoints_order, self.start_point, self.end_point)
    def update_particles(self):
        for i, particle in enumerate(self.particles):
            # Update kecepatan
            self.velocities[i] = random.sample(range(len(self.waypoints)), len(self.waypoints))
            
            # Pembaruan posisi partikel berdasarkan kecepatan
            self.particles[i] = self.apply_velocity(particle, self.velocities[i])

            # Perbarui personal best (p_best)
            if self.route_distance(self.particles[i]) < self.route_distance(self.p_best[i]):
                self.p_best[i] = self.particles[i]

        # Perbarui global best (g_best)
        self.g_best = min(self.p_best, key=lambda p: self.route_distance(p))

    def apply_velocity(self, particle, velocity):
        # Terapkan pertukaran posisi berdasarkan kecepatan
        for swap in velocity:
            i, j = swap, (swap + 1) % len(particle)
            particle[i], particle[j] = particle[j], particle[i]
        return particle

    def optimize(self):
        best_distance = float('inf')
        for iteration in range(self.num_iterations):
            self.update_particles()
            g_best_distance = self.route_distance(self.g_best)

            if g_best_distance < best_distance:
                best_distance = g_best_distance
                best_route = self.g_best

            print(f"Iterasi {iteration+1}/{self.num_iterations}, Jarak Terbaik: {best_distance:.2f} km")

        return best_route, best_distance
