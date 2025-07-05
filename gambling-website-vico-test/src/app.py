import streamlit as st
import numpy as np
from games.slot_machine import SlotMachine
from games.roulette import Roulette
from games.blackjack import Blackjack

# Configure the app
st.set_page_config(
    page_title="Virtual Casino",
    page_icon="🎰",
    layout="wide"
)

# Initialize session state
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.0

# Main app header
st.title("🎰 Virtual Casino")
st.markdown("### Welcome to the Virtual Casino! Play responsibly!")

# Display current balance
st.sidebar.header("Your Balance")
st.sidebar.metric("Current Balance", f"${st.session_state.balance:.2f}")

# Add funds section
with st.sidebar.expander("Add Funds"):
    amount = st.number_input("Amount to add:", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
    if st.button("Add Funds"):
        st.session_state.balance += amount
        st.success(f"Successfully added ${amount:.2f}")
        st.experimental_rerun()

# Game selection
game_choice = st.selectbox(
    "Choose your game:",
    ["Slot Machine", "Roulette", "Blackjack"]
)

# Display selected game
if game_choice == "Slot Machine":
    SlotMachine().play()
elif game_choice == "Roulette":
    Roulette().play()
elif game_choice == "Blackjack":
    Blackjack().play()

# Responsible gambling message
st.sidebar.markdown("---")
st.sidebar.markdown("""
### Responsible Gambling
Remember:
* This is for entertainment only
* Never bet more than you can afford to lose
* Take regular breaks
* Set time and money limits
""")
