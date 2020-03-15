## Learning round if hierarchy prob of coop is endogenous to member 
## attributes and not just some preset probability enforced by the hierarch.

from initialize_agents import agent_initialize
import numpy as np
import random
import matplotlib.pyplot as plt

agent_info = agent_initialize(
    num_agents = 99, 
    ideal_mean = 0.5, 
    ideal_sigma = 0.2
)

R = 3 # C,C
S = 0 # C,D
T = 5 # D,C
P = 1 # D,D

payoff_dictionary = {
    ("C", "C"): R,
    ("C", "D"): S, 
    ("D", "C"): T,
    ("D", "D"): P,
}

# Make sure agents play in both groups
# So they can make a reasonable expected utility calc

# n interactions per group per agent
def learning_round(agent_info, payoff_dictionary, num_ints):
    """
    Function for learning round
    """
    # Number of agents
    num_agents = agent_info.shape[0]

    # TFT Memory bank 
    tft_matrix = np.repeat("C", num_agents * num_agents)
    tft_matrix = tft_matrix.reshape((num_agents, num_agents))

    # Hierarchy members
    hierarchy_members = agent_info[agent_info['Membership'] == "h"]
    hierarchy_members = list(hierarchy_members['ID'])

    # Market members
    market_members = agent_info[agent_info['Membership'] == "m"]
    market_members = list(market_members['ID'])

    # Number of interactions per group
    num_ints = num_ints

    # Loop
    for i in range(1, num_agents+1):
        while agent_info.loc[i-1, "Hierarchy_Int"] < num_ints:
            j = random.choice(hierarchy_members)
            # Update interaction count
            agent_info.loc[i-1, "Hierarchy_Int"] += 1

            # Extract stratgies
            i_strategy = agent_info.loc[i-1, "Type"]
            j_strategy = agent_info.loc[j-1, "Type"]

            # Tit-for-tat?
            # agent i -- starting value is C if no history
            if i_strategy == "TFT" and tft_matrix[j-1, i-1] == "C":
                i_strategy = "C" 
            else:
                i_strategy = "D"
            # agent j
            if j_strategy == "TFT" and tft_matrix[i-1, j-1] == "C":
                j_strategy = "C"
            else:
                j_strategy = "D"

            if j_strategy == 'C':
                agent_info.loc[i-1,"Hierarchy_Coop_Belief"] = (agent_info.loc[i-1, "Hierarchy_Coop_Belief"] * (agent_info.loc[i-1, "Hierarchy_Int"] - 1) + 1) / agent_info.loc[i-1, "Hierarchy_Int"]
            else:
                agent_info.loc[i-1,"Hierarchy_Coop_Belief"] = (agent_info.loc[i-1, "Hierarchy_Coop_Belief"] * (agent_info.loc[i-1, "Hierarchy_Int"] - 1) + 0) / agent_info.loc[i-1, "Hierarchy_Int"]

        while agent_info.loc[i-1, "Market_Int"] < num_ints:
            j = random.choice(market_members)
            # Update interaction count
            agent_info.loc[i-1, "Market_Int"] += 1

            # Extract stratgies
            i_strategy = agent_info.loc[i-1, "Type"]
            j_strategy = agent_info.loc[j-1, "Type"]

            # Tit-for-tat?
            # agent i -- starting value is C if no history
            if i_strategy == "TFT" and tft_matrix[j-1, i-1] == "C":
                i_strategy = "C" 
            else:
                i_strategy = "D"
            # agent j
            if j_strategy == "TFT" and tft_matrix[i-1, j-1] == "C":
                j_strategy = "C"
            else:
                j_strategy = "D"

            # Learn
            # If in the market, agent updates average ideal point
            agent_info.loc[i-1, "Market_Ideal_Estimate"] = (agent_info.loc[i-1, "Market_Ideal_Estimate"] * (agent_info.loc[i-1, "Market_Int"] - 1) + agent_info.loc[j-1, "Ideal_Point"]) / agent_info.loc[i-1, "Market_Int"]

            # Update percent of observed agents that cooperate
            if j_strategy == 'C':
                agent_info.loc[i-1,"Market_Coop_Belief"] = (agent_info.loc[i-1, "Market_Coop_Belief"] * (agent_info.loc[i-1, "Market_Int"] - 1) + 1) / agent_info.loc[i-1, "Market_Int"]
            else:
                agent_info.loc[i-1,"Market_Coop_Belief"] = (agent_info.loc[i-1, "Market_Coop_Belief"] * (agent_info.loc[i-1, "Market_Int"] - 1) + 0) / agent_info.loc[i-1, "Market_Int"]

learning_round(
    agent_info = agent_info, 
    payoff_dictionary = payoff_dictionary,
    num_ints = 20
)
