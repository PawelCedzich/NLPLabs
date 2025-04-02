import pytest
from z2 import solution

@pytest.mark.parametrize("str1, str2, X, Y, expected_approximate, description", [
    ("", "", 0.5, 1.0, 0.0, "Tożsamość – brak zmian"),
    ("a", "a", 0.5, 1.0, 0.0, "Tożsamość – brak zmian"),

    ("a", "", 0.5, 1.0, 1.0, "Pojedyncze usunięcie"),
    ("", "a", 0.5, 1.0, 0.5, "Pojedyncze wstawienie"),

    ("abc", "abcd", 0.5, 1.0, 0.5, "Wstawienie jednego znaku"),  

    ("abc", "acb", 0.5, 1.0, 0.5, "Transpozycja dwóch znaków"),
    ("abc", "xbc", 0.5, 1.0, 1.0, "Zamiana pierwszego znaku"),
    ("abc", "abx", 0.5, 1.0, 0.5, "Zamiana ostatniego znaku"),

    ("ab", "ba", 0.5, 1.0, 0.5, "Transpozycja dwóch sąsiednich znaków"),
    ("abc", "bac", 0.5, 1.0, 0.5, "Zamiana pierwszego i drugiego znaku"),

    ("algorithm", "algortihm", 0.5, 1.0, 0.5, "Transpozycja w dłuższym napisie"),
    ("keyboard", "keybaord", 0.5, 1.0, 0.5, "Transpozycja w dłuższym napisie"),
    
    ("distance", "distancw", 0.5, 1.0, 0.5, "Zamiana w dłuższym napisie"),
    ("python", "pithon", 0.5, 1.0, 1.0, "Zamiana w dłuższym napisie"),
    
    ("abc", "abcd", 0.2, 1.0, 0.2, "Wstawienie z niską wagą X"),
    ("abc", "abcd", 0.8, 1.0, 0.8, "Wstawienie z wysoką wagą X"),
    
    ("abc", "acb", 0.2, 1.0, 0.2, "Transpozycja z niską wagą X"),
    ("abc", "acb", 0.8, 1.0, 0.8, "Transpozycja z wysoką wagą X"),
    
    ("abc", "xyz", 0.5, 0.5, 1.5, "Zamiana z niską wagą Y"),
    ("abc", "xyz", 0.5, 2.0, 5.5, "Zamiana z wysoką wagą Y"),

    ("abc", "abcd", 0.01, 1.0, 0.01, "Wstawienie z bardzo niską wagą X"),
    ("abc", "abcd", 1.5, 1.0, 1.5, "Wstawienie z bardzo wysoką wagą X"),
    
    ("abc", "acb", 0.01, 1.0, 0.01, "Transpozycja z bardzo niską wagą X"),
    ("algorytm", "aforyzm", 1.5, 1.0, 3.0, "Test"),

    #moje testu

    ("hello", "hero", 0.5, 1.0, 1.5, "Usunięcie 'l', różnica w dystansie na klawiaturze"),
    ("algorithm", "algorihm", 0.5, 1.0, 1.0, "Usunięcie 't', symulowanie literówki"),

    ("computer", "comouter", 0.5, 1.0, 1.0, "Zamiana 'p' na 'o', test na pomyłkę bliskich klawiszy"),
    ("robot", "reboot", 0.2, 0.8, 2.0, "Zamiana 'o' na 'e', 'b' na 'o', ciekawe różnice w rozkładzie klawiszy"),

    ("neural", "netural", 0.5, 1.0, 1.0, "Literówka wynikająca z zamiany miejscami 'u' i 't'"),
    ("matrix", "matrxi", 0.2, 1.0, 1.0, "Przestawienie liter, testowanie permutacji"),
    ("android", "andriod", 0.5, 0.8, 1.0, "Typowa literówka wynikająca z przestawienia liter"),

    ("cyborg", "cyber", 0.5, 1.0, 2.0, "Usunięcie 'o' i 'g', test skracania słów"),

    ("quantum", "quamtum", 0.5, 0.2, 1.0, "Zamiana 'n' na 'm', literówki są częste przy szybkim pisaniu"),
    ("hacker", "cracker", 0.5, 1.0, 3.0, "Większa zmiana, kilka liter do zamiany"),
    ("glitch", "glitxh", 0.2, 1.0, 1.0, "Zamiana 'c' na 'x', test literówek"),
    
    ("artificial", "artifical", 0.5, 0.8, 1.0, "Brak 'i', test na pominięcie znaku"),
    ("deepfake", "deefpake", 0.5, 1.0, 1.0, "Zamiana 'e' i 'p', symulowanie błędu pisania")

])
def test_weighted_edit_distance(str1, str2, X, Y, expected_approximate, description):
    result = solution(str1, str2, X, Y)
    assert result <= expected_approximate + 0.1, f"{description}: Expected ~{expected_approximate}, got {result}"
    print(f"\nTest case: '{str1}' to '{str2}' - {description}")
    print(f"Result: {result:.4f} (expected approximately {expected_approximate:.4f})")
