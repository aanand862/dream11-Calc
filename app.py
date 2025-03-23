import streamlit as st
import pandas as pd
import os
from datetime import datetime
import math 

# -------------------------------
# Private Access Authentication
# -------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Validate Credential (Shared in Whatsapp group)")
    code = st.text_input("Enter the passcode", type="password")
    if st.button("Enter"):
        if code == "0007":
            st.session_state.authenticated = True
            st.success("Access Granted!")
        else:
            st.error("Incorrect code. Please try again.")
    st.stop()

match_list = [
    "22-Mar-25 : KKR Vs RCB",
    "23-Mar-25 : SRH Vs RR",
    "23-Mar-25 : CSK Vs MI",
    "24-Mar-25 : DC Vs LSG",
    "25-Mar-25 : GT Vs PK",
    "26-Mar-25 : RR Vs KKR",
    "27-Mar-25 : SRH Vs LSG",
    "28-Mar-25 : CSK Vs RCB",
    "29-Mar-25 : GT Vs MI",
    "30-Mar-25 : DC Vs SRH",
    "30-Mar-25 : RR Vs CSK",
    "31-Mar-25 : MI Vs KKR",
    "01-Apr-25 : LSG Vs PK",
    "02-Apr-25 : RCB Vs GT",
    "03-Apr-25 : KKR Vs SRH",
    "04-Apr-25 : LSG Vs MI",
    "05-Apr-25 : CSK Vs DC",
    "05-Apr-25 : PK Vs RR",
    "06-Apr-25 : KKR Vs LSG",
    "06-Apr-25 : SRH Vs GT",
    "07-Apr-25 : MI Vs RCB",
    "08-Apr-25 : PK Vs CSK",
    "09-Apr-25 : GT Vs RR",
    "10-Apr-25 : RCB Vs DC",
    "11-Apr-25 : CSK Vs KKR",
    "12-Apr-25 : LSG Vs GT",
    "12-Apr-25 : SRH Vs PK",
    "13-Apr-25 : RR Vs RCB",
    "13-Apr-25 : DC Vs MI",
    "14-Apr-25 : LSG Vs CSK",
    "15-Apr-25 : PK Vs KKR",
    "16-Apr-25 : DC Vs RR",
    "17-Apr-25 : MI Vs SRH",
    "18-Apr-25 : RCB Vs PK",
    "19-Apr-25 : GT Vs DC",
    "19-Apr-25 : RR Vs LSG",
    "20-Apr-25 : PK Vs RCB",
    "20-Apr-25 : MI Vs CSK",
    "21-Apr-25 : KKR Vs GT",
    "22-Apr-25 : LSG Vs DC",
    "23-Apr-25 : SRH Vs MI",
    "24-Apr-25 : RCB Vs RR",
    "25-Apr-25 : CSK Vs SRH",
    "26-Apr-25 : KKR Vs PK",
    "27-Apr-25 : MI Vs LSG",
    "27-Apr-25 : DC Vs RCB",
    "28-Apr-25 : RR Vs GT",
    "29-Apr-25 : DC Vs KKR",
    "30-Apr-25 : CSK Vs PK",
    "01-May-25 : RR Vs MI",
    "02-May-25 : GT Vs SRH",
    "03-May-25 : RCB Vs CSK",
    "04-May-25 : KKR Vs RR",
    "04-May-25 : PK Vs LSG",
    "05-May-25 : SRH Vs DC",
    "06-May-25 : MI Vs GT",
    "07-May-25 : KKR Vs CSK",
    "08-May-25 : PK Vs DC",
    "09-May-25 : LSG Vs RCB",
    "10-May-25 : SRH Vs KKR",
    "11-May-25 : PK Vs MI",
    "11-May-25 : DC Vs GT",
    "12-May-25 : CSK Vs RR",
    "13-May-25 : RCB Vs SRH",
    "14-May-25 : GT Vs LSG",
    "15-May-25 : MI Vs DC",
    "16-May-25 : RR Vs PK",
    "17-May-25 : RCB Vs KKR",
    "18-May-25 : GT Vs CSK",
    "18-May-25 : LSG Vs SRH",
    "20-May-25 : Qualifier 1",
    "21-May-25 : Eliminator",
    "23-May-25 : Qualifier 2",
    "25-May-25 : Final"
]
# -------------------------------
# Preconfigured players list
# -------------------------------
players_list = ["Abh", "JJ", "Mait", "Ash", "Arp", "Gan","Goy","Sam","Ank"]

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
        return pd.DataFrame(columns=["match_id", "update_date","player", "team_index", "rank", "reward", "entry_fee", "net_earning"])

def save_match_data(new_data):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
    else:
        new_data.to_csv(DATA_FILE, index=False)

def update_data(df):
    """Overwrites the DATA_FILE with the provided DataFrame."""
    df.to_csv(DATA_FILE, index=False)

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
page = st.sidebar.selectbox("Navigation", ["Enter Match Data", "View Cumulative Earnings", "Manage Match Data"])

# -------------------------------
# Page 1: Enter Match Data
# -------------------------------
if page == "Enter Match Data":
    st.title("Enter Match Data")
    st.write("Fill in today's match details below.")

    # -------------------------
    # Step 1: Basic Inputs
    # -------------------------
    # Choose a match from the predefined list.
    match_id = st.selectbox("Select Match", match_list)
    
    # Select the players who participated.
    selected_players = st.multiselect("Select players who played", players_list)
    
    # For each selected player, ask for the number of teams they played.
    team_counts = {}
    if selected_players:
        st.markdown("### Step 1: Enter Number of Teams for Each Player")
        for player in selected_players:
            team_counts[player] = st.number_input(
                f"Number of teams for **{player}**", min_value=0, value=1, step=1, key=f"num_{player}"
            )
        
        # Compute total teams across all players.
        total_teams = sum(team_counts[player] for player in selected_players)
        st.write(f"Total teams in this match: **{total_teams}**")
        
        if total_teams < 3:
            st.warning("Not enough teams to assign winners. At least 4 teams are required.")
        else:
            # Determine number of winning positions.
            # Total winners = total_teams/2, split equally: top_count = bottom_count = total_teams/4.
            
            top_count = bottom_count = math.ceil(total_teams / 4)
                
            st.write(f"Number of Top Winners: **{top_count}**")
            st.write(f"Number of Bottom Winners: **{bottom_count}**")
            
            # -------------------------
            # Step 2: Top Ranking Assignment
            # -------------------------
            st.markdown("### Step 2: Assign Top Rankings")
            st.write(f"For each Top Rank (1 to {top_count}), select a player and then choose one of that player's teams.")
            top_rankings = []
            for i in range(1, top_count + 1):
                col1, col2 = st.columns(2)
                with col1:
                    top_player = st.selectbox(
                        f"Top Rank {i} - Select Player", options=selected_players, key=f"top_player_{i}"
                    )
                with col2:
                    available_teams = list(range(1, team_counts[top_player] + 1))
                    top_team = st.selectbox(
                        f"Top Rank {i} - Select Team", options=available_teams, key=f"top_team_{i}"
                    )
                top_rankings.append({
                    "rank": i,
                    "player": top_player,
                    "team": top_team
                })
            
            # -------------------------
            # Step 3: Bottom Ranking Assignment
            # -------------------------
            st.markdown("### Step 3: Assign Bottom Rankings")
            st.write(f"For each Bottom Rank (1 to {bottom_count}), select a player and then choose one of that player's teams.")
            bottom_rankings = []
            for i in range(1, bottom_count + 1):
                col1, col2 = st.columns(2)
                with col1:
                    bottom_player = st.selectbox(
                        f"Bottom Rank {i} - Select Player", options=selected_players, key=f"bottom_player_{i}"
                    )
                with col2:
                    available_teams = list(range(1, team_counts[bottom_player] + 1))
                    bottom_team = st.selectbox(
                        f"Bottom Rank {i} - Select Team", options=available_teams, key=f"bottom_team_{i}"
                    )
                bottom_rankings.append({
                    "rank": i,
                    "player": bottom_player,
                    "team": bottom_team
                })
            
            # -------------------------
            # Step 4: Submission & Validation
            # -------------------------
            if st.button("Submit Match Data"):
                # Validation: Ensure that within each category (top and bottom) the same player-team combination is not assigned more than once.
                top_assignments = [(entry["player"], entry["team"]) for entry in top_rankings]
                bottom_assignments = [(entry["player"], entry["team"]) for entry in bottom_rankings]
                if len(set(top_assignments)) != len(top_assignments):
                    st.error("Duplicate assignment found in Top Rankings. Please ensure each assignment is unique.")
                elif len(set(bottom_assignments)) != len(bottom_assignments):
                    st.error("Duplicate assignment found in Bottom Rankings. Please ensure each assignment is unique.")
                else:
                    # -------------------------
                    # Step 5: Compute Rewards and Save Data
                    # -------------------------
                    entry_fee = 50
                    total_prize_pool = total_teams * entry_fee
                    half_prize = total_prize_pool / 2
                    ratio = 0.5
                    # Calculate geometric progression first term for top and bottom categories.
                    first_term_top = half_prize * (1 - ratio) / (1 - ratio ** top_count)
                    first_term_bottom = half_prize * (1 - ratio) / (1 - ratio ** bottom_count)
                    
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    rows = []
                    for entry in top_rankings:
                        reward = first_term_top * (ratio ** (entry["rank"] - 1))
                        rows.append({
                            "match_id": match_id,
                            "update_date": now_str,
                            "player": entry["player"],
                            "team_index": entry["team"],
                            "category": "top",
                            "rank": entry["rank"],
                            "reward": round(reward, 2),
                            "entry_fee": entry_fee,
                            "net_earning": round(reward - entry_fee, 2)
                        })
                    for entry in bottom_rankings:
                        reward = first_term_bottom * (ratio ** (entry["rank"] - 1))
                        rows.append({
                            "match_id": match_id,
                            "update_date": now_str,
                            "player": entry["player"],
                            "team_index": entry["team"],
                            "category": "bottom",
                            "rank": entry["rank"],
                            "reward": round(reward, 2),
                            "entry_fee": entry_fee,
                            "net_earning": round(reward - entry_fee, 2)
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

        st.write("### View Match Data")
        unique_matches1 = df['match_id'].unique().tolist()
        view_match = st.multiselect("Select one/more match",unique_matches1,default= unique_matches1[0])
        df1 = df[df['match_id'].isin(view_match)]
        st.dataframe(df1)
        # Download button
        df_csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download All Match data ",data=df_csv ,file_name="All_Match_Data.csv",mime="text/csv")

# -------------------------------
# Page 3: Manage Match Data
# -------------------------------
elif page == "Manage Match Data":
    st.title("Manage Match Data")
    df = load_data()
    st.dataframe(load_data())
    if df.empty:
        st.write("No match data available to manage.")
    else:
        st.write("Select one or more Match IDs to delete from the records:")
        unique_matches = df['match_id'].unique().tolist()
        match_to_delete = st.multiselect("Select Match IDs to delete", unique_matches)

        if st.button("Delete Selected Match Data"):
            if not match_to_delete:
                st.error("Please select at least one match ID to delete.")
            else:
                # Filter out the selected match IDs
                updated_df = df[~df['match_id'].isin(match_to_delete)]
                update_data(updated_df)
                del_df = df[df['match_id'].isin(match_to_delete)]
                st.success("Selected match data deleted successfully!")
                st.write("### Below is deleted data : ")
                st.dataframe(del_df)
