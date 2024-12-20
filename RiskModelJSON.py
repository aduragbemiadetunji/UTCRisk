import json
import numpy as np
import matplotlib.pyplot as plt


class RiskModel:
    def __init__(self, config_path):
        # Load configuration from JSON file
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        # Ship configuration
        ship_config = config["ship_configuration"]
        self.ship_model = ship_config["ship_model"]
        self.length = float(ship_config["length"])
        self.width = float(ship_config["width"])
        self.mass = float(ship_config["mass"])
        
        # Grounding costs
        grounding_cost = config["grouding_cost"]
        self.cost_ship = float(grounding_cost["ship_damage"])
        self.cost_environment = float(grounding_cost["environment"])
        self.cost_cargo = float(grounding_cost["cargo"])
        self.cost_infrastructure = float(grounding_cost["infrastructure"])
        self.cost_reputation = float(grounding_cost["reputation"])

        # Engine configurations
        self.engines = {}
        self.engine_map = {}  # Maps "Engine 1" to "ME", "Engine 2" to "DG1", etc.
        for i, engine in enumerate(config["engines"], start=1):
            engine_name = engine["engine_name"]
            self.engines[engine_name] = {
                "failure_rate": float(engine["failure_rate"]),
                "start_time": float(engine["start_time"]),
                "restart_probability": float(engine["restart_probability"])
            }
            # Create mapping based on order, e.g., "Engine 1" -> "ME"
            self.engine_map[f"Engine {i}"] = engine_name

        # Machinery modes and scenarios
        self.modes = config["modes"]

    def compute_grounding_probability(self, ttg, mode):
        """ Computes the probability of grounding at a given waypoint for a particular mode """
        # Compute the probability of machinery failure in the given mode
        p_failure = self.compute_machinery_failure_probability(mode)
        
        # Compute the probability of recovery before grounding
        p_grounding_given_failure = self.compute_recovery_probability(ttg, mode)
        # print(p_grounding_given_failure)

        
        # Total grounding probability
        p_grounding = p_failure * p_grounding_given_failure
        return p_grounding
    
    def compute_machinery_failure_probability(self, mode):
        """ Compute the probability of machinery failure for the given MSO mode """
        mode_config = next((m for m in self.modes if m["mode_name"] == mode), None)
        if not mode_config:
            return 0

        failure_rates = []
        for scenario in mode_config["scenarios"]:
            action = scenario["action"]
            engine_name = action.split(" ", 1)[-1]  # Extract "Engine 1", "Engine 2", etc.
            mapped_engine_name = self.engine_map.get(engine_name)  # Map to actual engine name
            if mapped_engine_name:
                failure_rate = self.engines.get(mapped_engine_name, {}).get("failure_rate", 0)
                failure_rates.append(failure_rate)

    
    
        combined_failure_probability = 1 - np.prod([1 - rate for rate in failure_rates])
        return combined_failure_probability
    
    def compute_recovery_probability(self, ttg, mode):
        """ Compute probability of recovery based on scenarios in the JSON configuration """
        mode_config = next((m for m in self.modes if m["mode_name"] == mode), None)
        if not mode_config:
            return 1  # Default to full recovery probability if mode is not found

        # List to store probabilities of each restoration process within the mode
        scenario_probabilities = []
        temp_probability = 1  # Track combined probability for current scenario group

        for scenario in mode_config["scenarios"]:
            action = scenario["action"]
            operation = scenario["operation"]
            engine_name = action.split(" ", 1)[-1]
            
            # Map engine number to actual engine name
            mapped_engine_name = self.engine_map.get(engine_name)
            engine_data = self.engines.get(mapped_engine_name)
            if not engine_data:
                continue

            # Compute probability of this action
            # Distinguish between "start" and "restart" actions
            if "start" in action.lower():
                # Start actions assume a probability of 1
                p_action = self._recovery_time_probability(ttg, engine_data["start_time"])
            elif "restart" in action.lower():
                # Restart actions include the restart probability
                p_action = engine_data["restart_probability"] * self._recovery_time_probability(ttg, engine_data["start_time"])

            if operation == "AND":
                temp_probability *= p_action  # Sequential "AND" multiplies probabilities
            elif operation == "Terminate":
                temp_probability *= p_action  # Final action before termination
                scenario_probabilities.append(temp_probability)  # Save this scenario's total probability
                temp_probability = 1  # Reset for next scenario

        # Compute total probability for the mode by combining all scenario probabilities
        total_recovery_probability = np.prod([1 - p for p in scenario_probabilities])
        # print(f'operation: {operation}, engine_data: {engine_data}, p_action {p_action} probability: {temp_probability}')
        return total_recovery_probability


    def _recovery_time_probability(self, ttg, recovery_time):
        """ Computes the probability of successful recovery within the available time to grounding (TTG) """
        if ttg <= recovery_time:
            return 0  # No time to recover
        return np.exp(-recovery_time / ttg)

    def compute_total_risk(self, ttg, mode):
        """ Computes the total risk at a waypoint based on grounding probability and cost """
        p_grounding = self.compute_grounding_probability(ttg, mode)
        cost = self.cost_ship + self.cost_environment + self.cost_cargo + self.cost_infrastructure + self.cost_reputation
        total_risk = p_grounding * cost * 1000
        return total_risk

    def select_mso_mode(self, ttg):
        """ Selects the optimal MSO mode for a given waypoint to minimize risk and maximize efficiency """
        risks = {mode["mode_name"]: self.compute_total_risk(ttg, mode["mode_name"]) for mode in self.modes}
        return min(risks, key=risks.get)