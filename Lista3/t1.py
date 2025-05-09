import pytest
from z1 import solution

@pytest.mark.parametrize("str1, str2, expected_approximate, description", [
    ("", "", 0.0, "Tożsamość – brak zmian"),
    ("a", "a", 0.0, "Tożsamość – brak zmian"),

    ("a", "", 1.0, "Pojedyncze usunięcie"),
    ("", "a", 1.0, "Pojedyncza wstawka"),

    ("a", "aa", 1.0, "Pojedyncza wstawka tego samego znaku"),
    ("a", "ab", 1.0, "Pojedyncza wstawka innego znaku"),
    ("aa", "a", 1.0, "Pojedyncze usunięcie identycznego znaku"),
    ("ab", "a", 1.0, "Pojedyncze usunięcie innego znaku"),

    # Podstawienia z różnymi odległościami klawiszy
    ("a", "d", 0.4444, "Podstawienie – średnia odległość"),
    ("q", "w", 0.2222, "Podstawienie – sąsiadujące klawisze"),
    ("q", "p", 2.0, "Podstawienie – maksymalna odległość"),

    # Dwuznakowe ciągi
    ("ab", "ac", 0.4444, "Pojedyncze podstawienie w 2-znakowym ciągu"),
    ("ab", "cb", 0.6667, "Pojedyncze podstawienie na początku"),

    # Trzyznakowe ciągi z usunięciami
    ("asd", "ad", 0.2222, "Usunięcie środkowego znaku"),
    ("asd", "as", 0.2222, "Usunięcie ostatniego znaku"),
    ("abc", "bc", 1.1111, "Usunięcie pierwszego znaku"),

    # Dwa podstawienia
    ("algorithm", "algortihm", 1.3333, "Zamiana miejscami znaków"),
    ("keyboard", "keybaord", 2.2222, "Zamiana miejscami znaków"),

    
    # Mixed operations
    ("algorytm", "aforyzm", 2.4444, "Przykład znany i lubiany"),
    ("rockstar", "popstar", 3.0000, "Zamiana 'k' na 'p', usnięcie 'c', zamiana 'k' na 'p'"),

    # Moje testy
    ("hello", "hero", 1.5, "Usunięcie 'l', różnica w dystansie na klawiaturze"),
    ("algorithm", "algorihm", 1.0, "Usunięcie 't', symulowanie literówki"),

    ("computer", "comouter", 1.0, "Zamiana 'p' na 'o', test na pomyłkę bliskich klawiszy"),
    ("robot", "reboot", 2.0, "Zamiana 'o' na 'e', 'b' na 'o', ciekawe różnice w rozkładzie klawiszy"),

    ("neural", "netural", 1.0, "Literówka wynikająca z zamiany miejscami 'u' i 't'"),
    ("matrix", "matrxi", 1.7777, "Przestawienie liter, testowanie permutacji"),
    ("android", "andriod", 1.0, "Typowa literówka wynikająca z przestawienia liter"),

    ("cyborg", "cyber", 2.0, "Usunięcie 'o' i 'g', test skracania słów"),

    ("quantum", "quamtum", 1.0, "Zamiana 'n' na 'm', literówki są częste przy szybkim pisaniu"),
    ("hacker", "cracker", 3.0, "Większa zmiana, kilka liter do zamiany"),
    ("glitch", "glitxh", 1.0, "Zamiana 'c' na 'x', test literówek"),

    ("artificial", "artifical", 1.4444, "Brak 'i', test na pominięcie znaku"),
    ("deepfake", "deefpake", 1.5555, "Zamiana 'e' i 'p', symulowanie błędu pisania")


])
def test_weighted_edit_distance(str1, str2, expected_approximate, description):
    result = solution(str1, str2)
    assert result <= expected_approximate + 0.1, f"{description}: Expected ~{expected_approximate}, got {result}"
    print(f"\nTest case: '{str1}' to '{str2}' - {description}")
    print(f"Result: {result:.4f} (expected approximately {expected_approximate:.4f})")
