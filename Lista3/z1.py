# Układ klawiatury QWERTY jako mapa pozycji klawiszy
keyboard_layout = {
    'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4), 'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
    'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4), 'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8),
    'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4), 'n': (2, 5), 'm': (2, 6), ',': (2, 7), '.': (2, 8), '/': (2, 9)
}

# Funkcja, która zwraca odległość pomiędzy dwoma klawiszami
def get_key_distance(c1, c2):
    # Upewnij się, że klawisze są małymi literami
    c1, c2 = c1.lower(), c2.lower()
    if c1 in keyboard_layout and c2 in keyboard_layout:
        pos1 = keyboard_layout[c1]
        pos2 = keyboard_layout[c2]
        # Oblicz dystans jako liczbę kroków (Manhattan distance)
        distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        return (distance / 9) * 2  # Przeskaluj dystans do zakresu 0-2
    else:
        return 9  # Jeżeli klawisz nie istnieje, zwróć domyślną wartość 9

def solution(x: str, y: str) -> float:
    insert_cost = 1  # Koszt wstawienia znaku
    delete_cost = 1  # Koszt usunięcia znaku
    replace_cost = 1  # Koszt zamiany znaku

    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Inicjalizacja pierwszego wiersza i pierwszej kolumny
    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    # Funkcja do obliczania kosztu usunięcia
    def calculate_delete_cost(s, i):
        # Dla napisów długości 1 lub 2 koszt usunięcia to 1
        if len(s) <= 2:
            return 1  # Możesz dostosować to do swoich potrzeb
        # Dla pierwszego i ostatniego znaku koszt usunięcia to odległość do sąsiedniego
        if i == 0:
            return get_key_distance(s[i], s[i + 1])
        elif i == len(s) - 1:
            return get_key_distance(s[i], s[i - 1])
        # Dla innych znaków koszt usunięcia to średnia odległość do sąsiednich znaków
        else:
            left_distance = get_key_distance(s[i], s[i - 1])
            right_distance = get_key_distance(s[i], s[i + 1])
            return (left_distance + right_distance) / 2

    # Wypełnianie macierzy DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Bez kosztu, jeśli znaki są takie same
            else:
                # Koszt wstawienia, usunięcia i zamiany
                delete = dp[i - 1][j] + calculate_delete_cost(x, i - 1)  # Używamy nowej funkcji kosztu usunięcia
                insert = dp[i][j - 1] + insert_cost
                replace = dp[i - 1][j - 1] + get_key_distance(x[i - 1], y[j - 1]) * replace_cost

                dp[i][j] = min(delete, insert, replace)

    return dp[m][n]
