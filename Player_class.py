class Player():
    """player object to keep track of player state  """

    def __init__(self):
        self.money = 50
        self.generators = []
        self.cards = []
        self.resources = {'coal':0, 'oil':0, 'gas':0, 'uranium':0}

    def update_money(self, amount):
        if self.money + amount < 0:
            print "not enough money"
        else:
            self.money += amount

    def show_money(self):
        return self.money

    def show_generators(self):
        return len(self.generators), self.generators

    def purchase_generator(self, city, cost):
        if city not in self.generators:
            self.generators.append(city)
            self.update_money(-cost)
        else:
            print "already in city"

    def purchase_power_plant(self, card):
        if len(self.cards) < 3:
            self.cards.append(card)
            self.update_money(-card[0])
        else:
            print "must discard power plant"

    def show_power_plants(self):
        return self.cards

    def remove_power_plant(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print "don't own that power plant"






#**************************************************************

player_1 = Player()

print player_1.show_money()

player_1.update_money(25)

print player_1.show_money()

player_1.purchase_generator('Prague', 10)

print player_1.show_money()
print player_1.show_generators()

player_1.purchase_power_plant([39, 'gas', 2, 6, 'light'])
print player_1.show_money()
print player_1.show_power_plants()

player_1.remove_power_plant([39, 'gas', 2, 6, 'light'])
print player_1.show_money()
print player_1.show_power_plants()


