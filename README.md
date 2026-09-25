## 🚀 HDL Verification 
A collection of digital design modules written in Verilog, integrated with an automated verification framework built using cocotb and Python.
## 📋 Featured Projects
ProjectDescriptionTest CasesCounter8-bit counter featuring reset logic and overflow detection.3 ✅Vending MachineFinite State Machine (FSM) based vending system handling multiple states.7 ✅
## 🛠️ Prerequisites
Make sure you have the following installed on your system before getting started:

* Python (v3.9 or higher)

* Icarus Verilog (for HDL simulation)

* cocotb

## 💻 Setup & Installation
# 1. Create a virtual environment
python -m venv cocotb_env

# 2. Activate the virtual environment
# On Windows:
cocotb_env\Scripts\activate

# On Linux / macOS:
source cocotb_env/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

## 🏃 Running Tests
* You can run the verification environment for each project independently using their respective runners:
  # Run tests for the Counter module
python runners/run_counter.py

# Run tests for the Vending Machine module
python runners/run_vending.py

## 📁 Repository Structure
hdl-automation/
├── duts/               # Hardware designs (Design Under Test)
├── tests/              # Testbenches and test scenarios
├── runners/            # Simulation test runners
├── .gitignore          # Ignored simulation and environment files
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
## 👤 Author: Zeyad
