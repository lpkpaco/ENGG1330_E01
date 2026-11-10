from clues import add_clue



def sokoban_puzzle():
    import random

    directions = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}
    cells = []
    edges = []
    ports = []
    for row in range(1, 6):
        ports.extend([(0, row), (6, row), (row, 0), (row, 6)])
        for col in range(1, 6):
            cells.append((row, col))
            if row < 5:
                edges.append(((row, col), (row + 1, col)))
            if col < 5:
                edges.append(((row, col), (row, col + 1)))

    def blocked(a, b, walls):
        return (a, b) in walls or (b, a) in walls

    def step(player, boxes, walls, move, entrance, exit_cell):
        dr, dc = directions[move]
        target = (player[0] + dr, player[1] + dc)
        if player == entrance and target not in cells:
            return None
        if target not in cells + [entrance, exit_cell]:
            return None
        if blocked(player, target, walls):
            return None
        new_boxes = list(boxes)
        if target in boxes:
            landing = (target[0] + dr, target[1] + dc)
            if landing not in cells or landing in boxes:
                return None
            if blocked(target, landing, walls):
                return None
            new_boxes.remove(target)
            new_boxes.append(landing)
        return target, tuple(sorted(new_boxes))

    def search(boxes, walls, entrance, exit_cell, push):
        queue = [(entrance, tuple(sorted(boxes)))]
        seen = {queue[0]}
        reached = []
        index = 0
        while index < len(queue):
            player, current_boxes = queue[index]
            index += 1
            if player == exit_cell:
                return True
            if player not in reached:
                reached.append(player)
            for move in directions:
                result = step(player, current_boxes, walls, move, entrance, exit_cell)
                if result is None or result in seen:
                    continue
                if not push and result[1] != current_boxes:
                    continue
                if len(seen) >= 12000:
                    return False
                seen.add(result)
                queue.append(result)
        return exit_cell is None and len(reached) == 25

    def box_cells(walls, entrance, exit_cell):
        available = []
        for row, col in cells:
            count = 0
            for dr, dc in directions.values():
                other = (row + dr, col + dc)
                if other not in cells + [entrance, exit_cell] or blocked((row, col), other, walls):
                    count += 1
            if count <= 1:
                available.append((row, col))
        return available

    def generate_map():
        for attempt in range(100):
            entrance, exit_cell = random.sample(ports, 2)
            if abs(entrance[0] - exit_cell[0]) + abs(entrance[1] - exit_cell[1]) < 6:
                continue
            walls = random.sample(edges, 7)
            if not search([], walls, (1, 1), None, False):
                continue
            available = box_cells(walls, entrance, exit_cell)
            if len(available) < 6:
                continue
            boxes = random.sample(available, 6)
            if search(boxes, walls, entrance, exit_cell, False):
                continue
            if search(boxes, walls, entrance, exit_cell, True):
                return boxes, walls, entrance, exit_cell
        entrance, exit_cell = (0, 3), (6, 4)
        route = [(1, 3), (2, 3), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4)]
        available = box_cells([], entrance, exit_cell)
        for cell in route:
            if cell in available:
                available.remove(cell)
        boxes = [(1, 3)] + random.sample(available, 5)
        for turn in range(random.randint(0, 3)):
            for i in range(len(boxes)):
                row, col = boxes[i]
                boxes[i] = (col, 6 - row)
            entrance = (entrance[1], 6 - entrance[0])
            exit_cell = (exit_cell[1], 6 - exit_cell[0])
        return boxes, [], entrance, exit_cell

    def draw_map(player, boxes, walls, entrance, exit_cell):
        board = [[" "] * 26 for _ in range(11)]
        for x in range(26):
            board[0][x] = board[10][x] = "+" if x % 5 == 0 else "-"
        for y in range(1, 10):
            board[y][0] = "|"
            board[y][25] = "|"

        for (r1, c1), (r2, c2) in walls:
            if r1 != r2:
                y, x = 2 * min(r1, r2), 5 * (c1 - 1)
                board[y][x] = board[y][x + 5] = "+"
                for offset in range(1, 5):
                    board[y][x + offset] = "-"
            else:
                y, x = 2 * r1 - 1, 5 * min(c1, c2)
                board[y][x] = "|"
                board[y - 1][x] = board[y + 1][x] = "+"

        for row, col in boxes:
            y, x = 2 * row - 1, 5 * (col - 1) + 2
            board[y][x:x + 2] = ["[", "]"]
        if player in cells:
            row, col = player
            board[2 * row - 1][5 * (col - 1) + 2] = "@"
        for port, label in ((entrance, "I"), (exit_cell, "E")):
            row, col = port
            if row in (0, 6):
                y, x = (0 if row == 0 else 10), 5 * (col - 1) + 2
                for offset in range(1, 5):
                    board[y][5 * (col - 1) + offset] = " "
            else:
                y, x = 2 * row - 1, (0 if col == 0 else 25)
            board[y][x] = "@" if player == port else label
        for row in board:
            print("".join(row))
        print("I: entrance   E: exit   @: player   []: box")
        print("W/A/S/D: move   R: restart   Q: quit")
        print("Push boxes and reach E.")

    initial_boxes, walls, entrance, exit_cell = generate_map()
    boxes, player = initial_boxes, entrance
    while True:
        print()
        draw_map(player, boxes, walls, entrance, exit_cell)
        move = input("Move: ").strip().lower()
        if move == "q":
            break
        if move == "r":
            boxes, player = initial_boxes, entrance
            continue
        if move not in directions:
            continue
        result = step(player, boxes, walls, move, entrance, exit_cell)
        if result is not None:
            player, boxes = result
            if player == exit_cell:
                print("SOLVED")
                clue_name = "Scattered Archives"
                clue_text = "Member A: Station E-01 uses an actual frequency of 5.01 MHz.\nMember B: The government is jamming radio signals everywhere. How do we make sure people can actually hear our broadcast?\nMember C: No matter how many difficulties we have to overcome, we're READY."
                add_clue(clue_name, clue_text)
                print("\nClue collected:\n\033[1m" + clue_name + "\033[0m")
                print(clue_text)
                input("\nPress Enter to continue")
                return True



if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    sokoban_puzzle()