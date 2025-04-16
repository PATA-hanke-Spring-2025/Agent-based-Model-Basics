import pandas as pd
from reading import read_excel, read_value_elements
import importlib

def load():
    elements_df = read_excel("value_elements.csv")
    weights_df = read_excel("category_weights.csv")
    elements, weights = read_value_elements(elements_df, weights_df)    
    return {
        "elements": elements,
        "category_weights": weights
    }
    

def evaluate_offering(offering_scores, elements, category_weights, buyer_preferences=None):
    print(f"Elements: {category_weights}")
    
    # Ensure all offering scores exist in elements
    for element in list(offering_scores.keys()):
        if element not in elements:
            print(f"Warning: Removing unknown element: {element}")
            del offering_scores[element]

    for element, details in elements.items():
        if details['category'] == 'table_stakes':
            if element in offering_scores and offering_scores[element] < 6:
                return 0.0, {"table_stakes_failed": element}

    # Calculate scores by category
    category_scores = {cat: 0 for cat in category_weights.keys()}
    category_counts = {cat: 0 for cat in category_weights.keys()}

    for element, score in offering_scores.items():
        if element in elements:
            category = elements[element]['category']

            # Apply the base weight
            weight = elements[element]['weight']

            # Apply buyer preferences if available
            if buyer_preferences and element in buyer_preferences:
                weight *= buyer_preferences[element]

            # Calculate weighted score based on excellence
            if score >= 8:  # Excellent
                weighted_score = weight * score / 10
            elif score >= 6:  # Good
                weighted_score = 0.5 * weight * score / 10
            else:  # Poor
                weighted_score = 0.1 * weight * score / 10

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
    print(f"Overall score: {overall_score}, Category scores: {category_scores}")
    return overall_score, category_scores