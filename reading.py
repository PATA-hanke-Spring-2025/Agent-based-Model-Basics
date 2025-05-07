import os
import pandas as pd
import importlib

##For reading excel files
def read_excel(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, delimiter=";")
    elif filename.endswith(('.xls')):
        return pd.read_excel(filename, engine="xlrd")
    elif filename.endswith(('.xlsx')):
        return pd.read_excel(filename, engine='openpyxl')


##For creating the initial state probability matrix
def create_state_matrix(transition_data, states):
    matrix = []
    for from_state in states['State']:
        row = []
        for to_state in states['State']:
            value = transition_data.loc[transition_data['From/To'] == from_state, to_state].values[0]
            row.append(value)
        matrix.append(row)
    return pd.DataFrame(matrix, index=states['State'], columns=states['State'])


##For reading value_elements + category_weights
def read_value_elements(elements_df):
    elements = {}
    for _, row in elements_df.iterrows():
        element_name = row['element_name']
        weight = float(row['weight'])
        category = row['category']
        # Store the weight and category for each element
        elements[element_name] = {
            'weight': weight,
            'category': category
        }

    return elements

def read_value_weights( weights_df):
   
    category_weights = {}
    for _, row in weights_df.iterrows():
        category_weights[row['category']] = float(row['weight'])

    return category_weights