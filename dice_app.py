
import streamlit as st
import numpy as np
import pandas as pd
import random
from pathlib import Path
import matplotlib.pyplot as plt

st.set_page_config(page_title="Interactive Monte Carlo — Dice", layout="centered")

st.title("🎲 Interactive Monte Carlo: Dice Simulator")

# Parameters
st.sidebar.header("Simulation controls")
n_dice = st.sidebar.selectbox("Number of dice", [1,2,3,4], index=0)
n_rolls = st.sidebar.slider("Rolls per trial", 100, 20000, 2000, step=100)
n_trials = st.sidebar.slider("Monte Carlo trials (repeat experiments)", 1, 2000, 200)
show_images = st.sidebar.checkbox("Show last-roll images (from dice_app folder)", value=True)

run_sim = st.button("Run Monte Carlo")

# Optional: load dice images if available
dice_images = {}
dice_dir = Path("dice_app")  # change if your images are elsewhere
if dice_dir.exists():
    for i in range(1,7):
        img_path = dice_dir / f"{i}.png"
        if img_path.exists():
            dice_images[i] = str(img_path)

def single_experiment(n_dice, n_rolls):
    # returns array of sums for n_rolls
    rolls = np.random.randint(1, 7, size=(n_rolls, n_dice))
    return rolls.sum(axis=1)

if run_sim:
    progress = st.progress(0)
    all_means = []
    # run trials
    for t in range(n_trials):
        results = single_experiment(n_dice, n_rolls)
        all_means.append(results.mean())
        # periodically update progress
        if n_trials <= 50 or t % max(1, n_trials//50) == 0:
            progress.progress(int((t+1)/n_trials*100))

    df = pd.DataFrame({
        "trial": range(1, len(all_means)+1),
        "mean_sum": all_means
    })

    st.subheader("Monte Carlo results (summary)")
    st.write(df.describe().T)

    # Histogram of one representative trial (last run)
    st.subheader("Distribution of sums in the last trial")
    fig, ax = plt.subplots(figsize=(6,3.5))
    ax.hist(results, bins=np.arange(n_dice-0.5, 6*n_dice+1.5, 1))
    ax.set_xlabel("Sum of dice")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Histogram of trial means
    st.subheader("Distribution of trial means (each trial averaged over rolls)")
    fig2, ax2 = plt.subplots(figsize=(6,3.5))
    ax2.hist(df["mean_sum"], bins=30)
    ax2.set_xlabel("Mean sum")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

    # Table of empirical probabilities (from last trial)
    st.subheader("Empirical probabilities (last trial)")
    probs = pd.Series(results).value_counts(normalize=True).sort_index()
    st.table(probs)

    # Show last roll images (if available)
    if show_images and dice_images:
        st.subheader("Sample faces from last roll")
        last_roll = np.random.randint(1,7, size=(n_dice,))
        cols = st.columns(n_dice)
        for i, face in enumerate(last_roll):
            with cols[i]:
                if face in dice_images:
                    st.image(dice_images[face], use_column_width=True)
                else:
                    st.write(f"Face {face}")
else:
    st.info("Set parameters on the left and click **Run Monte Carlo**.")
 
  





   

 





