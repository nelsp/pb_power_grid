"""
Test Player Strategies for Power Grid
Each strategy implements methods to make game decisions
"""

import random


class RandomStrategy:
    """Random strategy: makes random legal moves"""
    
    def choose_auction_move(self, player, game_state, available_plants, can_buy, must_buy):
        """Choose a random plant to buy, or pass"""
        if must_buy and available_plants:
            # Find affordable plants
            affordable = [p for p in available_plants if player.money >= p.cost]
            if affordable:
                plant = random.choice(affordable)
                return {'action': 'buy', 'plant': plant, 'bid': plant.cost}
            else:
                return 'pass'  # Can't afford any
        elif can_buy and available_plants and random.random() > 0.3:
            # Find affordable plants
            affordable = [p for p in available_plants if player.money >= p.cost]
            if affordable:
                plant = random.choice(affordable)
                max_bid = min(plant.cost + 10, player.money)
                bid = random.randint(plant.cost, max_bid)
                return {'action': 'buy', 'plant': plant, 'bid': bid}
        return 'pass'
    
    def choose_resources(self, player, game_state, resources):
        """Buy random resources for owned plants"""
        purchases = {}
        
        for card in player.cards:
            if card.resource == 'green':
                continue  # No resources needed
            
            resource_type = card.resource
            if resource_type == 'nuclear':
                resource_type = 'uranium'
            elif resource_type == 'oil&gas':
                # Choose cheaper resource
                if 'oil' in resources and 'gas' in resources:
                    resource_type = random.choice(['oil', 'gas'])
                else:
                    resource_type = 'oil' if 'oil' in resources else 'gas'
            
            if resource_type in resources:
                # Buy up to capacity
                capacity = card.resource_cost * 2
                current = player.resources.get(resource_type, 0)
                needed = min(capacity - current, random.randint(0, capacity))
                if needed > 0:
                    purchases[resource_type] = purchases.get(resource_type, 0) + needed
        
        return purchases
    
    def choose_cities_to_build(self, player, game_state, must_build):
        """Choose random cities to build in"""
        if must_build:
            # Must build at least one
            available = self.get_available_cities(player, game_state)
            if available:
                return [random.choice(available)]
        else:
            # Optional building
            if random.random() > 0.2:  # 80% chance to build
                available = self.get_available_cities(player, game_state)
                if available:
                    num = random.randint(1, min(3, len(available)))
                    return random.sample(available, num)
        return []
    
    def get_available_cities(self, player, game_state):
        """Get cities player can build in"""
        available = []
        for city_name, occupancy in game_state.city_occupancy.items():
            position = len(occupancy)
            if position < game_state.step:
                available.append(city_name)
        return available


class GreedyStrategy:
    """Greedy strategy: tries to expand and power many cities"""
    
    def choose_auction_move(self, player, game_state, available_plants, can_buy, must_buy):
        """Buy plants that power many cities"""
        if not available_plants:
            return 'pass'
        
        # Filter to affordable plants
        affordable = [p for p in available_plants if player.money >= p.cost]
        if not affordable:
            return 'pass'
        
        if must_buy:
            # Choose plant that powers most cities
            best_plant = max(affordable, key=lambda p: p.cities)
            return {'action': 'buy', 'plant': best_plant, 'bid': best_plant.cost}
        
        if can_buy:
            # Prefer plants that power many cities
            affordable.sort(key=lambda p: p.cities, reverse=True)
            plant = affordable[0]
            bid = min(plant.cost + 5, player.money)
            return {'action': 'buy', 'plant': plant, 'bid': bid}
        
        return 'pass'
    
    def choose_resources(self, player, game_state, resources):
        """Buy resources for all owned plants"""
        purchases = {}
        
        for card in player.cards:
            if card.resource == 'green':
                continue
            
            resource_type = card.resource
            if resource_type == 'nuclear':
                resource_type = 'uranium'
            elif resource_type == 'oil&gas':
                # Choose cheaper resource (simplified: just use oil)
                resource_type = 'oil'
            
            if resource_type in resources:
                capacity = card.resource_cost * 2
                current = player.resources.get(resource_type, 0)
                needed = capacity - current
                if needed > 0:
                    purchases[resource_type] = purchases.get(resource_type, 0) + needed
        
        return purchases
    
    def choose_cities_to_build(self, player, game_state, must_build):
        """Build in as many cities as affordable"""
        available = self.get_available_cities(player, game_state)
        if not available:
            return []
        
        cities_to_build = []
        budget = player.money
        
        for city_name in available:
            if budget <= 0:
                break
            
            position = len(game_state.city_occupancy[city_name])
            building_cost = [10, 15, 20][position] if position < 3 else 999
            connection_cost = self.estimate_connection_cost(player, city_name, game_state)
            total_cost = building_cost + connection_cost
            
            if total_cost <= budget and position < game_state.step + 1:
                cities_to_build.append(city_name)
                budget -= total_cost
        
        if must_build and not cities_to_build and available:
            # Must build at least one, choose cheapest
            city = min(available, key=lambda c: [10, 15, 20][len(game_state.city_occupancy[c])])
            cities_to_build = [city]
        
        return cities_to_build
    
    def get_available_cities(self, player, game_state):
        """Get cities player can build in"""
        available = []
        for city_name, occupancy in game_state.city_occupancy.items():
            position = len(occupancy)
            if position < game_state.step:
                available.append(city_name)
        return available
    
    def estimate_connection_cost(self, player, city_name, game_state):
        """Estimate connection cost (simplified)"""
        if not player.generators:
            return 0
        return 10  # Simplified estimate


class ConservativeStrategy:
    """Conservative strategy: saves money, builds slowly"""
    
    def choose_auction_move(self, player, game_state, available_plants, can_buy, must_buy):
        """Buy only cheap plants"""
        if not available_plants:
            return 'pass'
        
        # Filter to affordable plants
        affordable = [p for p in available_plants if player.money >= p.cost]
        if not affordable:
            return 'pass'
        
        if must_buy:
            # Choose cheapest affordable
            cheapest = min(affordable, key=lambda p: p.cost)
            return {'action': 'buy', 'plant': cheapest, 'bid': cheapest.cost}
        
        if can_buy:
            # Only buy if we have enough money left (keep reserve)
            reserve = 20
            affordable_reserve = [p for p in affordable if p.cost <= player.money - reserve]
            if affordable_reserve:
                cheapest = min(affordable_reserve, key=lambda p: p.cost)
                return {'action': 'buy', 'plant': cheapest, 'bid': cheapest.cost}
        
        return 'pass'
    
    def choose_resources(self, player, game_state, resources):
        """Buy minimal resources"""
        purchases = {}
        
        for card in player.cards:
            if card.resource == 'green':
                continue
            
            resource_type = card.resource
            if resource_type == 'nuclear':
                resource_type = 'uranium'
            elif resource_type == 'oil&gas':
                resource_type = 'oil'
            
            if resource_type in resources:
                # Only buy what's needed for one production
                current = player.resources.get(resource_type, 0)
                needed = card.resource_cost - current
                if needed > 0:
                    purchases[resource_type] = purchases.get(resource_type, 0) + needed
        
        return purchases
    
    def choose_cities_to_build(self, player, game_state, must_build):
        """Build only if can afford easily"""
        if not must_build and player.money < 30:
            return []  # Save money
        
        available = self.get_available_cities(player, game_state)
        if not available:
            return []
        
        # Build in cheapest city
        if must_build:
            city = min(available, key=lambda c: [10, 15, 20][len(game_state.city_occupancy[c])])
            return [city]
        elif player.money >= 30:
            # Build one city if we have money
            city = min(available, key=lambda c: [10, 15, 20][len(game_state.city_occupancy[c])])
            return [city]
        
        return []
    
    def get_available_cities(self, player, game_state):
        """Get cities player can build in"""
        available = []
        for city_name, occupancy in game_state.city_occupancy.items():
            position = len(occupancy)
            if position < game_state.step:
                available.append(city_name)
        return available


class BalancedStrategy:
    """Balanced strategy: tries to balance expansion and efficiency"""
    
    def choose_auction_move(self, player, game_state, available_plants, can_buy, must_buy):
        """Buy efficient plants (cities per cost)"""
        if not available_plants:
            return 'pass'
        
        # Filter to affordable plants
        affordable = [p for p in available_plants if player.money >= p.cost]
        if not affordable:
            return 'pass'
        
        if must_buy:
            # Choose efficient plant
            best_plant = max(affordable, key=lambda p: p.cities / float(p.cost))
            return {'action': 'buy', 'plant': best_plant, 'bid': best_plant.cost}
        
        if can_buy:
            # Prefer efficient plants we can afford
            best_plant = max(affordable, key=lambda p: p.cities / float(p.cost))
            bid = min(best_plant.cost + 3, player.money)
            return {'action': 'buy', 'plant': best_plant, 'bid': bid}
        
        return 'pass'
    
    def choose_resources(self, player, game_state, resources):
        """Buy resources efficiently"""
        purchases = {}
        
        for card in player.cards:
            if card.resource == 'green':
                continue
            
            resource_type = card.resource
            if resource_type == 'nuclear':
                resource_type = 'uranium'
            elif resource_type == 'oil&gas':
                # Choose cheaper resource
                resource_type = 'oil'
            
            if resource_type in resources:
                # Buy to 1.5x capacity (safety margin but not full)
                capacity = card.resource_cost * 2
                target = int(card.resource_cost * 1.5)
                current = player.resources.get(resource_type, 0)
                needed = min(target - current, capacity - current)
                if needed > 0:
                    purchases[resource_type] = purchases.get(resource_type, 0) + needed
        
        return purchases
    
    def choose_cities_to_build(self, player, game_state, must_build):
        """Build strategically"""
        available = self.get_available_cities(player, game_state)
        if not available:
            return []
        
        # Build 1-2 cities per turn
        if must_build:
            city = min(available, key=lambda c: [10, 15, 20][len(game_state.city_occupancy[c])])
            return [city]
        else:
            # Build if we have good income potential
            if len(player.generators) < 10:
                # Early game: build more
                num = min(2, len(available))
                return random.sample(available, num) if available else []
            else:
                # Late game: be more selective
                if random.random() > 0.5:
                    return [random.choice(available)]
        
        return []
    
    def get_available_cities(self, player, game_state):
        """Get cities player can build in"""
        available = []
        for city_name, occupancy in game_state.city_occupancy.items():
            position = len(occupancy)
            if position < game_state.step:
                available.append(city_name)
        return available

