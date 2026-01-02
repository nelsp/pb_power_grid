# Auction System Refactoring Plan

## Problem Statement

The current auction implementation violates the principle that **game engines should only validate and execute moves, never make strategic decisions**. The game engine currently:

1. Makes decisions for players (forcing moves, fallback logic)
2. Lacks proper validation-retry loops
3. Doesn't require strategies to specify which plant to discard
4. Has complex nested logic that's hard to maintain

## Architecture Principles

### Game Engine Responsibilities
- **ASK** players for moves via their strategy
- **VALIDATE** moves using validation functions
- **REJECT** invalid moves by raising exceptions with clear error messages
- **RETRY** by asking again (up to max_retries)
- **EXECUTE** only valid moves
- **NEVER** make strategic decisions for players

### Player Strategy Responsibilities
- **DECIDE** what move to make based on game state
- **RETURN** properly formatted moves
- **HANDLE** validation errors by choosing different moves
- **SPECIFY** plant to discard when bidding with 3 plants owned

## Move Formats

### Auction Opening Move
```python
# Pass (not allowed in first round)
'pass'

# Start auction
{
    'action': 'buy',
    'plant': <Card object>,
    'bid': <integer amount>,
    'discard': <Card object>  # REQUIRED if player has 3 plants
}
```

### Auction Bid Response
```python
# Pass on this auction
'pass'

# Make a bid (simple)
<integer amount>

# Make a bid with discard info
{
    'bid': <integer amount>,
    'discard': <Card object>  # REQUIRED if player has 3 plants
}
```

## Validation Functions

### validate_auction_opening(player_idx, move)
Returns: `(valid: bool, error_message: str or None)`

Checks:
- Move format is correct
- Plant exists in current market
- Bid >= plant.cost and <= player.money
- If player has 3 plants:
  - Plant.cost > smallest_owned.cost
  - Discard card specified and owned

### validate_auction_bid(player_idx, bid_response, plant, current_bid, min_bid)
Returns: `(valid: bool, error_message: str or None, normalized_response)`

Checks:
- Response format is correct
- Bid >= min_bid and <= player.money
- If player has 3 plants:
  - Discard card specified and owned

## Implementation Steps

### Step 1: Update Strategy Interface
- [ ] Add `discard` parameter to auction move returns in all strategies
- [ ] Update `choose_auction_move()` to include discard logic
- [ ] Update `bid_in_auction()` to include discard logic

### Step 2: Refactor phase_2_auction
- [ ] Remove all decision-making logic (no forcing moves)
- [ ] Add validation-retry loop for auction opening
- [ ] Replace current implementation with clean validation flow
- [ ] Add try-except around strategy calls
- [ ] Raise exceptions on invalid moves

### Step 3: Refactor run_plant_auction
- [ ] Remove fallback decision logic
- [ ] Add validation-retry loop for each bid
- [ ] Raise exceptions on invalid bids
- [ ] Use discard info when executing purchase

### Step 4: Remove Helper Methods
- [ ] Delete `_ask_player_to_bid()` (violates principles)
- [ ] Keep only validation functions

### Step 5: Update Discard Execution
- [ ] Use `discard` from move instead of choosing smallest
- [ ] Execute resource validation after discard

## Detailed Implementation

### Phase 2 Auction Flow

```python
def phase_2_auction(self, verbose):
    players_who_bought = set()
    players_who_passed = set()
    is_first_round = self.game_state.round_num == 1

    while len(players_who_bought) + len(players_who_passed) < len(self.players):
        eligible = [p for p in player_order if p not in bought and p not in passed]
        if not eligible:
            break

        current_idx = eligible[0]
        player = self.players[current_idx]

        # Get move with validation-retry loop
        move = self._get_validated_auction_opening(current_idx, is_first_round, verbose)

        if move == 'pass':
            if is_first_round:
                raise Exception(f"Player {current_idx} cannot pass in first round")
            players_who_passed.add(current_idx)
            continue

        # Run auction with validation
        winner_idx, final_bid, discard = self._run_validated_auction(
            move['plant'], current_idx, move['bid'], move.get('discard'),
            eligible, players_who_passed, verbose
        )

        if winner_idx is not None:
            self._execute_plant_purchase(winner_idx, move['plant'], final_bid, discard, verbose)
            players_who_bought.add(winner_idx)
```

### Validation-Retry Helper

```python
def _get_validated_auction_opening(self, player_idx, is_first_round, verbose):
    player = self.players[player_idx]
    strategy = player.strategy
    max_retries = 3

    for attempt in range(max_retries):
        try:
            move = strategy.choose_auction_move(
                player, self.game_state,
                self.game_state.current_market,
                can_buy=True, must_buy=is_first_round
            )

            valid, error = self.validate_auction_opening(player_idx, move)

            if not valid:
                if attempt < max_retries - 1:
                    # Retry with error message
                    if verbose:
                        print(f"Player {player_idx} invalid move: {error}, retrying...")
                    continue
                else:
                    # Max retries exceeded
                    raise Exception(f"Player {player_idx} failed validation after {max_retries} attempts: {error}")

            return move

        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Player {player_idx} strategy error: {e}")
            if verbose:
                print(f"Player {player_idx} strategy raised exception: {e}, retrying...")
```

## Testing Plan

1. Test validation functions with various invalid inputs
2. Test retry loop with intentionally failing strategies
3. Test discard selection with players at 3 plants
4. Test first round (must buy) behavior
5. Test all strategies make valid moves

## Migration Notes

- Existing strategies will need updates to include discard logic
- Game logs may show retry attempts (good for debugging)
- Invalid strategy implementations will now fail fast with clear errors
- This is a breaking change for any custom strategies
