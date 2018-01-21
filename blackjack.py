import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = "Test"
score = 0
current_deck = ""
player_hand = ""
dealer_hand = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        contains = "Hand contains "
        for card in self.hand:
            contains += str(card) + " "
        return contains

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.value = 0
        aces = False
        for card in self.hand:
            rank = card.get_rank()
            if rank == 'A':
                aces = True
            self.value += VALUES[rank]
        if aces and (self.value + 10 <= 21):
            self.value += 10
        return self.value

    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards


# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop(-1)

    def __str__(self):
        # return a string representing the deck
        contains = "Deck contains "
        for card in self.deck:
            contains += str(card) + " "
        return contains


#define event handlers for buttons
def deal():
    global outcome, in_play, current_deck, player_hand, dealer_hand
    current_deck = Deck()
    current_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        player_hand.add_card(current_deck.deal_card())
        dealer_hand.add_card(current_deck.deal_card())
    print "Player " + str(player_hand) + "Dealer " + str(dealer_hand)
    in_play = True
    outcome = "Hit or stand?"

def hit():
    global outcome, in_play, score, player_hand, current_deck
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(current_deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        outcome = "You have busted! New deal?"
        in_play = False
        score -= 1

def stand():
    global outcome, in_play, score, player_hand, dealer_hand
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if player_hand.get_value() > 21:
        outcome = "Can't stand, you already busted! New deal?"
    elif in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(current_deck.deal_card())
    # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted, you win this round! New deal?"
            score += 1
        elif dealer_hand.get_value() > player_hand.get_value():
            outcome = "Dealer won this round. New deal?"
            score -= 1
        elif dealer_hand.get_value() == player_hand.get_value():
            outcome = "Dealer wins tie. New deal?"
            score -= 1
        else:
            outcome = "You won this round! New deal?"
            score += 1
        in_play = False

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    card = Card("S", "A")
    card.draw(canvas, [300, 300])

    canvas.draw_text(outcome, (20, 20), 20, 'white')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
