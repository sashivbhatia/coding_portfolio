# Probabilistic Modeling of Housie (Bingo) Games  

This project simulates and analyzes the game of **Housie** (also known as Bingo) using Python.  
The model estimates the distribution of the number of turns required for the **first player** to complete their ticket and applies statistical tools to calculate probabilities and visualize outcomes.  

---

## 📖 Overview  
The game of Housie involves players with tickets filled with numbers between 1 and 90. Numbers are drawn randomly without replacement until a ticket is completed.  
This project models the process with multiple players, runs repeated simulations, and applies statistical analysis to understand the distribution of game lengths.  

---

## ⚙️ Methods  
- **Ticket Generation:**  
  - Constructed tickets with valid Housie structure (15 numbers spread across a 3×9 grid).  
- **Game Simulation:**  
  - Randomly drew numbers until at least one ticket was fully completed.  
  - Counted the number of turns required for the fastest ticket to finish.  
- **Monte Carlo Simulation:**  
  - Repeated the game simulation 1000 times with `n` players to approximate the probability distribution.  
- **Statistical Analysis:**  
  - Calculated the **mean** and **standard deviation** of game length.  
  - Estimated probabilities of the game exceeding a threshold `x` turns using the normal distribution.  
- **Visualization:**  
  - Displayed histograms of simulation results to show the distribution of completion times.  

---

## 🎯 Example Output  
- Distribution of turns for the fastest ticket (for `n = 15` players, 1000 simulations).  
- Probability that a game takes longer than `x = 87` turns.  
- Statistical summary (mean and standard deviation of turns).  

---

## 🛠️ Tech Stack  
- **NumPy** (simulation, statistics)  
- **SciPy** (normal distribution probability calculations)  
- **Matplotlib** (visualization)  
- **Collections** (frequency analysis with `Counter`)  

  
