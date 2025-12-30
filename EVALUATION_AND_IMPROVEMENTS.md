# Power Grid Simulation Evaluation & Improvement Suggestions

## Executive Summary

This evaluation compares the current Python simulation code against the official Power Grid Deluxe rules. The codebase provides a good foundation with basic classes and data structures, but is missing critical game logic, phase implementation, and rule enforcement.

---

## Current Implementation Status

### ✅ What's Implemented

1. **Basic Classes**: Player, Card, Resource classes exist
2. **Board Setup**: Europe map with city connections and costs
3. **Card Market Setup**: Basic card deck management with dark/light cards
4. **Resource Market Structure**: Resource pricing and capacity lists
5. **Player State Tracking**: Money, generators (cities), cards (power plants), resources

### ❌ What's Missing or Incomplete

1. **No Game Engine**: No main game loop or phase management
2. **No Auction System**: Phase 2 (Auction) not implemented
3. **No Building Phase**: Phase 4 (Build Generators) not implemented
4. **No Bureaucracy Phase**: Phase 5 (Bureaucracy) not implemented
5. **No Step Transitions**: Steps 1→2→3 logic missing
6. **No Player Order Management**: Phase 1 (Determine Order) not implemented
7. **No End Game Conditions**: Game end detection missing
8. **No Validation**: Resource buying rules, plant capacity limits not enforced

---

## Detailed Rule Compliance Issues

### 1. Game Setup Issues

#### Problem: Market Setup Doesn't Match Rules
**Rules**: Europe market has 9 spaces (4 current + 5 future). Current code creates 9 cards but doesn't separate them correctly.

**Current Code** (`card_setup.py` line 37):
```python
first_nine_cards = dark_cards[:9]  # Just takes first 9, doesn't separate current/future
```

**Required**: 
- Top row: 4 cheapest plants (current market) 
- Bottom row: 5 larger plants (future market)
- Must be sorted by number

#### Problem: Step 3 Card Placement Incorrect
**Rules**: Step 3 card should be placed face-down **under** the supply stack (not at the end)

**Current Code** (`card_setup.py` line 44):
```python
remaining_deck.append(Card(config.get('stage_three_card')))  # Wrong: adds to end
```

**Required**: Insert Step 3 card randomly in the deck (under the stack), not at the end.

---

### 2. Phase 1: Determine Player Order - **NOT IMPLEMENTED**

**Rules**: 
- Rearrange player order based on most cities connected
- Tie-breaker: player with bigger (higher number) power plant

**Missing**: Entire phase implementation

**Suggested Implementation**:
```python
def determine_player_order(self, players, cities_dict):
    # Sort by cities connected (descending), then by largest plant number
    return sorted(players, key=lambda p: (
        -len(p.generators),  # Most cities first
        -max([card.cost for card in p.cards] if p.cards else [0])  # Tie-breaker: largest plant
    ))
```

---

### 3. Phase 2: Auction Power Plants - **NOT IMPLEMENTED**

**Rules**:
- First player chooses a plant from current market (4 plants)
- Players bid in clockwise order (player order)
- Minimum bid = plant number
- **Europe**: If all players pass, remove smallest plant from current market
- Each player can buy at most 1 plant per round
- Players can own max 3 plants (must discard if buying 4th)
- **Round 1**: All players MUST buy a plant (cannot pass)

**Missing**: Entire auction system

**Critical Issues**:
1. No bidding mechanism
2. No plant replacement after purchase
3. No "Europe rule" for all players passing
4. No first round mandatory purchase enforcement
5. No plant discarding when > 3 owned

**Suggested Implementation Structure**:
```python
def auction_phase(self, players, current_market, player_order):
    # Each player in order chooses to:
    # 1. Start auction on a plant from current market
    # 2. Pass (if not round 1)
    # Bidding continues until all but one pass
    # After purchase: remove from market, add new plant, re-sort
    pass
```

---

### 4. Phase 3: Buy Resources - **PARTIALLY IMPLEMENTED**

**Rules**:
- Players buy in **reverse player order** (last player first)
- Can only buy resources for plants they own
- Can store up to **2x the capacity** of each plant
- Resources must match plant type (coal, gas, oil, uranium, or hybrid)

**Current Issues**:

1. **No Reverse Order**: Code doesn't specify reverse order for buying
2. **No Validation**: `Player.purchase_resources()` doesn't check:
   - Player owns plants using that resource type
   - Storage capacity limits (2x per plant)
3. **Resource Type Matching**: No validation that resources match player's plants

**Current Code** (`Player_class.py` line 59-63):
```python
def purchase_resources(self, fuel, amount):
    """ checks the resource board for purchase updates the board and updates player money and resource holdings"""
    purchase = fuel.buy_resource(amount)
    self.update_money(-purchase[1])
    self.resources[fuel.show_name()] += amount  # No validation!
```

**Required**: Add validation:
- Check player has plants using this resource type
- Check total storage capacity (sum of 2x capacity for each plant)
- Check current resources + new purchase <= capacity

---

### 5. Phase 4: Build Generators - **NOT IMPLEMENTED**

**Rules**:
- Players build in **reverse player order**
- Build in any number of cities (as long as affordable)
- Cost = building cost (10/15/20 for position 1/2/3) + connection cost (shortest path)
- **Round 1**: All players MUST build at least 1 city
- If any plant number <= number of cities any player has, remove that plant immediately

**Missing**: Entire building phase

**Critical Missing Features**:
1. Pathfinding for connection costs (currently just hardcoded 5)
2. Building cost calculation based on city position (10/15/20)
3. Immediate plant removal when plant number <= cities
4. Round 1 mandatory building

**Current Code** (`board_setup.py` line 234):
```python
occ_city_dict[c] = [10,15,20]  # Has building costs but no logic to use them
```

**Pathfinding Issue**: Current code uses simplified connection cost (5 if not first city). Rules require shortest path calculation.

---

### 6. Phase 5: Bureaucracy - **NOT IMPLEMENTED**

**Rules**:
1. **Earn Money**: Based on cities powered (not connected!)
   - Payment table: 1 city = 1E, 2 = 2E, ... 10 = 22E, etc.
2. **Resupply Resources**: Based on number of players and current Step
   - Use resource refill summary card values
3. **Update Power Plant Market**:
   - Step 1 & 2: Move largest from future market to bottom of stack, add new plant
   - Step 3: Remove smallest from current market

**Missing**: Entire bureaucracy phase

**Critical Issues**:

1. **Powering Cities vs. Connecting Cities**: 
   - Code tracks `generators` (cities connected) but doesn't calculate **cities powered**
   - Cities powered = min(cities connected, total capacity from plants with resources)

2. **Resource Usage**: 
   - Must consume resources to power plants
   - Code has `use_resource()` but no logic to calculate how many cities can be powered

3. **Payment Calculation**: 
   - No payment table implementation
   - Should be based on cities powered, not cities connected

**Suggested Payment Table**:
```python
PAYMENT_TABLE = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
    11: 11, 12: 13, 13: 15, 14: 17, 15: 19, 16: 21, 17: 23, 18: 25, 19: 27, 20: 29
}
```

---

### 7. Step Transitions - **NOT IMPLEMENTED**

**Step 1 → Step 2**:
- Trigger: When a player connects a certain number of cities (depends on # of players: 4p=7, 5p=6, 6p=5)
- **Europe**: Remove smallest plant from current market (don't replace - market becomes 4+4)
- **North America**: Remove smallest, replace with new one (stays 4+4)

**Step 2 → Step 3**:
- Trigger: When Step 3 card is drawn from deck
- Remove Step 3 card and smallest plant from current market
- Market becomes 6 plants total (no separation)

**Missing**: All step transition logic

---

### 8. Resource Market Issues

**Current Implementation**: Resource market structure exists but has issues:

1. **Resupply Logic**: Code has resupply dictionaries but no integration with game steps
2. **Resource Usage**: `use_resource()` just adds to supply, but doesn't handle the complexity:
   - Resources should be consumed during bureaucracy phase
   - Need to calculate how many cities each player can power
   - Hybrid plants (oil&gas) need special handling

**Required**: 
- Integrate resupply with bureaucracy phase
- Calculate cities powered correctly (considering resources available)
- Handle hybrid plants correctly (can use oil OR gas)

---

### 9. Power Plant Storage Capacity - **NOT ENFORCED**

**Rules**: Each plant can store up to 2x its resource cost
- Plant requiring 2 coal can store max 4 coal
- Hybrid plants: can store total of 2x (e.g., 2x3=6 total gas+oil)

**Missing**: No validation in resource purchasing

**Required**: Add storage validation before allowing purchases

---

### 10. End Game Conditions - **NOT IMPLEMENTED**

**Rules**: Game ends immediately after Phase 4 (Build) when at least one player has connected **18 or more** cities.

**Missing**: No end game detection

**Required**: Check after each build phase if any player has 18+ cities

---

### 11. Player Order Track - **NOT IMPLEMENTED**

**Rules**: Player order is tracked on the board and changes each round based on cities connected.

**Current**: Code has `starting_player_order()` but no persistent tracking or updates

---

## Recommended Improvements (Priority Order)

### Priority 1: Core Game Loop

1. **Create GameEngine Class**
   - Main game loop
   - Phase management (1-5)
   - Round tracking
   - Step tracking

2. **Implement All 5 Phases**
   - Phase 1: Determine player order
   - Phase 2: Auction (with bidding)
   - Phase 3: Buy resources (reverse order, validation)
   - Phase 4: Build (reverse order, pathfinding)
   - Phase 5: Bureaucracy (earn, resupply, update market)

### Priority 2: Rule Enforcement

3. **Resource Buying Validation**
   - Check player owns plants using resource type
   - Check storage capacity (2x per plant)
   - Enforce reverse player order

4. **Power Plant Management**
   - Enforce 3-plant limit
   - Implement discarding when buying 4th plant
   - Validate auction bids (minimum = plant number)

5. **Building Validation**
   - Pathfinding for connection costs
   - Building cost based on position (10/15/20)
   - Check affordability

### Priority 3: Game Mechanics

6. **Cities Powered Calculation**
   - Calculate based on plants + resources (not just connections)
   - Handle hybrid plants correctly
   - Use for payment in bureaucracy

7. **Step Transitions**
   - Step 1 → 2: Trigger on city count
   - Step 2 → 3: Trigger on Step 3 card
   - Market changes for each step

8. **End Game Detection**
   - Check after Phase 4
   - Winner determination (most cities powered, tie-breaker: most money)

### Priority 4: Polish & Testing

9. **Error Handling**
   - Validate all moves
   - Clear error messages
   - Prevent illegal moves

10. **Testing Framework**
    - Unit tests for each phase
    - Integration tests for full game
    - Test edge cases (tie-breakers, step transitions)

---

## Code Quality Issues

### 1. Python 2 vs Python 3
Code uses Python 2 syntax (`print` without parentheses). Should migrate to Python 3.

### 2. Code Organization
- Test code mixed with class definitions
- No main game file
- Functions scattered across files

### 3. Documentation
- Missing docstrings for critical functions
- No explanation of game flow
- Comments are minimal

### 4. Data Structures
- Power plants stored as lists, should be objects with proper attributes
- Player cards could be better structured
- Game state should be a proper class

---

## Suggested Architecture

```
GameEngine
├── GameState
│   ├── Step (1, 2, or 3)
│   ├── Round
│   ├── Phase (determine_order, auction, buy_resources, build, bureaucracy)
│   ├── Players (list)
│   ├── PlayerOrder (list)
│   ├── PowerPlantMarket
│   ├── ResourceMarket
│   └── Board
├── Phase Handlers
│   ├── determine_order()
│   ├── auction_phase()
│   ├── buy_resources_phase()
│   ├── build_phase()
│   └── bureaucracy_phase()
└── Utilities
    ├── calculate_cities_powered()
    ├── calculate_connection_cost()
    ├── check_end_game()
    └── transition_steps()
```

---

## Conclusion

The current codebase provides good foundational classes and data structures but lacks the core game logic to actually play Power Grid. The most critical missing pieces are:

1. **Game Engine**: Main loop and phase management
2. **Auction System**: Complete bidding mechanism
3. **Building Phase**: Pathfinding and cost calculation
4. **Bureaucracy Phase**: Payment, resupply, market updates
5. **Rule Enforcement**: Validation for all player actions

With these additions and the suggested improvements, the simulation could accurately represent the Power Grid game.

