import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Load images
img = Image.open("95054298861.png")
img2 = Image.open("87981739647.png")

# Initialize the session state to track score and challenge completion
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'mean_solved' not in st.session_state:
    st.session_state.mean_solved = False
if 'median_solved' not in st.session_state:
    st.session_state.median_solved = False
if 'mode_solved' not in st.session_state:
    st.session_state.mode_solved = False
if 'box_solved' not in st.session_state:
    st.session_state.box_solved = False

# Helper functions to generate or reset data for each challenge using a unique key.
def generate_data(key):
    if key not in st.session_state:
        st.session_state[key] = np.random.randint(1, 20, size=10)
    return st.session_state[key]

def reset_data(key):
    st.session_state[key] = np.random.randint(1, 20, size=10)
    st.session_state[f"{key}_reset"] = True

# Challenge 1: Mean
def mean_challenge():
    st.header("Challenge 1: Mean")
    data = generate_data("data_mean")
    st.write("Data:", data)

    correct_mean = np.mean(data)
    if st.session_state.mean_solved:
        st.info("Challenge already solved!")
    else:
        user_input = st.text_input("What is the mean of the above data?", key="mean_input")
        if user_input:
            try:
                user_input = float(user_input)
                if np.isclose(user_input, correct_mean):
                    st.session_state.score += 1
                    st.session_state.mean_solved = True
                    st.success("Correct! You've passed the mean challenge.")
                else:
                    st.error(f"Oops! The correct mean was {correct_mean}.")
                    reset_data("data_mean")
            except ValueError:
                st.error("Please enter a valid number.")

# Challenge 2: Median
def median_challenge():
    st.header("Challenge 2: Median")
    data = generate_data("data_median")
    st.write("Data:", data)

    correct_median = np.median(data)
    if st.session_state.median_solved:
        st.info("Challenge already solved!")
    else:
        user_input = st.text_input("What is the median of the above data?", key="median_input")
        if user_input:
            try:
                user_input = float(user_input)
                if np.isclose(user_input, correct_median):
                    st.session_state.score += 1
                    st.session_state.median_solved = True
                    st.success("Correct! You've passed the median challenge.")
                else:
                    st.error(f"Oops! The correct median was {correct_median}.")
                    reset_data("data_median")
            except ValueError:
                st.error("Please enter a valid number.")

# Challenge 3: Mode
def mode_challenge():
    st.header("Challenge 3: Mode")
    data = generate_data("data_mode")
    st.write("Data:", data)

    # Calculate mode(s)
    modes = pd.Series(data).mode()
    correct_modes = set(modes)
    if st.session_state.mode_solved:
        st.info("Challenge already solved!")
    else:
        user_input = st.text_input(
            "What is/are the mode(s) of the above data? (Enter them separated by commas)",
            key="mode_input"
        )
        if user_input:
            try:
                user_input_set = set(map(int, user_input.split(',')))
                if user_input_set == correct_modes:
                    st.session_state.score += 1
                    st.session_state.mode_solved = True
                    st.success("Correct! You've passed the mode challenge.")
                else:
                    st.error(f"Oops! The correct mode(s) was/were {', '.join(map(str, correct_modes))}.")
                    reset_data("data_mode")
            except ValueError:
                st.error("Please enter valid numbers, separated by commas.")

# Challenge 4: Box and Whisker Plot
def box_whisker_challenge():
    st.header("Challenge 4: Box and Whisker Plot")
    data = generate_data("data_box")
    st.write("Data:", data)

    # Create a box plot
    fig, ax = plt.subplots()
    sns.boxplot(data=data, ax=ax)
    st.pyplot(fig)

    # Manually calculate the quartiles using the median-of-halves method.
    data_sorted = np.sort(data)
    n = len(data_sorted)
    if n % 2 == 0:
        lower_half = data_sorted[:n//2]
        upper_half = data_sorted[n//2:]
    else:
        lower_half = data_sorted[:n//2]
        upper_half = data_sorted[n//2+1:]
    
    q1 = np.median(lower_half)
    q3 = np.median(upper_half)
    correct_range = q3 - q1

    if st.session_state.box_solved:
        st.info("Challenge already solved!")
    else:
        user_input = st.text_input("What is the range between the 1st and 3rd quartile of the above data?", key="box_input")
        if user_input:
            try:
                user_input = float(user_input)
                if np.isclose(user_input, correct_range):
                    st.session_state.score += 1
                    st.session_state.box_solved = True
                    st.success("Correct! You've passed the box and whisker challenge.")
                else:
                    st.error(f"Oops! The correct range was {correct_range}.")
                    reset_data("data_box")
            except ValueError:
                st.error("Please enter a valid number.")

# Display the overall score in the sidebar.
def display_score():
    st.sidebar.header("Your Score")
    st.sidebar.write(f"Score: {st.session_state.score}/4")

# Main game loop
def game():
    st.title("Kendrick Lamar's Statistics Challenge!")
    st.image(
        img,
        caption="Hi. I'm Kendrick Lamar. My arch nemesis Drizzy Drake is really petty--you know, after our little 'altercations'--and won't let me make it to my Super Bowl Halftime performance without getting through some stupid math obstacles. Can you help me out?"
    )
    display_score()

    # Each challenge uses its own dataset.
    mean_challenge()
    median_challenge()
    mode_challenge()
    box_whisker_challenge()

    # Check if all challenges are solved (order independent) to display the success sequence.
    if (st.session_state.mean_solved and st.session_state.median_solved and 
        st.session_state.mode_solved and st.session_state.box_solved):
        st.balloons()
        st.success("Thanks! Now I can make it back to the Super Bowl in time!")
        st.image(
            img2,
            caption="I'll get him next time. I know I will..."
        )

if __name__ == "__main__":
    game()
