import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

    # Select a match from the predefined list
    match_id = st.selectbox("Select Match", match_list)
    
    # Collect the players who participated
    selected_players = st.multiselect("Select players who played", players_list)
    team_data = []  # List to accumulate one entry per team

    if selected_players:
        # Determine number of winning positions per half based on number of players.
        # (i.e., available winning ranks will be top1...top{k} and bottom1...bottom{k})
        k = len(selected_players) // 2
        if k == 0:
            st.warning("Please select at least 2 players to have valid winning positions.")
        else:
            # Create winning options and include them in the rank options.
            winning_options = [f"top{i}" for i in range(1, k+1)] + [f"bottom{i}" for i in range(1, k+1)]
            rank_options = ["No Win"] + winning_options

            # For each player, get the number of teams and display a row of rank selectboxes.
            for player in selected_players:
                st.markdown(f"### {player}")
                num_teams = st.number_input(f"Number of teams for {player}", min_value=0, value=1, step=1, key=f"num_teams_{player}")
                if num_teams > 0:
                    st.write("Select rank for each team:")
                    cols = st.columns(int(num_teams))
                    for i in range(int(num_teams)):
                        with cols[i]:
                            sel = st.selectbox(f"Team {i+1}", options=rank_options, key=f"rank_{player}_{i+1}")
                            team_data.append({
                                "player": player,
                                "team_index": i + 1,
                                "rank": sel
                            })

            if st.button("Submit Match Data"):
                # Validation: Every winning rank (i.e. every rank in winning_options)
                # must be assigned exactly once.
                assigned_winning_ranks = [entry["rank"] for entry in team_data if entry["rank"] != "No Win"]
                missing = [r for r in winning_options if assigned_winning_ranks.count(r) == 0]
                duplicated = [r for r in winning_options if assigned_winning_ranks.count(r) > 1]
                if missing or duplicated:
                    err_msg = ""
                    if missing:
                        err_msg += "Missing winning rank assignments for: " + ", ".join(missing) + ". "
                    if duplicated:
                        err_msg += "Duplicated winning rank assignments for: " + ", ".join(duplicated) + "."
                    st.error(err_msg)
                else:
                    # Calculate the total teams, entry fee and total prize pool
                    total_teams = len(team_data)
                    entry_fee = 50
                    total_prize_pool = total_teams * entry_fee
                    half_prize = total_prize_pool / 2

                    # For geometric progression: common ratio r = 0.5.
                    ratio = 0.5
                    # Calculate the first term so that the sum of rewards for each half equals half_prize.
                    first_term = half_prize * (1 - ratio) / (1 - ratio ** k)

                    # Capture the current date and time.
                    now_t = datetime.now()
                    formatted_datetime = now_t.strftime("%Y-%m-%d %H:%M:%S")
                    
                    rows = []
                    for entry in team_data:
                        reward = get_reward(entry["rank"], first_term, ratio)
                        net = reward - entry_fee
                        rows.append({
                            "match_id": match_id,
                            "update_date": formatted_datetime,
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
