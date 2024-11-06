# ant_colony.py

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
    def __init__(self, waypoints, start_point, end_point, n_ants=10, n_best=50, n_iterations=100, decay=0.95, alpha=1, beta=2):
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
        visited_mask = np.zeros(len(pheromone_row), dtype=bool)
        visited_mask[list(visited)] = True
        pheromone_row = np.copy(pheromone_row)
        pheromone_row[visited_mask] = 0
        epsilon = 1e-10
        distance_row = np.where(distance_row == 0, epsilon,
