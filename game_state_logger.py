"""
GameStateLogger - Handles recording game states to JSON for replay functionality
"""

import json
import hashlib
from datetime import datetime


class GameStateLogger:
    """Manages logging of game states to JSON file for replay capability"""

    def __init__(self, game_id=None, output_file=None):
        """
        Initialize the game state logger

        Args:
            game_id: Unique identifier for the game (CID). If None, generates from timestamp
            output_file: Path to output JSON file. If None, uses game_id.json
        """
        if game_id is None:
            # Generate a unique game ID based on timestamp
            timestamp = datetime.now().isoformat()
            game_id = hashlib.sha256(timestamp.encode()).hexdigest()[:16]

        self.game_id = game_id
        self.step_number = 0
        self.output_file = output_file or f"game_{game_id}.json"
        self.states = []

    def log_state(self, game_state, description=None):
        """
        Log a game state

        Args:
            game_state: GameState object to serialize
            description: Optional description of this state (e.g., "after_auction")
        """
        state_entry = {
            "gameId": self.game_id,
            "stepNumber": self.step_number,
            "gameState": game_state.to_dict()
        }

        if description:
            state_entry["description"] = description

        self.states.append(state_entry)
        self.step_number += 1

    def write_to_file(self):
        """Write all logged states to the JSON file"""
        with open(self.output_file, 'w') as f:
            json.dump(self.states, f, indent=2)

    def append_to_file(self):
        """Append the latest state to the JSON file (streaming mode)"""
        if not self.states:
            return

        # Write all states (overwrites file each time)
        # For true streaming, we could use jsonlines format instead
        self.write_to_file()

    def get_state_count(self):
        """Return the number of states logged"""
        return len(self.states)

    def reset(self):
        """Reset the logger (clears all states but keeps game_id)"""
        self.states = []
        self.step_number = 0
