import streamlit as st
import numpy as np
import time

class Roulette:
    def __init__(self):
        self.numbers = list(range(37))  # 0-36
        self.colors = {0: 'green'}
        # Assign red and black colors
        for i in range(1, 37):
            if i in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                self.colors[i] = 'red'
            else:
                self.colors[i] = 'black'

    def spin(self):
        return np.random.choice(self.numbers)

    def calculate_winnings(self, bet_amount, bet_type, bet_value, result):
        if bet_type == 'number' and result == bet_value:
            return bet_amount * 35
        elif bet_type == 'color' and self.colors[result] == bet_value:
            return bet_amount * 2
        elif bet_type == 'even/odd':
            if bet_value == 'even' and result % 2 == 0 and result != 0:
                return bet_amount * 2
            elif bet_value == 'odd' and result % 2 == 1:
                return bet_amount * 2
        return 0

    def play(self):
        st.header("🎲 Roulette")
        
        # Betting options
        bet_type = st.selectbox("Select bet type:", ['number', 'color', 'even/odd'])
        
        if bet_type == 'number':
            bet_value = st.number_input("Choose a number:", min_value=0, max_value=36, value=0)
        elif bet_type == 'color':
            bet_value = st.selectbox("Choose color:", ['red', 'black', 'green'])
        else:
            bet_value = st.selectbox("Choose:", ['even', 'odd'])
        
        bet_amount = st.number_input("Place your bet ($):", min_value=1.0, max_value=st.session_state.balance, value=10.0, step=1.0)
        
        if st.button("SPIN! 🎲"):
            if bet_amount > st.session_state.balance:
                st.error("Insufficient funds!")
                return
            
            st.session_state.balance -= bet_amount
            
            # Spinning animation
            with st.empty():
                for _ in range(3):
                    temp_result = self.spin()
                    st.write(f"Spinning... {temp_result} {self.colors[temp_result]}")
                    time.sleep(0.3)
                
                # Final result
                result = self.spin()
                st.write(f"Result: {result} {self.colors[result]}")
                
                # Calculate winnings
                winnings = self.calculate_winnings(bet_amount, bet_type, bet_value, result)
                
                if winnings > 0:
                    st.success(f"🎉 You won ${winnings:.2f}!")
                    st.session_state.balance += winnings
                else:
                    st.info("Try again! 🎲")
                
                # Show balance update
                st.metric("Balance", f"${st.session_state.balance:.2f}")
        
        # Display paytable
        with st.expander("View Payouts"):
            st.markdown("""
            ### Roulette Payouts
            * Single Number: 35 to 1
            * Red/Black: 1 to 1
            * Even/Odd: 1 to 1
            """)
