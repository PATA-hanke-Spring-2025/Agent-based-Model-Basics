import pandas as pd
from reading import read_excel, read_value_elements
import importlib

def evaluate_offering(probabilities, elements, category_weights, states, current_state):
    """Evaluate a B2B offering based on its element scores and buyer preferences"""
    print(f"Elements: {elements}")
    print(f"Probabilities: {probabilities}")
    print(f"States: {states}")
    print(f"Current State: {current_state}")

    # Ensure probabilities are mapped to states correctly
    state_probabilities = {state: prob for state, prob in zip(states, probabilities)}

    # Check for table stakes failure
    for element, details in elements.items():
        if details['category'] == 'table_stakes':
            # Ensure the element exists in state_probabilities
            if element in state_probabilities and state_probabilities[element] < 6:  # Adjust threshold as needed
                return 0.0, {"table_stakes_failed": element}

    # Calculate scores by category
    category_scores = {cat: 0 for cat in category_weights.keys()}
    category_counts = {cat: 0 for cat in category_weights.keys()}

    for element, details in elements.items():
        if element in state_probabilities:
            score = state_probabilities[element]
            category = details['category']

            # Apply the base weight
            weight = details['weight']

            # Calculate weighted score based on excellence
            if score >= 0.8:  # Excellent
                weighted_score = weight * score
            elif score >= 0.6:  # Good
                weighted_score = 0.5 * weight * score
            else:  # Poor
                weighted_score = 0.1 * weight * score

            category_scores[category] += weighted_score
            category_counts[category] += 1

    # Normalize category scores
    for cat in category_scores:
        if category_counts[cat] > 0:
            category_scores[cat] /= category_counts[cat]

    # Calculate overall score
    overall_score = 0
    for cat, score in category_scores.items():
        overall_score += score * category_weights[cat]

    return overall_score, category_scores
