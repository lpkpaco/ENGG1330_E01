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
        ports.append((0, row))
        ports.append((6, row))
        ports.append((row, 0))
        ports.append((row, 6))
        for col in range(1, 6):
            cells.append((row, col))
            if row < 5:
                edges.append(((row, col), (row + 1, col)))
            if col < 5:
                edges.append(((row, col), (row, col + 1)))

    def blocked(a, b, walls):
        if (a, b) in walls:
            return True
        if (b, a) in walls:
            return True
        return False

    def step(player, boxes, walls, move, entrance, end):
        dr, dc = directions[move]
        target = (player[0] + dr, player[1] + dc)
        if player == entrance and target not in cells:
            return None
        if target not in cells + [entrance, end]:
            return None
        if blocked(player, target, walls):
            return None
        new_boxes = list(boxes)
        if target in boxes:
            nxt = (target[0] + dr, target[1] + dc)
            if nxt not in cells or nxt in boxes:
                return None
            if blocked(target, nxt, walls):
                return None
            new_boxes.remove(target)
            new_boxes.append(nxt)
        return target, tuple(sorted(new_boxes))

    def search(boxes, walls, entrance, end, push):
        start = (entrance, tuple(sorted(boxes)))
        queue = [start]
        seen = set()
        seen.add(start)
        reached = []
        i = 0
        while i < len(queue):
            player, cur_boxes = queue[i]
            i = i + 1
            if player == end:
                return True
            if player not in reached:
                reached.append(player)
            for move in directions:
                result = step(player, cur_boxes, walls, move, entrance, end)
                if result == None:
                    continue
                if result in seen:
                    continue
                if push == False and result[1] != cur_boxes:
                    continue
                if len(seen) >= 12000:
                    return False
                seen.add(result)
                queue.append(result)
        if end == None and len(reached) == 25:
            return True
        return False

    def box_cells(walls, entrance, end):
        available = []
        for row, col in cells:
            count = 0
            for dr, dc in directions.values():
                other = (row + dr, col + dc)
                if other not in cells + [entrance, end] or blocked((row, col), other, walls):
                    count = count + 1
            if count <= 1:
                available.append((row, col))
        return available

    def generate_map():
        for attempt in range(100):
            entrance, end = random.sample(ports, 2)
            dist = abs(entrance[0] - end[0]) + abs(entrance[1] - end[1])
            if dist < 6:
                continue
            walls = random.sample(edges, 7)
            if search([], walls, (1, 1), None, False) == False:
                continue
            available = box_cells(walls, entrance, end)
            if len(available) < 6:
                continue
            boxes = random.sample(available, 6)
            if search(boxes, walls, entrance, end, False):
                continue
            if search(boxes, walls, entrance, end, True):
                return boxes, walls, entrance, end
        entrance, end = (0, 3), (6, 4)
        route = [(1, 3), (2, 3), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4)]
        available = box_cells([], entrance, end)
        for cell in route:
            if cell in available:
                available.remove(cell)
        boxes = [(1, 3)] + random.sample(available, 5)
        turns = random.randint(0, 3)
        for t in range(turns):
            for i in range(len(boxes)):
                row, col = boxes[i]
                boxes[i] = (col, 6 - row)
            entrance = (entrance[1], 6 - entrance[0])
            end = (end[1], 6 - end[0])
        return boxes, [], entrance, end

    def build_board(player, boxes, walls, entrance, end):
        board = []
        for y in range(11):
            board.append([" "] * 26)
        for x in range(26):
            if x % 5 == 0:
                board[0][x] = "+"
                board[10][x] = "+"
            else:
                board[0][x] = "-"
                board[10][x] = "-"
        for y in range(1, 10):
            board[y][0] = "|"
            board[y][25] = "|"

        for wall in walls:
            r1, c1 = wall[0]
            r2, c2 = wall[1]
            if r1 != r2:
                y = 2 * min(r1, r2)
                x = 5 * (c1 - 1)
                board[y][x] = "+"
                board[y][x + 5] = "+"
                for offset in range(1, 5):
                    board[y][x + offset] = "-"
            else:
                y = 2 * r1 - 1
                x = 5 * min(c1, c2)
                board[y][x] = "|"
                board[y - 1][x] = "+"
                board[y + 1][x] = "+"

        for row, col in boxes:
            y = 2 * row - 1
            x = 5 * (col - 1) + 2
            board[y][x] = "["
            board[y][x + 1] = "]"
        if player in cells:
            row, col = player
            board[2 * row - 1][5 * (col - 1) + 2] = "@"
        for port in (entrance, end):
            if port == entrance:
                label = "I"
            else:
                label = "E"
            row, col = port
            if row == 0 or row == 6:
                if row == 0:
                    y = 0
                else:
                    y = 10
                x = 5 * (col - 1) + 2
                for offset in range(1, 5):
                    board[y][5 * (col - 1) + offset] = " "
            else:
                y = 2 * row - 1
                if col == 0:
                    x = 0
                else:
                    x = 25
            if player == port:
                board[y][x] = "@"
            else:
                board[y][x] = label
        lines = []
        for row in board:
            lines.append("".join(row))
        return lines

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
        start_boxes, walls, entrance, end = generate_map()
        boxes = start_boxes
        player = entrance
        status = ""

        while True:
            board = build_board(player, boxes, walls, entrance, end)
            scr.erase()
            scr.addstr(0, 0, "Push the boxes and get to E.".ljust(78))
            if status != "":
                if status == "SOLVED":
                    attr = color_ok
                else:
                    attr = color_normal
                scr.addstr(1, 0, status[:78].ljust(78), attr)
            n = 0
            for line in board:
                scr.addstr(3 + n, 0, line, color_normal)
                n = n + 1
            y = 3 + len(board)
            scr.addstr(y, 0, "I entrance   E exit   @ you   [] box".ljust(78))
            scr.addstr(y + 1, 0, "WASD or arrows to move, R restart, Q quit".ljust(78))
            scr.refresh()

            if player == end:
                scr.addstr(1, 0, "SOLVED".ljust(78), color_ok)
                scr.refresh()
                curses.napms(900)
                return True

            key = scr.getkey()
            status = ""
            if key == "q" or key == "Q":
                return False
            if key == "r" or key == "R":
                boxes = start_boxes
                player = entrance
                continue
            move = key_to_move.get(key)
            if move == None:
                continue
            result = step(player, boxes, walls, move, entrance, end)
            if result != None:
                player, boxes = result

    if stdscr == None:
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
