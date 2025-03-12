import pandas as pd
from agents import Buyer
from model import Model

transition_data = pd.read_csv("SellerTransition.csv", delimiter=";")
states = pd.read_csv("BuyerStates.csv", delimiter=";")

buyer = Buyer(transition_data, states)
model = Model(buyer)

step_count = 0
while buyer.state not in ["Satisfied", "Dissatisfied"]:
    print(f"Current state: {buyer.state}")
    model.step()
    step_count += 1

print(f"Final State: {buyer.state}")
print(f"Steps Taken: {step_count}")