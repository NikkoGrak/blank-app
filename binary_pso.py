import numpy as np
import random
from geopy.distance import geodesic


# Fungsi untuk menghitung jarak antara dua titik menggunakan geodesic (latitude, longitude)
def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers


# Fungsi untuk menghitung total jarak dalam rute
def total_distance(route, start_point, end_point):
    """
    Menghitung total jarak rute berdasarkan waypoint yang dipilih.
    """
    distance = distance_between_points(start_point, route[0])
    for i in range(len(route) - 1):
        distance += distance_between_points(route[i], route[i + 1])
    distance += distance_between_points(route[-1], end_point)
    return distance


# Kelas Binary PSO (BPSO) untuk TSP
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
        Hitung jarak total untuk rute berdasarkan partikel (binary).
        Pastikan semua waypoint digunakan.
        """
        selected_indices = [i for i in range(len(particle)) if particle[i] == 1]

        # Jika tidak ada waypoint yang dipilih, anggap semua waypoint
        if len(selected_indices) == 0:
            selected_indices = list(range(self.num_waypoints))

        selected_waypoints = [self.waypoints[idx] for idx in selected_indices]
        return total_distance(selected_waypoints, self.start_point, self.end_point)

    def update_velocity(self, particle, velocity, p_best, g_best):
        """
        Update kecepatan partikel berdasarkan rumus PSO.
        """
        r1, r2 = random.random(), random.random()

        # Update kecepatan
        new_velocity = (
            self.inertia_weight * velocity
            + self.c1 * r1 * (p_best - particle)
            + self.c2 * r2 * (g_best - particle)
        )
        return np.clip(new_velocity, 0, 1)

    def update_position(self, particle, velocity):
        """
        Update posisi partikel (binary) berdasarkan probabilitas sigmoid dari kecepatan.
        """
        # sigmoid = 1 / (1 + np.exp(-velocity))
        k = 2  # Faktor pengali untuk sigmoid
        sigmoid = 1 / (1 + np.exp(-k * velocity))
        new_particle = np.array([1 if random.random() < sigmoid[i] else 0 for i in range(len(particle))])

        # Pastikan minimal satu waypoint dipilih
        if np.sum(new_particle) == 0:
            new_particle[random.randint(0, len(new_particle) - 1)] = 1

        return new_particle

    def optimize(self):
        """
        Jalankan optimasi BPSO untuk menemukan solusi optimal.
        """
        best_distance = float('inf')
        best_route = None

        for iteration in range(self.num_iterations):
            for i in range(self.num_particles):
                # Update kecepatan dan posisi partikel
                self.velocities[i] = self.update_velocity(
                    self.particles[i], self.velocities[i], self.p_best[i], self.g_best
                )
                self.particles[i] = self.update_position(self.particles[i], self.velocities[i])

                # Update personal best jika solusi baru lebih baik
                if self.route_distance(self.particles[i]) < self.route_distance(self.p_best[i]):
                    self.p_best[i] = self.particles[i]

            # Update global best
            self.g_best = min(self.p_best, key=lambda p: self.route_distance(p))
            g_best_distance = self.route_distance(self.g_best)

            if g_best_distance < best_distance:
                best_distance = g_best_distance

                # Simpan rute terbaik sebagai indeks waypoint
                best_route = [i for i in range(len(self.g_best)) if self.g_best[i] == 1]

            print(f"Iteration {iteration + 1}/{self.num_iterations}, Best Distance: {best_distance:.2f} km")

        return best_route, best_distance




 


# import numpy as np
# import random
# from geopy.distance import geodesic


# # Fungsi untuk menghitung jarak antara dua titik menggunakan geodesic (latitude, longitude)
# def distance_between_points(p1, p2):
#     return geodesic(p1, p2).kilometers


# # Fungsi untuk menghitung total jarak dalam rute
# def total_distance(selected_waypoints, start_point, end_point):
#     """
#     Menghitung total jarak rute berdasarkan waypoint yang dipilih.
#     """
#     if len(selected_waypoints) == 0:
#         return float('inf')  # Jika tidak ada waypoint, jarak tidak valid

#     distance = distance_between_points(start_point, selected_waypoints[0])  # Jarak dari titik awal ke waypoint pertama
#     for i in range(len(selected_waypoints) - 1):
#         distance += distance_between_points(selected_waypoints[i], selected_waypoints[i + 1])
#     distance += distance_between_points(selected_waypoints[-1], end_point)  # Jarak dari waypoint terakhir ke titik akhir
#     return distance


# # Kelas Binary PSO (BPSO) untuk TSP
# class BPSO_TSP:
#     def __init__(self, waypoints, start_point, end_point, num_particles, num_iterations, inertia_weight, c1, c2):
#         self.waypoints = waypoints
#         self.start_point = start_point
#         self.end_point = end_point
#         self.num_particles = num_particles
#         self.num_iterations = num_iterations
#         self.inertia_weight = inertia_weight
#         self.c1 = c1  # Koefisien kognitif
#         self.c2 = c2  # Koefisien sosial

#         self.num_waypoints = len(self.waypoints)

#         # Inisialisasi posisi dan kecepatan partikel
#         self.particles = [self.initialize_particle() for _ in range(num_particles)]
#         self.velocities = [self.initialize_velocity() for _ in range(num_particles)]

#         # Inisialisasi personal best dan global best
#         self.p_best = self.particles[:]
#         self.g_best = min(self.particles, key=lambda p: self.route_distance(p))

#     def initialize_particle(self):
#         """
#         Inisialisasi partikel sebagai array biner (0 atau 1).
#         """
#         return np.random.randint(2, size=self.num_waypoints)

#     def initialize_velocity(self):
#         """
#         Inisialisasi kecepatan sebagai array float dalam rentang [0, 1].
#         """
#         return np.random.random(self.num_waypoints)

#     def route_distance(self, particle):
#         """
#         Hitung jarak total untuk partikel biner.
#         """
#         selected_indices = [i for i in range(len(particle)) if particle[i] == 1]
#         selected_waypoints = [self.waypoints[idx] for idx in selected_indices]
#         return total_distance(selected_waypoints, self.start_point, self.end_point)

#     def update_velocity(self, particle, velocity, p_best, g_best):
#         """
#         Update kecepatan partikel berdasarkan rumus PSO.
#         """
#         r1, r2 = random.random(), random.random()

#         # Update kecepatan dengan formula PSO
#         new_velocity = (
#             self.inertia_weight * velocity
#             + self.c1 * r1 * (p_best - particle)
#             + self.c2 * r2 * (g_best - particle)
#         )

#         # Batasi kecepatan dalam rentang [0, 1]
#         return np.clip(new_velocity, 0, 1)

#     def update_position(self, particle, velocity):
#         """
#         Update posisi partikel (biner) berdasarkan probabilitas sigmoid dari kecepatan.
#         """
#         sigmoid = 1 / (1 + np.exp(-velocity))
#         new_particle = np.array([1 if random.random() < sigmoid[i] else 0 for i in range(len(particle))])

#         # Pastikan minimal ada satu waypoint dipilih
#         if np.sum(new_particle) == 0:
#             new_particle[random.randint(0, len(new_particle) - 1)] = 1

#         return new_particle

#     def optimize(self):
#         """
#         Jalankan optimasi BPSO untuk menemukan solusi optimal.
#         """
#         best_distance = float('inf')
#         best_route = None

#         for iteration in range(self.num_iterations):
#             for i in range(self.num_particles):
#                 # Update kecepatan dan posisi partikel
#                 self.velocities[i] = self.update_velocity(
#                     self.particles[i], self.velocities[i], self.p_best[i], self.g_best
#                 )
#                 self.particles[i] = self.update_position(self.particles[i], self.velocities[i])

#                 # Update personal best jika solusi baru lebih baik
#                 if self.route_distance(self.particles[i]) < self.route_distance(self.p_best[i]):
#                     self.p_best[i] = self.particles[i]

#             # Update global best
#             self.g_best = min(self.p_best, key=lambda p: self.route_distance(p))
#             g_best_distance = self.route_distance(self.g_best)

#             if g_best_distance < best_distance:
#                 best_distance = g_best_distance
#                 best_route = [i for i, bit in enumerate(self.g_best) if bit == 1]

#             print(f"Iteration {iteration + 1}/{self.num_iterations}, Best Distance: {best_distance:.2f} km")

#         return best_route, best_distance
