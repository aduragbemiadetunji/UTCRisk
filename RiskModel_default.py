import numpy as np
import matplotlib.pyplot as plt

class RiskModel:
    def __init__(self, machinery_modes, 
                 cost_ship, cost_environment, cost_cargo, cost_infrastructure, cost_reputation,
                 failure_rate_me, failure_rate_dg1, failure_rate_dg2, failure_rate_hsg,
                 start_me_time, restart_me_probability, start_dg1_time, restart_dg1_probability, 
                 start_dg2_time, restart_dg2_probability, restart_hsg_time):

        self.machinery_modes = machinery_modes
        
        
        # Risk Costs
        self.cost_ship = cost_ship
        self.cost_environment = cost_environment
        self.cost_cargo = cost_cargo
        self.cost_infrastructure = cost_infrastructure
        self.cost_reputation = cost_reputation
        
        # Failure rates  I WILL STILL CHANGE THIS TO MODES INSTEAD
        self.failure_rate_me = failure_rate_me
        self.failure_rate_dg1 = failure_rate_dg1
        self.failure_rate_dg2 = failure_rate_dg2
        self.failure_rate_hsg = failure_rate_hsg
        
        # Restoration times and probabilities
        self.start_me_time = start_me_time
        self.restart_me_probability = restart_me_probability
        self.start_dg1_time = start_dg1_time
        self.restart_dg1_probability = restart_dg1_probability
        self.start_dg2_time = start_dg2_time
        self.restart_dg2_probability = restart_dg2_probability
        self.restart_hsg_time = restart_hsg_time
        
        # TTG (Time-to-Grounding) data block
        # self.ttg_data = ttg_data
        

    
    def compute_grounding_probability(self, ttg, mode):
        """ Computes the probability of grounding at a given waypoint for a particular mode """
        # Get TTG for this waypoint using the current ship state
        
        # Compute the probability of machinery failure in the given mode
        p_failure = self.compute_machinery_failure_probability(mode)
        
        # Assume failure occurs at some point, now compute the probability of recovering before grounding
        p_grounding_given_failure = self.compute_recovery_probability(ttg, mode)

        
        # Total grounding probability (Equation 5)
        p_grounding = p_failure * p_grounding_given_failure
        # print(p_grounding_given_failure)


        # print(p_grounding_given_failure)
        return p_grounding
    
    
    def compute_machinery_failure_probability(self, mode):
        """ Compute the probability of machinery failure for the given MSO mode """
        if mode == 'PTO':
            return 1 - np.exp(-self.failure_rate_me)
        elif mode == 'MEC':
            return 1 - np.exp(-self.failure_rate_me)
        elif mode == 'PTI':
            return 1 - np.exp(-self.failure_rate_dg1 - self.failure_rate_dg2)
        else:
            return 0
        

    
    def compute_recovery_probability(self, ttg, mode):
        """ Compute probability of failure to recover before grounding """ #CHANGE THIS TO MODE INSTEAD OF MACHINERYYY, LIKE JUST RETURN THE PROBABILITY INSTEAD OF FOLLOWING TABLE 2
        if mode == 'PTO':
            # Restart main engine
            p_restart_me = self.restart_me_probability * self._recovery_time_probability(ttg, self.start_me_time)


            # Option 2: Start DG1 and HSG
            p_start_dg1 = self._recovery_time_probability(ttg, self.start_dg1_time)
            p_start_hsg_dg1 = self._recovery_time_probability(ttg, self.restart_hsg_time)

            # Option 3: Start DG2 and HSG
            p_start_dg2 = self._recovery_time_probability(ttg, self.start_dg2_time)
            p_start_hsg_dg2 = self._recovery_time_probability(ttg, self.restart_hsg_time)


            return (1 - p_restart_me) * (1 - (p_start_dg1 * p_start_hsg_dg1)) * (1 - (p_start_dg2 * p_start_hsg_dg2))
        elif mode == 'MEC':
            # Restart ME or Start HSG
            p_restart_me = self.restart_me_probability * self._recovery_time_probability(ttg, self.start_me_time)
            p_start_hsg = self._recovery_time_probability(ttg, self.restart_hsg_time)
            return 1 - (p_restart_me or p_start_hsg)
        elif mode == 'PTI':
            # Restart DG1 or DG2 or Start ME
            p_restart_dg1 = self.restart_dg1_probability * self._recovery_time_probability(ttg, self.start_dg1_time)
            p_restart_dg2 = self.restart_dg2_probability * self._recovery_time_probability(ttg, self.start_dg2_time)
            p_start_me = self._recovery_time_probability(ttg, self.start_me_time)
            return 1 - (p_restart_dg1 or p_restart_dg2 or p_start_me)
    
    def _recovery_time_probability(self, ttg, recovery_time):
        """ Computes the probability of successful recovery within the available time to grounding (TTG) """
        if ttg <= recovery_time:
            return 0  # No time to recover
        return np.exp(-recovery_time / ttg)
    
    def compute_total_risk(self, ttg, mode):
        """ Computes the total risk at a waypoint based on grounding probability and cost """
        p_grounding = self.compute_grounding_probability(ttg, mode)
        cost = self.cost_ship + self.cost_environment + self.cost_cargo + self.cost_infrastructure + self.cost_reputation
        
        # Total risk (Equation 10)
        total_risk = p_grounding * cost * 100
        # print(total_risk)
        return total_risk
    
    def select_mso_mode(self, ttg):
        """ Selects the optimal MSO mode for a given waypoint to minimize risk and maximize efficiency """
        risks = {}
        for mode in self.machinery_modes:
            risks[mode] = self.compute_total_risk(ttg, mode)

        return min(risks, key=risks.get)



# Initialize the RiskModel with parameters
risk_model = RiskModel( 
    machinery_modes=['PTO', 'MEC', 'PTI'], cost_ship=100000, cost_environment=50000, 
    cost_cargo=200000, cost_infrastructure=150000, cost_reputation=10000, 
    failure_rate_me=3e-9, failure_rate_dg1=6e-9, failure_rate_dg2=6e-9, failure_rate_hsg=2e-9, 
    start_me_time=50, restart_me_probability=0.4, start_dg1_time=35, restart_dg1_probability=0.5, 
    start_dg2_time=35, restart_dg2_probability=0.5, restart_hsg_time=12,
)





ttgs = np.linspace(0, 2000, 100)
# ttgs = []

""" Evaluates the total risk for the entire path, across all waypoints """
total_risk = 0
risk_list = []




for ttg in ttgs:
    mode = risk_model.select_mso_mode(ttg)
    risk = risk_model.compute_total_risk(ttg, mode)
    risk_list.append(risk)
    total_risk += risk_model.compute_total_risk(ttg, mode)
    # print(mode)

print(f"Total Risk: {total_risk}")
# print(len(risk_list))


plt.plot(ttgs, risk_list)
plt.ylabel('Risk')
plt.xlabel('TTG (seconds)')
plt.show()



#     mode = self.select_mso_mode(waypoint)
#     total_risk += self.compute_total_risk(waypoint, mode)


# return total_risk



