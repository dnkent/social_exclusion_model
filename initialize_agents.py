# Function for initializing all agents in the model

import pandas as pd
import numpy as np
import random
from scipy.stats import truncnorm


def agent_initialize(n_agents, ideal_mean, ideal_sigma, h_perc) -> pd.DataFrame:
    '''
    Function that creates a dataframe with all starting agent info
    '''
    # Master dataframe
    agent_info = pd.DataFrame(
        columns = [
            'ID',                   # Agent ID
            'Membership',           # Hierarchy or market member
            'Type',                 # Pre-specified type (TFT, COOP, DEF)
            'Ideal_Point',          # Pre-specified ideal point
            'Market_Ideal_Estimate',# Agent est of market avg ip
            'Market_Coop_Belief',   # Agent est of market coop %
            'Market_Int',           # Number of interactions in market
            'Score'                 # Agent aggregate score
        ]
    )

    # IDs
    agent_info['ID'] = list(range(1, n_agents+1))

    # Member of hierarchy or market at pre-set probability
    membership = np.random.choice(
        ['h', 'm'], 
        n_agents, 
        p = [h_perc, 1 - h_perc]
        )
    agent_info['Membership'] = membership # fill in dataframe

    # Agent type 
    strategies = np.random.choice(
        ['TFT', 'C', 'D'], # Possible strategies
        n_agents,
        p = [0.34, 0.33, 0.33] # 0.34 because needs to sum to 1
    )
    agent_info['Type'] = strategies # fill in dataframe

    # Ideal points: truncated normal b/w 0 and 1
    agent_info['Ideal_Point'] = truncnorm.rvs(
        a = (0 - ideal_mean) / ideal_sigma,
        b = (1 - ideal_mean) / ideal_sigma,
        loc = ideal_mean,
        scale = ideal_sigma, 
        size = n_agents
    )

    # Start remaining quantities at 0 and update as model runs
    agent_info['Market_Ideal_Estimate'] = np.zeros(n_agents)
    agent_info['Market_Coop_Belief'] = np.zeros(n_agents)
    agent_info['Market_Int'] = np.zeros(n_agents)
    agent_info['Score'] = np.zeros(n_agents)

    # Return data frame for use
    return agent_info