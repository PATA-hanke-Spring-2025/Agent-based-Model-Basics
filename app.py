import pandas as pd
from agents import Buyer
from model import Model

transition_data = pd.read_csv("BuyerTransition.csv", delimiter=";")
states = pd.read_csv("BuyerStates.csv", delimiter=";")

buyer = Buyer(transition_data, states)
model = Model(buyer)

step_count = 0
state_history = []

while buyer.state not in ["Satisfied", "Dissatisfied"]:
    print(f"Current state: {buyer.state}")
    state_history.append(buyer.state)
    model.step()
    step_count += 1

results_df = pd.DataFrame({
    "State History": state_history,
    "Step Number": range(1, len(state_history) + 1)
})

results_df.to_csv("simulation_results.csv", index=False)

print(f"Simulation results saved to simulation_results.csv. Total steps: {step_count}")