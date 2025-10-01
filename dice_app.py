import streamlit as st
import random
import gspread
import pandas as pd
from PIL import Image
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import numpy as np

# --- Page Setup ---
st.set_page_config(page_title="🎲 Class Dice Roller", layout="wide")
st.title("🎲 Class Dice Roller — Interactive")

# --- Google Sheets Authentication ---
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
gc = gspread.authorize(credentials)

# Open your sheet
sheet = gc.open("Classdiceroll").sheet1  # Make sure sheet exists and first row has correct headers

# --- Initialize session state ---
if "rolls" not in st.session_state:
    st.session_state.rolls = []

# --- Dice Images ---
dice_images = {}
dice_dir = Path("dice_images")  # Folder where dice1.png, dice2.png ... dice6.png are stored
for i in range(1, 7):
    img_path = dice_dir / f"dice{i}.png"
    if img_path.exists():
        dice_images[i] = str(img_path)

# --- Student Input ---
student_name = st.text_input("Enter your name")
n_dice = st.number_input("Number of dice to roll", min_value=1, max_value=4, value=1, step=1)

# --- Roll Dice Button ---
if st.button("Roll Dice"):
        rolls = np.random.randint(1, 7, size=n_dice)
        total = rolls.sum()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store in session
        st.session_state.rolls.extend(rolls.tolist())

        # Prepare row for Google Sheet (pad rolls to 4 columns)
        row = [student_name] + rolls.tolist() + [0]*(4-len(rolls)) + [timestamp]
        sheet.append_row(row)

        st.success(f"{student_name} rolled {rolls.tolist()} (Total: {total})")

        # Show dice images for current roll
        st.subheader("Your Dice Faces")
        cols = st.columns(n_dice)
        for i, face in enumerate(rolls):
            with cols[i]:
                if face in dice_images:
                    st.image(dice_images[face], width=100)
                else:
                    st.write(f"Face {face}")

# --- Show Class Rolls from Google Sheet ---
data = pd.DataFrame(sheet.get_all_records())

# Remove leading/trailing spaces and fix case
data.columns = [c.strip() for c in data.columns]
data = pd.DataFrame(sheet.get_all_records())
data.columns = [c.strip() for c in data.columns]  # remove spaces
totals = data[['Roll1','Roll2','Roll3','Roll4']].sum(axis=1)

# Columns we expect
required_cols = ['Roll1','Roll2','Roll3','Roll4']

# Only proceed if all expected columns exist
if not data.empty and all(col in data.columns for col in required_cols):
    totals = data[required_cols].sum(axis=1)
    
    # Plot histogram
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(totals, bins=np.arange(1, 25+1)-0.5, edgecolor='black')
    ax.set_xlabel("Sum of Dice")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.write(f"Class Roll Stats: Mean={totals.mean():.2f}, Max={totals.max()}, Min={totals.min()}")
else:
    st.info("No rolls yet or sheet headers missing. Be the first to roll!")




# --- Show Previous Rolls in Session ---
if st.session_state.rolls:
    st.subheader("Previous Rolls in This Session")
    cols = st.columns(len(st.session_state.rolls))
    for i, r in enumerate(st.session_state.rolls):
        if r in dice_images:
            cols[i].image(dice_images[r], width=50)
        else:
            cols[i].write(r)

    # Histogram of session rolls
    df = pd.DataFrame({"Roll": st.session_state.rolls})
    st.bar_chart(df["Roll"].value_counts().sort_index())








