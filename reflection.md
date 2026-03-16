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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
