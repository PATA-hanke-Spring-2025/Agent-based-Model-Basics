import pandas as pd
from agents import Buyer
from model import Model

transition_data = pd.read_csv("SellerTransition.csv", delimiter=";")
states = pd.read_csv("BuyerStates.csv")

buyer = Buyer(transition_data, states)
model = Model(buyer)

num_steps = 5
for _ in range(num_steps):
    print(f"Current State: {buyer.state}")
    model.step()