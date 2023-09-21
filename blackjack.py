import tkinter
import random


def load_images() -> list[tuple[int, tkinter.PhotoImage]]:
    suits = ('club', 'diamond', 'heart', 'spade')
    faces = ('jack', 'king', 'queen')
    card_images = []
    ext = 'png' if tkinter.TkVersion >= 8.6 else 'ppm'

    for suit in suits:
        for card in range(1, 11):
            pic_path = f"cards\\{card}_{suit}.{ext}"
            image = tkinter.PhotoImage(file=pic_path)
            card_images.append((card, image,))
        for card in faces:
            pic_path = f"cards\\{card}_{suit}.{ext}"
            image = tkinter.PhotoImage(file=pic_path)
            card_images.append((10, image,))
    return card_images


def deal_card(frame: tkinter.Frame) -> tuple[int, tkinter.PhotoImage]:
    card = deck.pop(0)
    tkinter.Label(frame, image=card[1], relief='raised').pack(side='left')
    return card


def score_hand(hand: list[tuple[int, tkinter.PhotoImage]]) -> int:
    score = 0
    ace = False
    for card in hand:
        card_value = card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer() -> None:
    score = score_hand(dealer_hand)
    back_image.pack_forget()
    player_score = score_hand(player_hand)
    while score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        score = score_hand(dealer_hand)
        dealer_score_label.set(score)
    if score == 21:
        result.set("Blackjack, Dealer Wins")
    elif score > 21:
        result.set("Dealer bust, Player Wins")
    elif score > player_score:
        result.set("Dealer wins")
    elif score == player_score:
        result.set("Draw")
    else:
        result.set("Player wins")


def deal_player() -> None:
    player_hand.append(deal_card(player_card_frame))
    score = score_hand(player_hand)
    player_score_label.set(score)
    if score == 21:
        result.set("Blackjack, Player Wins")
    elif score > 21:
        result.set("Player bust, Dealer Wins")


def new_game() -> None:
    global deck, dealer_card_frame, player_card_frame, back_image
    result.set("")
    dealer_card_frame.destroy()
    player_card_frame.destroy()
    player_hand.clear()
    dealer_hand.clear()

    deck = cards.copy()
    random.shuffle(deck)
    dealer_card_frame = tkinter.Frame(card_frame, bg="green")
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    player_card_frame = tkinter.Frame(card_frame, bg="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()
    back_image = tkinter.Label(dealer_card_frame, image=back_card)
    back_image.pack(side='left')


def play():
    root.mainloop()


root = tkinter.Tk()

root.title("Blackjack")
root.geometry("640x480")
root.configure(bg='green')


# Result of the match
result = tkinter.StringVar()
tkinter.Label(root, textvariable=result, bg="green", fg="white").grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(root, relief="sunken", bd=1, bg="green")
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

# Dealer Frame
dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", bg="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, bg="green", fg="white").grid(row=1, column=0)
dealer_card_frame = tkinter.Frame(card_frame)

# Player Frame
player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", bg="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, bg="green", fg="white").grid(row=3, column=0)
player_card_frame = tkinter.Frame(card_frame)

# The buttons
button_frame = tkinter.Frame()
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')
stand_button = tkinter.Button(button_frame, text="Stand", command=deal_dealer, width=5)
stand_button.grid(row=0, column=0)
hit_button = tkinter.Button(button_frame, text="Hit", command=deal_player, width=5)
hit_button.grid(row=0, column=1)

tkinter.Button(button_frame, text="New Game", command=new_game, width=10).grid(row=1, column=0, columnspan=2)

back_card = tkinter.PhotoImage(file="cards\\back.png")
cards = load_images()
back_image = tkinter.Label()

deck = []
dealer_hand = []
player_hand = []

new_game()

if __name__ == '__main__':
    root.mainloop()
