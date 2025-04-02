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

def solution(x: str, y: str) -> float:
    insert_cost = 1  

    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]


    for i in range(m + 1):
        dp[i][0] = i 
    for j in range(n + 1):
        dp[0][j] = j 

    def calculate_delete_cost(s, i):
        if len(s) <= 2:
            return 1
        if i == 0:
            return get_key_distance(s[i], s[i + 1]) * (2 / 9)
        elif i == len(s) - 1:
            return get_key_distance(s[i], s[i - 1]) * (2 / 9)
        else:
            left_distance = get_key_distance(s[i], s[i - 1])
            right_distance = get_key_distance(s[i], s[i + 1])
            return (left_distance + right_distance) / 2 * (2 / 9)


    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] 
            else:
                delete = dp[i - 1][j] + calculate_delete_cost(x, i - 1) 
                insert = dp[i][j - 1] + insert_cost
                replace = get_key_distance(x[i - 1], y[j - 1]) * (2 / 9)

                dp[i][j] = min(delete, insert, replace)

    return dp[m][n]
