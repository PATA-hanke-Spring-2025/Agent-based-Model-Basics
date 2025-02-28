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


buyer = Buyer(df)

print("Initial state:", buyer.state)
print("Transition phase:")
print(df)

step_count = 1

while step_count < 101:  # limited to 100 steps
    current_probabilities = df[df["current_state"] == buyer.state]["probability"]
    if current_probabilities.sum() == 0:
        print("Invalid transition.")
        break
    
    print(f"Step {step_count}: {buyer.state}")
    buyer.step()
    step_count += 1