# --- STREAMLIT VERSION ---
import streamlit as st
from PIL import Image
import random

# Path to card images folder
card_images_path = 'card_images/'

# List of all individual card filenames (excluding card_back.png and orig_cards.gif)
card_filenames = [
    "2-spades.png", "3-spades.png", "4-spades.png", "5-spades.png",
    "6-spades.png", "7-spades.png", "8-spades.png", "9-spades.png",
    "10-spades.png", "J-spades.png", "Q-spades.png", "K-spades.png",
    "A-spades.png", "wild-spades.png", "joker.png"
]

# Load card images into a list
def load_card_images(filenames, path):
    return [Image.open(path + filename) for filename in filenames]

# Initialize deck: Duplicate each card to form pairs, shuffle them, and return the deck
def initialize_deck(filenames, path):
    cards = load_card_images(filenames, path)
    deck = cards * 2  # Create pairs of cards
    random.shuffle(deck)  # Shuffle the deck
    return deck

# Check if two selected cards match
def match_check(deck, flipped):
    if len(flipped) == 2:
        return deck[flipped[0]] == deck[flipped[1]]
    return False

# Display the memory board of cards
def display_board(deck, flipped_cards, matched_cards):
    cols = st.columns(15)  # Create 8 columns for a larger grid
    for i, card in enumerate(deck):
        col = cols[i % 15]  # Assign the card to the correct column
        with col:  # To control the alignment of each card
            if i in flipped_cards or i in matched_cards:
                st.image(card, use_column_width=True)  # Show the revealed or matched card
            else:
                # Show the card back
                if st.button("", key=f"card-{i}"):  # Using a button to track clicks
                    st.session_state.flipped_cards.append(i)
                st.image(Image.open(card_images_path + "card_back.png"), use_column_width=True)
                
    # Add custom CSS to ensure fixed height and alignment
    st.markdown(
        """
        <style>
        .element-container {
            display: flex;
            justify-content: center;
        }
        img {
            max-height: 150px;  /* Set a fixed height for all images */
            object-fit: cover;  /* Ensure all images are centered and scaled */
        }
        </style>
        """, unsafe_allow_html=True
    )


# CSS to disable the "View fullscreen" magnifier icon on images
def inject_css():
    st.markdown(
        """
        <style>
        /* Hide the fullscreen icon (magnifying glass) */
        button[title="View fullscreen"] {
            display: none;
        }

        /* Center align the current turn */
        .centered-text {
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 24px;
        }

        /* Add margin between the score and the game board */
        .score-area {
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Main Streamlit application logic
def main_streamlit():
    st.title("Memory Match Game")

    # Inject custom CSS
    inject_css()

    # Mode selection logic
    if 'mode' not in st.session_state:
        st.write("Select Game Mode:")
        if st.button("One Player"):
            st.session_state.mode = 'one_player'
            st.session_state.scores = [0]  # Only one score for one player
            initialize_game()  # Initialize the game
        if st.button("Two Players"):
            st.session_state.mode = 'two_players'
            st.session_state.scores = [0, 0]  # Two scores for two players
            initialize_game()  # Initialize the game
    else:
        # If mode is already selected, run the game
        if 'deck' not in st.session_state:
            initialize_game()

        # Display the current scores on the main page
        if st.session_state.mode == 'one_player':
            st.write(f"<div class='score-area'>Matches: {st.session_state.scores[0]} / {len(card_filenames)}</div>", unsafe_allow_html=True)
        else:
            st.write(f"<div class='score-area'>Player 1 Matches: {st.session_state.scores[0]} / {len(card_filenames)}</div>", unsafe_allow_html=True)
            st.write(f"<div class='score-area'>Player 2 Matches: {st.session_state.scores[1]} / {len(card_filenames)}</div>", unsafe_allow_html=True)
            
            # Display current turn in two-player mode
            st.markdown(f"<div class='centered-text'>Current Turn: Player {st.session_state.current_player + 1}</div>", unsafe_allow_html=True)

        # Render the memory game board
        display_board(st.session_state.deck, st.session_state.flipped_cards, st.session_state.matched_cards)

        # Check if two cards are flipped
        if len(st.session_state.flipped_cards) == 2:
            if match_check(st.session_state.deck, st.session_state.flipped_cards):
                st.session_state.matched_cards.extend(st.session_state.flipped_cards)
                st.session_state.scores[st.session_state.current_player] += 1  # Increment score for the current player
            if st.session_state.mode == 'two_players':
                # Switch to the other player after checking matches
                st.session_state.current_player = 1 - st.session_state.current_player
            # Reset flipped cards after a brief delay
            st.session_state.flipped_cards = []

def initialize_game():
    st.session_state.deck = initialize_deck(card_filenames, card_images_path)
    st.session_state.flipped_cards = []  # Stores indices of currently flipped cards
    st.session_state.matched_cards = []  # Stores indices of matched cards
    if st.session_state.mode == 'two_players':
        st.session_state.current_player = 0  # Track current player (0 or 1)

# Run the Streamlit app
if __name__ == "__main__":
    main_streamlit()
