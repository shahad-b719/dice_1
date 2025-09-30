# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 19:54:16 2025

@author: shahad
"""
import streamlit as st
import random
import pandas as pd
from PIL import Image

# Title
###st.title("🎲 Virtual Dice Roller")

# Initialize session state to store rolls
if "rolls" not in st.session_state:
    st.session_state.rolls = []

# Button to roll dice
if st.button("Roll the Dice!"):
    roll = random.randint(1, 6)
    st.session_state.rolls.append(roll)
    st.success(f"You rolled a {roll}")

# Show all rolls as a histogram
if st.session_state.rolls:
    df = pd.DataFrame({"Roll": st.session_state.rolls})
    st.bar_chart(df["Roll"].value_counts().sort_index())



