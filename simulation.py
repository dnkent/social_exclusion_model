#-----------------------------------
# Simulation output for entire model
#-----------------------------------
from initialize_agents import agent_initialize
from learning_rounds import learning_round
from model_iteration import model_round
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
from scipy.stats import truncnorm

# So the more we put a weight on the hierarchy ideal point
# Then the fewer agents select in at equilibrium
# But the higher their average payoffs are
random.seed(12345)

# Create agents
agent_info = agent_initialize(
    n_agents = 99,      # ideal divisible by 3 
    ideal_mean = 0.5, 
    ideal_sigma = 0.2,
    h_perc = 0.50 # starting percent in hierarchy, can tip either way
)

R = 3 # C,C
S = 0 # C,D
T = 5 # D,C
P = 1 # D,D

payoffs = {
    ("C", "C"): R,
    ("C", "D"): S, 
    ("D", "C"): T,
    ("D", "D"): P,
}

# Have them learn
learning_round(
    agent_info = agent_info, 
    payoffs = payoffs,
    n_ints = 10 # can vary
)

for i in range(0, 20):
    model_round(
        agent_info = agent_info,
        payoffs = payoffs,
        m_pref_weight = 1, # market coop at middle of ideal points
        h_pref_weight = 1, # this drives all to hierarchy when at 1
        h_ideal = 0.5,
        defection = 0.5, # penalty for defection
        h_tax = 0.05, # this drives membership too
        h_coop = 0.95,
        order = 'simultaneous', # options are 'step' and 'simultaneous'
        h_ideal_endog = False # Options are True or False
    )
    print(agent_info.loc[1, 'Score'])
    print(agent_info.Membership.value_counts())
    #print(agent_info['Score'].describe()['50%'])

# Quick look at results
df = agent_info.groupby(['Membership']).size()
df.plot(kind = 'bar')

sum(agent_info[agent_info['Membership'] == 'h']['Ideal_Point'])/len(
    agent_info[agent_info['Membership'] == 'h']
)

# Average scores 
# Hierarchy
sum(agent_info[agent_info['Membership'] == 'h']['Score'])/len(
    agent_info[agent_info['Membership'] == 'h']
)

# Market
sum(agent_info[agent_info['Membership'] == 'm']['Score'])/len(
    agent_info[agent_info['Membership'] == 'm']
)

# More restrictive the hierarchy, then the smaller
# So smaller hierarchy leads to larger payoffs