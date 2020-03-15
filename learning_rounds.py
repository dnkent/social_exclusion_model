# Function to run learning rounds where agents estimate characteristics
# of the market and hierarchy

import numpy as np
import pandas as pd
import random

def learning_round(agent_info: pd.DataFrame, payoffs: dict, n_ints):
    '''
    Function for learning round: agents make estimates about market unknowns
    The hierarchy (a tradeoff of autonomy for security) has no uncertainty
    '''
    # Number of agents
    n_agents = len(agent_info)

    # TFT Memory bank -- start all C
    tft_matrix = np.repeat('C', n_agents * n_agents) # create elements
    tft_matrix.shape = (n_agents, n_agents) # turn into matrix

    # Hierarchy members
    h_members = list(agent_info[agent_info['Membership'] == 'h']['ID'])
    # Market members
    m_members = list(agent_info[agent_info['Membership'] == 'm']['ID'])

    # Have each agent play a random market member to learn about the market
    for i in range(0, n_agents):
        while agent_info.loc[i, 'Market_Int'] < n_ints:
            j = random.choice(m_members) - 1 # subtract 1 for indexing

            # Update interaction count
            agent_info.loc[i, 'Market_Int'] += 1

            # Extract stratgies
            i_strategy = agent_info.loc[i, 'Type']
            j_strategy = agent_info.loc[j, 'Type']

            # Tit-for-tat? Start at C if no history, otherwise last play
            if i_strategy == 'TFT' and tft_matrix[j, i] == 'C':
                i_strategy = 'C' 
            else:
                i_strategy = 'D'
            # agent j
            if j_strategy == 'TFT' and tft_matrix[i, j] == 'C':
                j_strategy = 'C'
            else:
                j_strategy = 'D'

            # Update market ideal point estimate
            agent_info.loc[i, 'Market_Ideal_Estimate'] = (
                agent_info.loc[i, 'Market_Ideal_Estimate'] *  # current estimate
                (agent_info.loc[i, 'Market_Int'] - 1) +  # n-ints - 1
                agent_info.loc[j, 'Ideal_Point'] # Other IP
            ) / agent_info.loc[i, 'Market_Int'] # n-interactions

            # Update percent of observed agents that cooperate
            if j_strategy == 'C':
                agent_info.loc[i,'Market_Coop_Belief'] = (
                    agent_info.loc[i, 'Market_Coop_Belief'] * # obs coop 
                    (agent_info.loc[i, 'Market_Int'] - 1) + 1 # +1 if coop
                ) / agent_info.loc[i, 'Market_Int'] # n-ints
            else:
                agent_info.loc[i,'Market_Coop_Belief'] = (
                    agent_info.loc[i, 'Market_Coop_Belief'] * # obs coop
                    (agent_info.loc[i, 'Market_Int'] - 1) + 0 # +0 if no coop
                ) / agent_info.loc[i, 'Market_Int']