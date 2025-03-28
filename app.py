import streamlit as st
import pandas as pd
import os
from datetime import datetime
import math 
from io import StringIO
from github import Github

#st.write("Token loaded:", st.secrets["gt_token"][:4] + "..." + st.secrets["gt_token"][-4:])

# Hide default Streamlit elements
hide_streamlit_style = """
<style>
/* Hide the default Streamlit hamburger menu */
#MainMenu {visibility: hidden;}
/* Hide the “Made with Streamlit” footer */
footer {visibility: hidden;}
/* Hide the Streamlit header */
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------------------
# Private Access Authentication
# -------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("User Authentication ")
    code = st.text_input("Enter Passcode (Whatsapp me share kia gaya h):", type="password")
    if st.button("Enter"):
        if code == st.secrets['pass']:
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
    # Replace 'YOUR_TOKEN' with your GitHub personal access token
    gt_token = st.secrets["gt_token"]
    g = Github(gt_token)

    # Replace 'username/repo_name' with your repository identifier
    repo = g.get_repo("aanand862/dream11-Calc")
    # Define the path to your CSV file within the repo
    fl_path = "match_data.csv"
    #df_temp = new_data.to_csv(index=False)
    
    

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df_temp = df.to_csv(index=False)
        df.to_csv(DATA_FILE, index=False)
        # Get the file contents from the repo
        file = repo.get_contents(fl_path)
        commit_message = "Automated Update CSV file with new data"
        repo.update_file(fl_path, commit_message, df_temp, file.sha)
    else:
        df_temp = new_data.to_csv(index=False)
        file = repo.get_contents(fl_path)
        commit_message = "Automated Update CSV file with new data"
        repo.update_file(fl_path, commit_message, df_temp, file.sha)
        new_data.to_csv(DATA_FILE, index=False)

def update_data(df):
    gt_token = st.secrets['gt_token']
    g = Github(gt_token)

    # Replace 'username/repo_name' with your repository identifier
    repo = g.get_repo("aanand862/dream11-Calc")
    # Define the path to your CSV file within the repo
    fl_path = "match_data.csv"

    # Get the file contents from the repo
    file = repo.get_contents(fl_path)
    df_temp = df.to_csv(index=False)
    commit_message = "Automated Update CSV file with new data"
    repo.update_file(fl_path, commit_message, df_temp, file.sha)
    
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

#To handle default value of select match
def get_match_date(match_str):
    # Extract date part from a string like "22-Mar-25 : KKR Vs RCB"
    date_part = match_str.split(" : ")[0]
    return datetime.strptime(date_part, "%d-%b-%y").date()

today_date = datetime.today().date()
# Filter matches whose date is today or in the future
future_matches = [m for m in match_list if get_match_date(m) >= today_date]
if future_matches:
    # Sort by date and choose the earliest
    default_match = sorted(future_matches, key=get_match_date)[0]
else:
    default_match = match_list[0]


# -------------------------------
# Sidebar Navigation
# -------------------------------
#page = st.sidebar.selectbox("Navigation", ["Enter Match Data", "View Cumulative Earnings", "Delete Wrong Entry"])
page = st.sidebar.radio("Navigation", ["Enter Match Data", "View Cumulative Earnings", "Delete Wrong Entry"])

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
    #match_id = st.selectbox("Select Match", match_list)
    # Use the default_match to set the default index in the selectbox.
    match_id = st.selectbox("Select Match", match_list, index=match_list.index(default_match))
    # Check if an entry for the selected match is already present
    existing_df = load_data()
    if not existing_df.empty and match_id in existing_df["match_id"].unique():
        st.error(f"Entry is already done for match '{match_id}'. You cannot reenter match data for this match.")
        st.stop()
    
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
            
            # Build a list of all teams for this match.
            # Build a list of all team entries in "Player - Team X" format.
            all_teams = []
            for player in selected_players:
                for team_index in range(1, team_counts[player] + 1):
                    all_teams.append(f"{player} - T {team_index}")
            
            # -------------------------
            # Step 2: Top Ranking Assignment Grid
            # -------------------------
            st.markdown("### Step 2: Assign Top Rankings")
            st.write(f"Select a team for each Top Rank (1 to {top_count}).")
            top_rankings = {}
            top_cols = st.columns(top_count)
            for i in range(top_count):
                with top_cols[i]:
                    choice = st.radio(f"Top Rank {i+1}", options=["Select a team"] + all_teams, key=f"top_rank_{i+1}")
                    top_rankings[i+1] = choice
                           
            # -------------------------
            # Step 3: Bottom Ranking Assignment Grid
            # -------------------------
            st.markdown("### Step 3: Assign Bottom Rankings")
            st.write(f"Select a team for each Bottom Rank (1 to {bottom_count}).")
            bottom_rankings = {}
            bottom_cols = st.columns(bottom_count)
            for i in range(bottom_count):
                with bottom_cols[i]:
                    choice = st.radio(f"Bottom Rank {i+1}", options=["Select a team"] + all_teams, key=f"bottom_rank_{i+1}")
                    bottom_rankings[i+1] = choice
            
            # -------------------------
            # Step 4: Submission & Validation
            # -------------------------

    if st.button("Submit Match Data"):
        # Validate that every top and bottom rank is assigned a team.
        unassigned_top = [rank for rank, team in top_rankings.items() if team == "Select a team"]
        unassigned_bottom = [rank for rank, team in bottom_rankings.items() if team == "Select a team"]
        if unassigned_top:
            st.error(f"Please assign a team for Top Rank(s): {unassigned_top}")
        elif unassigned_bottom:
            st.error(f"Please assign a team for Bottom Rank(s): {unassigned_bottom}")
        else:
            # Validate uniqueness across each category.
            top_values = list(top_rankings.values())
            bottom_values = list(bottom_rankings.values())
            if len(set(top_values)) != len(top_values):
                st.error("Duplicate team assignment found in Top Rankings. Please ensure each assignment is unique.")
            elif len(set(bottom_values)) != len(bottom_values):
                st.error("Duplicate team assignment found in Bottom Rankings. Please ensure each assignment is unique.")
            # Additional validation: a single team should not be assigned multiple ranks across categories.
            elif len(set(top_values + bottom_values)) != len(top_values + bottom_values):
                st.error("A single team has been assigned multiple ranks. Please assign each team only once.")
            else:
                # -------------------------
                # Step 5: Compute Rewards and Save Data
                # -------------------------
                entry_fee = 50
                total_prize_pool = total_teams * entry_fee
                ratio = 0.5
                # Custom reward calculation: using a reward_list based on total teams.
                reward_list = []    
                for i in range(top_count):
                    temp = (total_teams - i) ** 2
                    reward_list.append(temp)
                
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                rows = []
                for rank, team_str in top_rankings.items():
                    # Expected format: "Player - T X"
                    try:
                        player, team_part = team_str.split(" - T ")
                        team_index = int(team_part)
                    except Exception as e:
                        st.error(f"Error parsing team info for Top Rank {rank}: {team_str}")
                        st.stop()
                    wt = reward_list[rank - 1] / sum(reward_list)
                    reward = total_prize_pool * wt * 0.5
                    rows.append({
                                "match_id": match_id,
                                "update_date": now_str,
                                "player": player,
                                "team_index": team_index,
                                "category": "top",
                                "rank": rank,
                                "reward": round(reward, 2),
                                "entry_fee": entry_fee,
                                "net_earning": round(reward - entry_fee, 2)})
                # Process Bottom Rankings
                for rank, team_str in bottom_rankings.items():
                    try:
                        player, team_part = team_str.split(" - T ")
                        team_index = int(team_part)
                    except Exception as e:
                        st.error(f"Error parsing team info for Bottom Rank {rank}: {team_str}")
                        st.stop()
                    wt = reward_list[rank - 1] / sum(reward_list)
                    reward = total_prize_pool * wt * 0.5
                    rows.append({
                            "match_id": match_id,
                            "update_date": now_str,
                            "player": player,
                            "team_index": team_index,
                            "category": "bottom",
                            "rank": rank,
                            "reward": round(reward, 2),
                            "entry_fee": entry_fee,
                            "net_earning": round(reward - entry_fee, 2)})
                
                ranked_teams = set(list(top_rankings.values()) + list(bottom_rankings.values()))
                non_rows = []
                for player in selected_players:
                    for team_index in range(1, team_counts[player] + 1):
                        team_str = f"{player} - T {team_index}"
                        if team_str not in ranked_teams:
                            non_rows.append({
                                    "match_id": match_id,
                                    "update_date": now_str,
                                    "player": player,
                                    "team_index": team_index,
                                    "category": "non",
                                    "rank": "No Win",
                                    "reward": 0,
                                    "entry_fee": entry_fee,
                                    "net_earning": -entry_fee})
                all_rows = rows + non_rows
                
                new_df = pd.DataFrame(all_rows)
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
        st.write("### Ab Tak Ka hisab : ")
        cum = cum.set_index("player")
        #cum = pd.to_numeric(cum["Cumulative Earnings (Rs.)"])
        #st.bar_chart(cum)
        cum = cum.sort_values(by="Cumulative Earnings (Rs.)", ascending=False)
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
elif page == "Delete Wrong Entry":
    st.title("Manage Match Data")
    df = load_data()
    if df.empty:
        st.write("No match data available to manage.")
    else:
        st.dataframe(df)
        st.write("Select one or more entries (based on match_id and update_date) to delete:")
        # Create a composite key for deletion (do not modify original df)
        df_temp = df.copy()
        df_temp["entry_id"] = df_temp["match_id"] + " | " + df_temp["update_date"]
        unique_entries = df_temp["entry_id"].unique().tolist()
        entries_to_delete = st.multiselect("Select entries to delete", unique_entries)
        
        if st.button("Delete Selected Match Data"):
            if not entries_to_delete:
                st.error("Please select at least one entry to delete.")
            else:
                # Filter out rows with matching composite keys.
                updated_df = df_temp[~df_temp["entry_id"].isin(entries_to_delete)]
                # Drop the composite column before saving back.
                updated_df = updated_df.drop(columns=["entry_id"])
                update_data(updated_df)
                # Get the deleted rows for display.
                del_df = df_temp[df_temp["entry_id"].isin(entries_to_delete)].drop(columns=["entry_id"])
                st.success("Selected match data deleted successfully!")
                st.write("### Below is deleted data:")
                st.dataframe(del_df)
