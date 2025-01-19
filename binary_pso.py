import numpy as np
import random
from geopy.distance import geodesic
import time


# Fungsi untuk menghitung jarak antara dua titik menggunakan geodesic
def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers


# Fungsi untuk menghitung total jarak dalam rute
def total_distance(particle, waypoints, start_point, end_point):
    """
    Menghitung total jarak rute berdasarkan partikel biner.
    """
    # Pilih waypoint berdasarkan nilai biner dalam partikel
    selected_waypoints = [waypoints[i] for i in range(len(particle)) if particle[i] == 1]

    # Jika tidak ada waypoint yang dipilih, anggap semua waypoint
    if len(selected_waypoints) == 0:
        selected_waypoints = waypoints

    # Hitung total jarak
    distance = distance_between_points(start_point, selected_waypoints[0])
    for i in range(len(selected_waypoints) - 1):
        distance += distance_between_points(selected_waypoints[i], selected_waypoints[i + 1])
    distance += distance_between_points(selected_waypoints[-1], end_point)
    return distance


# Kelas Binary PSO (BPSO)
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

        # Inisialisasi posisi dan kecepatan partikel
        self.particles = [self.initialize_particle() for _ in range(num_particles)]
        self.velocities = [self.initialize_velocity() for _ in range(num_particles)]

        # Inisialisasi personal best dan global best
        self.p_best = self.particles[:]
        self.g_best = min(self.particles, key=lambda p: self.route_distance(p))

    def initialize_particle(self):
        """
        Inisialisasi partikel sebagai array biner (0 atau 1).
        """
        return np.random.randint(2, size=self.num_waypoints)

    def initialize_velocity(self):
        """
        Inisialisasi kecepatan sebagai array float dalam rentang [0, 1].
        """
        return np.random.random(self.num_waypoints)

    def route_distance(self, particle):
        """
        Hitung jarak total untuk partikel (tanpa decode_route).
        """
        return total_distance(particle, self.waypoints, self.start_point, self.end_point)

    def update_velocity(self, particle, velocity, p_best, g_best):
        """
        Update kecepatan partikel berdasarkan rumus PSO.
        """
        r1, r2 = random.random(), random.random()

        # Update kecepatan dengan formula PSO
        new_velocity = (
            self.inertia_weight * velocity
            + self.c1 * r1 * (p_best - particle)
            + self.c2 * r2 * (g_best - particle)
        )

        # Batasi kecepatan dalam rentang [0, 1]
        return np.clip(new_velocity, 0, 1)

    def update_position(self, particle, velocity):
        """
        Update posisi partikel (biner) berdasarkan probabilitas sigmoid dari kecepatan.
        """
        sigmoid = 1 / (1 + np.exp(-velocity))
        new_particle = np.array([1 if random.random() < sigmoid[i] else 0 for i in range(len(particle))])
        return new_particle

    def optimize(self):
        """
        Jalankan optimasi BPSO untuk menemukan solusi optimal.
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

                # Update personal best jika diperlukan
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

        # Konversi partikel terbaik ke indeks waypoint
        best_route_indices = [i for i, bit in enumerate(best_route) if bit == 1]
        return best_route_indices, best_distance


# Contoh Penggunaan
if __name__ == "__main__":
    # Data contoh (koordinat latitude dan longitude)
    waypoints = [
        (6.121435, 106.774124), (6.193125, 106.821858), (6.135200, 106.813301),
        (6.110367, 106.779455), (6.150210, 106.798912)
    ]
    start_point = (6.121435, 106.774124)  # Titik awal
    end_point = (6.193125, 106.821858)  # Titik akhir

    # Parameter BPSO
    num_particles = 30
    num_iterations = 50
    inertia_weight = 0.5
    c1 = 1.5
    c2 = 1.5

    # Inisialisasi dan optimasi
    bpso = BinaryPSO(waypoints, start_point, end_point, num_particles, num_iterations, inertia_weight, c1, c2)
    best_route_indices, best_distance = bpso.optimize()

    print("\nOptimal Route (Indices):", best_route_indices)
    print("Optimal Distance (km):", best_distance)
