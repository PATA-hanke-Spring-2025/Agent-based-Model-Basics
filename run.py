import json
from agents import Buyer
import pandas as pd

with open("master-parameters.json", "r") as file:
    state_transitions = json.load(file)

data = []
for current_state, transitions in state_transitions.items():
    for next_state, probability in transitions.items():
        data.append({"current_state": current_state.upper(),"next_state": next_state.upper(), "probability": probability})

df = pd.DataFrame(data)

print("Transition phase:")
print(df)

sim_count = 0
total_steps = 0

while sim_count < 100:  # limited to 100 sims
    buyer = Buyer(df) # reset for each sim
    step_count = 1  # reset for each sim

    #print("Initial state:", buyer.state) = currently NOT_INTERESTED
    
    while True:
        current_probabilities = df[df["current_state"] == buyer.state]["probability"]
        if current_probabilities.sum() == 0:
            print("Invalid transition.")
            break
        
        buyer.step()
        step_count += 1
        if buyer.state in ["SATISFIED", "DISSATISFIED"]:
            print(f"Final step {step_count}: {buyer.state}")           
            break
    total_steps += step_count
    sim_count += 1

average_steps = total_steps / sim_count
print(f"Average steps in {sim_count} sims: {average_steps}")