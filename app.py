import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -------------------------------
# Preconfigured players list
# -------------------------------
players_list = ["Anand", "JJ", "Maity", "Ashutosh", "Arpan", "Ganesh"]

# File to store match data persistently
DATA_FILE = "match_data.csv"

# -------------------------------
# Utility functions
# -------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Define an empty dataframe with the required columns
        return pd.DataFrame(columns=["match_id", "player", "team_index", "rank", "reward", "entry_fee", "net_earning"])

def save_match_data(new_data):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
    else:
        new_data.to_csv(DATA_FILE, index=False)

def get_reward(rank_str, first_term, ratio):
    """Return reward for a winning team based on its rank.
       For a rank like 'top1' or 'bottom2', extract the number and compute:
           reward = first_term * (ratio ** (n - 1))
       If the team did not win (i.e. 'No Win') then reward is 0.
    """
    if rank_str == "No Win":
        return 0
    try:
        if rank_str.startswith("top"):
            num = int(rank_str[3:])
        elif rank_str.startswith("bottom"):
            num = int(rank_str[6:])
        else:
            return 0
        return first_term * (ratio ** (num - 1))
    except Exception as e:
        return 0

# -------------------------------
# Sidebar Navigation
# -------------------------------
page = st.sidebar.selectbox("Navigation", ["Enter Match Data", "View Cumulative Earnings"])

# -------------------------------
# Page 1: Enter Match Data
# -------------------------------
if page == "Enter Match Data":
    st.title("Enter Match Data")
    st.write("Fill in today's match details below.")

    # Use current timestamp as default match id (or you can let users type an identifier)
    default_match_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    match_id = st.text_input("Match ID (e.g. date/time)", value=default_match_id)

    # Select the players that participated in this match
    selected_players = st.multiselect("Select players who played", players_list)

    team_data = []  # This list will accumulate one entry per team

    if selected_players:
        st.write("For each selected player, specify how many teams they played and assign a rank for each team.")
        # Determine number of winning positions per half based on number of players.
        # (Assuming that winners available are n/2 for top and n/2 for bottom.)
        k = len(selected_players) // 2
        if k == 0:
            st.warning("Please select at least 2 players to have valid winning positions.")
        else:
            # Prepare the list of valid winning rank options
            winning_options = [f"top{i}" for i in range(1, k+1)] + [f"bottom{i}" for i in range(1, k+1)]
            # Include an option if the team did not win.
            rank_options = ["No Win"] + winning_options

            # For each player, let the user enter how many teams they played and the rank for each team.
            for player in selected_players:
                num_teams = st.number_input(f"Number of teams for **{player}**", min_value=0, value=1, step=1, key=f"num_teams_{player}")
                for team in range(1, int(num_teams) + 1):
                    sel = st.selectbox(f"Select rank for **{player} - Team {team}**", 
                                       options=rank_options,
                                       key=f"rank_{player}_{team}")
                    team_data.append({
                        "player": player,
                        "team_index": team,
                        "rank": sel
                    })

            if st.button("Submit Match Data"):
                if not team_data:
                    st.error("No team data entered.")
                else:
                    # Calculate total teams played in this match
                    total_teams = len(team_data)
                    entry_fee = 50
                    total_prize_pool = total_teams * entry_fee

                    # Split prize pool equally between top and bottom winners
                    half_prize = total_prize_pool / 2

                    # For geometric progression: using default common ratio r = 0.5.
                    ratio = 0.5
                    # Number of winning positions in each half is k
                    # Calculate first term (reward for rank 1) so that:
                    # a * (1 - ratio^k) / (1 - ratio) = half_prize.
                    first_term = half_prize * (1 - ratio) / (1 - ratio ** k)

                    # Create rows with computed rewards
                    rows = []
                    for entry in team_data:
                        reward = get_reward(entry["rank"], first_term, ratio)
                        net = reward - entry_fee
                        rows.append({
                            "match_id": match_id,
                            "player": entry["player"],
                            "team_index": entry["team_index"],
                            "rank": entry["rank"],
                            "reward": round(reward, 2),
                            "entry_fee": entry_fee,
                            "net_earning": round(net, 2)
                        })

                    new_df = pd.DataFrame(rows)
                    save_match_data(new_df)
                    st.success("Match data saved successfully!")
                    st.write("### Match Data Summary")
                    st.dataframe(new_df)

# -------------------------------
# Page 2: View Cumulative Earnings
# -------------------------------
elif page == "View Cumulative Earnings":
    st.title("Cumulative Earnings")
    df = load_data()
    if df.empty:
        st.write("No match data available yet.")
    else:
        # Sum net earnings per player over all matches
        cum = df.groupby("player")["net_earning"].sum().reset_index()
        cum = cum.rename(columns={"net_earning": "Cumulative Earnings (Rs.)"})
        st.write("### Earnings per Player")
        st.dataframe(cum)

        st.write("### Detailed Match Data")
        st.dataframe(df)
