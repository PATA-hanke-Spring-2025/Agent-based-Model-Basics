class Model:
    def __init__ (self, agent) :
        self.agent = agent

    def step(self):
        self.agent.step()
