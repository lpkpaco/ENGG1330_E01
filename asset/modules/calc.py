def circuit_difficulty(hp, radiation):
    bonus = 0
    if hp < 25:
        bonus = bonus + 3
    elif hp < 50:
        bonus = bonus + 2
    elif hp < 75:
        bonus = bonus + 1
    if radiation >= 75:
        bonus = bonus + 3
    elif radiation >= 50:
        bonus = bonus + 2
    elif radiation >= 25:
        bonus = bonus + 1
    if bonus <= 0:
        return 9, 12, 6
    if bonus <= 2:
        return 12, 14, 7
    if bonus <= 4:
        return 15, 16, 8
    if bonus <= 5:
        return 19, 18, 9
    return 24, 20, 10
