import numpy as np

class Buyer:
    """
    Attributes:
        "Not Interested", "Evaluating", "Budgeting", "Deciding", "Go Nogo", "Delivered", "Satisfied"
    """
    def __init__(self):
        self.state = "Not Interested"

        # Not Interested
        self.NotInt_NotInt = 0.7
        self.NotInt_Eval = 0.3
        self.NotInt_Budget = 0.0
        self.NotInt_Decide = 0.0
        self.NotInt_GoNogo = 0.0
        self.NotInt_Deliver = 0.0
        self.NotInt_Satisf = 0.0
        self.NotInt_Dissatisfied = 0.0 

        # Evaluating
        self.Eval_NotInt = 0.3
        self.Eval_Eval = 0.3
        self.Eval_Budget = 0.4
        self.Eval_Decide = 0.0
        self.Eval_GoNogo = 0.0
        self.Eval_Deliver = 0.0
        self.Eval_Satisf = 0.0
        self.Eval_Dissatisfied = 0.0

        # Budgeting
        self.Budget_NotInt = 0.2
        self.Budget_Eval = 0.2
        self.Budget_Budget = 0.3
        self.Budget_Decide = 0.3
        self.Budget_GoNogo = 0.0
        self.Budget_Deliver = 0.0
        self.Budget_Satisf = 0.0
        self.Budget_Dissatisfied = 0.0

        # Deciding
        self.Decide_NotInt = 0.1
        self.Decide_Eval = 0.2
        self.Decide_Budget = 0.1
        self.Decide_Decide = 0.3
        self.Decide_GoNogo = 0.3
        self.Decide_Deliver = 0.0
        self.Decide_Satisf = 0.0
        self.Decide_Dissatisfied = 0.0

        # Go_NOGO
        self.GoNogo_NotInt = 0.0
        self.GoNogo_Eval = 0.0
        self.GoNogo_Budget = 0.0
        self.GoNogo_Decide = 0.1
        self.GoNogo_GoNogo = 0.2
        self.GoNogo_Deliver = 0.7
        self.GoNogo_Satisf = 0.0
        self.GoNogo_Dissatisfied = 0.0

        # Delivered
        self.Deliver_NotInt = 0.0
        self.Deliver_Eval = 0.0
        self.Deliver_Budget = 0.0
        self.Deliver_Decide = 0.0
        self.Deliver_GoNogo = 0.0
        self.Deliver_Deliver = 0.0 
        self.Deliver_Satisf = 0.8
        self.Deliver_Dissatisfied = 0.2

        # Satisfied
        self.Satisf_NotInt = 0.0
        self.Satisf_Eval = 0.0
        self.Satisf_Budget = 0.0
        self.Satisf_Decide = 0.0
        self.Satisf_GoNogo = 0.0
        self.Satisf_Deliver = 0.0
        self.Satisf_Satisfied = 0.9
        self.Satisf_Dissatisfied = 0.1

        # Dissatisfied 
        self.Dissatisfied_NotInt = 0.0
        self.Dissatisfied_Eval = 0.0
        self.Dissatisfied_Budget = 0.0
        self.Dissatisfied_Decide = 0.0
        self.Dissatisfied_GoNogo = 0.0
        self.Dissatisfied_Deliver = 0.0
        self.Dissatisfied_Satisfied = 0.1
        self.Dissatisfied_Dissatisfied = 0.9

        self.transition_matrix = self.create_initial_matrix()

    def create_initial_matrix(self):
        return np.array ([
            [self.NotInt_NotInt, self.NotInt_Eval, self.NotInt_Budget, self.NotInt_Decide, self.NotInt_GoNogo, self.NotInt_Deliver, self.NotInt_Satisf, self.NotInt_Dissatisfied],
            [self.Eval_NotInt, self.Eval_Eval, self.Eval_Budget, self.Eval_Decide, self.Eval_GoNogo, self.Eval_Deliver, self.Eval_Satisf, self.Eval_Dissatisfied],
            [self.Budget_NotInt, self.Budget_Eval, self.Budget_Budget, self.Budget_Decide, self.Budget_GoNogo, self.Budget_Deliver, self.Budget_Satisf, self.Budget_Dissatisfied],
            [self.Decide_NotInt, self.Decide_Eval, self.Decide_Budget, self.Decide_Decide, self.Decide_GoNogo, self.Decide_Deliver, self.Decide_Satisf, self.Decide_Dissatisfied],
            [self.GoNogo_NotInt, self.GoNogo_Eval, self.GoNogo_Budget, self.GoNogo_Decide, self.GoNogo_GoNogo, self.GoNogo_Deliver, self.GoNogo_Satisf, self.GoNogo_Dissatisfied],
            [self.Deliver_NotInt, self.Deliver_Eval, self.Deliver_Budget, self.Deliver_Decide, self.Deliver_GoNogo, self.Deliver_Deliver, self.Deliver_Satisf, self.Deliver_Dissatisfied],
            [self.Satisf_NotInt, self.Satisf_Eval, self.Satisf_Budget, self.Satisf_Decide, self.Satisf_GoNogo, self.Satisf_Deliver, self.Satisf_Satisfied, self.Satisf_Dissatisfied],
            [self.Dissatisfied_NotInt, self.Dissatisfied_Eval, self.Dissatisfied_Budget, self.Dissatisfied_Decide, self.Dissatisfied_GoNogo, self.Dissatisfied_Deliver, self.Dissatisfied_Satisfied, self.Dissatisfied_Dissatisfied]
        ])
    
    def step(self):
        states = ["Not Interested", "Evaluating", "Budgeting", "Deciding", "Go Nogo", "Delivered", "Satisfied", "Dissatisfied"]
        current_state_index = states.index(self.state)
        probabilities = self.transition_matrix[current_state_index]
        next_state_index = np.random.choice(range(len(states)), p = probabilities)
        self.state = states[next_state_index]
        return self.state