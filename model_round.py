
# Function to run single round of the model
def model_round(agent_info, payoff_dictionary):
    """
    Function for actual model round
    Scores are updated and decisions made
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
