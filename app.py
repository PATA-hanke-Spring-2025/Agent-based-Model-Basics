import pandas as pd
from agents import Agent
from model import Model
from reading import read_excel
import os
import datetime

if __name__ == "__main__":
    transition_file = "SellerTransition.csv"
    states_file = "SellerStates.csv"
    
    if os.path.exists("SellerTransition.xlsx"):
        transition_file = "SellerTransition.xlsx"
    elif os.path.exists("SellerTransition.xls"):
        transition_file = "SellerTransition.xls"

    if os.path.exists("SellerStates.xlsx"):
        states_file = "SellerStates.xlsx"
    elif os.path.exists("SellerStates.xls"):
        states_file = "SellerStates.xls"

    transition_data = read_excel(transition_file)
    states = read_excel(states_file)

last_id = states['State'].iloc[-1]

agent = Agent(transition_data, states)
model = Model(agent)

# Define the number of steps for the simulation
num_steps = 100  # Adjust this value as needed

# Run the simulation for the specified number of steps
for step in range(num_steps):
    print(f"Step {step + 1}")
    model.step()

# Save the results
model.save_results("simulation_results.csv")
print(f"Simulation results saved to simulation_results.csv. Total steps: {num_steps}")