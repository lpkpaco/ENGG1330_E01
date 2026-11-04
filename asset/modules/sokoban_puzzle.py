def draw_map(player, boxes):
    board = []
    for row in range(11):
        board.append([" "] * 26)

    for x in range(26):
        if x % 5 == 0:
            board[0][x] = "+"
            board[10][x] = "+"
        else:
            board[0][x] = "-"
            board[10][x] = "-"

    for x in range(21, 25):
        board[0][x] = " "

    for y in range(1, 10):
        board[y][0] = "|"
        if y != 9:
            board[y][25] = "|"

    board[2][15] = "+"
    board[2][20] = "+"
    for x in range(16, 20):
        board[2][x] = "-"

    board[3][20] = "|"

    for y in range(5, 8):
        board[y][10] = "|"

    for x in range(10, 26):
        if x % 5 == 0:
            board[8][x] = "+"
        else:
            board[8][x] = "-"

    for row, col in boxes:
        y = 2 * row - 1
        x = 5 * (col - 1) + 2
        board[y][x] = "["
        board[y][x + 1] = "]"

    if player != (0, 5):
        row, col = player
        y = 2 * row - 1
        x = 5 * (col - 1) + 2
        board[y][x] = "@"

    if player == (0, 5):
        print(" " * 22 + "@")
    print(" " * 22 + "v")

    for y in range(11):
        line = "".join(board[y])
        if y == 9:
            line += "  >"
        print(line)
        
    print("W/A/S/D: move   R: reset   Q: quit")


def sokoban_puzzle():
    initial_boxes = [(1, 4), (1, 5), (2, 2), (3, 2), (3, 4), (4, 1)]
    walls = [
        ((1, 4), (2, 4)),
        ((2, 4), (2, 5)),
        ((3, 2), (3, 3)),
        ((4, 2), (4, 3)),
        ((4, 3), (5, 3)),
        ((4, 4), (5, 4)),
        ((4, 5), (5, 5))
    ]
    boxes = initial_boxes[:]
    player = (0, 5)
    directions = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}

    while True:
        print()
        draw_map(player, boxes)
        move = input("Move: ").strip().lower()

        if move == "q":
            return False
        if move == "r":
            boxes = initial_boxes[:]
            player = (0, 5)
            continue
        if move not in directions:
            continue

        dr, dc = directions[move]
        next_cell = (player[0] + dr, player[1] + dc)

        if player == (0, 5) and next_cell != (1, 5):
            continue
        if player == (5, 5) and next_cell == (5, 6):
            print("success")
            return True
        if player == (1, 5) and next_cell == (0, 5):
            player = next_cell
            continue
        if not (1 <= next_cell[0] <= 5 and 1 <= next_cell[1] <= 5):
            continue
        if (player, next_cell) in walls or (next_cell, player) in walls:
            continue

        if next_cell in boxes:
            new_box = (next_cell[0] + dr, next_cell[1] + dc)
            if not (1 <= new_box[0] <= 5 and 1 <= new_box[1] <= 5):
                continue
            if new_box in boxes:
                continue
            if (next_cell, new_box) in walls or (new_box, next_cell) in walls:
                continue
            boxes.remove(next_cell)
            boxes.append(new_box)

        player = next_cell


if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    sokoban_puzzle()