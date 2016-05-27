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
	def create_initial_deck(cls, cards):
		light_cards = [c for c in cards if c.type == 'light']
		dark_cards = [c for c in cards if c.type == 'dark']
		
		shuffle(dark_cards)
		first_nine = sorted(dark_cards[:9], key=lambda x: x.cost)
		rest = dark_cards[9:] + light_cards
		shuffle(rest)
		
		return first_nine + rest