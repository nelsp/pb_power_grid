# pb_power_grid
simulate the power grid game

Game setup: only europe and 3-6 players

Based on number of players, generate random graph of europe, initial player order, market setup (cards shuffled) and resources allocated

Class Player:
	Money
	Generators - occupied cities
	Cards - power plants
	Resources

Class Resource

Class Market
	Append stage 3 card
		Reshuffle ALL cards at stage 3

Class Game_state:
	Graph
	Players
	Resources
	Stage - steps
		3-5 vs 6 players
	Market - cards shown
		Next card on deck light or dark
	Occupied cities
	Round - turn number
	
Class turn_order:
	Players

Events:

1 auction power plants
	If round 1 must purchase
	If cards > 3 must discard

2 buy resources

3 build generators
	If round 1 must buy


Update:
	Money
	Resources
	Cards
	Round
	Turn_order
	End_game - check



Each Player writes code that:

	Given:
		Player - self
		Game_state
		Event_number
	Returns:
		Legal action - include discard if more than 3 cards

