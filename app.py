import ipywidgets as widgets
from IPython.display import display
from agents import Buyer
from model import Model

buyer = Buyer()
model = Model(buyer)

sliders = {}
for attr in dir(buyer):
    if attr.startswith(('NotInt_', 'Eval_', 'Budget_', 'Decide_', 'GoNogo_', 'Deliver_', 'Satisf_', 'Dissatisfied_')):
        sliders[attr] = widgets.FloatSlider(value=getattr(buyer, attr), min=0, max=1, step=0.01, description=attr)

output = widgets.Output()
step_button = widgets.Button(description="Take Step")

def updateProb(change) :
    newProbs = {attr: slider.value for attr, slider in sliders.items()}
    model.update_transition_matrix(**newProbs)
    with output:
        output.clear_output()
        print("Updated Matrix")
        print(buyer.transition_matrix)
        print(f"Initial State: {buyer.state}")

def take_step(b):
    model.step()
    with output:
        print(f"State Updated: {buyer.state}")

for slider in sliders.values():
    slider.observe(updateProb, names='value')

step_button.on_click(take_step)

for slider in sliders.values():
    display(slider)
display(step_button)
display(output)

updateProb(None)
