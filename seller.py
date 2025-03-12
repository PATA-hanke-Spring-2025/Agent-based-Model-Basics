import csv
import random
import json
 
RANDOM_SEED = 42  
random.seed(RANDOM_SEED)
 
with open("seller-parameters.json", "r") as file:
    transition_matrix = json.load(file)


 
class SellerAgent:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.state = "PROSPECTING"
 
    def step(self):
        possible_transitions = transition_matrix["seller"].get(self.state, {})
        if possible_transitions:
            next_state = random.choices(
                list(possible_transitions.keys()), 
                weights=list(possible_transitions.values())
            )[0]
            return self.state, next_state  
        return self.state, self.state
 
 
with open("simulation_results.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time Step", "Agent ID", "Agent Type", '''current_state_id''', "Current State", '''final_state_id''',  "Final State (of Agent)"])
 
    seller = SellerAgent(unique_id=1)  
    for step in range(10):  
        current_state, next_state = seller.step()
        writer.writerow([step + 1, seller.unique_id, "Seller", current_state, next_state])
        seller.state = next_state
        print(f"Step {step + 1}: {current_state} -> {next_state}")