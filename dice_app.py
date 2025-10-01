import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Page setup ---
st.set_page_config(page_title="🎲 Class Dice Roller", layout="wide")
st.title("🎲 Class Dice Roller — Interactive")

sa_file = st.secrets["gcp"]["service_account_json"]

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(sa_file, scope)
gc = gspread.authorize(credentials)

# Open Google Sheet
sheet = gc.open("Classdiceroll").sheet1

# --- Dice images ---
dice_images = {}
dice_dir = Path("dice_app")  # folder with 1.png … 6.png
if dice_dir.exists():
    for i in range(1, 7):
        img_path = dice_dir / f"{i}.png"
        if img_path.exists():
            dice_images[i] = str(img_path)

# --- Student input ---
student_name = st.text_input("Enter your name")
n_dice = st.number_input("Number of dice to roll", min_value=1, max_value=4, value=1, step=1)

# --- Roll button ---
if st.button("Roll Dice"):
    if student_name.strip() == "":
        st.warning("Please enter your name before rolling.")
    else:
        rolls = np.random.randint(1, 7, size=n_dice)
        total = rolls.sum()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare row for Google Sheet (pad rolls to 4 columns)
        row = [student_name] + rolls.tolist() + [0]*(4-len(rolls)) + [timestamp]
        sheet.append_row(row)
        st.success(f"{student_name} rolled {rolls.tolist()} (Total: {total})")

        # Show dice images
        st.subheader("Your Dice Faces")
        cols = st.columns(n_dice)
        for i, face in enumerate(rolls):
            with cols[i]:
                if face in dice_images:
                    st.image(dice_images[face], use_column_width=True)
                else:
                    st.write(f"Face {face}")

# --- Show class rolls ---
st.subheader("Class Rolls So Far")
data = pd.DataFrame(sheet.get_all_records())
if not data.empty:
    st.dataframe(data)

    # Compute total per row
    totals = data[['Roll1','Roll2','Roll3','Roll4']].sum(axis=1)

    # Histogram of totals
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(totals, bins=np.arange(1, 25+1)-0.5, edgecolor='black')
    ax.set_xlabel("Sum of dice")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Stats
    st.write(f"Class Roll Stats: Mean={totals.mean():.2f}, Max={totals.max()}, Min={totals.min()}")
else:
    st.info("No rolls yet. Be the first to roll!")


# --- Reset rolls ---
if st.button("Reset Rolls"):
    st.experimental_rerun()
