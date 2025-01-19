import numpy as np
import random
from geopy.distance import geodesic
import time


# Fungsi untuk menghitung jarak antara dua titik menggunakan geodesic
def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers


# Fungsi untuk menghitung total jarak dalam rute
def total_distance(route, start_point, end_point):
    distance = distance_between_points(start_point, route[0])
    for i in range(len(route) - 1):
        distance += distance_between_points(route[i], route[i + 1])
    distance += distance_between_points(route[-1], end_point)
    return distance


# Kelas PSO untuk TSP dengan representasi permutasi
class PSO_TSP:
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

        # Inisialisasi posisi dan kecepatan partikel
        self.particles = [self.initialize_particle() for _ in range(num_particles)]
        self.velocities = [self.initialize_velocity() for _ in range(num_particles)]

        # Inisialisasi personal best dan global best
        self.p_best = self.particles[:]
        self.g_best = min(self.particles, key=lambda p: self.route_distance(p))

    def initialize_particle(self):
        """
        Inisialisasi partikel sebagai permutasi indeks waypoint.
        """
        particle = list(range(self.num_waypoints))
        random.shuffle(particle)
        return particle

    def initialize_velocity(self):
        """
        Inisialisasi kecepatan sebagai daftar swap kosong.
        """
        return []

    def route_distance(self, particle):
        """
        Hitung jarak total untuk rute berdasarkan partikel (permutasi).
        """
        route = [self.waypoints[i] for i in particle]
        return total_distance(route, self.start_point, self.end_point)

    def calculate_swaps(self, source, target):
        """
        Hitung daftar swap untuk mengubah permutasi `source` menjadi `target`.
        """
        swaps = []
        s = source[:]
        for i in range(len(s)):
            if s[i] != target[i]:
                # Temukan indeks elemen yang salah
                swap_index = s.index(target[i])
                # Rekam swap
                swaps.append((i, swap_index))
                # Lakukan swap
                s[i], s[swap_index] = s[swap_index], s[i]
        return swaps

    def apply_swaps(self, particle, swaps):
        """
        Terapkan daftar swap pada partikel.
        """
        p = particle[:]
        for i, j in swaps:
            p[i], p[j] = p[j], p[i]
        return p

    def update_velocity(self, particle, velocity, p_best, g_best):
        """
        Update kecepatan dengan menggabungkan swap dari p_best dan g_best.
        """
        r1, r2 = random.random(), random.random()

        # Hitung swap menuju p_best dan g_best
        p_best_swaps = self.calculate_swaps(particle, p_best)
        g_best_swaps = self.calculate_swaps(particle, g_best)

        # Gabungkan swap berdasarkan probabilitas
        new_velocity = velocity[:]
        if r1 < self.c1:
            new_velocity += p_best_swaps
        if r2 < self.c2:
            new_velocity += g_best_swaps

        # Batasi panjang velocity untuk menghindari terlalu banyak swap
        return new_velocity[:self.num_waypoints]

    def update_position(self, particle, velocity):
        """
        Update posisi partikel dengan menerapkan swap dari velocity.
        """
        return self.apply_swaps(particle, velocity)

    def optimize(self):
        """
        Optimasi PSO untuk TSP.
        """
        best_distance = float('inf')
        best_route = None
        start_time = time.time()

        for iteration in range(self.num_iterations):
            for i in range(self.num_particles):
                # Update kecepatan dan posisi partikel
                self.velocities[i] = self.update_velocity(
                    self.particles[i], self.velocities[i], self.p_best[i], self.g_best
                )
                self.particles[i] = self.update_position(self.particles[i], self.velocities[i])

                # Hitung jarak rute untuk personal best
                if self.route_distance(self.particles[i]) < self.route_distance(self.p_best[i]):
                    self.p_best[i] = self.particles[i]

            # Update global best
            self.g_best = min(self.p_best, key=lambda p: self.route_distance(p))
            g_best_distance = self.route_distance(self.g_best)

            if g_best_distance < best_distance:
                best_distance = g_best_distance
                best_route = self.g_best

            print(f"Iteration {iteration + 1}/{self.num_iterations}, Best Distance: {best_distance:.2f} km")

        end_time = time.time()
        print(f"\nWaktu komputasi: {end_time - start_time:.2f} detik")
        return best_route, best_distance

