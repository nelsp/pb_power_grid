# Python 3.11 Conversion Summary

## Changes Made

All code has been successfully converted from Python 2 to Python 3.11 syntax.

### 1. Print Statements
- Changed all `print "text"` to `print("text")`
- Files updated:
  - `Player_class.py`
  - `card_setup.py`
  - `board_setup.py`
  - `total_board_setup.py`
  - `create_use_resources.py`

### 2. File I/O
- Changed `json.loads(open('file.json').read())` to use context managers:
  ```python
  with open('config.json', 'r') as f:
      config = json.load(f)
  ```
- Files updated:
  - `run_game.py`
  - `card_setup.py`

### 3. Dictionary Methods
- Changed `if key in dict.keys():` to `if key in dict:` (more Pythonic)
- Files updated:
  - `create_use_resources.py`
  - `game_engine.py`

### 4. Code Organization
- Wrapped test code in `if __name__ == '__main__':` blocks to prevent execution on import
- Files updated:
  - `Player_class.py`
  - `create_use_resources.py`

### 5. Indentation Fixes
- Fixed tab/space inconsistencies in `card.py`

### 6. Resource Reference Fixes
- Fixed `self.resources` to `self.game_state.resources` in `game_engine.py`

## Testing

The game now runs successfully with Python 3.11:

```bash
cd C:\Users\nelsp\alison_pg\pb_power_grid
python run_game.py
```

## Compatibility Notes

- All code is now Python 3.11 compatible
- No Python 2-specific syntax remains
- The game engine runs without errors
- All imports work correctly

## Files Modified

1. `Player_class.py` - Print statements, test code wrapping
2. `card.py` - Indentation fixes
3. `card_setup.py` - Print statements, file I/O
4. `board_setup.py` - Print statements
5. `total_board_setup.py` - Print statements
6. `create_use_resources.py` - Print statements, dictionary methods, test code wrapping
7. `game_engine.py` - Resource references, dictionary iteration
8. `run_game.py` - File I/O

## Status

✅ **Conversion Complete** - All code is Python 3.11 compatible and the game runs successfully.

