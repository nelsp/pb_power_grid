import create_use_resources as res




class Player(res.Resource):
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

    def show_resources(self):
        return self.resources

    def show_generators(self):
        return len(self.generators), self.generators

    def purchase_generator(self, city, cost):
        if city not in self.generators:
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

    def purchase_resources(self, fuel, amount):
        """ checks the resource board for purchase updates the board and updates player money and resource holdings"""
        purchase = fuel.buy_resource(amount)
        self.update_money(-purchase[1])
        self.resources[fuel.show_name()] += amount

    def use_resources_to_power(self, fuel, amount):
        """ returns resource to the supply and updates players resource holdings"""
        fuel.use_resource(amount)
        self.resources[fuel.show_name()] -= amount


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

total_supply_coal = 27
start_supply_coal = (2, 9)

coal_cl = [[1, [0, 0, 0, 0]], [2, [0, 0, 0, 0]], [3, [0, 0, 0, 0]], [4, [0, 0, 0, 0]], [5, [0, 0, 0, 0]],
           [6, [0, 0, 0, 0]], [7, [0, 0]], [8, [0, 0]], [9, [0, 0]]]

coal = res.Resource(total_supply_coal, start_supply_coal, coal_cl, 'coal')
coal.initialize_supply()

print('starting resource board')
coal.show_board()

player_1.purchase_resources(coal, 4)
print player_1.show_resources()
print player_1.show_money()

coal.show_board()
player_1.use_resources_to_power(coal, 2)
print player_1.show_resources()
coal.show_supply()
print 'test'





