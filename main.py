import streamlit as st
from PIL import Image
import random

# Path to your card images folder
card_images_path = 'card_images/'

# List of all individual card filenames
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
    cols = st.columns(10)  # Create 10 columns for a grid with 10 cards per row
    for i, card in enumerate(deck):
        col = cols[i % 10]  # Assign the card to the correct column
        with col:
            if i in flipped_cards or i in matched_cards:
                st.image(card, use_column_width=True)
            else:
                # Show the card back
                st.image(Image.open(card_images_path + "card_back.png"), use_column_width=True)

            # Use image click handling to register the flip
            if st.image(Image.open(card_images_path + "card_back.png"), use_column_width=True, key=f"card-{i}"):
                if i not in flipped_cards and i not in matched_cards:
                    st.session_state.flipped_cards.append(i)

# Main Streamlit application logic
def main_streamlit():
    st.title("Memory Match Game")

    # Initialize the game if not already done
    if 'deck' not in st.session_state:
        st.session_state.deck = initialize_deck(card_filenames, card_images_path)
        st.session_state.flipped_cards = []  # Stores indices of currently flipped cards
        st.session_state.matched_cards = []  # Stores indices of matched cards

    # Display the game board
    display_board(st.session_state.deck, st.session_state.flipped_cards, st.session_state.matched_cards)

# Run the Streamlit app
if __name__ == "__main__":
    main_streamlit()
