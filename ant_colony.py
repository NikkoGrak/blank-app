# ant_colony.py
import streamlit as st
import numpy as np
import random
from geopy.distance import geodesic
from data_utils import read_waypoints_from_excel

def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers

def total_distance(route, start_point, end_point):
    distance = distance_between_points(start_point, route[0])
    for i in range(len(route) - 1):
        distance += distance_between_points(route[i], route[i + 1])
    distance += distance_between_points(route[-1], end_point)
    return distance

class AntColony:
    def __init__(self, waypoints, start_point, end_point, n_ants, n_best, n_iterations, decay, alpha, beta):
        self.waypoints = waypoints
        self.start_point = start_point
        self.end_point = end_point
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        
        self.distances = self.calculate_distances_matrix()
        self.pheromone = np.ones(self.distances.shape) / len(waypoints)

    def calculate_distances_matrix(self):
        num_waypoints = len(self.waypoints)
        distances = np.zeros((num_waypoints, num_waypoints))
        for i in range(num_waypoints):
            for j in range(i + 1, num_waypoints):
                distances[i][j] = distance_between_points(self.waypoints[i], self.waypoints[j])
                distances[j][i] = distances[i][j]
        return distances

    def route_distance(self, route):
        return total_distance([self.waypoints[i] for i in route], self.start_point, self.end_point)

    def pheromone_update(self, all_routes, all_distances):
        self.pheromone *= self.decay
        sorted_routes = sorted(zip(all_routes, all_distances), key=lambda x: x[1])
        for route, distance in sorted_routes[:self.n_best]:
            for i in range(len(route) - 1):
                self.pheromone[route[i]][route[i + 1]] += 1.0 / distance
            self.pheromone[route[-1]][route[0]] += 1.0 / distance

    def select_next_waypoint(self, pheromone_row, distance_row, visited):
        # Membuat array boolean untuk visited
        visited_mask = np.zeros(len(pheromone_row), dtype=bool)
        visited_mask[list(visited)] = True  # Set true untuk indeks yang sudah dikunjungi
        pheromone_row = np.copy(pheromone_row)
        pheromone_row[visited_mask] = 0  # Set feromon pada titik yang sudah dikunjungi ke 0

        # Avoid division by zero by adding a small epsilon to distance_row
        epsilon = 1e-10
        distance_row = np.where(distance_row == 0, epsilon, distance_row)  # Replace zero distances with epsilon

        # Menghitung probabilitas dengan memperhitungkan alpha dan beta
        with np.errstate(divide='ignore', invalid='ignore'):
            probabilities = (pheromone_row ** self.alpha) * ((1.0 / distance_row) ** self.beta)

        # Create a list of unvisited points
        unvisited = [i for i in range(len(pheromone_row)) if i not in visited]

        # If all probabilities are zero or contain NaN values, choose randomly among unvisited nodes
        if np.isnan(probabilities).any() or probabilities.sum() == 0:
            return random.choice(unvisited)

        # Normalisasi probabilitas
        probabilities /= probabilities.sum()

        # Pilih titik berikutnya berdasarkan probabilitas
        return np.random.choice(len(pheromone_row), p=probabilities)

    def generate_route(self):
        route = []
        visited = set()
        current = random.randint(0, len(self.waypoints) - 1)
        route.append(current)
        visited.add(current)
        while len(visited) < len(self.waypoints):
            next_city = self.select_next_waypoint(self.pheromone[current], self.distances[current], visited)
            route.append(next_city)
            visited.add(next_city)
            current = next_city
        return route

    def optimize(self):
        #column for widget AG, ACO and PSO
        # col1, col2 , col3 = st.columns(3)
        best_route = None
        best_distance = float('inf')
        for iteration in range(self.n_iterations):
            all_routes = [self.generate_route() for _ in range(self.n_ants)]
            all_distances = [self.route_distance(route) for route in all_routes]

            self.pheromone_update(all_routes, all_distances)
            shortest_distance = min(all_distances)
            if shortest_distance < best_distance:
                best_distance = shortest_distance
                best_route = all_routes[all_distances.index(shortest_distance)]
            print(f"Iterasi {iteration+1}/{self.n_iterations}, Jarak Terbaik: {best_distance:.2f} km")
            # col2.write(f"Iterasi {iteration+1}/{self.n_iterations}, Jarak Terbaik: {best_distance:.2f} km")
        
        return best_route, best_distance
