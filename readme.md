# Simulating B2B Buyer-Seller Interactions with Value-Based Decision Logic​

This project goal is to simulate B2B buyer-seller interactions using an agent-based model that incorporates value-based decision logic. 

## Description

 The simulation allows users to model and analyze the dynamics of decision-making processes between buyers and sellers in a business-to-business context. It leverages state transition matrices, value elements, and category weights, incorporating industry types, participant knowledge, and selected strategies to simulate realistic interactions. The system is modular and designed for flexibility, allowing exploration of diverse scenarios and datasets.

## Getting Started

### Dependencies
Before installing and running the program, ensure the following prerequisites are met:

- Operating System: Windows 10 or later (or any OS with Python support).
- Python Version: Python 3.8 or later installed on your system.

Libraries: The following Python libraries must be installed:
- pandas: For data manipulation and analysis.
- openpyxl: For reading and writing .xlsx Excel files.
- xlrd: For reading .xls Excel files.
- matplotlib: For creating visualizations.
- seaborn: For advanced data visualization.
- importlib: For dynamically importing modules (built into Python, no need to install).

Summary of Installation Commands for Libraries:
- pip install pandas
- pip install openpyxl
- pip install xlrd
- pip install matplotlib
- pip install seaborn

### Installing

- To download the program, you can clone the repository from Github
```
git clone https://github.com/PATA-hanke-Spring-2025/Agent-based-Model-Basics.git
cd Agent-based-Model-Basics
```
or you can download the Zip file and extract it.
- Ensure that the following important files are present in the root directory:

#### Project Files
| File                                  | Description                                            |
| ------------------------------------- | ------------------------------------------------------ |
| `app.py`                              | Main script to load and the simulation.                |
| `agents.py`                           | Defines th agents and its behavior.                    |
| `model.py`                            | Manages and runs the simulation loop for agents.       |
| `reading.py`                          | Reads input files e.g.g transition data                |
| `value_calculator.py`                 | Calculates value scores based on elements and weights. |
| `visualize_results.py`                | Generates visualizations from simulation output.       |
| `BuyerStates.csv`                     | State definitions for buyer agents.                    |
| `SellerStates.csv`                    | State definitions for seller agents.                   |
| `BuyerTransition.csv`                 | State transition matrix for buyers.                    |
| `SellerTransition.csv`                | State transition matrix for sellers.                   |
| `category_weights.csv`                | Weights for different decision-making categories.      |
| `value_elements.csv`                  | Defines specific elements of value used in scoring.    |
| `master-parameters.md`                | Optional notes about parameters used.                  |

- Do not rename required input files unless you also update corresponding paths in the source code.
- Ensure that all CSV/XLSX input files are placed in the same directroy as the code unless configured otherwise.

### Executing program

- To run the simulation:
```
python app.py
```
- After running the simulation, results will be saved in a CSV file automatically.
- Then file is named using the format:
```
aggregated_simulation_results_YYYY-MM-DD_HH-MM-SS.csv
```
This timestamp format ensures that each result file is unique and reflects the exact time the simulation was executed.
- The program will also generate and display visual charts based on the simulation results, helping you analyze the state transitions and overall behaviour.


## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)

To Run:


Install xlrd, openpyxl, pandas, importlib, matplotlib and seaborn. If you don't have these installed using pip ("pip install xlrd", "pip install openpyxl", "pip install pandas" "pip install importlib", "pip install matplotlib", "pip install seaborn")

Run "python app.py"

