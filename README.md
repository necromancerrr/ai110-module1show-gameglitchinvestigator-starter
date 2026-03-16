# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player tries to identify a secret number within a limited number of attempts. The difficulty setting controls the range and attempt limit.

**Bugs found:**
1. **Backwards hints** — `check_guess` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when it was too low, actively misleading the player on every guess.
2. **Hard mode easier than Normal** — `get_range_for_difficulty` returned `1–50` for Hard but `1–100` for Normal, inverting the difficulty curve.
3. **New Game didn't fully reset** — Clicking "New Game" only reset `attempts` and `secret`. The `status`, `history`, and `score` carried over, making the game immediately unplayable after a win or loss.
4. **New Game ignored difficulty** — The new-game block hardcoded `random.randint(1, 100)` instead of calling `get_range_for_difficulty()`, so difficulty had no effect on subsequent games.

**Fixes applied:**
- Moved all game logic (`check_guess`, `parse_guess`, `get_range_for_difficulty`, `update_score`) from `app.py` into `logic_utils.py`.
- Fixed the hint direction in `check_guess` — `guess > secret` now correctly returns `"Too High"` paired with "Go LOWER!".
- Fixed the New Game block to reset all five session state fields: `attempts`, `secret`, `status`, `history`, and `score`.
- Fixed the New Game block to use `random.randint(low, high)` derived from the selected difficulty.
- Added 6 new pytest tests in `tests/test_game_logic.py` covering hint direction, input parsing, and difficulty ranges. All 9 tests pass.

## 📸 Demo

**pytest — all 9 tests passing:**
[pytest results](image.png)

**Fixed game (winning run):**
[Fixed winning game](winning_game.png)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
