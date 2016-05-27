import json
from Classes.game import Game
from Classes.resource import Resource
from Classes.market import Market
from Classes.card import Card
config = json.loads(open('config.json').read())

def create_resource_market():
  resources = []
  initial_resources = config.get('resource_market')
  for r in initial_resources.keys():
    # initialize resource costs as objects
    resources = resources + [Resource({'type': r, 'cost': c}) for c in initial_resources.get(r)] * 3
  return resources

def create_initial_deck_and_market():
  # Create the whole deck
  cards = [Card(c) for c in config.get('cards')]
  deck = Game.create_initial_deck(cards)
  
  # Initial market will be first 9
  initial_market = Market(deck[:9])
  rest = deck[9:]
  
  # Add the phase 3 card
  rest.append(Card(config.get('stage_three_card')))
  
  return initial_market, rest

def initialize_game():
  props = {}
  props['resources'] = create_resource_market()
  props['market'], props['deck'] = create_initial_deck_and_market()
  
  return Game(props)
  

game = initialize_game()

print [c.cost for c in game.market.inactive_market]


