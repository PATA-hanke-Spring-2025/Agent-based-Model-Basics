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
def read_value_elements(elements_file, weights_file):
    """Read value elements and category weights from CSV files."""
    elements_df = pd.read_csv(elements_file, delimiter=";")
    weights_df = pd.read_csv(weights_file, delimiter=";")

    elements = {}
    for _, row in elements_df.iterrows():
        element_name = row['element_name']
        weight = float(row['weight'])
        category = row['category']
        touch_count = int(row['touch_count'])
        # Store the weight, category, and touch count for each element
        elements[element_name] = {
            'weight': weight,
            'category': category,
            'touch_count': touch_count
        }

    category_weights = {}
    for _, row in weights_df.iterrows():
        category_weights[row['category']] = float(row['weight'])

    return elements, category_weights


# ##For reading the plugins + creating the plugin matrix
"""def read_plugins(agent):
    plugin_status = False
    plugin_file = "Plugins.xlsx"
    plugins = None
    plugin_data = {}
    loaded_plugins = {}
    if os.path.exists(plugin_file):
        plugins=read_excel(plugin_file)
        if plugins is not None:
            plugin_status=True 
            for index, row in plugins.iterrows():   
                plugin_name=row['Name']
                plugin_import=row['Import']
                plugin_function=row['Main Function']
                
                module = importlib.import_module(plugin_import)
                # Load plugin-specific data if load() exists
                plugin_loaded_data = {}
                if hasattr(module, 'load'):
                    plugin_loaded_data = module.load()

                plugin_data[plugin_name]={
                    'function': plugin_function,
                    'import': plugin_import,
                    'data_for_loading': plugin_loaded_data}
               
                loaded_plugins[plugin_name]=(module,plugin_function)
               
            if plugin_status==True:
                print("Plugins loaded")
            else:
                print("No plugins loaded")
    return plugins, plugin_data, loaded_plugins"""