# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 19:54:16 2025

@author: shahad
"""
import streamlit as st
import random
import pandas as pd
from PIL import Image

st.title("🎲 Virtual Dice Roller with Images")

# Initialize session state
if "rolls" not in st.session_state:
    st.session_state.rolls = []

# Button to roll dice
if st.button("Roll the Dice!"):
    roll = random.randint(1, 6)
    st.session_state.rolls.append(roll)
    st.success(f"You rolled a {roll}")

    # Show big image for current roll
   # Show big image for current roll
    img = Image.open(fr"C:\Users\shahad\Desktop\dice app\dice{roll}.png")
    st.image(img, width=150)

# Show previous rolls as small dice images
if st.session_state.rolls:
    st.write("Previous rolls:")
    cols = st.columns(len(st.session_state.rolls))
  # Show previous rolls as small dice images
    for i, r in enumerate(st.session_state.rolls):
      img = Image.open(fr"C:\Users\shahad\Desktop\dice app\dice{r}.png")
      cols[i].image(img, width=50)

    # Show histogram of all rolls
    df = pd.DataFrame({"Roll": st.session_state.rolls})
    st.bar_chart(df["Roll"].value_counts().sort_index())






