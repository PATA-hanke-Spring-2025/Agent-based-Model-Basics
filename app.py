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

step_count = 0
state_history = []
next_state = []
next_step = []

while agent.state != last_id:
    state_history.append(agent.state)
    model.step()
    next_state.append(agent.state)
    step_count += 1
    next_step.append(step_count+1)

results_df = pd.DataFrame({
    "Current State": state_history,
    "Current Step Number": range(1, len(state_history) + 1),
    "Next State": next_state,
    "Next Step Number": next_step
})

timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"simulation_results_{timestamp_str}.csv"
results_df.to_csv(filename, index=False)

print(f"Simulation results saved to simulation_results.csv. Total steps: {step_count}")