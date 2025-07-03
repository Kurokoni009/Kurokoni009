import streamlit as st
import numpy as np
import time

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        suits = {"hearts": "♥️", "diamonds": "♦️", "clubs": "♣️", "spades": "♠️"}
        values = {11: "J", 12: "Q", 13: "K", 1: "A"}
        card_value = values.get(self.value, str(self.value))
        return f"{card_value}{suits[self.suit]}"

class Blackjack:
    def __init__(self):
        self.suits = ["hearts", "diamonds", "clubs", "spades"]
        self.values = list(range(1, 14))
        self.deck = [Card(suit, value) for suit in self.suits for value in self.values]
        np.random.shuffle(self.deck)
    
    def card_value(self, card):
        if card.value > 10:
            return 10
        elif card.value == 1:  # Ace
            return 11
        return card.value
    
    def calculate_hand(self, hand):
        total = 0
        aces = 0
        
        for card in hand:
            value = self.card_value(card)
            if value == 11:
                aces += 1
            total += value
        
        # Adjust for aces
        while total > 21 and aces:
            total -= 10
            aces -= 1
        
        return total
    
    def deal_card(self):
        if not self.deck:
            self.__init__()
        return self.deck.pop()
    
    def play(self):
        st.header("🃏 Blackjack")
        
        # Initialize or reset game state
        if 'player_hand' not in st.session_state:
            st.session_state.player_hand = []
            st.session_state.dealer_hand = []
            st.session_state.game_phase = 'betting'
            st.session_state.current_bet = 0
        
        # Betting phase
        if st.session_state.game_phase == 'betting':
            bet = st.number_input("Place your bet ($):", min_value=1.0, max_value=st.session_state.balance, value=10.0, step=1.0)
            
            if st.button("Deal"):
                if bet > st.session_state.balance:
                    st.error("Insufficient funds!")
                    return
                
                st.session_state.balance -= bet
                st.session_state.current_bet = bet
                
                # Deal initial cards
                st.session_state.player_hand = [self.deal_card(), self.deal_card()]
                st.session_state.dealer_hand = [self.deal_card(), self.deal_card()]
                st.session_state.game_phase = 'playing'
                st.experimental_rerun()
        
        # Playing phase
        elif st.session_state.game_phase == 'playing':
            # Display hands
            st.write("### Dealer's Hand:")
            st.write(f"{str(st.session_state.dealer_hand[0])} 🂠")  # Hide second card
            
            st.write("### Your Hand:")
            st.write(" ".join(str(card) for card in st.session_state.player_hand))
            st.write(f"Your total: {self.calculate_hand(st.session_state.player_hand)}")
            
            # Player decisions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Hit"):
                    st.session_state.player_hand.append(self.deal_card())
                    if self.calculate_hand(st.session_state.player_hand) > 21:
                        st.session_state.game_phase = 'game_over'
                        st.experimental_rerun()
            
            with col2:
                if st.button("Stand"):
                    st.session_state.game_phase = 'dealer_turn'
                    st.experimental_rerun()
        
        # Dealer's turn
        elif st.session_state.game_phase == 'dealer_turn':
            st.write("### Dealer's Hand:")
            st.write(" ".join(str(card) for card in st.session_state.dealer_hand))
            
            dealer_total = self.calculate_hand(st.session_state.dealer_hand)
            while dealer_total < 17:
                st.session_state.dealer_hand.append(self.deal_card())
                dealer_total = self.calculate_hand(st.session_state.dealer_hand)
            
            st.write(f"Dealer's total: {dealer_total}")
            
            st.write("### Your Hand:")
            st.write(" ".join(str(card) for card in st.session_state.player_hand))
            player_total = self.calculate_hand(st.session_state.player_hand)
            st.write(f"Your total: {player_total}")
            
            st.session_state.game_phase = 'game_over'
            st.experimental_rerun()
        
        # Game over
        elif st.session_state.game_phase == 'game_over':
            st.write("### Dealer's Hand:")
            st.write(" ".join(str(card) for card in st.session_state.dealer_hand))
            dealer_total = self.calculate_hand(st.session_state.dealer_hand)
            st.write(f"Dealer's total: {dealer_total}")
            
            st.write("### Your Hand:")
            st.write(" ".join(str(card) for card in st.session_state.player_hand))
            player_total = self.calculate_hand(st.session_state.player_hand)
            st.write(f"Your total: {player_total}")
            
            # Determine winner
            if player_total > 21:
                st.error("Bust! You lose!")
            elif dealer_total > 21:
                st.success("Dealer bust! You win!")
                st.session_state.balance += st.session_state.current_bet * 2
            elif player_total > dealer_total:
                st.success("You win!")
                st.session_state.balance += st.session_state.current_bet * 2
            elif player_total < dealer_total:
                st.error("Dealer wins!")
            else:
                st.info("Push! It's a tie!")
                st.session_state.balance += st.session_state.current_bet
            
            if st.button("Play Again"):
                st.session_state.game_phase = 'betting'
                st.session_state.player_hand = []
                st.session_state.dealer_hand = []
                st.session_state.current_bet = 0
                st.experimental_rerun()
        
        # Display paytable
        with st.expander("View Rules"):
            st.markdown("""
            ### Blackjack Rules
            * Beat the dealer's hand without going over 21
            * Face cards are worth 10
            * Aces are worth 11 or 1
            * Blackjack pays 2:1
            """)
