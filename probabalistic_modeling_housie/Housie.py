import numpy as np
from scipy.stats import norm
import random
import matplotlib.pyplot as plt
from collections import Counter

# Universal variable for the number of players
n = 15  # Number of players

# Housie number generator class
class HousieNumberGenerator:
    def __init__(self):
        self.called_numbers = set()
    
    def generate_number(self):
        if len(self.called_numbers) == 90:
            raise ValueError("All numbers from 1 to 90 have already been called!")
        while True:
            number = random.randint(1, 90)
            if number not in self.called_numbers:
                self.called_numbers.add(number)
                return number

def generate_housie_ticket():
    ticket = [[0] * 9 for _ in range(3)]
    column_ranges = [
        range(1, 10), range(10, 20), range(20, 30), range(30, 40),
        range(40, 50), range(50, 60), range(60, 70), range(70, 80), range(80, 91)
    ]
    one_number_columns = random.sample(range(9), 3)
    two_number_columns = [col for col in range(9) if col not in one_number_columns]
    column_numbers = {}
    for col in one_number_columns:
        column_numbers[col] = sorted(random.sample(column_ranges[col], 1))
    for col in two_number_columns:
        column_numbers[col] = sorted(random.sample(column_ranges[col], 2))
    for col, numbers in column_numbers.items():
        positions = random.sample(range(3), len(numbers))
        for pos, number in zip(positions, numbers):
            ticket[pos][col] = number
    return ticket

def play_housie_with_n_players(n):
    tickets = [generate_housie_ticket() for _ in range(n)]
    tickets_numbers = [
        {num for row in ticket for num in row if num != 0} for ticket in tickets
    ]
    number_generator = HousieNumberGenerator()
    remaining_counts = [len(ticket_numbers) for ticket_numbers in tickets_numbers]
    turns = 0
    while all(remaining > 0 for remaining in remaining_counts):
        called_number = number_generator.generate_number()
        turns += 1
        for i, ticket_numbers in enumerate(tickets_numbers):
            if called_number in ticket_numbers:
                remaining_counts[i] -= 1
                ticket_numbers.remove(called_number)
                if remaining_counts[i] == 0:
                    return turns

def calculate_probability(results, x):
    results_array = np.array(results)
    mean = np.mean(results_array)
    std_dev = np.std(results_array)
    probability = 1 - norm.cdf(x, loc=mean, scale=std_dev)
    return probability, mean, std_dev

def run_simulation_with_probability_and_plot(x):
    results = [play_housie_with_n_players(n) for _ in range(1000)]
    frequency = Counter(results)
    x_values = list(frequency.keys())
    y_values = list(frequency.values())
    plt.figure(figsize=(10, 6))
    plt.bar(x_values, y_values, width=1, edgecolor="black")
    plt.xlabel("Number of Turns (Fastest Ticket)")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Turns to Complete the Fastest Ticket (n={n} Players, 1000 Simulations)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    probability, mean, std_dev = calculate_probability(results, x)
    print(f"Mean number of turns: {mean:.2f}")
    print(f"Standard deviation of turns: {std_dev:.2f}")
    print(f"Probability of the game taking longer than {x} turns: {probability:.2%}")

# Example: Set x (threshold for longer games) and run the simulation
x_threshold = 87
run_simulation_with_probability_and_plot(x_threshold)
