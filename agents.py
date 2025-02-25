from mesa import Agent
import random 

class Buyer(Agent):
    """
    A Buyer Agent
    
    Attributes:
        "Not Interested", "Evaluating", "Budgeting", "Deciding", "Go Nogo", "Delivered", "Satisfied"
    """
    def __init__(self, id, model):
        """
        Create a new buyer

        Arguments:
            id: integer identifier.
            model: reference to containing model.
        """
        super().__init__(id, model)
        self.state = "Not Interested"
    
    def step(self):
        """
        Simulate the process
        """

        chance = random.random()

        if self.state == "Not Interested":
            if chance < 0.3:
                self.state = "Evaluating"

        elif self.state == "Evaluating":
            if chance < 0.4:
                self.state = "Budgeting"
            elif chance < 0.7:
                self.state = "Not Interested"

        elif self.state == "Budgeting":
            if chance < 0.2:
                self.state == "Not Interested"
            elif chance < 0.4:
                self.state == "Evaluating"
            elif chance < 0.7:
                self.state = "Deciding"

        elif self.state == "Deciding":
            if chance < 0.1:
                self.state == "Not Interested"
            elif chance < 0.3:
                self.state == "Evaluating"
            elif chance < 0.4:
                self.state == "Budgeting"
            elif chance < 0.7:
                self.state == "Go Nogo"
        
        elif self.state == "Go Nogo":
            if chance < 0.1:
                self.state = "Deciding"
            if chance < 0.8:
                self.state = "Delivered"
            
        elif self.state == "Delivered":
            if chance < 0.8:
                self.state = "Satisfied"
            else: self.state = "Dissatsified"
        
        elif self.state == "Satisfied":
            if chance < 0.1:
                self.state = "Dissatisfied"
        
        elif self.state == "Dissatisfied":
            if chance < 0.1:
                self.state = "Satisfied"