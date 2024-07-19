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
            margin-top: 20px;
        }
        .form-container {
            display: flex;
            align-items: center;
            gap: 10px;
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

    # Form to handle input and submission
    with st.form(key='name_form'):
        st.write('<div class="form-container">', unsafe_allow_html=True)
        name = st.text_input("Enter your name:")
        submit_button = st.form_submit_button(label="Submit")
        st.write('</div>', unsafe_allow_html=True)

    if submit_button and name:
        st.write(f"Hello, {name}!")
        # Display the colored letters
        display_colored_letters(letters_and_colors)

if __name__ == "__main__":
    main()
