import random

def create_deck() -> list:
    """Create a deck"""
    deck = []
    C = ['Spade', 'Hearth', 'Diamond', 'Club']
    V = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for value in V:
        for card in C:
            deck.append((value, card))
    return deck

def shuffle_deck() -> list:
    """Shuffle the deck"""
    deck = create_deck()
    new_deck = []
    for i in range(51):
        nb = random.randint(1,(51-i))
        new_deck.append(deck.pop(nb))
    new_deck.append(deck[0])
    return new_deck

def calcul_value(hand: list) -> int:
    """Compute the value of a hand"""
    value = 0
    ace = 0
    count_ace = 0
    for cards in hand:
        if cards[0] in ['J','Q','K']:
            value += 10
        elif cards[0] == 'A':
            ace += 1
        else :
            value += int(cards[0])
    #Compute the aces
    for _ in range(ace):
        if value > 10 :
            value += 1
            if value > 21 and count_ace != 0:
                count_ace -= 1
                value -= 10
        else :
            count_ace += 1
            value += 11

    return value




def round(money: int) -> str:
    """A round of blackjack"""
    print('==========================================================')
    print('')
    my_value = 0
    dealer_value = 0
    dbl = False

    #Prepare the deck and distribute hands.
    deck = shuffle_deck()
    player_hand = [deck.pop(0), deck.pop(1)]
    dealer_hand = [deck.pop(0)]


    #Computation of the value of each hand
    my_value = calcul_value(player_hand)
    dealer_value = calcul_value(dealer_hand)

    #Display hands
    for card in dealer_hand :
        print(card[0], card[1])
    print("This is the dealer's hand.")
    print('')

    for card in player_hand :
        print(card[0], card[1])
    print('This is your hand.')
    print('')


    #Player's turn
    #The player chooses
    choice = input("What do you want to do (Hit, Stand, DoubleDown) ? ").lower()
    if choice in ["hit", "h", "doubledown", "double down", "dbl",] :
        hit = True
        while hit :
            if choice not in ["hit", "h"]:
                hit = False
                dbl = True

            print('')

            #Distribution and display of the hand
            player_hand.append(deck.pop(0))
            for card in player_hand :
                print(card[0], card[1])
            print('This is now your hand.')
            print('')

            #Computation of the value of the player's hand and of a potential loose
            my_value = calcul_value(player_hand) 
            if my_value > 21 :
                if dbl :
                    return('Lost Dbl')
                else:
                    return('Lost')

            #The player chooses
            if hit :
                choice = input('Do you want to Hit, Stand or DoubleDown ? ').lower()
                if choice in ["stand", "s"]:
                    hit = False


    print('')

    #Dealer's turn
    while dealer_value < 17 :

        #Computation of the value of the dealer's hand
        dealer_hand.append(deck.pop(0))

        #Calcul de la valeur de sa main
        dealer_value = calcul_value(dealer_hand)

    #Print dealer's hand
    for card in dealer_hand :
        print(card[0], card[1])
    print("This is the dealer's hand.")
    print('')

    #BlackJack check
    if my_value == 21:
        if dealer_value == 21:
            print('Double BlackJack !')
            return("Tie")
        else:
            print('BlackJack !')
            if dbl :
                return('Win Dbl')
            else :
                return("Win BJ")

    #Determine the winner
    if dealer_value > 21 :
        print('The dealer busted.')
        if dbl :
            return('Win Dbl')
        else :
            return('Win')
    elif dealer_value == my_value :
        return('Tie')
    elif dealer_value > my_value :
        if dbl :
            return('Lost Dbl')
        else:
            return('Lost')
    else :
        if dbl :
            return('Win Dbl')
        else :
            return('Win')

def game(money: int) -> int:
    """A game of BlackJack"""
    while True :
        bet = input("You have "+str(money)+" dollars. How much do you want to bet ? ")
        try :
            bet = int(bet)
            if bet > money :
                raise ValueError
            break
        except :
            print("Invalid input.")

    result_round = round(bet)

    #Update the money depending on the outcome of the round
    if result_round == 'Lost':
        print('You lost the round. You lost your bet')
        money -= bet
    elif result_round == 'Win':
        print('You won the round . You win double the amount of your bet.')
        money += bet
    elif result_round == 'Win BJ':
        print('You won the round with a BlackJack ! You win back three time the amount of your bet !')
        money += bet*2
    elif result_round == 'Win Dbl':
        print('You won the round with a DoubleDown ! You win back three time the amount of your bet !')
        money += bet*2
    elif result_round == 'Lost Dbl':
        print('You lost the round with a DoubleDown. You loose double the amount of your bet.')
        money -= bet*2
    else :
        print("It's a tie. You can take back your bet.")

    if money <= 0 :
        return money

    #The player choose if he wants to play again
    if input("Do you want to try again ? Yes / No ").lower() in ["yes", "y"]:
        print('')
        return game(money)
    else :
        return money

#Start the game
starting_money = 10
final_money = game(starting_money)

print('')
print(f'You left the casino with {final_money} dollars.')
if final_money < 0 :
    print('You owe money. And they will do everything to get it back. Everything.')

# A faire :
#   BlackJack et DoubleDown dans une même main
