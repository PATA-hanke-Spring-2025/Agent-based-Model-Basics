import pandas as pd
from agents import Agent
from model import Model
from reading import read_excel, read_value_elements
from value_calculator import ValuePropositionCalculator
import os
import datetime

if __name__ == "__main__":
    transition_file = "SellerTransition.csv"
    states_file = "SellerStates.csv"
    value_elements_file = "value_elements.csv"
    category_weights_file = "category_weights.csv"

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
    value_elements, category_weights = read_value_elements(value_elements_file, category_weights_file)

    last_id = states['State'].iloc[-1]

    # Number of simulation runs
    num_runs = 1000

    # Initialize the value calculator
    value_calculator = ValuePropositionCalculator(value_elements_file, category_weights_file)

    # Aggregate results
    aggregated_results = []

    for run in range(num_runs):
        agent = Agent(transition_data, states, value_elements, category_weights)
        model = Model(agent)

        step_count = 0
        state_history = []
        next_state = []
        next_step = []

        while agent.state != last_id:
            state_history.append(agent.state)
            model.step()

            # Dynamically update weights for touched elements
            for element in value_calculator.elements.keys():
                value_calculator.update_element_weight(element)

            # Save updated elements to the CSV file after each step
            value_calculator.save_elements_to_file()

            next_state.append(agent.state)
            step_count += 1
            next_step.append(step_count + 1)

        # Store results for this run
        results_df = pd.DataFrame({
            "Run": [run + 1] * len(state_history),
            "Current State": state_history,
            "Current Step Number": range(1, len(state_history) + 1),
            "Next State": next_state,
            "Next Step Number": next_step
        })
        aggregated_results.append(results_df)

    # Combine all results into a single DataFrame
    all_results_df = pd.concat(aggregated_results, ignore_index=True)

    # Save aggregated results to a CSV file
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"aggregated_simulation_results_{timestamp_str}.csv"
    all_results_df.to_csv(filename, index=False)

    print(f"Aggregated simulation results saved to {filename}. Total runs: {num_runs}")