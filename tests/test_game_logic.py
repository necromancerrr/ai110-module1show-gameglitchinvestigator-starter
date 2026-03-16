from logic_utils import check_guess, parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# --- Bug 1 regression: hints were backwards ---

def test_hint_direction_too_high():
    # Guess of 80 against secret of 50 is too high — player must go LOWER.
    # Before the fix, this returned "Too Low" (wrong direction).
    assert check_guess(80, 50) == "Too High"

def test_hint_direction_too_low():
    # Guess of 10 against secret of 50 is too low — player must go HIGHER.
    # Before the fix, this returned "Too High" (wrong direction).
    assert check_guess(10, 50) == "Too Low"

# --- Bug 3 regression: New Game reset ---
# The new_game block in app.py resets session_state directly, so we test
# the logic_utils helpers that a correct reset depends on.

def test_parse_guess_valid():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_guess_empty():
    ok, val, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_get_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_get_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100
