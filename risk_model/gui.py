import customtkinter as ctk
from tkinter import messagebox

import json
import os

ctk.set_appearance_mode("Light")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class RiskAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Ship Risk Analysis GUI")
        self.geometry("1400x900")  # Set a larger width to accommodate horizontal layout

        # Step 1: Ship Configuration Frame
        self.ship_config_frame = ctk.CTkFrame(self, corner_radius=10)
        self.ship_config_frame.pack(pady=10, padx=10, fill="x")
        self.create_ship_config_section()

        # Initialize storage for modes and scenarios, other frames are added dynamically
        self.modes = []
        self.engine_frame = None  # Placeholder for engine frame
        self.modes_frame = None  # Placeholder for modes frame


    def create_ship_config_section(self):
        title = ctk.CTkLabel(self.ship_config_frame, text="Ship Configuration", font=ctk.CTkFont(size=15, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=5)

        # Ship configuration fields, loaded horizontally
        ctk.CTkLabel(self.ship_config_frame, text="Ship Model/Type").grid(row=1, column=0, padx=5, pady=5)
        self.ship_name_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Ship Model/Type")
        self.ship_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Length (m)").grid(row=1, column=2, padx=5, pady=5)
        self.length_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Length (m)")
        self.length_entry.grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Width (m)").grid(row=1, column=4, padx=5, pady=5)
        self.width_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Width (m)")
        self.width_entry.grid(row=1, column=5, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Mass/Displacement (tons)").grid(row=1, column=6, padx=5, pady=5)
        self.mass_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Mass/Displacement (tons)")
        self.mass_entry.grid(row=1, column=7, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Number of Engines").grid(row=1, column=8, padx=5, pady=5)
        self.num_engines_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Number of Engines")
        self.num_engines_entry.grid(row=1, column=9, padx=5, pady=5)

        # Cost of grounding parameters, loaded vertically
        grounding_cost_title = ctk.CTkLabel(self.ship_config_frame, text="Cost of Grounding", font=ctk.CTkFont(size=13, weight="bold"))
        grounding_cost_title.grid(row=2, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkLabel(self.ship_config_frame, text="Ship Damage").grid(row=3, column=0, padx=5, pady=5)
        self.cost_ship_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Cost of Ship Damage")
        self.cost_ship_entry.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Recovery").grid(row=3, column=2, padx=5, pady=5)
        self.cost_recovery_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Cost of Recovery")
        self.cost_recovery_entry.grid(row=3, column=3, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Cargo").grid(row=3, column=4, padx=5, pady=5)
        self.cost_cargo_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Cost of Cargo")
        self.cost_cargo_entry.grid(row=3, column=5, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Environmental").grid(row=4, column=0, padx=5, pady=5)
        self.cost_environment_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Environmental Damage Cost")
        self.cost_environment_entry.grid(row=4, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Infrastructure").grid(row=4, column=2, padx=5, pady=5)
        self.cost_infrastructure_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Infrastructure Damage Cost")
        self.cost_infrastructure_entry.grid(row=4, column=3, padx=5, pady=5)

        ctk.CTkLabel(self.ship_config_frame, text="Reputation").grid(row=4, column=4, padx=5, pady=5)
        self.cost_reputation_entry = ctk.CTkEntry(self.ship_config_frame, placeholder_text="Reputation Damage Cost")
        self.cost_reputation_entry.grid(row=4, column=5, padx=5, pady=5)

        # Button to proceed to engine parameters after ship configuration
        self.load_engines_button = ctk.CTkButton(self.ship_config_frame, text="Next: Define Engines", command=self.load_engine_parameters)
        self.load_engines_button.grid(row=5, column=0, columnspan=4, pady=10)



    def load_engine_parameters(self):
        try:
            # Validate engine number input
            self.num_engines = int(self.num_engines_entry.get())
            if self.num_engines <= 0:
                raise ValueError("Number of engines must be positive.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of engines.")
            return

        # Step 2: Load Engine Parameters Frame after Ship Configuration
        if self.engine_frame is None:
            self.engine_frame = ctk.CTkFrame(self, corner_radius=10)
            self.engine_frame.pack(pady=10, padx=10, fill="x")

        title = ctk.CTkLabel(self.engine_frame, text="Engine Parameters", font=ctk.CTkFont(size=15, weight="bold"))
        title.grid(row=0, column=0, columnspan=4, pady=5)

        # Column headers for better organization
        headers = ["Engine Name", "Failure Rate", "Start Time (s)", "Restart Probability"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.engine_frame, text=header)
            header_label.grid(row=1, column=col, padx=5, pady=5)

        # Store engine parameters and populate engine names for dropdown use in modes
        self.engine_entries = []
        self.engine_names = []
        for i in range(self.num_engines):
            engine_name = ctk.CTkEntry(self.engine_frame, placeholder_text="Name")
            engine_name.grid(row=i+2, column=0, padx=5, pady=5)
            self.engine_names.append(f"Engine {i+1}")

            failure_rate = ctk.CTkEntry(self.engine_frame, placeholder_text="Failure Rate")
            failure_rate.grid(row=i+2, column=1, padx=5, pady=5)

            start_time = ctk.CTkEntry(self.engine_frame, placeholder_text="Start Time (s)")
            start_time.grid(row=i+2, column=2, padx=5, pady=5)

            restart_prob = ctk.CTkEntry(self.engine_frame, placeholder_text="Restart Probability (0-1)")
            restart_prob.grid(row=i+2, column=3, padx=5, pady=5)

            self.engine_entries.append((engine_name, failure_rate, start_time, restart_prob))

        # Button to proceed to Machinery Modes after defining engines
        self.load_modes_button = ctk.CTkButton(self.engine_frame, text="Next: Define Machinery Modes", command=self.create_modes_section)
        self.load_modes_button.grid(row=self.num_engines + 2, column=0, columnspan=4, pady=10)

    def create_modes_section(self):
        # Step 3: Load Machinery Modes Frame
        if self.modes_frame is None:
            self.modes_frame = ctk.CTkFrame(self, corner_radius=10)
            self.modes_frame.pack(pady=10, padx=10, fill="x")

        # Title for mode section
        title = ctk.CTkLabel(self.modes_frame, text="Add Machinery Mode", font=ctk.CTkFont(size=15, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=5)

        # Input field and button for adding modes
        self.mode_name_entry = ctk.CTkEntry(self.modes_frame, placeholder_text="Mode Name")
        self.mode_name_entry.grid(row=1, column=0, padx=5, pady=5)

        self.add_mode_button = ctk.CTkButton(self.modes_frame, text="Add Mode", command=self.add_mode)
        self.add_mode_button.grid(row=1, column=1, padx=5, pady=5)

        self.generate_file_frame = ctk.CTkFrame(self, corner_radius=10)
        self.generate_file_frame.pack(pady=20, padx=10, fill="x")
        self.generate_button = ctk.CTkButton(self.generate_file_frame, text="Generate File", command=self.generate_file, fg_color='green')
        self.generate_button.pack(pady=10)
        self.output_label1 = ctk.CTkLabel(self.generate_file_frame, text="", font=ctk.CTkFont(size=12))
        self.output_label1.pack()





    def add_mode(self):
        mode_name = self.mode_name_entry.get()
        if not mode_name:
            messagebox.showerror("Input Error", "Please enter a mode name.")
            return

        # Create a new frame for the mode's scenarios horizontally
        mode_index = len(self.modes)
        scenario_frame = ctk.CTkFrame(self.modes_frame, corner_radius=10)
        scenario_frame.grid(row=2, column=mode_index, padx=10, pady=5, sticky="nsew")

        # Header for the scenario section
        mode_title = ctk.CTkLabel(scenario_frame, text=f"Mode: {mode_name}", font=ctk.CTkFont(size=13, weight="bold"))
        mode_title.grid(row=0, column=0, columnspan=2, pady=5)

        # Button to add scenarios within the mode
        self.add_scenario_button = ctk.CTkButton(scenario_frame, text="Add Scenario", command=lambda: self.add_scenario_row(scenario_frame, mode_index))
        self.add_scenario_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Append this mode with its own unique empty list of scenarios
        self.modes.append({"name": mode_name, "frame": scenario_frame, "scenarios": []})



    def handle_operation(self, operation, scenario_frame, row, mode_index):
        """
        Handles the addition of extra actions in case of 'AND' or 'OR' operations
        without resetting existing selections.
        """
        if operation == "Terminate":
            return  # No additional actions are needed; terminate here

        # Add new action dropdown to extend the scenario based on 'AND' or 'OR' operation
        new_action_options = [f"Restart {engine}" for engine in self.engine_names] + [f"Start {engine}" for engine in self.engine_names]
        new_action_dropdown = ctk.CTkOptionMenu(scenario_frame, values=new_action_options)
        new_action_dropdown.grid(row=row, column=2, padx=5, pady=5)

        # New operation dropdown for further chaining or termination
        new_operation_type = ctk.CTkOptionMenu(scenario_frame, values=["Terminate", "AND", "OR"])
        new_operation_type.grid(row=row, column=3, padx=5, pady=5)

        # Configure command for chaining
        new_operation_type.configure(command=lambda: self.handle_operation(new_operation_type.get(), scenario_frame, row + 1, mode_index))

        # Append the new action and operation to the specific mode's scenario list
        self.modes[mode_index]["scenarios"].append((new_action_dropdown, new_operation_type))



    # Modify add_scenario_row to add scenarios to the specific mode's scenarios list
    def add_scenario_row(self, scenario_frame, mode_index):
        row = len(scenario_frame.grid_slaves()) // 2 + 1

        # Combined dropdown for action and engine selection
        action_options = [f"Restart {engine}" for engine in self.engine_names] + [f"Start {engine}" for engine in self.engine_names]
        action_dropdown = ctk.CTkOptionMenu(scenario_frame, values=action_options)
        action_dropdown.grid(row=row, column=0, padx=5, pady=5)

        # AND/OR/Terminate operation selection
        operation_type = ctk.CTkOptionMenu(scenario_frame, values=["Terminate", "AND", "OR"],
                                        command=lambda op, row=row: self.add_additional_action(op, scenario_frame, row))
        operation_type.grid(row=row, column=1, padx=5, pady=5)

        # Append the scenario to the correct mode's scenario list
        self.modes[mode_index]["scenarios"].append((action_dropdown, operation_type))



    def add_additional_action(self, operation, scenario_frame, row):
        if operation == "Terminate":
            return  # Stop adding further actions

        # Combined dropdown for additional action selection
        action_options = [f"Restart {engine}" for engine in self.engine_names] + [f"Start {engine}" for engine in self.engine_names]
        action_dropdown = ctk.CTkOptionMenu(scenario_frame, values=action_options)
        action_dropdown.grid(row=row, column=0, padx=5, pady=5)

        # AND/OR/Terminate operation selection for the additional action
        operation_type = ctk.CTkOptionMenu(scenario_frame, values=["Terminate", "AND", "OR"],
                                           command=lambda op, r=row+1: self.add_additional_action(op, scenario_frame, r))
        operation_type.grid(row=row, column=1, padx=5, pady=5)



    def generate_file(self):
        # Extract Ship Configuration
        ship_config = {
            "ship_model": self.ship_name_entry.get(),
            "length": self.length_entry.get(),
            "width": self.width_entry.get(),
            "mass": self.mass_entry.get()
        }

                # Extract Cost of Grounding
        grounding_cost = {
            "ship_damage": self.cost_ship_entry.get(),
            "recovery": self.cost_recovery_entry.get(),
            "cargo": self.cost_cargo_entry.get(),
            "environment": self.cost_environment_entry.get(),
            "infrastructure": self.cost_infrastructure_entry.get(),
            "reputation": self.cost_reputation_entry.get()
        }

        # Extract Engine Parameters
        engines = []
        for engine_entry in self.engine_entries:
            engine_name, failure_rate, start_time, restart_prob = engine_entry
            engines.append({
                "engine_name": engine_name.get(),
                "failure_rate": failure_rate.get(),
                "start_time": start_time.get(),
                "restart_probability": restart_prob.get()
            })

        # Extract Modes and Scenarios
        modes = []
        for mode in self.modes:
            mode_data = {
                "mode_name": mode["name"],
                "scenarios": []
            }
            # Loop through each scenario specifically tied to this mode
            for scenario_action, operation_type in mode["scenarios"]:
                mode_data["scenarios"].append({
                    "action": scenario_action.get(),
                    "operation": operation_type.get()
                })
            modes.append(mode_data)  # Append mode with its scenarios to the modes list

        # Combine all data into one configuration
        config_data = {
            "ship_configuration": ship_config,
            "grouding_cost": grounding_cost,
            "engines": engines,
            "modes": modes
        }

        # Save to JSON file
        file_path = "ship_config.json"
        with open(file_path, "w") as json_file:
            json.dump(config_data, json_file, indent=4)

        # Update output label to indicate success
        self.output_label1.configure(text=f"Configuration file generated: {os.path.abspath(file_path)}")








# Run the app
if __name__ == "__main__":
    app = RiskAnalysisApp()
    app.mainloop()
