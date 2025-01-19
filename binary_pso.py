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

# Kelas BPSO untuk TSP
class BPSO_TSP:
    def __init__(self, waypoints, start_point, end_point, num_particles, num_iterations, inertia_weight, c1, c2):
        self.waypoints = waypoints
        self.start_point = start_point
        self.end_point = end_point
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.inertia_weight = inertia_weight
        self.c1 = c1  # Koefisien kognitif
        self.c2 = c2  # Koefisien sosial

        self.num_waypoints = len(self.waypoints)
        self.distances = self.calculate_distances_matrix()

        # Inisialisasi posisi partikel sebagai array biner
        self.particles = [self.initialize_particle() for _ in range(num_particles)]
        self.velocities = [self.initialize_velocity() for _ in range(num_particles)]

        # Inisialisasi personal best dan global best
        self.p_best = self.particles[:]
        self.g_best = min(self.particles, key=lambda p: self.route_distance(self.decode_route(p)))

    def calculate_distances_matrix(self):
        distances = np.zeros((self.num_waypoints, self.num_waypoints))
        for i in range(self.num_waypoints):
            for j in range(i + 1, self.num_waypoints):
                distances[i][j] = distance_between_points(self.waypoints[i], self.waypoints[j])
                distances[j][i] = distances[i][j]
        return distances

    def initialize_particle(self):
        # Membuat partikel biner dengan panjang sesuai jumlah waypoints
        return np.random.randint(2, size=self.num_waypoints)

    def initialize_velocity(self):
        # Kecepatan awal adalah array float dalam rentang [0, 1]
        return np.random.random(self.num_waypoints)

    def decode_route(self, particle):
        # Decode partikel biner menjadi rute berdasarkan posisi dengan nilai 1
        return [self.waypoints[i] for i in range(len(particle)) if particle[i] == 1]

    def route_distance(self, route):
        if len(route) < 2:  # Rute tidak valid jika kurang dari 2 waypoint
            return float('inf')
        return total_distance(route, self.start_point, self.end_point)

    def update_velocity(self, particle, velocity, p_best, g_best):
        r1, r2 = random.random(), random.random()

        # Update kecepatan berdasarkan formula PSO
        new_velocity = (
            self.inertia_weight * velocity
            + self.c1 * r1 * (p_best - particle)
            + self.c2 * r2 * (g_best - particle)
        )

        # Batasan kecepatan dalam rentang [0, 1]
        return np.clip(new_velocity, 0, 1)

    def update_position(self, particle, velocity):
        # Update posisi menggunakan sigmoid untuk menentukan probabilitas
        sigmoid = 1 / (1 + np.exp(-velocity))
        new_particle = np.array([1 if random.random() < sigmoid[i] else 0 for i in range(len(particle))])
        return new_particle

    def optimize(self):
        best_distance = float('inf')
        best_route = None

        for iteration in range(self.num_iterations):
            for i in range(self.num_particles):
                # Update kecepatan dan posisi partikel
                self.velocities[i] = self.update_velocity(
                    self.particles[i], self.velocities[i], self.p_best[i], self.g_best
                )
                self.particles[i] = self.update_position(self.particles[i], self.velocities[i])

                # Hitung jarak rute untuk personal best
                decoded_route = self.decode_route(self.particles[i])
                if self.route_distance(decoded_route) < self.route_distance(self.decode_route(self.p_best[i])):
                    self.p_best[i] = self.particles[i]

            # Update global best
            self.g_best = min(self.p_best, key=lambda p: self.route_distance(self.decode_route(p)))
            g_best_distance = self.route_distance(self.decode_route(self.g_best))

            if g_best_distance < best_distance:
                best_distance = g_best_distance
                best_route = self.decode_route(self.g_best)

            print(f"Iteration {iteration + 1}/{self.num_iterations}, Best Distance: {best_distance:.2f} km")

        return best_route, best_distance

# Contoh penggunaan
if __name__ == "__main__":
    # Contoh data (replace dengan data nyata jika diperlukan)
    waypoints = [(0, 0), (1, 1), (2, 0), (1, -1)]
    start_point = (0, 0)
    end_point = (2, 0)

    bpso = BPSO_TSP(waypoints, start_point, end_point, num_particles=10, num_iterations=100, inertia_weight=0.5, c1=2.0, c2=2.0)
    best_route, best_distance = bpso.optimize()

    print("Best Route:", best_route)
    print("Best Distance:", best_distance)
