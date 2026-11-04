import curses
import locale
import random
locale.setlocale(locale.LC_ALL, "")

from asset.modules.circuit import generate_circuit
from asset.modules.sliding_puzzle_curses import sliding_puzzle
from asset.modules.sokoban_puzzle import sokoban_puzzle


def put(scr, y, x, text, attr=0):
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
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

def draw_map(scr, y, x, loc, location_items=None):
    if location_items is None:
        location_items = {}

    def cell(n, width):
        item = location_items.get(n)
        if item is None and n in location_items:
            body = "-"
        elif item:
            body = item
        else:
            body = ""
        if loc == n:
            body = "@" + body
        if len(body) > width:
            body = body[: width - 1] + "."
        return body.ljust(width)

    put(scr, y, x, "############################")
    put(scr, y + 1, x, "# 1.BASE     2.TRASH CAN   #")
    put(scr, y + 2, x, "#" + cell(1, 13) + cell(2, 13) + "#")
    put(scr, y + 3, x, "# ----+----------+----     #")
    put(scr, y + 4, x, "#     |          |         #")
    put(scr, y + 5, x, "# ----+----------+----     #")
    put(scr, y + 6, x, "#" + cell(3, 13) + cell(4, 13) + "#")
    put(scr, y + 7, x, "# 3.WAREHOUSE  4.STORE     #")
    put(scr, y + 8, x, "############################")


def pick_item(scr, item):
    """Ask the player whether to add an item to their inventory."""
    scr.move(12, 0)
    scr.clrtoeol()
    put(scr, 12, 0, f"You found a {item}")
    put(scr, 13, 0, "Press Enter to pick it up or Space to skip:")
    scr.refresh()

    while True:
        key = scr.getkey()
        if key in ("\n", "\r", "KEY_ENTER"):
            return f"You picked up the {item}", item
        if key == " ":
            return "You skipped", None


def restore_curses(scr):
    """Put the main game screen back after shell/input puzzles."""
    try:
        curses.initscr()
    except curses.error:
        pass
    curses.noecho()
    curses.cbreak()
    try:
        curses.meta(True)
    except curses.error:
        pass
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    try:
        scr.keypad(True)
        scr.nodelay(False)
        scr.clear()
        scr.refresh()
    except curses.error:
        pass
    curses.flushinp()


def run_game(scr, puzzle):
    """Run a puzzle and return True if the player solved it."""
    if puzzle == "sliding_puzzle":
        result = bool(sliding_puzzle(scr))
        restore_curses(scr)
        return result
    if puzzle == "circuit_puzzle":
        result = bool(generate_circuit(5, 20, 10, scr))
        restore_curses(scr)
        return result
    if puzzle == "sokoban_puzzle":
        curses.def_prog_mode()
        curses.endwin()
        try:
            result = bool(sokoban_puzzle())
        finally:
            try:
                curses.reset_prog_mode()
            except curses.error:
                pass
            restore_curses(scr)
        return result
    return False


LOCATION_PUZZLES = {
    2: "circuit_puzzle",
    3: "sliding_puzzle",
    4: "sokoban_puzzle",
}


def encounter(scr):
    """Offer a random puzzle encounter and return its reward."""
    scenario = random.choice(["scenario A", "scenario B", "scenario C"])
    puzzles = ["sliding_puzzle", "sokoban_puzzle", "circuit_puzzle"]
    put(scr, 12, 0, f"You encountered {scenario}!")
    put(scr, 13, 0, "Press Enter to continue or Space to skip:")
    scr.refresh()

    while True:
        key = scr.getkey()
        if key in ("\n", "\r", "KEY_ENTER"):
            puzzle = random.choice(puzzles)
            put(scr, 12, 0, f"Solve {puzzle} to pass.")
            scr.refresh()
            if run_game(scr, puzzle):
                return "You solved the puzzle", "Circuit Board"
            return "Puzzle failed", None
        if key == " ":
            return "You skipped", None


LOCATION_ITEMS = {
    2: ("Water", "Canned Pineapple", "Dog Food"),
    3: ("Circuit Board", "Battery", "Antenna", "Amplifier"),
    4: ("Canned Pineapple", "Medicine", "Tuner", "Amplifier"),
}


def generate_item(loc=None):
    """Generate one item appropriate for a location. Base has no loot."""
    if loc not in LOCATION_ITEMS:
        return None
    return random.choice(LOCATION_ITEMS[loc])


def regen_map():
    """Roll one item for every loot location and return {loc: item}."""
    return {loc: generate_item(loc) for loc in LOCATION_ITEMS}


def dispose_item(items, slot):
    """Toss the inventory slot chosen with 5-8. Returns a status string."""
    if slot < 0 or slot >= len(items):
        return "Bad slot."
    item = items[slot]
    if not item:
        return f"Slot {slot + 5} empty."
    items[slot] = None
    return f"Disposed {item}."


def loc_generation(scr, loc):
    """Generate a random event and item when the player enters a location."""
    event = random.choice(("nothing", "found_item", "encounter"))
    if event == "nothing":
        return "Nothing here.", None
    if event == "found_item":
        item = generate_item(loc)
        return pick_item(scr, item)
    return encounter(scr)

def main(stdscr, hp=100, hunger=100, thirst=100, radiation=0, loc=1,
         items=None):
    if items is None:
        items = [None, None, None, None]
    visited_locations = {loc}
    solved_locations = set()
    location_items = regen_map()
    dispose_mode = False
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
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if h < 24 or w < 80:
            put(stdscr, 0, 0, "Resize to 80x24 by urself", white)
            put(stdscr, 1, 0, "Now: " + str(w) + "x" + str(h), white)
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord("q"), ord("Q")):
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
        draw_map(stdscr, 2, 33, loc, location_items)
        if dispose_mode:
            put(stdscr, 12, 34, "DISPOSE: press 5-8.", yellow)
            put(stdscr, 13, 34, "9 cancel dispose.", yellow)
        else:
            put(stdscr, 12, 34, "Press 1-4 to move.", white)
            put(stdscr, 13, 34, "5-8 use, 9 dispose.", white)
        names = {1: "Base", 2: "Trash can", 3: "Warehouse", 4: "Store"}
        put(stdscr, 15, 34, "Here: " + names.get(loc, "?"), cyan)
        box(stdscr, 0, 62, 17, 18, white)
        put(stdscr, 0, 64, " ACTIONS ", white)
        put(stdscr, 2, 64, "1-4 Move", white)
        put(stdscr, 3, 64, "1 Base", white)
        put(stdscr, 4, 64, "2 Trash can", white)
        put(stdscr, 5, 64, "3 Warehouse", white)
        put(stdscr, 6, 64, "4 Store", white)
        put(stdscr, 8, 64, "5-8 Use/Toss", white)
        put(stdscr, 13, 64, "9 Dispose", white)
        put(stdscr, 9, 64, "5 [" + (items[0] if items[0] else " ") + "]", white)
        put(stdscr, 10, 64, "6 [" + (items[1] if items[1] else " ") + "]", white)
        put(stdscr, 11, 64, "7 [" + (items[2] if items[2] else " ") + "]", white)
        put(stdscr, 12, 64, "8 [" + (items[3] if items[3] else " ") + "]", white)
        box(stdscr, 17, 0, 7, 80, white)
        put(stdscr, 17, 2, " DIALOGUE / INPUT ", white)
        put(stdscr, 19, 2, "> " + status, white)
        put(stdscr, 21, 2, "Q quit", white)

        stdscr.refresh()
        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            return
        if ch == -1:
            continue
        try:
            key = chr(ch)
        except ValueError:
            status = "Unknown key."
            continue

        if dispose_mode:
            if key == "9":
                dispose_mode = False
                status = "Dispose cancelled."
            elif key in ("5", "6", "7", "8"):
                status = dispose_item(items, int(key) - 5)
                dispose_mode = False
            else:
                status = "Dispose: press 5-8, or 9 to cancel."
            continue

        if key == "9":
            dispose_mode = True
            status = "Dispose mode: press 5-8 to toss."
            continue

        if key == "1":
            new_loc = 1
            status = "Moved to Base."
        elif key == "2":
            new_loc = 2
            status = "Moved to Trash can."
        elif key == "3":
            new_loc = 3
            status = "Moved to Warehouse."
        elif key == "4":
            new_loc = 4
            status = "Moved to Store."
        else:
            new_loc = None

        if new_loc is not None:
            if new_loc == loc:
                status = "You are already here."
            else:
                loc = new_loc
                if loc not in visited_locations:
                    item = location_items.get(loc)
                    if not item:
                        visited_locations.add(loc)
                        status = "Nothing left here."
                    else:
                        puzzle = LOCATION_PUZZLES.get(loc)
                        if puzzle and loc not in solved_locations:
                            if not run_game(stdscr, puzzle):
                                status = "Puzzle failed. Come back to try again."
                                item = None
                            else:
                                solved_locations.add(loc)
                        if item:
                            empty_slot = next(
                                (index for index, value in enumerate(items) if not value),
                                None,
                            )
                            if empty_slot is None:
                                status = f"Found {item}, but inventory is full."
                            else:
                                visited_locations.add(loc)
                                items[empty_slot] = item
                                location_items[loc] = None
                                status = f"Found {item}. Added to slot {empty_slot + 5}."
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

if __name__ == "__main__":
    curses.wrapper(main)