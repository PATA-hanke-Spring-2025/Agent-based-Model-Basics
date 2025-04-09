import pandas as pd
from agents import Agent
from model import B2BValueElementsModel  # Import the correct model class
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

    # Initialize the B2BValueElementsModel
    model = B2BValueElementsModel(
        num_buyers=30,  # Example number of buyers
        num_sellers=10,  # Example number of sellers
        transitions_file="state_transitions.csv",
        states=states,  # Pass the states DataFrame
        transition_data=transition_data  # Pass the transition data
    )

    # Run the model for a fixed number of steps
    step_count = 50
    for step in range(step_count):
        model.step()

    # Collect results
    results_df = model.datacollector.get_model_vars_dataframe()

    # Save results to a CSV file
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"simulation_results_{timestamp_str}.csv"
    results_df.to_csv(filename, index=False)

    print(f"Simulation results saved to {filename}. Total steps: {step_count}")