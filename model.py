class Model:
    def __init__ (self, buyer) :
        self.buyer = buyer

    def step(self):
        self.buyer.step()
