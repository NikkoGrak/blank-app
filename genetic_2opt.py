#genetic.py

import streamlit as st
import pandas as pd
import numpy as np
import random
from geopy.distance import geodesic
from data_utils import read_waypoints_from_excel



# Fungsi untuk menghitung jarak antara dua titik
def distance_between_points(p1, p2):
    return geodesic(p1, p2).kilometers

# Fungsi untuk menghitung total jarak dalam rute
def total_distance(route, start_point, end_point):
    distance = distance_between_points(start_point, route[0])
    for i in range(len(route) - 1):
        distance += distance_between_points(route[i], route[i + 1])
    distance += distance_between_points(route[-1], end_point)
    return distance
# Kelas algoritma genetika untuk TSP
class GA_TSP:
    def __init__(self, waypoints, start_point, end_point, pop_size, elite_size, mutation_rate, generations):
        self.waypoints = waypoints
        self.start_point = start_point
        self.end_point = end_point
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def create_route(self):
        route = random.sample(range(len(self.waypoints)), len(self.waypoints))
        return route

    def initial_population(self):
        return [self.create_route() for _ in range(self.pop_size)]

    def rank_routes(self, population):
        fitness_results = {}
        for i, route in enumerate(population):
            distance = total_distance([self.waypoints[i] for i in route], self.start_point, self.end_point)
            fitness_results[i] = 1 / distance  # Menggunakan invers jarak sebagai fitness
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    # def selection(self, ranked_routes):
    #     selection_results = []
    #     df = pd.DataFrame(ranked_routes, columns=["Index", "Fitness"])
    #     df['cum_sum'] = df.Fitness.cumsum()
    #     df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    #     for _ in range(self.elite_size):
    #         selection_results.append(ranked_routes[_][0])

    #     for _ in range(len(ranked_routes) - self.elite_size):
    #         pick = 100 * random.random()
    #         for i in range(len(ranked_routes)):
    #             if pick <= df.iat[i, 3]:
    #                 selection_results.append(ranked_routes[i][0])
    #                 break
    #     return selection_results
    def selection(self, ranked_routes):
        tournament_size = 5
        selection_results = []
        for _ in range(self.elite_size):
            selection_results.append(ranked_routes[_][0])
        for _ in range(len(ranked_routes) - self.elite_size):
            tournament = random.sample(ranked_routes, tournament_size)
            selection_results.append(max(tournament, key=lambda x: x[1])[0])
        return selection_results


    def mating_pool(self, population, selection_results):
        return [population[i] for i in selection_results]

    def breed(self, parent1, parent2):
        gene_a = int(random.random() * len(parent1))
        gene_b = int(random.random() * len(parent1))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        child_p1 = parent1[start_gene:end_gene]
        child_p2 = [item for item in parent2 if item not in child_p1]

        child = child_p1 + child_p2
        return child

    def breed_population(self, matingpool):
        children = []
        length = len(matingpool) - self.elite_size
        pool = random.sample(matingpool, len(matingpool))

        for i in range(self.elite_size):
            children.append(matingpool[i])

        for i in range(length):
            child = self.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    # def mutate(self, individual):
    #     for swapped in range(len(individual)):
    #         if random.random() < self.mutation_rate:
    #             swap_with = int(random.random() * len(individual))

    #             individual[swapped], individual[swap_with] = individual[swap_with], individual[swapped]
    #     return individual
    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            start, end = sorted(random.sample(range(len(individual)), 2))
            individual[start:end] = reversed(individual[start:end])
        return individual

    def mutate_population(self, population):
        mutated_pop = [self.mutate(ind) for ind in population]
        return mutated_pop

    def next_generation(self, current_gen):
        ranked_routes = self.rank_routes(current_gen)
        selection_results = self.selection(ranked_routes)
        matingpool = self.mating_pool(current_gen, selection_results)
        children = self.breed_population(matingpool)
        next_generation = self.mutate_population(children)
        return next_generation



    # def optimize(self):
    #     #column for widget AG, ACO and PSO
    #     col1, col2 , col3 = st.columns(3)
    #     pop = self.initial_population()
    #     print("Initial distance: " + str(1 / self.rank_routes(pop)[0][1]))
        

    #     for i in range(self.generations):
    #         pop = self.next_generation(pop)
    #         best_distance = 1 / self.rank_routes(pop)[0][1]
    #         print(f"Generasi {i+1}/{self.generations}, Jarak Terbaik: {best_distance:.2f} km")
    #         col1.write(f"Generasi {i+1}/{self.generations}, Jarak Terbaik: {best_distance:.2f} km")

    #     best_route_index = self.rank_routes(pop)[0][0]
    #     best_route = pop[best_route_index]
    #     best_distance = 1 / self.rank_routes(pop)[0][1]

    #     # Jalankan algoritma 2-opt untuk mengoptimalkan rute
    #     best_route = two_opt(best_route, self.waypoints, self.start_point, self.end_point)
    #     best_distance = total_distance([self.waypoints[i] for i in best_route], self.start_point, self.end_point)

    #     print(f"Jarak terbaik setelah 2-opt: {best_distance:.2f} km")
    #     col2.write(f"Jarak terbaik setelah 2-opt: {best_distance:.2f} km")
        
    #     return best_route, best_distance


 # Fungsi 2-opt sebagai metode dalam kelas
    def two_opt(self, route):
        """ Algoritma 2-opt untuk mengoptimalkan rute """
        improved = True
        best_distance = total_distance([self.waypoints[i] for i in route], self.start_point, self.end_point)

        while improved:
            improved = False
            for i in range(1, len(route) - 1):
                for j in range(i + 1, len(route)):
                    new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                    new_distance = total_distance([self.waypoints[k] for k in new_route], self.start_point, self.end_point)
                    
                    if new_distance < best_distance:
                        route = new_route
                        best_distance = new_distance
                        improved = True
        return route

    def optimize(self):
        col1, col2, col3 = st.columns(3)
        pop = self.initial_population()
        print("Initial distance: " + str(1 / self.rank_routes(pop)[0][1]))

        for i in range(self.generations):
            pop = self.next_generation(pop)
            best_distance = 1 / self.rank_routes(pop)[0][1]
            # print(f"Generasi {i+1}/{self.generations}, Jarak Terbaik: {best_distance:.2f} km")
            # col1.write(f"Generasi {i+1}/{self.generations}, Jarak Terbaik: {best_distance:.2f} km")

        best_route_index = self.rank_routes(pop)[0][0]
        best_route = pop[best_route_index]

        # Jalankan algoritma 2-opt sebagai metode kelas
        best_route = self.two_opt(best_route)
        best_distance = total_distance([self.waypoints[i] for i in best_route], self.start_point, self.end_point)

        # print(f"Jarak terbaik setelah 2-opt: {best_distance:.2f} km")
        # col2.write(f"Jarak terbaik setelah 2-opt: {best_distance:.2f} km")
        
        return best_route, best_distance
