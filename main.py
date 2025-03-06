import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import statistics
from collections import Counter

def calculate_statistics(data):
    ordered_data = sorted(data)
    data_mean = statistics.mean(ordered_data)
    data_median = statistics.median(ordered_data)
    data_mode = calculate_mode(ordered_data)
    data_range = max(ordered_data) - min(ordered_data)
    
    return ordered_data, data_mean, data_median, data_mode, data_range

def calculate_mode(data):
    # Count the frequency of each element in the dataset
    count = Counter(data)
    max_freq = max(count.values())
    modes = [key for key, value in count.items() if value == max_freq]
    
    if len(modes) == len(set(data)):
        return "No unique mode"
    return modes if len(modes) > 1 else modes[0]

def plot_data(data):
    plt.figure(figsize=(10, 5))
    sns.histplot(data, bins=min(10, len(set(data))), color='blue')
    
    mean_value = statistics.mean(data)
    median_value = statistics.median(data)
    
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {round(mean_value, 2)}')
    plt.axvline(median_value, color='green', linestyle='dashed', linewidth=2, label=f'Median: {round(median_value, 2)}')
    
    data_mode = calculate_mode(data)
    if isinstance(data_mode, list):  # If there are multiple modes
        mode_label = "Modes: " + ", ".join(map(str, data_mode))
        plt.axvline(data_mode[0], color='purple', linestyle='dashed', linewidth=2, label=mode_label)
    elif data_mode != "No unique mode":  # If there is a single mode
        plt.axvline(data_mode, color='purple', linestyle='dashed', linewidth=2, label=f'Mode: {data_mode}')
    
    plt.legend()
    plt.xlabel("Data Values")
    plt.ylabel("Frequency")
    plt.title("Data Distribution with Mean, Median, and Mode")
    st.pyplot(plt)

def plot_box_plot(data):
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=data, color='skyblue')
    plt.title("Box and Whisker Plot")
    plt.xlabel("Data Values")
    st.pyplot(plt)
    
    # Calculate IQR (Interquartile Range)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    return IQR

def game_page():
    img = Image.open("95054298861.png")
    img2 = Image.open("87981739647.png")
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
    for challenge in ['mean', 'median', 'mode', 'box', 'box_plot'] :
        if f'{challenge}_solved' not in st.session_state:
            st.session_state[f'{challenge}_solved'] = False
    
    def generate_data(key):
        if key not in st.session_state:
            st.session_state[key] = np.random.randint(1, 20, size=10)
        return st.session_state[key]
    
    def reset_data(key):
        st.session_state[key] = np.random.randint(1, 20, size=10)
        st.session_state[f"{key}_reset"] = True
    
    def challenge(name, calculation, key):
        st.header(f"Challenge: {name.capitalize()}")
        data = generate_data(key)
        st.write("Data:", data)
    
        correct_value = calculation(data)
        if st.session_state[f'{key}_solved']:
            st.info("Challenge already solved!")
        else:
            user_input = st.text_input(f"What is the {name} of the above data?", key=f"{key}_input")
            if user_input:
                try:
                    user_input = float(user_input)
                    if np.isclose(user_input, correct_value):
                        st.session_state.score += 1
                        st.session_state[f'{key}_solved'] = True
                        st.success(f"Correct! You've passed the {name} challenge.")
                    else:
                        st.error(f"Oops! The correct {name} was {correct_value}.")
                        reset_data(key)
                except ValueError:
                    st.error("Please enter a valid number.")
    
    st.title("Kendrick Lamar's Statistics Challenge!")
    st.image(img, caption="Hi. I'm Kendrick Lamar. My arch nemesis Drake is really petty and won't let me make it to my Super Bowl Halftime performance without getting through some stupid math obstacles. Can you help me out?")
    
    challenge("mean", np.mean, "mean")
    challenge("median", np.median, "median")
    challenge("mode", calculate_mode, "mode")
    challenge("range", lambda x: max(x) - min(x), "box")
    
    # Add the new box plot challenge for IQR
    st.header("Challenge: Box and Whisker Plot - Interquartile Range (IQR)")
    data = generate_data("box_plot")
    plot_box_plot(data)  # Display the box plot
    IQR = np.percentile(data, 75) - np.percentile(data, 25)
    
    if st.session_state["box_plot_solved"]:
        st.info("Challenge already solved!")
    else:
        user_input = st.text_input("What is the Interquartile Range (IQR) of the above data?", key="box_plot_input")
        if user_input:
            try:
                user_input = float(user_input)
                if np.isclose(user_input, IQR):
                    st.session_state.score += 1
                    st.session_state["box_plot_solved"] = True
                    st.success(f"Correct! You've passed the Box and Whisker Plot challenge.")
                else:
                    st.error(f"Oops! The correct IQR was {IQR}.")
                    reset_data("box_plot")
            except ValueError:
                st.error("Please enter a valid number.")
    
    if all(st.session_state[f'{key}_solved'] for key in ['mean', 'median', 'mode', 'box', 'box_plot']):
        st.balloons()
        st.success("Thanks! Now I can make it back to the Super Bowl in time!")
        st.image(img2, caption="I'll get him next time. I know I will...")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Statistical Calculator", "Kendrick Lamar's Statistics Challenge"])
    
    if page == "Statistical Calculator":
        st.title("Statistical Calculator")
        user_input = st.text_input("Enter a list of numbers separated by commas:")
        if user_input:
            try:
                data = [float(x.strip()) for x in user_input.split(",")]
                ordered_data, data_mean, data_median, data_mode, data_range = calculate_statistics(data)
                st.write("### Ordered Data:", ordered_data)
                st.write("### Calculated Statistics:")
                st.write(f"Mean: {data_mean}")
                st.write(f"Median: {data_median}")
                st.write(f"Mode: {data_mode}")
                st.write(f"Range: {data_range}")
                plot_data(data)

                # Add the box plot here
                st.write("### Box and Whisker Plot")
                plot_box_plot(data)  # Display box plot for the entered data

            except ValueError:
                st.error("Please enter a valid list of numbers.")
    else:
        game_page()

if __name__ == "__main__":
    main()
