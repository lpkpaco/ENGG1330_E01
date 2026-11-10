def sokoban_puzzle(stdscr=None):
    import curses
    import locale
    import random

    locale.setlocale(locale.LC_ALL, "")

    directions = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}
    key_to_move = {
        "w": "w", "W": "w", "KEY_UP": "w",
        "a": "a", "A": "a", "KEY_LEFT": "a",
        "s": "s", "S": "s", "KEY_DOWN": "s",
        "d": "d", "D": "d", "KEY_RIGHT": "d",
    }
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

    def build_board(player, boxes, walls, entrance, exit_cell):
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
        return ["".join(row) for row in board]

    def game(scr):
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        color_normal = curses.color_pair(1)
        color_ok = curses.color_pair(2)
        scr.keypad(True)

        scr.erase()
        scr.addstr(0, 0, "Generating map...".ljust(78))
        scr.refresh()
        initial_boxes, walls, entrance, exit_cell = generate_map()
        boxes, player = initial_boxes, entrance
        status = ""

        while True:
            board = build_board(player, boxes, walls, entrance, exit_cell)
            scr.erase()
            scr.addstr(0, 0, "Push boxes and reach E.".ljust(78))
            if status:
                attr = color_ok if status == "SOLVED" else color_normal
                scr.addstr(1, 0, status[:78].ljust(78), attr)
            for i, line in enumerate(board):
                scr.addstr(3 + i, 0, line, color_normal)
            y = 3 + len(board)
            scr.addstr(y, 0, "I: entrance   E: exit   @: player   []: box".ljust(78))
            scr.addstr(y + 1, 0, "W/A/S/D or arrows: move   R: restart   Q: quit".ljust(78))
            scr.refresh()

            if player == exit_cell:
                scr.addstr(1, 0, "SOLVED".ljust(78), color_ok)
                scr.refresh()
                curses.napms(900)
                return True

            key = scr.getkey()
            status = ""
            if key in ("q", "Q"):
                return False
            if key in ("r", "R"):
                boxes, player = initial_boxes, entrance
                continue
            move = key_to_move.get(key)
            if move is None:
                continue
            result = step(player, boxes, walls, move, entrance, exit_cell)
            if result is not None:
                player, boxes = result

    if stdscr is None:
        return curses.wrapper(game)
    return game(stdscr)


if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    sokoban_puzzle()
