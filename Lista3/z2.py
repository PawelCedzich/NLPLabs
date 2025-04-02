keyboard_layout = {
    'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4), 'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
    'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4), 'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8),
    'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4), 'n': (2, 5), 'm': (2, 6)
}

def get_key_distance(c1, c2, X, Y):
    c1, c2 = c1.lower(), c2.lower()
    if c1 in keyboard_layout and c2 in keyboard_layout:
        pos1 = keyboard_layout[c1]
        pos2 = keyboard_layout[c2]

        if pos1 is None or pos2 is None:
            return None
        
        distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        if distance == 1:
            return X
        else:
            return Y 
    else:
        return 9


def solution(str1: str, str2: str, X: float, Y: float) -> float:
    
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]


    for i in range(m + 1):
        dp[i][0] = i 
    for j in range(n + 1):
        dp[0][j] = j * X

    def calculate_delete_cost(str1, i):
        for i in range(m + 1):
            if i == 1 or i == 2:
                dp[i][0] = i * Y
            if i == 0:
                return get_key_distance(str1[i], str1[i + 1] , X, Y)
            elif i == len(str1) - 1: 
                return get_key_distance(str1[i], str1[i - 1], X, Y)
            else:  
                left_distance = get_key_distance(str1[i], str1[i - 1])
                right_distance = get_key_distance(str1[i], str1[i + 1])
                return (left_distance + right_distance)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] 
            else:
                delete = dp[i - 1][j] + calculate_delete_cost(str1, i - 1) 
                insert = dp[i][j - 1] + X
                replace = get_key_distance(str1[i - 1], str2[j - 1], X, Y)
                transpose = (
                    dp[i - 2][j - 2] + min(X, Y)
                    if i > 1 and j > 1 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1]
                    else float('inf')
                )   

                dp[i][j] = min(delete, insert, replace, transpose)

    return dp[m][n]
