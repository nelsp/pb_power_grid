import random


number_of_players = 5

def market_setup(number_of_players):

    """returns 2 lists, the first 9 dark cards for the starting marketplace and the rest of the deck ready for play"""

    cards = [['44', 'green', '0', '6'], ['36', 'green', '0', '5'], ['31', 'green', '0', '4'], ['28', 'green', '0', '3'], ['24', 'green', '0', '3'], ['17', 'green', '0', '2'], ['11', 'green', '0', '1'],
             ['46', 'gas', '2', '7'], ['39', 'gas', '2', '6'], ['34', 'gas', '3', '6'], ['26', 'gas', '1', '4'], ['19', 'gas', '1', '3'], ['16', 'gas', '2', '3'], ['14', 'gas', '1', '2'], ['5', 'gas', '2', '1'],
             ['40', 'coal', '2', '6'], ['33', 'coal', '3', '6'], ['29', 'coal', '2', '5'], ['27', 'coal', '1', '4'], ['25', 'coal', '2', '5'], ['20', 'coal', '3', '4'], ['15', 'coal', '1', '2'], ['12', 'coal', '2', '2'],
             ['9', 'coal', '3', '2'], ['7', 'coal', '1', '1'], ['4', 'coal', '2', '1'], ['3', 'coal', '2', '1'], ['42', 'oil', '2', '6'], ['38', 'oil', '3', '6'], ['30', 'oil', '2', '5'], ['23', 'oil', '2', '4'],
             ['18', 'oil', '2', '3'], ['10', 'oil', '2', '2'], ['6', 'oil', '1', '1'], ['50', 'nuclear', '2', '7'], ['37', 'nuclear', '2', '6'], ['32', 'nuclear', '2', '5'], ['21', 'nuclear', '1', '3'],
             ['13', 'nuclear', '1', '2'], ['35', 'oil&gas', '2', '5'], ['22', 'oil&gas', '3', '5'], ['8', 'oil&gas', '2', '3']]

    for c in cards:
        for i in range(len(c)):
            if len(c[i])< 3:
                c[i] = int(c[i])

    for c in cards:
        if c[0] < 16:
            c.append('dark')
        else:
            c.append('light')

    dark_cards = []
    light_cards = []

    for c in cards:
        if c[0] < 16:
            dark_cards.append(c)
        else:
            light_cards.append(c)

    random.shuffle(dark_cards)
    random.shuffle(light_cards)

    if number_of_players == 3:
        dark_cards = dark_cards[:-2]
        light_cards = light_cards[:-6]

    elif number_of_players == 4:
        dark_cards = dark_cards[:-1]
        light_cards = light_cards[:-3]


    first_nine_cards = dark_cards[:9]
    rest_of_dark_cards = dark_cards[9:]

    remaining_deck = rest_of_dark_cards + light_cards
    random.shuffle(remaining_deck)
    remaining_deck.append([99, 'stage three', 0, 0, 'light'])

    return first_nine_cards, remaining_deck

#*****************************************************************



test_initial_market = market_setup(number_of_players)

print test_initial_market[0]
print test_initial_market[1]










