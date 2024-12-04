from card import Card
from random import shuffle

class Game:
	def __init__(self, props):
		self.market = props.get('market')
		self.deck = props.get('deck')
		self.board = props.get('board')
		self.players = props.get('players')
		self.phase = props.get('phase')
		self.turn_order = props.get('turn_order')
		self.resources = props.get('resources')

	@classmethod
	def create_initial_deck(cls, cards, num_players=5):
		light_cards = [c for c in cards if c.type == 'light']
		dark_cards = [c for c in cards if c.type == 'dark']
		
		shuffle(dark_cards)
		shuffle(light_cards)
		
		#Remove cards if playing with less players
		if num_players == 3:
			dark_cards = dark_cards[:-2]
			light_cards = light_cards[:-6]
		if num_players == 4:
			dark_cards = dark_cards[:-1]
			light_cards = light_cards[:-3]
		
		first_nine = sorted(dark_cards[:9], key=lambda x: x.cost)
		rest = dark_cards[9:] + light_cards
		shuffle(rest)
		
		return first_nine + rest