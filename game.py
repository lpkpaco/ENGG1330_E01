import curses
import locale
locale.setlocale(locale.LC_ALL, "")

def put(scr, y, x, text, attr=0):
    try:
        scr.addstr(y, x, text, attr)
    except:
        pass

def box(scr, y, x, h, w, attr=0):
    put(scr, y, x, "+" + "-" * (w - 2) + "+", attr)
    for i in range(1, h - 1):
        put(scr, y + i, x, "|", attr)
        put(scr, y + i, x + w - 1, "|", attr)
    put(scr, y + h - 1, x, "+" + "-" * (w - 2) + "+", attr)

def bar(scr, y, x, value, attr):
    n = value // 10
    if n > 10:
        n = 10
    if n < 0:
        n = 0
    put(scr, y, x, "[" + "#" * n + "-" * (10 - n) + "] " + str(value).rjust(3), attr)

def draw_map(scr, y, x, loc):
    put(scr, y, x, "############################")
    put(scr, y + 1, x, "# 1.BASE     2.TRASH CAN   #")
    put(scr, y + 2, x, "#                          #")
    put(scr, y + 3, x, "# ----+----------+----     #")
    put(scr, y + 4, x, "#     |          |         #")
    put(scr, y + 5, x, "# ----+----------+----     #")
    put(scr, y + 6, x, "#                          #")
    put(scr, y + 7, x, "# 3.WAREHOUSE  4.STORE     #")
    put(scr, y + 8, x, "############################")
    spots = {
        1: (y + 2, x + 5),
        2: (y + 2, x + 18),
        3: (y + 6, x + 5),
        4: (y + 6, x + 18),
    }
    if loc in spots:
        py, px = spots[loc]
        put(scr, py, px, "#")

def main(stdscr, hp, hunger, thirst, radiation, loc, items):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    green = curses.color_pair(1)
    brown = curses.color_pair(2)
    blue = curses.color_pair(3)
    yellow = curses.color_pair(4)
    white = curses.color_pair(5)
    cyan = curses.color_pair(6)
    status = ""
    stdscr.keypad(True)

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if h < 24 or w < 80:
            put(stdscr, 0, 0, "Resize to 80x24 by urself", white)
            put(stdscr, 1, 0, "Now: " + str(w) + "x" + str(h), white)
            stdscr.refresh()
            key = stdscr.getkey()
            if key in ("q", "Q"):
                return
            continue
        box(stdscr, 0, 0, 9, 32, white)
        put(stdscr, 0, 2, " STATS ", white)
        put(stdscr, 2, 2, "HP / Health", white)
        bar(stdscr, 2, 14, hp, green)
        put(stdscr, 3, 2, "Hunger", white)
        bar(stdscr, 3, 14, hunger, brown)
        put(stdscr, 4, 2, "Thirst", white)
        bar(stdscr, 4, 14, thirst, blue)
        put(stdscr, 5, 2, "Radiation", white)
        bar(stdscr, 5, 14, radiation, yellow)
        box(stdscr, 0, 32, 17, 30, white)
        put(stdscr, 0, 34, " SCENE ", white)
        draw_map(stdscr, 2, 33, loc)
        put(stdscr, 12, 34, "Press 1-4 to move.", white)
        put(stdscr, 13, 34, "Press 5-8 to use item.", white)
        names = {1: "Base", 2: "Trash can", 3: "Warehouse", 4: "Store"}
        put(stdscr, 15, 34, "Here: " + names.get(loc, "?"), cyan)
        box(stdscr, 0, 62, 17, 18, white)
        put(stdscr, 0, 64, " ACTIONS ", white)
        put(stdscr, 2, 64, "1-4 Move", white)
        put(stdscr, 3, 64, "1 Base", white)
        put(stdscr, 4, 64, "2 Trash can", white)
        put(stdscr, 5, 64, "3 Warehouse", white)
        put(stdscr, 6, 64, "4 Store", white)
        put(stdscr, 8, 64, "5-8 Use item", white)
        put(stdscr, 9, 64, "5 [" + (items[0] if items[0] else " ") + "]", white)
        put(stdscr, 10, 64, "6 [" + (items[1] if items[1] else " ") + "]", white)
        put(stdscr, 11, 64, "7 [" + (items[2] if items[2] else " ") + "]", white)
        put(stdscr, 12, 64, "8 [" + (items[3] if items[3] else " ") + "]", white)
        box(stdscr, 17, 0, 7, 80, white)
        put(stdscr, 17, 2, " DIALOGUE / INPUT ", white)
        put(stdscr, 19, 2, "> " + status, white)
        put(stdscr, 21, 2, "Q quit", white)

        stdscr.refresh()
        key = stdscr.getkey()

        if key in ("q", "Q"):
            return
        elif key == "1":
            loc = 1
            status = "Moved to Base."
        elif key == "2":
            loc = 2
            status = "Moved to Trash can."
        elif key == "3":
            loc = 3
            status = "Moved to Warehouse."
        elif key == "4":
            loc = 4
            status = "Moved to Store."
        elif key == "5":
            if items[0]:
                status = "Used " + items[0] + "."
            else:
                status = "Slot 5 empty."
        elif key == "6":
            if items[1]:
                status = "Used " + items[1] + "."
            else:
                status = "Slot 6 empty."
        elif key == "7":
            if items[2]:
                status = "Used " + items[2] + "."
            else:
                status = "Slot 7 empty."
        elif key == "8":
            if items[3]:
                status = "Used " + items[3] + "."
            else:
                status = "Slot 8 empty."
        else:
            status = "Unknown key."

def generate_item():
    itemlist = {(0, 29): "Water", (30, 59): "Canned Pineapple", (60, 69): "Dog Food", (70, 74): "Circuit Board", (75, 79): "Battery", (80, 82): "Antenna", (83, 85): "Amplifier", (86, 100): None}
    import secrets
    rand_item_id = secrets.SystemRandom.randint(0, 100)
    for key, value in itemlist:
        if rand_item_id in range(key[0], key[1]+1):
            return value

if __name__ == "__main__":
    curses.wrapper(main)