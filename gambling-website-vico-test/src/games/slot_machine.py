import streamlit as st
import numpy as np
import time

class SlotMachine:
    def __init__(self):
        self.symbols = ["🍎", "🍋", "🍒", "💎", "7️⃣", "🌟"]
        self.payouts = {
            "🍎": 2,
            "🍋": 3,
            "🍒": 4,
            "💎": 5,
            "7️⃣": 10,
            "🌟": 15
        }

    def spin(self):
        return [np.random.choice(self.symbols) for _ in range(3)]

    def calculate_winnings(self, bet, result):
        if len(set(result)) == 1:  # All symbols match
            return bet * self.payouts[result[0]]
        elif len(set(result)) == 2:  # Two symbols match
            return bet * 0.5
        return 0

    def play(self):
        st.header("🎰 Slot Machine")
        
        # Betting
        bet = st.number_input("Place your bet ($):", min_value=1.0, max_value=st.session_state.balance, value=10.0, step=1.0)
        
        if st.button("SPIN! 🎰"):
            if bet > st.session_state.balance:
                st.error("Insufficient funds!")
                return
                
            st.session_state.balance -= bet
            
            # Animation effect
            with st.empty():
                for _ in range(3):
                    temp_result = self.spin()
                    st.write("".join(temp_result))
                    time.sleep(0.2)
                
                # Final result
                result = self.spin()
                st.write("".join(result))
                
                # Calculate winnings
                winnings = self.calculate_winnings(bet, result)
                
                if winnings > 0:
                    st.success(f"🎉 You won ${winnings:.2f}!")
                    st.session_state.balance += winnings
                else:
                    st.info("Try again! 🎲")
                
                # Show balance update
                st.metric("Balance", f"${st.session_state.balance:.2f}")
        
        # Display paytable
        with st.expander("View Paytable"):
            st.markdown("### Symbol Payouts (Multipliers)")
            for symbol, payout in self.payouts.items():
                st.write(f"{symbol}: {payout}x")
            st.markdown("Two matching symbols: 0.5x")
