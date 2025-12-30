"""
Power Grid Game Engine
Implements the complete game logic according to Power Grid Deluxe rules
"""

import random
import copy
from card import Card
import create_use_resources as res


# Payment table: cities powered -> Elektro earned
PAYMENT_TABLE = {
    0: 10, 1: 22, 2: 33, 3: 44, 4: 54, 5: 64, 6: 73, 7: 82, 8: 90, 9: 98, 10: 105,
    11: 112, 12: 118, 13: 124, 14: 129, 15: 134, 16: 138, 17: 142, 18: 145, 19: 148, 20: 150
}

# Resource resupply tables [Step1, Step2, Step3] for each number of players
RESUPPLY_TABLES = {
    'coal': {2: [2, 6, 2], 3: [2, 6, 2], 4: [3, 7, 4], 5: [3, 8, 4], 6: [5, 10, 5]},
    'gas': {2: [2, 3, 5], 3: [2, 3, 5], 4: [3, 4, 5], 5: [3, 5, 7], 6: [4, 6, 8]},
    'oil': {2: [2, 2, 3], 3: [2, 2, 3], 4: [3, 3, 4], 5: [4, 3, 5], 6: [4, 5, 6]},
    'uranium': {2: [1, 1, 2], 3: [1, 1, 2], 4: [1, 2, 2], 5: [2, 3, 3], 6: [2, 3, 4]}
}

# Step transition thresholds (number of cities to trigger Step 2)
STEP_2_THRESHOLDS = {2: 7, 3: 7, 4: 7, 5: 6, 6: 5}


class GameState:
    """Represents the current state of the game"""
    
    def __init__(self, players, current_market, future_market, deck, board_graph, 
                 resources, player_order, step=1, round_num=1, phase='determine_order'):
        self.players = players  # List of Player objects
        self.current_market = current_market  # List of Card objects (4 plants)
        self.future_market = future_market  # List of Card objects (4-5 plants)
        self.deck = deck  # List of Card objects
        self.board_graph = board_graph  # Dictionary graph of cities
        self.resources = resources  # Dict of Resource objects {'coal': Resource, ...}
        self.player_order = player_order  # List of player indices in order
        self.step = step  # 1, 2, or 3
        self.round_num = round_num
        self.phase = phase  # determine_order, auction, buy_resources, build, bureaucracy
        self.step_3_triggered = False
        self.game_over = False
        self.winner = None
        
        # Track city occupancy: {city_name: [player_indices]}
        self.city_occupancy = {}
        for city_node in board_graph:
            city_name = city_node[1] if isinstance(city_node, tuple) else city_node
            self.city_occupancy[city_name] = []


class GameEngine:
    """Main game engine for Power Grid"""
    
    def __init__(self, players, current_market, future_market, deck, board_graph, resources, player_order, num_players):
        self.num_players = num_players
        self.players = players
        self.game_state = GameState(
            players=players,
            current_market=sorted(current_market, key=lambda c: c.cost),
            future_market=sorted(future_market, key=lambda c: c.cost),
            deck=deck,
            board_graph=board_graph,
            resources=resources,
            player_order=player_order,
            step=1,
            round_num=1,
            phase='determine_order'
        )
    
    def run_game(self, player_strategies, verbose=True, max_rounds=20):
        """Run the complete game
        
        Args:
            player_strategies: List of strategy objects for each player
            verbose: Whether to print game progress
            max_rounds: Maximum number of rounds to play (default: 20)
        """
        if verbose:
            print("=" * 60)
            print("POWER GRID - Game Starting")
            print("=" * 60)
        
        while not self.game_state.game_over:
            # Check if we've reached max rounds
            if self.game_state.round_num > max_rounds:
                self.game_state.game_over = True
                if verbose:
                    print(f"\nMaximum rounds ({max_rounds}) reached.")
                break
            
            if verbose:
                print("\n" + "=" * 60)
                print(f"Round {self.game_state.round_num} - Step {self.game_state.step}")
                print("=" * 60)
            
            # Phase 1: Determine Player Order
            self.phase_1_determine_order()
            if verbose:
                print(f"Player Order: {[f'P{p}' for p in self.game_state.player_order]}")
            
            # Phase 2: Auction Power Plants
            self.phase_2_auction(player_strategies, verbose)
            
            # Phase 3: Buy Resources
            self.phase_3_buy_resources(player_strategies, verbose)
            
            # Phase 4: Build Generators
            self.phase_4_build(player_strategies, verbose)
            
            # Check for end game after building
            if self.check_end_game():
                break
            
            # Phase 5: Bureaucracy
            self.phase_5_bureaucracy(verbose)
            
            # Check step transitions
            self.check_step_transitions(verbose)
            
            # Print account balances at end of round
            if verbose:
                print(f"\nAccount Balances (End of Round {self.game_state.round_num}):")
                for player_idx in self.game_state.player_order:
                    player = self.players[player_idx]
                    print(f"  Player {player_idx}: {player.money}E")
            
            # Prepare for next round
            self.game_state.round_num += 1
            self.game_state.phase = 'determine_order'
        
        # Game over - determine winner
        winner_idx = self.determine_winner()
        if verbose:
            print("\n" + "=" * 60)
            print("GAME OVER")
            if self.game_state.round_num > max_rounds:
                print(f"Maximum rounds ({max_rounds}) reached.")
            print("=" * 60)
            print(f"Winner: Player {winner_idx}")
            self.print_final_scores(verbose)
        
        return winner_idx
    
    def phase_1_determine_order(self):
        """Phase 1: Determine player order based on cities connected"""
        # Sort by cities connected (descending), then by largest plant (descending)
        def sort_key(player_idx):
            player = self.players[player_idx]
            cities_count = len(player.generators)
            largest_plant = max([card.cost for card in player.cards] if player.cards else [0])
            return (-cities_count, -largest_plant)  # Negative for descending
        
        self.game_state.player_order = sorted(self.game_state.player_order, key=sort_key)
        self.game_state.phase = 'auction'
    
    def phase_2_auction(self, player_strategies, verbose):
        """Phase 2: Auction power plants"""
        players_who_bought = set()
        
        # First round: all players must buy
        is_first_round = (self.game_state.round_num == 1)
        
        # Continue until all players have had a chance to buy or pass
        auction_round = 0
        max_auction_rounds = len(self.players) * 2  # Safety limit
        
        while auction_round < max_auction_rounds:
            auction_round += 1
            any_action = False
            
            for player_idx in self.game_state.player_order:
                if player_idx in players_who_bought:
                    continue  # Already bought this round
                
                player = self.players[player_idx]
                strategy = player_strategies[player_idx]
                
                # Get available plants (current market only)
                available_plants = [card for card in self.game_state.current_market]
                
                # Check if player can buy (has < 3 plants, or can replace)
                can_buy = len(player.cards) < 3
                if len(player.cards) == 3:
                    # Can only buy if new plant is larger than smallest owned
                    smallest_owned = min([card.cost for card in player.cards])
                    available_plants = [p for p in available_plants if p.cost > smallest_owned]
                    can_buy = len(available_plants) > 0
                
                if not available_plants and not is_first_round:
                    continue  # No plants available, skip
                
                # Get player's move
                move = strategy.choose_auction_move(
                    player, self.game_state, available_plants, can_buy, is_first_round
                )
                
                if move is None or move == 'pass':
                    if not is_first_round:
                        continue  # Pass
                    else:
                        # First round: must buy, choose cheapest available
                        if available_plants:
                            move = {'action': 'buy', 'plant': available_plants[0], 'bid': available_plants[0].cost}
                        else:
                            continue
                
                if move.get('action') == 'buy':
                    plant = move['plant']
                    bid = move.get('bid', plant.cost)
                    
                    # Validate bid
                    if bid < plant.cost:
                        bid = plant.cost
                    if bid > player.money:
                        if verbose:
                            print(f"Player {player_idx}: Invalid bid {bid}E (only has {player.money}E)")
                        continue
                    
                    # Execute purchase
                    player.cards.append(plant)
                    player.update_money(-bid)
                    
                    # Remove plant from market
                    self.game_state.current_market.remove(plant)
                    
                    # If player has > 3 plants, discard smallest
                    if len(player.cards) > 3:
                        player.cards.sort(key=lambda c: c.cost)
                        discarded = player.cards.pop(0)
                        if verbose:
                            print(f"Player {player_idx}: Discarded plant {discarded.cost}")
                    
                    # Add new plant to market
                    self.update_market_after_purchase()
                    
                    players_who_bought.add(player_idx)
                    any_action = True
                    
                    if verbose:
                        print(f"Player {player_idx} bought plant {plant.cost} for {bid}E")
            
            # Check if all players have passed (except first round)
            if not is_first_round and not any_action and len(players_who_bought) == 0:
                # Europe rule: remove smallest plant
                if self.game_state.current_market:
                    smallest = min(self.game_state.current_market, key=lambda c: c.cost)
                    self.game_state.current_market.remove(smallest)
                    if verbose:
                        print(f"All players passed - removed plant {smallest.cost}")
                    self.update_market_after_purchase()
                break
            
            # Check if all players have bought (first round requirement)
            if is_first_round and len(players_who_bought) == len(self.players):
                break
        
        self.game_state.phase = 'buy_resources'
    
    def draw_next_plant(self):
        """Draw next plant from deck, handling Step 3 card
        
        In Steps 1 & 2, only draws dark cards (cost < 16).
        In Step 3, draws any card.
        """
        if not self.game_state.deck:
            return None
        
        # In Steps 1 & 2, only draw dark cards (cost < 16)
        if self.game_state.step < 3:
            # Look through deck for a dark card
            checked = 0
            max_checks = len(self.game_state.deck)
            skipped_cards = []
            
            while checked < max_checks and self.game_state.deck:
                plant = self.game_state.deck.pop(0)
                checked += 1
                
                # Check for Step 3 card
                if hasattr(plant, 'resource') and plant.resource == 'stage three':
                    self.game_state.step_3_triggered = True
                    continue  # Skip Step 3 card
                
                # If dark card (cost < 16), return it
                if plant.cost < 16:
                    # Put skipped light cards back at the end
                    if skipped_cards:
                        self.game_state.deck.extend(skipped_cards)
                    return plant
                else:
                    # Light card - save to put back later
                    skipped_cards.append(plant)
            
            # No dark card found - put skipped cards back
            if skipped_cards:
                self.game_state.deck.extend(skipped_cards)
            return None
        
        # Step 3: draw any card
        plant = self.game_state.deck.pop(0)
        # Check for Step 3 card
        if hasattr(plant, 'resource') and plant.resource == 'stage three':
            self.game_state.step_3_triggered = True
            if self.game_state.deck:
                return self.game_state.deck.pop(0)
            return None
        return plant
    
    def update_market_after_purchase(self):
        """Update power plant market after a purchase"""
        # If in Step 3, market should have 6 plants total (no separation)
        if self.game_state.step == 3:
            # Combine markets and keep 6 smallest
            all_plants = sorted(self.game_state.current_market + self.game_state.future_market, key=lambda c: c.cost)
            # Fill from deck if needed
            while len(all_plants) < 6:
                new_plant = self.draw_next_plant()
                if new_plant:
                    all_plants.append(new_plant)
                else:
                    break
            all_plants.sort(key=lambda c: c.cost)
            # Keep only 6 smallest
            if len(all_plants) > 6:
                # Remove excess (largest)
                excess = all_plants[6:]
                self.game_state.deck.extend(excess)
                all_plants = all_plants[:6]
            self.game_state.current_market = all_plants
            self.game_state.future_market = []
        else:
            # Steps 1 & 2: Maintain 4 current + 4-5 future
            # Fill from deck if needed
            while len(self.game_state.current_market) < 4:
                new_plant = self.draw_next_plant()
                if new_plant:
                    self.game_state.current_market.append(new_plant)
                else:
                    break
            
            while len(self.game_state.future_market) < 4 and self.game_state.step < 3:
                new_plant = self.draw_next_plant()
                if new_plant:
                    self.game_state.future_market.append(new_plant)
                else:
                    break
            
            # Sort markets
            self.game_state.current_market.sort(key=lambda c: c.cost)
            self.game_state.future_market.sort(key=lambda c: c.cost)
            
            # Move largest from future to bottom of deck (Steps 1 & 2)
            if self.game_state.future_market and self.game_state.step < 3:
                largest = max(self.game_state.future_market, key=lambda c: c.cost)
                self.game_state.future_market.remove(largest)
                self.game_state.deck.append(largest)
    
    def phase_3_buy_resources(self, player_strategies, verbose):
        """Phase 3: Buy resources (reverse player order)"""
        # Reverse order
        buy_order = list(reversed(self.game_state.player_order))
        
        for player_idx in buy_order:
            player = self.players[player_idx]
            strategy = player_strategies[player_idx]
            
            # Get player's resource purchase decision
            purchases = strategy.choose_resources(player, self.game_state, self.game_state.resources)
            
            if purchases:
                for resource_type, amount in purchases.items():
                    if amount > 0 and resource_type in self.game_state.resources:
                        # Validate purchase
                        if self.validate_resource_purchase(player, resource_type, amount):
                            resource = self.game_state.resources[resource_type]
                            purchase_result = resource.buy_resource(amount)
                            if isinstance(purchase_result, tuple):
                                cost = purchase_result[1]
                                player.update_money(-cost)
                                player.resources[resource_type] += amount
                                if verbose:
                                    print(f"Player {player_idx} bought {amount} {resource_type} for {cost}E")
        
        self.game_state.phase = 'build'
    
    def validate_resource_purchase(self, player, resource_type, amount):
        """Validate that player can buy this resource"""
        # Check if player owns plants using this resource type
        has_plant = False
        total_capacity = 0
        
        for card in player.cards:
            if card.resource == resource_type:
                has_plant = True
                total_capacity += card.resource_cost * 2  # Can store 2x capacity
            elif card.resource == 'oil&gas' and resource_type in ['oil', 'gas']:
                has_plant = True
                total_capacity += card.resource_cost * 2  # Hybrid: total capacity
        
        if not has_plant:
            return False
        
        # Check capacity
        current_amount = player.resources.get(resource_type, 0)
        if current_amount + amount > total_capacity:
            return False
        
        return True
    
    def phase_4_build(self, player_strategies, verbose):
        """Phase 4: Build generators (reverse player order)"""
        # Reverse order
        build_order = list(reversed(self.game_state.player_order))
        
        # First round: all players must build at least one city
        is_first_round = (self.game_state.round_num == 1)
        
        for player_idx in build_order:
            player = self.players[player_idx]
            strategy = player_strategies[player_idx]
            
            # Get cities to build in
            cities_to_build = strategy.choose_cities_to_build(
                player, self.game_state, is_first_round
            )
            
            if cities_to_build:
                for city_name in cities_to_build:
                    if city_name in self.game_state.city_occupancy:
                        # Calculate cost
                        position = len(self.game_state.city_occupancy[city_name])
                        building_cost = [10, 15, 20][position] if position < 3 else 999
                        connection_cost = self.calculate_connection_cost(
                            player_idx, city_name
                        )
                        total_cost = building_cost + connection_cost
                        
                        # Check if affordable and valid
                        # Step 1: position < 1 (1 player), Step 2: position < 2 (2 players), Step 3: position < 3 (3 players)
                        if player.money >= total_cost and position < self.game_state.step:
                            player.update_money(-total_cost)
                            player.generators.append(city_name)
                            self.game_state.city_occupancy[city_name].append(player_idx)
                            
                            if verbose:
                                print(f"Player {player_idx} built in {city_name} for {total_cost}E (building: {building_cost}E, connection: {connection_cost}E)")
                        
                        # Check if any plant should be removed (plant number <= cities)
                        self.remove_plants_below_city_count(player_idx)
        
        self.game_state.phase = 'bureaucracy'
    
    def calculate_connection_cost(self, player_idx, target_city):
        """Calculate shortest path connection cost"""
        player = self.players[player_idx]
        
        if not player.generators:
            return 0  # First city is free
        
        # Find shortest path from any existing city to target
        min_cost = float('inf')
        
        # Convert graph format
        graph = {}
        for node1, connections in self.game_state.board_graph.items():
            city1 = node1[1] if isinstance(node1, tuple) else node1
            graph[city1] = {}
            for node2, cost in connections.items():
                city2 = node2[1] if isinstance(node2, tuple) else node2
                graph[city1][city2] = cost
        
        # Simple shortest path (Dijkstra-like, simplified)
        for start_city in player.generators:
            if start_city in graph and target_city in graph:
                # Direct connection
                if target_city in graph.get(start_city, {}):
                    cost = graph[start_city][target_city]
                    min_cost = min(min_cost, cost)
                else:
                    # Try 2-hop paths (simplified)
                    for intermediate in graph.get(start_city, {}):
                        if target_city in graph.get(intermediate, {}):
                            cost = graph[start_city][intermediate] + graph[intermediate][target_city]
                            min_cost = min(min_cost, cost)
        
        # If no path found, use a default high cost
        if min_cost == float('inf'):
            min_cost = 50  # Default high cost
        
        return int(min_cost)
    
    def remove_plants_below_city_count(self, player_idx):
        """Remove plants from market if plant number <= any player's city count"""
        player = self.players[player_idx]
        city_count = len(player.generators)
        
        # Check all players for max city count
        max_cities = max([len(p.generators) for p in self.players])
        
        # Check current market
        to_remove = []
        for plant in self.game_state.current_market:
            if plant.cost <= max_cities:
                to_remove.append(plant)
        
        for plant in to_remove:
            self.game_state.current_market.remove(plant)
            new_plant = self.draw_next_plant()
            if new_plant:
                self.game_state.current_market.append(new_plant)
        
        self.game_state.current_market.sort(key=lambda c: c.cost)
    
    def phase_5_bureaucracy(self, verbose):
        """Phase 5: Bureaucracy - earn money, resupply, update market"""
        # 1. Earn money based on cities powered (and consume resources)
        for player_idx, player in enumerate(self.players):
            cities_powered = self.calculate_cities_powered(player)
            # Consume resources to power cities
            self.consume_resources_for_power(player, cities_powered)
            payment = PAYMENT_TABLE.get(cities_powered, 0)
            player.update_money(payment)
            if verbose:
                print(f"Player {player_idx} powered {cities_powered} cities, earned {payment}E")
        
        # 2. Resupply resources
        step_idx = self.game_state.step - 1
        for resource_type, resource in self.game_state.resources.items():
            if resource_type in RESUPPLY_TABLES:
                resupply_amount = RESUPPLY_TABLES[resource_type][self.num_players][step_idx]
                resource.resupply(resupply_amount)
                if verbose:
                    print(f"Resupplied {resupply_amount} {resource_type}")
        
        # 3. Update power plant market (Steps 1 & 2 only)
        if self.game_state.step < 3:
            if self.game_state.future_market:
                largest = max(self.game_state.future_market, key=lambda c: c.cost)
                self.game_state.future_market.remove(largest)
                self.game_state.deck.append(largest)
            
            # Add new plant to future market (Steps 1 & 2: only dark cards)
            if len(self.game_state.future_market) < 5:
                new_plant = self.draw_next_plant()
                if new_plant:
                    self.game_state.future_market.append(new_plant)
                    self.game_state.future_market.sort(key=lambda c: c.cost)
        
        self.game_state.phase = 'determine_order'
    
    def calculate_cities_powered(self, player):
        """Calculate how many cities a player can power (without consuming resources)"""
        cities_connected = len(player.generators)
        
        # Calculate total power from plants with resources
        total_power = 0
        
        for card in player.cards:
            if card.resource == 'green':
                # Ecological plants always work
                total_power += card.cities
            elif card.resource in ['coal', 'gas', 'oil', 'uranium']:
                # Check if player has enough resources
                resource_type = card.resource
                if resource_type == 'nuclear':
                    resource_type = 'uranium'
                available = player.resources.get(resource_type, 0)
                if available >= card.resource_cost:
                    total_power += card.cities
            elif card.resource == 'oil&gas':
                # Hybrid: can use oil or gas
                oil_available = player.resources.get('oil', 0)
                gas_available = player.resources.get('gas', 0)
                if oil_available + gas_available >= card.resource_cost:
                    total_power += card.cities
        
        # Can only power as many cities as connected
        return min(cities_connected, total_power)
    
    def consume_resources_for_power(self, player, cities_to_power):
        """Consume resources to power the specified number of cities"""
        if cities_to_power == 0:
            return
        
        # Sort plants by efficiency (cities per resource cost), prefer green
        plants_to_use = []
        for card in player.cards:
            if card.resource == 'green':
                plants_to_use.append((card, 'green', 0))
            else:
                resource_type = card.resource
                if resource_type == 'nuclear':
                    resource_type = 'uranium'
                available = player.resources.get(resource_type, 0) if resource_type != 'oil&gas' else (
                    player.resources.get('oil', 0) + player.resources.get('gas', 0)
                )
                if available >= card.resource_cost:
                    plants_to_use.append((card, resource_type, card.resource_cost))
        
        # Sort by efficiency (green first, then by cities/cost)
        plants_to_use.sort(key=lambda x: (x[1] != 'green', -x[0].cities / float(x[2] + 1)))
        
        # Use plants to power cities
        cities_powered = 0
        for card, resource_type, cost in plants_to_use:
            if cities_powered >= cities_to_power:
                break
            
            if resource_type == 'green':
                cities_powered += card.cities
            else:
                # Consume resources
                if resource_type == 'oil&gas':
                    # Use cheaper resource first
                    oil_avail = player.resources.get('oil', 0)
                    gas_avail = player.resources.get('gas', 0)
                    if oil_avail >= cost:
                        player.resources['oil'] -= cost
                        self.game_state.resources['oil'].use_resource(cost)
                    elif gas_avail >= cost:
                        player.resources['gas'] -= cost
                        self.game_state.resources['gas'].use_resource(cost)
                    else:
                        # Use combination
                        remaining = cost
                        if oil_avail > 0:
                            use_oil = min(remaining, oil_avail)
                            player.resources['oil'] -= use_oil
                            self.game_state.resources['oil'].use_resource(use_oil)
                            remaining -= use_oil
                        if remaining > 0:
                            player.resources['gas'] -= remaining
                            self.game_state.resources['gas'].use_resource(remaining)
                else:
                    player.resources[resource_type] -= cost
                    self.game_state.resources[resource_type].use_resource(cost)
                
                cities_powered += card.cities
    
    def check_step_transitions(self, verbose):
        """Check and handle step transitions"""
        # Step 1 -> Step 2
        if self.game_state.step == 1:
            threshold = STEP_2_THRESHOLDS.get(self.num_players, 7)
            for player in self.players:
                if len(player.generators) >= threshold:
                    self.game_state.step = 2
                    if verbose:
                        print(f"\nSTEP 2 TRIGGERED! (Player has {len(player.generators)} cities)")
                    # Europe: remove smallest plant, don't replace
                    if self.game_state.current_market:
                        smallest = min(self.game_state.current_market, key=lambda c: c.cost)
                        self.game_state.current_market.remove(smallest)
                        self.update_market_after_purchase()
                    break
        
        # Step 2 -> Step 3
        if self.game_state.step == 2 and self.game_state.step_3_triggered:
            self.game_state.step = 3
            if verbose:
                print("\nSTEP 3 TRIGGERED!")
            # Remove smallest plant
            if self.game_state.current_market:
                smallest = min(self.game_state.current_market, key=lambda c: c.cost)
                self.game_state.current_market.remove(smallest)
            # Combine markets (Step 3 has 6 plants total)
            all_plants = self.game_state.current_market + self.game_state.future_market
            all_plants.sort(key=lambda c: c.cost)
            self.game_state.current_market = all_plants[:6]
            self.game_state.future_market = []
    
    def check_end_game(self):
        """Check if game should end (18+ cities)"""
        for player in self.players:
            if len(player.generators) >= 18:
                self.game_state.game_over = True
                return True
        return False
    
    def determine_winner(self):
        """Determine winner: most cities powered, tie-breaker: most money"""
        best_players = []
        best_powered = -1
        
        for player_idx, player in enumerate(self.players):
            cities_powered = self.calculate_cities_powered(player)
            if cities_powered > best_powered:
                best_powered = cities_powered
                best_players = [(player_idx, player)]
            elif cities_powered == best_powered:
                best_players.append((player_idx, player))
        
        # Tie-breaker: most money
        if len(best_players) > 1:
            best_players.sort(key=lambda x: x[1].money, reverse=True)
        
        return best_players[0][0]
    
    def print_final_scores(self, verbose):
        """Print final scores for all players"""
        if not verbose:
            return
        
        print("\nFinal Scores:")
        for player_idx, player in enumerate(self.players):
            cities_powered = self.calculate_cities_powered(player)
            cities_connected = len(player.generators)
            print(f"Player {player_idx}: {cities_powered} cities powered, {cities_connected} cities connected, {player.money}E")

