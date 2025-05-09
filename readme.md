# Simulating B2B Buyer-Seller Interactions with Value-Based Decision Logic​

This project goal is to simulate B2B buyer-seller interactions using an agent-based model that incorporates value-based decision logic. 

## Description

 The simulation allows users to model and analyze the dynamics of decision-making processes between buyers and sellers in a business-to-business context. It leverages state transition matrices, value elements, and category weights, incorporating industry types, participant knowledge, and selected strategies to simulate realistic interactions. The system is modular and designed for flexibility, allowing exploration of diverse scenarios and datasets.

## Getting Started

### Dependencies
Before installing and running the program, ensure the following prerequisites are met:

- **Operating System**: Windows 10 or later (or any OS with Python support).
- **Python Version**: Python 3.8 or later installed on your system.

Libraries: The following Python libraries must be installed:
- `pandas`: For data manipulation and analysis.
- `openpyxl`: For reading and writing .xlsx Excel files.
- `xlrd`: For reading .xls Excel files.
- `matplotlib`: For creating visualizations.
- `seaborn`: For advanced data visualization.
- `importlib`: For dynamically importing modules (built into Python, no need to install).

Summary of Installation Commands for Libraries:
```bash
pip install pandas
pip install openpyxl
pip install xlrd
pip install matplotlib
pip install seaborn
```
### Installing
To download the program, you can either:
- Clone the repository from Github
```
git clone https://github.com/PATA-hanke-Spring-2025/Agent-based-Model-Basics.git
```
- Or download the Zip file and extract it.
Ensure that the following important files are present in the root directory:

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

### Executing Program

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

If you encounter issues while running the simulation, here are some common troubleshooting tips:
### Common Issues
**Missing Module Errors**
- Make sure all required libraries are installed. You can re-run:
```
pip install pandas openpyxl xlrd matplotlib seaborn
```
**FileNotFoundError**
- Ensure that all required input files (e.g., `SellerStates.csv`, `SellerTransition.csv`) are in the same directory as the Python scripts.
**Excel file read errors**
- Confirm that `.xlsx` files are not open in another application (e.g., Excel).
- Make sure file extensions are correct (`.csv`, `.xlsx`, etc.).
**Simulation shows no input or empty CSV**
- Check that the state and transition files are properly formatted and not empty.

###Debug Tips
- You can add or enable `print()` statements in `app.py` to inspect what's happening step-by-step.
- To verify your input files, open them in Excel or a text editor and confirm headers and data consistency.

## Authors

This project was developed by students from Haaga-Helia University of Applied Sciences in Spring 2025
- **Panelo Jonas**  
  GitHub: [`@JJonnass`](https://github.com/JJonnass)
  
- **Lyubavskaya Tatiana**   
  GitHub: [`@lTanjal`](https://github.com/lTanjal)

- **Arasola Sakari**  
  GitHub: [`@sakariarasola`](https://github.com/sakariarasola)

- **Klimovas Nojus**  
  GitHub: [`@Veyefill`](https://github.com/Veyefill)

- **Bui Quang**  
  GitHub: [`@JohnnyBui1004`](https://github.com/JohnnyBui1004)

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

