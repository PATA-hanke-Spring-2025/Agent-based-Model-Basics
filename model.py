import numpy as np 

class Model:
    def __init__ (self, buyer) :
        self.buyer = buyer

    def update_transition_matrix(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.buyer, key, value)
        self.buyer.transition_matrix = self.buyer.create_initial_matrix()

    def step(self):
        self.buyer.step()
