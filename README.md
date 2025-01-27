# UTCRisk
The Risk part of the UTC project. It assumes the user has Time to Grounding (TTG) estimated, and uses this to estimate the risk based on machinery components and modes.

The package has five (5) files:
- RiskModel_default file
- Machinery_GUI file
- ship_config JSON file
- RiskModelJSON file
- risk_example file

## RiskModel_default file
The RiskModel default file is based on the machinery example as described in the paper: https://www.mdpi.com/2077-1312/11/2/327
The machinery mode is based on the example from the paper

## Machinery_GUI file
The GUI file is used to generalize the default file such that you can specify engine numbers and parameters, as well as the machinery modes and restoration scenarios,
necessary to re-operate each of the modes. The end goal is to generate a JSON file with all these configuartions.

## ship_config JSON file
The JSON file generated has all the configuration file, and has been designed to fit a particular format. You necessarily dont need to use the GUI to generate 
this JSON file, as long as you follow the template and naming convention. For the restoration scenrio, it follows the format:

    modes: [ {
        mode name: xx,
        scenarios:[
            {
            action: Start/Restart,
            operation: Terminate/AND
            },
            {
                ...
            },
            {
                ...
            }, 
            ]
        },
        {
        mode name: yy,
                .
                .
                .
        }
        
    ]

The action can be to "Start" or "Restart" with the Engine type eg "Engine 1", depending on the restoraion sequence

For example: "Start Engine 1".

The operation can be "Terminate" or "AND". Terminate is for just one action, while AND is to add more actions, that cummulatively restores the scenario, before you Terminte which ends the sequence.

Multiple actions in a mode means there are multiple ways to restore the engines.

## RiskModelJSON file
The RiskModelJSON uses the JSON file to build the model based on the configuration parameters in the JSON file.

## risk_example file
The risk_example file has three ways to use the models based on need and the structure of the TTG.

    case 1: For getting risk for a single ttg value
    case 2: For getting total risk given a couple of ttg values like in case of a trajectory
    case 3: To display the Risk profile given a large enough timeframe until the decline phases off



## Installation

    The package just requires the installation of the following packages
    - numpy
    - matplotlib
    - customtkinter


1. Clone the Repository 

    git clone https://github.com/aduragbemiadetunji/UTCRisk

    cd UTCRisk

2. Install the Package: Use pip to install the package in editable mode:

    pip install -e . 

3. Install Additional Dependencies (if not automatically installed): If the requirements are not installed during setup, install them manually:

    pip install -r requirements.txt


## How to Use

1. Run Example Scripts: Use the provided example scripts in the examples/ directory:

    python examples/risk_example.py

2. Use the GUI: Run the GUI to generate JSON configurations:

    python -m risk_model.gui

## Uninstallation

    pip uninstall utcrisk

