import streamlit as st

# Define a list of letters and their corresponding colors
letters_and_colors = [
    ('A', '#FF5733'),  # Red
    ('B', '#33FF57'),  # Green
    ('C', '#3357FF'),  # Blue
    ('D', '#F1C40F'),  # Yellow
    ('E', '#9B59B6')   # Purple
]

def display_colored_letters(letters_and_colors):
    # Inject custom CSS
    st.write("""
        <style>
        .letter {
            display: inline-block;
            width: 2em;
            height: 2em;
            text-align: center;
            vertical-align: middle;
            line-height: 2em;
            margin: 0.2em;
            border-radius: 0.25em;
            font-size: 1.5em;
        }
        .row {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display letters in a row
    row = "<div class='row'>"
    for letter, color in letters_and_colors:
        row += f"<span class='letter' style='background-color: {color};'>{letter}</span>"
    row += "</div>"
    st.write(row, unsafe_allow_html=True)


def main():
    st.title("Colored Letters Display")

    # Display the colored letters
    display_colored_letters(letters_and_colors)


if __name__ == "__main__":
    main()
