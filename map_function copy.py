#map function
import curses
import locale
import random

locale.setlocale(locale.LC_ALL, "")

from asset.modules.sliding_puzzle_curses import sliding_puzzle
from asset.modules.sokoban_puzzle import sokoban_puzzle
from asset.modules.circuit import generate_circuit

#draw designated text on the screen at given coordinates
def put(scr, y, x, text, attr=0):
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass

#draw a box on the screen at given coordinates with specified height and width
def box(scr, y, x, h, w, attr=0):
    put(scr, y, x, "+" + "-" * (w - 2) + "+", attr)
    for i in range(1, h - 1):
        put(scr, y + i, x, "|", attr)
        put(scr, y + i, x + w - 1, "|", attr)
    put(scr, y + h - 1, x, "+" + "-" * (w - 2) + "+", attr)

#draw a progress bar on the screen at given coordinates with specified value and attributes
def bar(scr, y, x, value, attr):
    n = value // 10
    if n > 10:
        n = 10
    if n < 0:
        n = 0
    put(scr, y, x, "[" + "#" * n + "-" * (10 - n) + "] " + str(value).rjust(3), attr)

#draw map
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
        put(scr, py, px, "@")

def pick_item(scr, item):
    scr.move(12, 0)
    scr.clrtoeol()
    put(scr, 12, 0, f"You found a {item}\nPress Enter to pick up the item or Press space to skip:")
    scr.refresh()

    while True:
        key = scr.getkey()
        if key in ("\n", "\r", "KEY_ENTER"):
            return (f"You picked up the {item}", item)
        elif key == " ":
            return (f"You skipped", None)

def run_game(scr, puzzle):
    if puzzle == "sliding_puzzle":
        return sliding_puzzle(scr)
    elif puzzle == "sokoban_puzzle":
        return sokoban_puzzle()
    elif puzzle == "circuit_puzzle":
        return generate_circuit(5, 20, 10)

def encounter(scr): 
    scr.move(12, 0)
    scr.clrtoeol()
    scenario_list = ["scenario A", "scenario B", "scenario C"]
    puzzle_list = ["sliding_puzzle", "sokoban_puzzle", "circuit_puzzle"]
    scenario = random.choice(scenario_list)
   
    put(scr, 12, 0, f"You encountered {scenario}!\nPress Enter to continue or Press space to skip:")
    scr.refresh()

    while True:
        key = scr.getkey()
        if key in ("\n", "\r", "KEY_ENTER"):
            puzzle = random.choice(puzzle_list)
            put(scr, 12, 0, f"solve {puzzle} to pass")

            scr.refresh()
            #run one of the puzzle
            result = run_game(scr, puzzle)
            if result:
                return ("You solved the puzzle", None) #or maybe we can give some rewards
        elif key == " ":
            return ("You skipped", None)
def loc_generation(scr, loc):
    item_list = ["food", "water", "medicine","Antenna","Tuner","Amplifier"]
    event = random.choice(["nothing", "found_item", "encounter"])
    if event == "nothing":
        return ("nothing here", None)
    elif event == "found_item":
        item = random.choice(item_list)
        message , item = pick_item(scr, item)

        return (message, item)
    elif event == "encounter":
        message, item = encounter(scr)
        return (message, item)


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.use_default_colors()
    
    # Set up a color pair if you want colored text
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    white = curses.color_pair(1)
    
    loc = 1  # Current location (1-4)
    message = ""
    while True:
        stdscr.erase()
    
        draw_map(stdscr, 0, 0, loc)
        put(stdscr, 12, 0, message, white)
        put(stdscr, 10, 0, "1-4: Move | Q: Quit", white)
    
        stdscr.refresh()
    
        key = stdscr.getkey()
    
        if key in ("q", "Q"):
            return
        elif key in ["2", "3", "4"]:
            new_loc = int(key)

            if new_loc == loc:
                message, item = "You are already here!", None
            else:
                loc = new_loc
                message, item = loc_generation(stdscr, loc)
        elif key == "1":
            loc = 1
            message = "You are at the base"

if __name__ == "__main__":
    curses.wrapper(main) 