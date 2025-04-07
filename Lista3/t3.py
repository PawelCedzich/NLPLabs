import pytest
from z3 import solution

@pytest.mark.parametrize("str1, str2, expected_approximate, description", [
    ("", "", 0.0, "Test 1"),
    ("hello", "hello", 0.0, "Test 2"),

    ("a", "", 0.4236, "Test 3"),
    ("", "a", 2.3605, "Test 4"),

    ("key", "keys", 1.6611, "Test 5"),
    ("keyboard", "keybard", 0.56, "Test 6"),

    ("r", "t", 1.9873, "Test 7"),

    ("abc", "xbc", 0.5, "Test 8"),
    ("abc", "abx", 0.3, "Test 9"),

    ("ab", "ba", 2.4820, "Test 10"),
    ("abc", "bac", 2.4820, "Test 11"),

    ("aforyzm", "algorytm", 4.9347, "Test 12"),
    ("kitten", "sitting", 6.2394, "Test 13"),

    ("abc", "xyz", 1.99, "Test 14"),
    ("a"*100+"b", "a"*100+"c", 1.6450, "Test 15"),

    ("racecar", "racecarx", 0.08, "Test 16"),

    ("abc", "abcd", 0.9, "Test 17"),
    ("abc", "acb", 2.0335, "Test 18"),
    ("asdf", "asdg", 0.83, "Test 19"),

    ("keyboardkeyboard", "keyboardkeyboard", 0.0, "Test 20"),
    ("keyboardkeyboard", "keyboadkeyboad", 1.1, "Test 21"),

    ("ello", "hello", 0.6631, "Test 22"),
    ("hell", "hello", 1.7830, "Test 23"),

    ("abcde", "xyzab", 2.98, "Test 24"),
    ("aaaa", "bbbb", 3.72, "Test 25"),

     # Moje testy
    # ("hello", "hero", 1.5, "Usunięcie 'l', różnica w dystansie na klawiaturze"),
    # ("algorithm", "algorihm", 1.0, "Usunięcie 't', symulowanie literówki"),

    # ("computer", "comouter", 1.0, "Zamiana 'p' na 'o', test na pomyłkę bliskich klawiszy"),
    # ("robot", "reboot", 2.33, "Zamiana 'o' na 'e', 'b' na 'o', ciekawe różnice w rozkładzie klawiszy"),

    # ("neural", "netural", 1.0, "Literówka wynikająca z zamiany miejscami 'u' i 't'"),
    # ("matrix", "matrxi", 2.33, "Przestawienie liter, testowanie permutacji"),
    # ("android", "andriod", 1.0, "Typowa literówka wynikająca z przestawienia liter"),

    # ("cyborg", "cyber", 2.0, "Usunięcie 'o' i 'g', test skracania słów"),

    # ("quantum", "quamtum", 1.0, "Zamiana 'n' na 'm', literówki są częste przy szybkim pisaniu"),
    # ("hacker", "cracker", 3.0, "Większa zmiana, kilka liter do zamiany"),
    # ("glitch", "glitxh", 1.0, "Zamiana 'c' na 'x', test literówek"),

    # ("artificial", "artifical", 1.67, "Brak 'i', test na pominięcie znaku"),
    # ("deepfake", "deefpake", 2.11, "Zamiana 'e' i 'p', symulowanie błędu pisania")


])
def test_weighted_edit_distance(str1, str2, expected_approximate, description):
    result = solution(str1, str2)
    assert result <= expected_approximate + 0.1, f"{description}: Expected ~{expected_approximate}, got {result:.2f}"
    print(f"\n{description}")
    print(f"Input: '{str1}' → '{str2}'")
    print(f"Result: {result:.2f} (expected {expected_approximate:.2f} + 0.1)\n")

    