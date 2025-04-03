def test(probabilities, plugin_info, states, current_state):

    if current_state == "Proposing":
        negotiating_index = states.index("Negotiating")
        adjustment = 0.2
        if negotiating_index < len(probabilities): #Bounds check
            probabilities[negotiating_index] = min(1.0, probabilities[negotiating_index] + adjustment) #Increase by adjustment, but don't exceed 1.0

    return probabilities