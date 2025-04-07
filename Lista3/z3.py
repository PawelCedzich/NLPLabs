import numpy as np
from collections import Counter

keyboard_layout = {
    'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4), 'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
    'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4), 'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8),
    'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4), 'n': (2, 5), 'm': (2, 6)
}

def get_key_distance(c1, c2):
    c1, c2 = c1.lower(), c2.lower()
    if c1 in keyboard_layout and c2 in keyboard_layout:
        pos1 = keyboard_layout[c1]
        pos2 = keyboard_layout[c2]

        if pos1 is None or pos2 is None:
            return None
        
        distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        return distance 
    else:
        return 9 

def calculate_costs(text):
    char_counts = Counter(text)
    
    avg_frequency = sum(char_counts.values()) / len(char_counts)
    
    char_weights = {char: count / avg_frequency for char, count in char_counts.items()}
    
    default_weight = sum(char_weights.values()) / len(char_weights)
    
    return char_weights, default_weight

def solution(x: str, y: str) -> float:
    with open('wordlist.txt', 'r') as f:
        wordlist_content = f.read().replace("\n", "")
    
    normalized_counts, default_weight = calculate_costs(wordlist_content)
    
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i 
    for j in range(n + 1):
        dp[0][j] = j 

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  
            else:
                insert_cost = dp[i][j - 1] + normalized_counts.get(y[j - 1], default_weight)
                delete_cost = dp[i - 1][j] + (1.0 / normalized_counts.get(x[i - 1], default_weight))
                replace_cost = get_key_distance(x[i - 1], y[j - 1]) * (2 / 9) + normalized_counts.get(y[j - 1], default_weight)

                dp[i][j] = min(delete_cost, insert_cost, replace_cost)
    return dp[m][n]
