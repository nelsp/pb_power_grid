"""
Unit tests for Power Grid Game Engine
Tests cover all major functions with edge cases and boundary conditions
"""

import pytest
import copy
from game_engine import GameEngine, GameState, PAYMENT_TABLE, RESUPPLY_TABLES, STEP_2_THRESHOLDS
from Player_class import Player
from card import Card
import create_use_resources as res


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_cards():
    """Create sample power plant cards for testing"""
    # Card class takes a dictionary with keys: cost, resource, resource_cost, cities
    return [
        Card({'cost': 3, 'resource': 'oil', 'resource_cost': 2, 'cities': 1}),
        Card({'cost': 4, 'resource': 'coal', 'resource_cost': 2, 'cities': 1}),
        Card({'cost': 5, 'resource': 'oil&gas', 'resource_cost': 2, 'cities': 1}),
        Card({'cost': 6, 'resource': 'gas', 'resource_cost': 1, 'cities': 1}),
        Card({'cost': 7, 'resource': 'oil', 'resource_cost': 3, 'cities': 2}),
        Card({'cost': 8, 'resource': 'coal', 'resource_cost': 3, 'cities': 2}),
        Card({'cost': 9, 'resource': 'oil', 'resource_cost': 1, 'cities': 1}),
        Card({'cost': 10, 'resource': 'coal', 'resource_cost': 2, 'cities': 2}),
        Card({'cost': 11, 'resource': 'uranium', 'resource_cost': 1, 'cities': 2}),
        Card({'cost': 12, 'resource': 'oil&gas', 'resource_cost': 2, 'cities': 2}),
        Card({'cost': 13, 'resource': 'green', 'resource_cost': 0, 'cities': 1}),
        Card({'cost': 14, 'resource': 'gas', 'resource_cost': 2, 'cities': 2}),
        Card({'cost': 15, 'resource': 'coal', 'resource_cost': 2, 'cities': 3}),
        Card({'cost': 16, 'resource': 'oil', 'resource_cost': 2, 'cities': 3, 'type': 'light'}),  # Cost 16+ are light
    ]


@pytest.fixture
def sample_players():
    """Create sample players for testing"""
    # Player class only accepts name in __init__, initializes other fields automatically
    return [
        Player("Player0"),
        Player("Player1"),
        Player("Player2"),
        Player("Player3"),
    ]


@pytest.fixture
def sample_resources():
    """Create sample resource market for testing"""
    # Resource class needs: total_supply, start_allocation, capacity_list, name
    # Simplified capacity lists for testing
    coal_cl = [[1, [0, 0, 0, 0]], [2, [0, 0, 0, 0]], [3, [0, 0, 0, 0]], [4, [0, 0, 0, 0]],
               [5, [0, 0, 0, 0]], [6, [0, 0, 0, 0]], [7, [0, 0]], [8, [0, 0]], [9, [0, 0]]]
    gas_cl = [[1, [0, 0, 0, 0]], [2, [0, 0, 0, 0]], [3, [0, 0, 0, 0]], [4, [0, 0, 0, 0]],
              [5, [0, 0, 0, 0]], [6, [0, 0, 0, 0]], [7, [0, 0]], [8, [0, 0]], [9, [0, 0]]]
    oil_cl = [[1, [0, 0, 0, 0]], [2, [0, 0, 0, 0]], [3, [0, 0, 0, 0]], [4, [0, 0, 0, 0]],
              [5, [0, 0, 0, 0]], [6, [0, 0, 0, 0]], [7, [0, 0]], [8, [0, 0]], [9, [0, 0]]]
    uranium_cl = [[1, [0, 0, 0, 0]], [2, [0, 0, 0, 0]], [3, [0, 0, 0, 0]], [4, [0, 0, 0, 0]],
                  [5, [0, 0, 0, 0]], [6, [0, 0, 0, 0]], [7, [0, 0]], [8, [0, 0]], [9, [0, 0]]]

    coal = res.Resource(27, (2, 9), coal_cl, 'coal')
    coal.initialize_supply()
    gas = res.Resource(24, (3, 8), gas_cl, 'gas')
    gas.initialize_supply()
    oil = res.Resource(20, (3, 9), oil_cl, 'oil')
    oil.initialize_supply()
    uranium = res.Resource(12, (8, 9), uranium_cl, 'uranium')
    uranium.initialize_supply()

    return {
        'coal': coal,
        'oil': oil,
        'gas': gas,
        'uranium': uranium
    }


@pytest.fixture
def simple_board_graph():
    """Create a simple board graph for testing"""
    # Simple graph: A -- B -- C
    #               |    |
    #               D -- E
    graph = {
        ('region', 'A'): {('region', 'B'): 5, ('region', 'D'): 10},
        ('region', 'B'): {('region', 'A'): 5, ('region', 'C'): 7, ('region', 'E'): 8},
        ('region', 'C'): {('region', 'B'): 7},
        ('region', 'D'): {('region', 'A'): 10, ('region', 'E'): 6},
        ('region', 'E'): {('region', 'B'): 8, ('region', 'D'): 6}
    }
    return graph


@pytest.fixture
def game_engine(sample_players, sample_cards, sample_resources, simple_board_graph):
    """Create a basic game engine for testing"""
    current_market = sample_cards[:4]
    future_market = sample_cards[4:8]
    deck = sample_cards[8:]
    player_order = [0, 1, 2, 3]

    engine = GameEngine(
        players=sample_players,
        current_market=current_market,
        future_market=future_market,
        deck=deck,
        board_graph=simple_board_graph,
        resources=sample_resources,
        player_order=player_order,
        num_players=4,
        enable_logging=False
    )
    return engine


# ============================================================================
# GameState Tests
# ============================================================================

class TestGameState:
    """Test GameState class initialization and serialization"""

    def test_init(self, sample_players, sample_cards, sample_resources, simple_board_graph):
        """Test that GameState initializes correctly"""
        current_market = sample_cards[:4]
        future_market = sample_cards[4:8]
        deck = sample_cards[8:]
        player_order = [0, 1, 2, 3]

        state = GameState(
            players=sample_players,
            current_market=current_market,
            future_market=future_market,
            deck=deck,
            board_graph=simple_board_graph,
            resources=sample_resources,
            player_order=player_order
        )

        assert state.step == 1
        assert state.round_num == 1
        assert state.phase == 'determine_order'
        assert state.game_over is False
        assert state.step_3_triggered is False
        assert len(state.city_occupancy) == 5  # A, B, C, D, E
        assert all(len(occupants) == 0 for occupants in state.city_occupancy.values())

    def test_to_dict(self, game_engine):
        """Test that GameState serializes to dictionary correctly"""
        state_dict = game_engine.game_state.to_dict()

        assert 'players' in state_dict
        assert 'current_market' in state_dict
        assert 'future_market' in state_dict
        assert 'deck' in state_dict
        assert 'resources' in state_dict
        assert 'step' in state_dict
        assert 'round_num' in state_dict
        assert 'phase' in state_dict

        # Check that all values are serializable (basic types)
        assert isinstance(state_dict['step'], int)
        assert isinstance(state_dict['round_num'], int)
        assert isinstance(state_dict['phase'], str)
        assert isinstance(state_dict['players'], list)
        assert isinstance(state_dict['current_market'], list)


# ============================================================================
# Helper Function Tests
# ============================================================================

class TestDrawNextPlant:
    """Test draw_next_plant() function"""

    def test_normal_draw(self, game_engine):
        """Test drawing a normal plant from deck"""
        initial_deck_size = len(game_engine.game_state.deck)
        plant = game_engine.draw_next_plant()

        assert plant is not None
        assert len(game_engine.game_state.deck) == initial_deck_size - 1

    def test_empty_deck(self, game_engine):
        """Test drawing when deck is empty"""
        game_engine.game_state.deck = []
        plant = game_engine.draw_next_plant()

        assert plant is None

    def test_step_3_card_trigger(self, game_engine):
        """Test that drawing Step 3 card sets trigger and draws next card"""
        step_3_card = Card({'cost': 0, 'resource': 'stage three', 'resource_cost': 0, 'cities': 0})
        next_card = Card({'cost': 20, 'resource': 'coal', 'resource_cost': 2, 'cities': 3, 'type': 'light'})
        game_engine.game_state.deck = [step_3_card, next_card]

        plant = game_engine.draw_next_plant()

        assert game_engine.game_state.step_3_triggered is True
        assert plant == next_card

    def test_step_3_card_with_empty_deck_after(self, game_engine):
        """Test drawing Step 3 card when it's the last card"""
        step_3_card = Card({'cost': 0, 'resource': 'stage three', 'resource_cost': 0, 'cities': 0})
        game_engine.game_state.deck = [step_3_card]

        plant = game_engine.draw_next_plant()

        assert game_engine.game_state.step_3_triggered is True
        assert plant is None


class TestUpdateMarketAfterPurchase:
    """Test update_market_after_purchase() function"""

    def test_step_1_refill_current_market(self, game_engine, sample_cards):
        """Test market update in Step 1 with purchase from current market"""
        game_engine.game_state.step = 1
        # Remove one from current market to simulate purchase
        game_engine.game_state.current_market = sample_cards[:3]  # Only 3 cards
        game_engine.game_state.future_market = sample_cards[3:8]  # 5 cards
        game_engine.game_state.deck = sample_cards[8:12]

        game_engine.update_market_after_purchase()

        # Should have 4 in current, 5 in future (or less if deck exhausted)
        assert len(game_engine.game_state.current_market) == 4
        assert len(game_engine.game_state.future_market) == 5
        # Current market should have lowest cost cards
        if len(game_engine.game_state.current_market) > 0 and len(game_engine.game_state.future_market) > 0:
            assert max(c.cost for c in game_engine.game_state.current_market) <= min(c.cost for c in game_engine.game_state.future_market)

    def test_step_2_market_ordering(self, game_engine, sample_cards):
        """Test that Step 2 maintains proper market ordering"""
        game_engine.game_state.step = 2
        game_engine.game_state.current_market = [sample_cards[5], sample_cards[2], sample_cards[0]]  # Unordered
        game_engine.game_state.future_market = [sample_cards[7], sample_cards[6]]
        game_engine.game_state.deck = sample_cards[8:12]

        game_engine.update_market_after_purchase()

        # Check that current market is sorted
        current_costs = [c.cost for c in game_engine.game_state.current_market]
        assert current_costs == sorted(current_costs)

        # Check that future market is sorted
        future_costs = [c.cost for c in game_engine.game_state.future_market]
        assert future_costs == sorted(future_costs)

    def test_step_3_single_market(self, game_engine, sample_cards):
        """Test that Step 3 combines markets into single 6-card market"""
        game_engine.game_state.step = 3
        game_engine.game_state.current_market = sample_cards[:4]
        game_engine.game_state.future_market = sample_cards[4:9]
        game_engine.game_state.deck = sample_cards[9:12]

        game_engine.update_market_after_purchase()

        # Step 3 should have 6 cards in current market, 0 in future
        assert len(game_engine.game_state.current_market) <= 6
        assert len(game_engine.game_state.future_market) == 0

        # Should be sorted
        costs = [c.cost for c in game_engine.game_state.current_market]
        assert costs == sorted(costs)

    def test_empty_deck_handling(self, game_engine, sample_cards):
        """Test market update when deck is empty"""
        game_engine.game_state.step = 1
        game_engine.game_state.current_market = sample_cards[:2]
        game_engine.game_state.future_market = sample_cards[4:6]
        game_engine.game_state.deck = []  # Empty deck

        game_engine.update_market_after_purchase()

        # Should have whatever cards are available, properly split
        total_cards = len(game_engine.game_state.current_market) + len(game_engine.game_state.future_market)
        assert total_cards == 4  # Only the 4 we started with


class TestValidateResourcePurchase:
    """Test validate_resource_purchase() function"""

    def test_valid_purchase_single_plant(self, game_engine, sample_cards):
        """Test valid resource purchase for a plant that uses that resource"""
        player = game_engine.players[0]
        player.cards = [sample_cards[1]]  # Coal plant, uses 2 coal, powers 1 city
        player.resources = {'coal': 0, 'oil': 0, 'gas': 0, 'uranium': 0}

        # Should be able to buy 4 coal (2x capacity)
        assert game_engine.validate_resource_purchase(player, 'coal', 4) is True

    def test_invalid_purchase_no_plant(self, game_engine):
        """Test that player cannot buy resources without appropriate plant"""
        player = game_engine.players[0]
        player.cards = []

        assert game_engine.validate_resource_purchase(player, 'coal', 2) is False

    def test_invalid_purchase_wrong_resource(self, game_engine, sample_cards):
        """Test that player cannot buy resources for wrong type"""
        player = game_engine.players[0]
        player.cards = [sample_cards[1]]  # Coal plant

        # Cannot buy oil for a coal plant
        assert game_engine.validate_resource_purchase(player, 'oil', 2) is False

    def test_capacity_limit(self, game_engine, sample_cards):
        """Test that purchases respect capacity limits (2x resource cost)"""
        player = game_engine.players[0]
        player.cards = [sample_cards[1]]  # Coal plant, uses 2 coal
        player.resources = {'coal': 3, 'oil': 0, 'gas': 0, 'uranium': 0}

        # Capacity is 4 (2 * 2), currently has 3, should not be able to buy 2 more
        assert game_engine.validate_resource_purchase(player, 'coal', 2) is False
        # But should be able to buy 1
        assert game_engine.validate_resource_purchase(player, 'coal', 1) is True

    def test_hybrid_plant_oil(self, game_engine, sample_cards):
        """Test that hybrid oil/gas plant can buy oil"""
        player = game_engine.players[0]
        player.cards = [sample_cards[2]]  # Oil&gas plant, uses 2
        player.resources = {'coal': 0, 'oil': 0, 'gas': 0, 'uranium': 0}

        assert game_engine.validate_resource_purchase(player, 'oil', 4) is True

    def test_hybrid_plant_gas(self, game_engine, sample_cards):
        """Test that hybrid oil/gas plant can buy gas"""
        player = game_engine.players[0]
        player.cards = [sample_cards[2]]  # Oil&gas plant, uses 2
        player.resources = {'coal': 0, 'oil': 0, 'gas': 0, 'uranium': 0}

        assert game_engine.validate_resource_purchase(player, 'gas', 4) is True


class TestCalculateConnectionCost:
    """Test calculate_connection_cost() function"""

    def test_first_city_free(self, game_engine):
        """Test that first city has zero connection cost"""
        player = game_engine.players[0]
        player.generators = []

        cost = game_engine.calculate_connection_cost(0, 'A')
        assert cost == 0

    def test_direct_connection(self, game_engine):
        """Test connection cost for directly connected cities"""
        player = game_engine.players[0]
        player.generators = ['A']

        # A -> B costs 5 in our simple graph
        cost = game_engine.calculate_connection_cost(0, 'B')
        assert cost == 5

    def test_two_hop_connection(self, game_engine):
        """Test connection cost for cities requiring intermediate city"""
        player = game_engine.players[0]
        player.generators = ['A']

        # A -> B -> C costs 5 + 7 = 12
        cost = game_engine.calculate_connection_cost(0, 'C')
        assert cost == 12

    def test_shortest_path_from_multiple_cities(self, game_engine):
        """Test that shortest path is chosen when player has multiple cities"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']

        # From A: A->D = 10
        # From B: B->D->E = 8 + 6 = 14, but B->E = 8 direct
        # Should choose A->D = 10 or find better path
        cost = game_engine.calculate_connection_cost(0, 'D')
        assert cost == 10  # Direct from A


class TestCalculateCitiesPowered:
    """Test calculate_cities_powered() function"""

    def test_no_cities_connected(self, game_engine, sample_cards):
        """Test that player cannot power cities if not connected to any"""
        player = game_engine.players[0]
        player.generators = []
        player.cards = [sample_cards[1]]  # Coal plant, powers 1
        player.resources = {'coal': 10, 'oil': 0, 'gas': 0, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 0

    def test_green_plant(self, game_engine, sample_cards):
        """Test that ecological (green) plants always work"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[10]]  # Green plant, powers 1
        player.resources = {'coal': 0, 'oil': 0, 'gas': 0, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 1  # Can power 1 city with green plant

    def test_insufficient_resources(self, game_engine, sample_cards):
        """Test that plants without resources cannot power cities"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[1]]  # Coal plant, needs 2 coal
        player.resources = {'coal': 1, 'oil': 0, 'gas': 0, 'uranium': 0}  # Only 1 coal

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 0  # Cannot power any cities

    def test_sufficient_resources(self, game_engine, sample_cards):
        """Test that plants with sufficient resources can power cities"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[1]]  # Coal plant, needs 2 coal, powers 1
        player.resources = {'coal': 2, 'oil': 0, 'gas': 0, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 1

    def test_limited_by_connections(self, game_engine, sample_cards):
        """Test that cities powered is limited by cities connected"""
        player = game_engine.players[0]
        player.generators = ['A']  # Only 1 city
        player.cards = [sample_cards[7]]  # Coal plant, powers 2 cities
        player.resources = {'coal': 10, 'oil': 0, 'gas': 0, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 1  # Can only power 1 city (limited by connections)

    def test_multiple_plants(self, game_engine, sample_cards):
        """Test calculating power from multiple plants"""
        player = game_engine.players[0]
        player.generators = ['A', 'B', 'C']  # 3 cities
        player.cards = [
            sample_cards[1],   # Coal plant, needs 2 coal, powers 1
            sample_cards[10],  # Green plant, powers 1
        ]
        player.resources = {'coal': 2, 'oil': 0, 'gas': 0, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 2  # Coal plant + green plant

    def test_hybrid_plant_with_oil(self, game_engine, sample_cards):
        """Test hybrid oil/gas plant can use oil"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[2]]  # Oil&gas plant, needs 2, powers 1
        player.resources = {'coal': 0, 'oil': 2, 'gas': 0, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 1

    def test_hybrid_plant_with_gas(self, game_engine, sample_cards):
        """Test hybrid oil/gas plant can use gas"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[2]]  # Oil&gas plant, needs 2, powers 1
        player.resources = {'coal': 0, 'oil': 0, 'gas': 2, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 1

    def test_hybrid_plant_with_mixed(self, game_engine, sample_cards):
        """Test hybrid oil/gas plant can use combination"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[2]]  # Oil&gas plant, needs 2, powers 1
        player.resources = {'coal': 0, 'oil': 1, 'gas': 1, 'uranium': 0}

        cities = game_engine.calculate_cities_powered(player)
        assert cities == 1


class TestCheckStepTransitions:
    """Test check_step_transitions() function"""

    def test_step_1_to_2_trigger(self, game_engine):
        """Test transition from Step 1 to Step 2 when threshold reached"""
        game_engine.game_state.step = 1
        # For 4 players, threshold is 7 cities
        game_engine.players[0].generators = ['A', 'B', 'C', 'D', 'E'] + ['F', 'G']  # 7 cities

        game_engine.check_step_transitions(verbose=False)

        assert game_engine.game_state.step == 2

    def test_step_1_stays_below_threshold(self, game_engine):
        """Test that Step 1 remains if threshold not reached"""
        game_engine.game_state.step = 1
        game_engine.players[0].generators = ['A', 'B', 'C']  # 3 cities

        game_engine.check_step_transitions(verbose=False)

        assert game_engine.game_state.step == 1

    def test_step_2_to_3_trigger(self, game_engine, sample_cards):
        """Test transition from Step 2 to Step 3 when Step 3 card drawn"""
        game_engine.game_state.step = 2
        game_engine.game_state.step_3_triggered = True
        game_engine.game_state.current_market = sample_cards[:4]
        game_engine.game_state.future_market = sample_cards[4:8]

        game_engine.check_step_transitions(verbose=False)

        assert game_engine.game_state.step == 3
        # In Step 3, markets should be combined
        assert len(game_engine.game_state.future_market) == 0

    def test_step_2_stays_without_trigger(self, game_engine):
        """Test that Step 2 remains if Step 3 not triggered"""
        game_engine.game_state.step = 2
        game_engine.game_state.step_3_triggered = False

        game_engine.check_step_transitions(verbose=False)

        assert game_engine.game_state.step == 2


class TestCheckEndGame:
    """Test check_end_game() function"""

    def test_end_game_trigger(self, game_engine):
        """Test that game ends when player reaches 18 cities"""
        cities = ['city' + str(i) for i in range(18)]
        game_engine.players[0].generators = cities

        result = game_engine.check_end_game()

        assert result is True
        assert game_engine.game_state.game_over is True

    def test_end_game_not_triggered(self, game_engine):
        """Test that game continues with fewer than 18 cities"""
        game_engine.players[0].generators = ['A', 'B', 'C']

        result = game_engine.check_end_game()

        assert result is False
        assert game_engine.game_state.game_over is False


class TestDetermineWinner:
    """Test determine_winner() function"""

    def test_winner_by_cities_powered(self, game_engine, sample_cards):
        """Test that player with most cities powered wins"""
        # Player 0: 2 cities powered (has 2 green plants, 2 cities connected)
        game_engine.players[0].generators = ['A', 'B']
        game_engine.players[0].cards = [sample_cards[10], sample_cards[10]]  # 2 Green plants, each powers 1
        game_engine.players[0].money = 50

        # Player 1: 1 city powered (has 1 green plant, 1 city connected)
        game_engine.players[1].generators = ['C']
        game_engine.players[1].cards = [sample_cards[10]]  # Green, powers 1
        game_engine.players[1].money = 100

        winner = game_engine.determine_winner()
        assert winner == 0  # Player 0 wins despite less money

    def test_tie_breaker_money(self, game_engine, sample_cards):
        """Test that money is tie-breaker when cities powered are equal"""
        # Both players: 1 city powered
        game_engine.players[0].generators = ['A']
        game_engine.players[0].cards = [sample_cards[10]]  # Green, powers 1
        game_engine.players[0].money = 50

        game_engine.players[1].generators = ['B']
        game_engine.players[1].cards = [sample_cards[10]]  # Green, powers 1
        game_engine.players[1].money = 100

        winner = game_engine.determine_winner()
        assert winner == 1  # Player 1 wins with more money


# ============================================================================
# Phase Function Tests
# ============================================================================

class TestPhase1DetermineOrder:
    """Test phase_1_determine_order() function"""

    def test_order_by_cities(self, game_engine, sample_cards):
        """Test that players are ordered by number of cities (descending)"""
        game_engine.players[0].generators = ['A']
        game_engine.players[1].generators = ['B', 'C']
        game_engine.players[2].generators = ['D', 'E', 'F']
        game_engine.players[3].generators = []

        game_engine.phase_1_determine_order()

        # Order should be: P2 (3 cities), P1 (2 cities), P0 (1 city), P3 (0 cities)
        assert game_engine.game_state.player_order == [2, 1, 0, 3]

    def test_tie_breaker_largest_plant(self, game_engine, sample_cards):
        """Test that largest plant is tie-breaker for equal cities"""
        game_engine.players[0].generators = ['A']
        game_engine.players[0].cards = [sample_cards[3]]  # Cost 6

        game_engine.players[1].generators = ['B']
        game_engine.players[1].cards = [sample_cards[7]]  # Cost 10

        game_engine.phase_1_determine_order()

        # Order should be: P1 (larger plant), P0
        assert game_engine.game_state.player_order[0] == 1


class TestPhase5Bureaucracy:
    """Test phase_5_bureaucracy() function"""

    def test_payment_for_cities(self, game_engine, sample_cards):
        """Test that players receive correct payment for cities powered"""
        player = game_engine.players[0]
        player.generators = ['A', 'B']
        player.cards = [sample_cards[10]]  # Green plant, powers 1
        initial_money = player.money

        game_engine.phase_5_bureaucracy(verbose=False)

        # Should get paid for 1 city powered
        expected_payment = PAYMENT_TABLE[1]
        assert player.money == initial_money + expected_payment

    def test_resource_resupply(self, game_engine):
        """Test that resources are resupplied correctly"""
        # Deplete coal
        initial_coal = game_engine.game_state.resources['coal'].count
        game_engine.game_state.resources['coal'].buy_resource(10)

        game_engine.phase_5_bureaucracy(verbose=False)

        # Should resupply based on step and player count
        step_idx = game_engine.game_state.step - 1
        expected_resupply = RESUPPLY_TABLES['coal'][game_engine.num_players][step_idx]
        # Check that resources increased
        assert game_engine.game_state.resources['coal'].count > initial_coal - 10

    def test_step_1_market_update(self, game_engine, sample_cards):
        """Test that Step 1 moves highest future market plant to deck"""
        game_engine.game_state.step = 1
        game_engine.game_state.current_market = sample_cards[:4]
        game_engine.game_state.future_market = sample_cards[4:8]
        game_engine.game_state.deck = sample_cards[8:10]

        # Get the highest cost card from future market
        highest = max(game_engine.game_state.future_market, key=lambda c: c.cost)

        game_engine.phase_5_bureaucracy(verbose=False)

        # Highest should be in deck now (at the end)
        assert highest in game_engine.game_state.deck
        assert highest not in game_engine.game_state.future_market

    def test_step_3_market_update(self, game_engine, sample_cards):
        """Test that Step 3 removes smallest plant from game"""
        game_engine.game_state.step = 3
        game_engine.game_state.current_market = sample_cards[5:11]  # 6 cards
        game_engine.game_state.future_market = []
        game_engine.game_state.deck = sample_cards[11:13]

        smallest = min(game_engine.game_state.current_market, key=lambda c: c.cost)

        game_engine.phase_5_bureaucracy(verbose=False)

        # Smallest should be removed completely
        assert smallest not in game_engine.game_state.current_market
        assert smallest not in game_engine.game_state.deck


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for complete game scenarios"""

    def test_full_round_execution(self, game_engine, sample_cards):
        """Test that a full round executes without errors"""
        # Create simple strategies (mock)
        class SimpleStrategy:
            def choose_auction_move(self, player, game_state, available_plants, can_buy, is_first_round):
                if is_first_round and available_plants:
                    return {'action': 'buy', 'plant': available_plants[0], 'bid': available_plants[0].cost}
                return 'pass'

            def choose_resources(self, player, game_state, resources):
                return {}

            def choose_cities_to_build(self, player, game_state, is_first_round):
                if is_first_round:
                    return ['A']
                return []

        strategies = [SimpleStrategy() for _ in range(4)]

        # Execute one round
        game_engine.phase_1_determine_order()
        game_engine.phase_2_auction(strategies, verbose=False)
        game_engine.phase_3_buy_resources(strategies, verbose=False)
        game_engine.phase_4_build(strategies, verbose=False)
        game_engine.phase_5_bureaucracy(verbose=False)

        # Check that state is consistent
        assert game_engine.game_state.round_num == 1
        # All players should have bought a plant in first round
        assert all(len(p.cards) > 0 for p in game_engine.players)

    def test_money_never_negative(self, game_engine, sample_cards):
        """Test that player money never goes negative in any phase"""
        class AggressiveStrategy:
            def choose_auction_move(self, player, game_state, available_plants, can_buy, is_first_round):
                if available_plants:
                    # Try to bid more than we have
                    return {'action': 'buy', 'plant': available_plants[0], 'bid': 1000}
                return 'pass'

            def choose_resources(self, player, game_state, resources):
                # Try to buy maximum resources
                return {'coal': 100, 'oil': 100}

            def choose_cities_to_build(self, player, game_state, is_first_round):
                # Try to build everywhere
                return ['A', 'B', 'C', 'D', 'E']

        strategies = [AggressiveStrategy() for _ in range(4)]

        # Execute phases
        game_engine.phase_1_determine_order()
        game_engine.phase_2_auction(strategies, verbose=False)
        game_engine.phase_3_buy_resources(strategies, verbose=False)
        game_engine.phase_4_build(strategies, verbose=False)
        game_engine.phase_5_bureaucracy(verbose=False)

        # Verify no player has negative money
        for player in game_engine.players:
            assert player.money >= 0, f"Player has negative money: {player.money}"


# ============================================================================
# Run tests
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
