import streamlit as st
import random
import requests
import pandas as pd
from collections import Counter
import logging
import streamlit
import os
import warnings

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

streamlit_root_logger = logging.getLogger(streamlit.__name__)
dictionary_api_key = os.environ["DICT_API_KEY"]

# Sample list of words
df = pd.read_csv("data/easy_words.csv")
WORDS = df['words'].str.lower().to_list()
FEEDBACKS = [["blank", "blank", "blank", "blank", "blank"],
             ["blank", "blank", "blank", "blank", "blank"],
             ["blank", "blank", "blank", "blank", "blank"],
             ["blank", "blank", "blank", "blank", "blank"],
             ["blank", "blank", "blank", "blank", "blank"],
             ["blank", "blank", "blank", "blank", "blank"]]
GUESSES = ["     ", "     ", "     ", "     ", "     ", "     "]
COLORS = {'green': '#6aaa64', 'yellow': '#c9b458', 'gray': '#787c7e', 'blank': "#fafff5"}
LETTERS_AND_COLORS = {}


def choose_word():
    return random.choice(WORDS)


def check_guess(guess, target, letters_and_colors):
    target_count = Counter(target)

    feedback = [""] * len(target)

    for i, char in enumerate(guess):
        if char == target[i] and target_count[char] != 0:
            feedback[i] = "green"
            target_count[char] = target_count[char] - 1
            letters_and_colors[char] = "green"

        elif char in target:
            feedback[i] = "yellow"
            if letters_and_colors.get(char) != "green":
                letters_and_colors[char] = "yellow"

        else:
            feedback[i] = "gray"
            if letters_and_colors.get(char) != "green" or letters_and_colors.get(char) != "yellow":
                letters_and_colors[char] = "gray"

    # second loop to remove any duplicate letters when only one letter
    # Ex: target - liver, guess - hello
    for i, char in enumerate(guess):
        if feedback[i] == 'yellow':
            if target_count[char] == 0:
                feedback[i] = 'gray'
            else:
                target_count[char] = target_count[char] - 1

    return feedback


def is_valid_word(guess):
    dictionary_api = f"https://dictionaryapi.com/api/v3/references/learners/json/{guess}?key={dictionary_api_key}"
    result = requests.get(dictionary_api, verify=False)
    return type(result.json()[0]) != str


def reset_game():
    st.session_state.target = choose_word()
    st.session_state.guesses = GUESSES
    st.session_state.feedback = FEEDBACKS
    st.session_state.index = 0
    st.session_state.letters_and_colors = LETTERS_AND_COLORS
    if st.session_state.name:
        streamlit_root_logger.info(f"Name: {st.session_state.name} Team: {st.session_state.team} started game, their word is {st.session_state.target}")


def go_back():
    st.session_state.name = ''
    st.session_state.team = ''
    reset_game()


def wordle_table(guesses, feedback):
    st.write("""
        <style>
        .cell {
            display: inline-block;
            width: 2em;
            height: 2em;
            text-align: center;
            vertical-align: middle;
            line-height: 2em;
            margin: 0.1em;
            border-radius: 0.25em;
            font-size: 1.2em;
        }
        .row {
            display: flex;
            justify-content: center;
            flex-wrap: nowrap;
        }
        .button-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    for i, (guess, fb) in enumerate(zip(guesses, feedback)):
        row = "<div class='row'>"
        for j, (char, fb_color) in enumerate(zip(guess, fb)):
            color = COLORS.get(fb_color, '#ffffff')
            row += f"<span class='cell' style='background-color: {color};'>{char}</span>"
        row += "</div>"
        st.write(row, unsafe_allow_html=True)


def display_letters_and_colors(letters_and_colors):
    # Inject custom CSS
    st.write("""
        <style>
        .letter {
            display: inline-block;
            width: 20px;
            height: 20px;
            text-align: center;
            vertical-align: middle;
            margin: 0.1em;
            border-radius: 0.25em;
            color: black;
            font-size: small;
        }
        .form-container {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display letters in a row
    row = "<div class='row'>"
    for letter in [chr(x) for x in range(97, 123)]:
        color = letters_and_colors.get(letter, 'white')
        row += f"<span class='letter' style='background-color: {color};'>{letter}</span>"
    row += "</div>"
    st.write(row, unsafe_allow_html=True)


def main():

    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'team' not in st.session_state:
        st.session_state.team = ''
    if 'target' not in st.session_state:
        reset_game()

    if st.session_state.name == '' or st.session_state.team == '':
        st.title("""👨‍👩‍👧‍👧 Welcome to Dyuthi and Yuk's Baby Gender Reveal! 👨‍👩‍👧‍👦\n\nWill it be a baby boy, girl, or a mini T-Rex? 🦖 Stay Tuned! """)
        with st.form(key='name_team_form'):
            st.write('<div class="form-container">', unsafe_allow_html=True)
            name = st.text_input("Enter your name:", key="name_input")
            team = st.radio("Select your team:", options=["Boy", "Girl", "Mini T-Rex"], key="team_input")
            submit_button = st.form_submit_button(label="Go to the game", on_click=reset_game)
            st.write('</div>', unsafe_allow_html=True)

        if submit_button:
            if name.strip() != '' and team:
                st.session_state.name = name.strip()
                st.session_state.team = team
            else:
                st.error("Please enter your name and select a team.")
    else:
        # st.write(f"{st.session_state.name.capitalize()} for Team {st.session_state.team.capitalize()}! Enter your 5-letter word")
        target = st.session_state.target
        guesses = st.session_state.guesses
        feedback = st.session_state.feedback
        letters_and_colors = st.session_state.letters_and_colors

        st.write('<div class="form-container">', unsafe_allow_html=True)
        with st.form(key='wordle_form', clear_on_submit=True):
            guess = st.text_input("Enter a 5-letter word", max_chars=len(target), label_visibility="collapsed", placeholder="Enter 5-letter word").lower()
            submit_button = st.form_submit_button(label="Submit")
        st.write('</div>', unsafe_allow_html=True)

        if submit_button:
            guess = guess.lower()
            if len(guess) == len(target):
                if not is_valid_word(guess):
                    st.warning('Not a valid word', icon="⚠️")
                else:
                    if st.session_state.index == 6:
                        st.error(f"Oops! The correct answer is {target}. Score : 0 \n\nPlay again to get more points for your team!")
                        streamlit_root_logger.info(f"Name: {st.session_state.name} Team: {st.session_state.team} Score: 0")
                    else:
                        guesses[st.session_state.index] = guess
                        feedback[st.session_state.index] = check_guess(guess, target, letters_and_colors)
                        st.session_state.guesses = guesses
                        st.session_state.feedback = feedback
                        st.session_state.index += 1

                        if guess == target:
                            score = 7 - st.session_state.index
                            st.success(f"Congratulations! You guessed the word! Score : {score}. \n\nPlay again to get more points for your team!")
                            streamlit_root_logger.info(f"Name: {st.session_state.name} Team: {st.session_state.team} Score: {score}")

                        elif guess != target and st.session_state.index == 6:
                            st.error(f"Oops! The correct answer is {target}. Score : 0 \n\nPlay again to get more points for your team!")
                            streamlit_root_logger.info(f"Name: {st.session_state.name} Team: {st.session_state.team} Score: 0")

            else:
                st.error("Guess must be {} letters long.".format(len(target)))

        with st.form(key='control_form'):

            display_letters_and_colors(letters_and_colors)
            wordle_table(guesses, feedback)

            st.write('<div class="form-container2">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Go Back", on_click=go_back):
                    pass

            with col2:
                if st.form_submit_button("Play Again", on_click=reset_game):
                    pass

            st.write('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
