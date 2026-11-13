def sliding_puzzle(stdscr=None):
    import curses
    import locale
    import random

    locale.setlocale(locale.LC_ALL, "")

    GOAL = ["01", "02", "03", "04", "05", "06", "07", "08", "00"]

    def inversion_count(tiles):
        a = [int(t) for t in tiles if t != "00"]
        count = 0
        for i in range(len(a) - 1):
            for k in a[i + 1 :]:
                if k < a[i]:
                    count += 1
        return count

    def fresh_board():
        tiles = ["00", "01", "02", "03", "04", "05", "06", "07", "08"]
        while True:
            random.shuffle(tiles)
            if tiles != GOAL and inversion_count(tiles) % 2 == 0:
                return tiles[:]

    def to_matrix(tiles):
        return [tiles[0:3], tiles[3:6], tiles[6:9]]

    def find_xy(matrix, tile):
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if cell == tile:
                    return x, y
        return None

    def try_move(tiles, move):
        if move in list("0123456789"):
            move = "0" + move
        if move not in tiles:
            return tiles, "Tile not found"
        if move == "00":
            return tiles, "Tile not found"

        matrix = to_matrix(tiles)
        move_pos = find_xy(matrix, move)
        blank_pos = find_xy(matrix, "00")
        if move_pos is None or blank_pos is None:
            return tiles, "Tile not found"

        mx, my = move_pos
        bx, by = blank_pos
        if abs(mx - bx) + abs(my - by) != 1:
            return tiles, "Tile not adjacent to blank"

        bi = by * 3 + bx
        mi = my * 3 + mx
        tiles = tiles[:]
        tiles[bi], tiles[mi] = tiles[mi], tiles[bi]
        return tiles, ""

    def game(scr):
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        color_normal = curses.color_pair(1)
        color_ok = curses.color_pair(2)
        scr.keypad(True)
        tiles = fresh_board()
        status = ""
        while True:
            matrix = to_matrix(tiles)
            scr.erase()
            scr.addstr(0, 0, "Move a tile:".ljust(78))
            if status:
                scr.addstr(1, 0, status[:78].ljust(78))
            for y, row in enumerate(matrix):
                scr.addstr(3 + y, 0, "|" + "|".join(row) + "|", color_normal)
            scr.refresh()
            if tiles == GOAL:
                scr.addstr(1, 0, "SOLVED".ljust(78), color_ok)
                scr.refresh()
                curses.napms(900)
                return True
            key = scr.getkey()
            status = ""
            if key in ("q", "Q"):
                return False
            if key not in list("0123456789"):
                status = "Tile not found"
                continue
            tiles, status = try_move(tiles, key)
    if stdscr is None:
        return curses.wrapper(game)
    return game(stdscr)

sliding_puzzle_curses = sliding_puzzle

if __name__ == "__main__":
    import pyfiglet
    from time import sleep

    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    sliding_puzzle()
