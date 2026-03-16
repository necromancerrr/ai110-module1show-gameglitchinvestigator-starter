# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

### Bug 1: Hints were backwards
**Expected:** When my guess was too high, the hint should say "Go LOWER!" and when my guess was too low, it should say "Go HIGHER!"
**Actual:** The hints were reversed — guessing too high showed "📈 Go HIGHER!" and guessing too low showed "📉 Go LOWER!" — pointing me in the wrong direction every time.

### Bug 2: Hard difficulty was easier than Normal
**Expected:** Hard mode should be harder than Normal mode, meaning a wider range of numbers to guess from.
**Actual:** Hard mode used a range of 1–50, which is *smaller* than Normal's 1–100, making Hard mode accidentally easier than Normal.

### Bug 3: New Game didn't fully reset the game
**Expected:** Clicking "New Game" should reset everything — history, score, status, and the secret number — so you can start fresh.
**Actual:** Only `attempts` and `secret` were reset. The `history`, `score`, and `status` were left over from the previous game. If you had won or lost, `status` stayed as `"won"` or `"lost"`, causing the new game to immediately stop and become unplayable.

### Bug 4: New Game ignored the selected difficulty
**Expected:** When starting a new game, the secret number should be picked from the range matching the current difficulty setting.
**Actual:** The new game always called `random.randint(1, 100)` instead of using `get_range_for_difficulty()`, so the difficulty setting had no effect on the new secret number.

---

## 2. How did you use AI as a teammate?

I used Claude (Claude Code) as my primary AI tool throughout this project.

**Correct suggestion — Bug 1 (backwards hints):**
I asked the AI to look at `check_guess` in `app.py` and explain what was wrong. It immediately identified that the return values were swapped: when `guess > secret` the code returned `"📈 Go HIGHER!"` instead of `"📉 Go LOWER!"`. It suggested reversing the two message strings. I verified this was correct by writing a regression test (`test_hint_direction_too_high`) that asserts `check_guess(80, 50) == "Too High"` and running `pytest` — the test passed. I also manually played the game and confirmed hints now point in the right direction.

**Incorrect/misleading suggestion — refactoring `check_guess` return value:**
When moving `check_guess` into `logic_utils.py`, the AI initially suggested keeping the original return signature of `(outcome, message)` tuple so app.py wouldn't need changes. However, the existing starter tests (`test_guess_too_high`, etc.) compare the result directly to a string like `"Too High"`, which means a tuple return would cause all three tests to fail. I caught this by running `pytest` before accepting the suggestion — tests failed — so I changed `check_guess` to return only the outcome string and handled the display message in `app.py` with a `HINT_MESSAGES` dictionary instead.

---

## 3. Debugging and testing your fixes

**How I decided a bug was really fixed:** I required two things to be true at the same time — `pytest` had to pass *and* the live game had to behave correctly in the browser. Passing tests alone weren't enough because the tests don't cover the Streamlit UI state.

**Test I ran — Bug 1 regression:**
I added `test_hint_direction_too_high` and `test_hint_direction_too_low` to `tests/test_game_logic.py`. Before the fix, those same assertions would have failed because the old logic returned `"Too Low"` when guess > secret. After the fix, both tests passed in `pytest`. This confirmed the hint direction was correct at the logic level without needing to click through the UI every time.

**Test I ran — New Game reset (Bug 3):**
Because `new_game` resets `st.session_state` directly in `app.py`, it can't easily be unit-tested. Instead I tested it manually: I played a full game to a win, watched `status` become `"won"`, then clicked "New Game". Before the fix the game immediately showed "You already won" and stopped. After adding the `status = "playing"`, `history = []`, and `score = 0` resets, clicking "New Game" cleared the board and started a fresh round.

**AI help with tests:** The AI suggested the specific test names and assertion patterns for the hint-direction regression tests. I reviewed each one to make sure the inputs (e.g., guess=80, secret=50) clearly demonstrated the before/after behavior of the bug, then accepted them.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number kept changing because every time the user clicked "Submit", Streamlit re-ran the entire `app.py` script from top to bottom. The line `secret = random.randint(low, high)` was at the top level with no guard, so it picked a brand-new number on every rerun — making it impossible to actually guess the right answer.

Streamlit "reruns" are like hitting refresh on the whole script — every button click, every input change causes the file to execute again from line 1. `st.session_state` is a dictionary that survives across those reruns, like a sticky note that doesn't get erased. So instead of calling `random.randint()` every time, we check `if "secret" not in st.session_state` first and only generate a new number when the game genuinely hasn't started yet.

The fix that gave the game a stable secret number was wrapping the `randint` call in that `if "secret" not in st.session_state:` guard. Once the key exists in session state, Streamlit skips the line on every subsequent rerun and keeps the same value for the lifetime of the game.

---

## 5. Looking ahead: your developer habits

**Habit I want to keep:** Writing regression tests the moment I fix a bug. For Bug 1 I immediately wrote `test_hint_direction_too_high` so that if the hint logic ever gets accidentally reversed again, the test will catch it automatically. This is much more reliable than remembering to manually re-test every edge case by hand.

**What I'd do differently:** Before accepting any AI suggestion that touches a function's return type or signature, I'd run the existing tests *first* to create a baseline, then re-run them after the change. I assumed the AI's refactoring suggestion was safe until pytest showed me the tuple-vs-string mismatch — a quick "run tests first" habit would have caught that faster.

**How this project changed my thinking:** AI-generated code looks confident and complete even when it has subtle logical errors baked in, so reading it the same way I'd read my own first draft — skeptically and with tests — is the right default. The AI is a fast first draft, not a finished product.
