import curses
import json
import locale
import os
import random
locale.setlocale(locale.LC_ALL, "")

from asset.puzzles.circuit import generate_circuit
from asset.puzzles.sliding_puzzle_curses import sliding_puzzle
from asset.puzzles.sokoban_puzzle import sokoban_puzzle
from asset.modules.readplot import readplot

init = False
DAYS = 7
ACTIONS = 3

prop_file = os.path.join(os.path.dirname(__file__), "asset", "modules", "properties.json")
f = open(prop_file, "r")
item_props = json.load(f)
f.close()

def put(scr, y, x, text, attr=0):
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass

def wrap_plot_line(text, width):
    words = text.split()
    if len(words) == 0:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        if len(current + " " + word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines

def load_intro_beats(name):
    try:
        raw_lines = readplot()
    except OSError:
        return [["Plot file could not be loaded."]]
    beats = []
    current = []
    for line in raw_lines:
        stripped = line.strip()
        if stripped == "This is your day 2" or stripped == "DAY 3" or stripped.startswith("DAY 6"):
            break
        if stripped == "":
            if current != []:
                beats.append(current)
                current = []
            continue
        current.append(line.replace("{name}", name))
    if current != []:
        beats.append(current)
    if beats == []:
        return [["(No opening plot found.)"]]
    return beats

def init_gameplot(scr, name=None, hp=100, hunger=100, thirst=100, radiation=0,
                  loc=1, items=None, location_items=None):
    global init
    if init:
        if name == None:
            return "You"
        return name
    if items == None:
        items = [None, None, None, None]
    if location_items == None:
        location_items = {}

    green = curses.color_pair(1)
    brown = curses.color_pair(2)
    blue = curses.color_pair(3)
    yellow = curses.color_pair(4)
    white = curses.color_pair(5)
    cyan = curses.color_pair(6)
    names = {1: "Base", 2: "Trash can", 3: "Warehouse", 4: "Store"}
    scr.keypad(True)

    def draw_frame(dialogue_lines, footer="Enter: continue    Q: skip intro"):
        h, w = scr.getmaxyx()
        scr.erase()
        if h < 24 or w < 80:
            put(scr, 0, 0, "Resize to 80x24 by urself", white)
            put(scr, 1, 0, "Now: " + str(w) + "x" + str(h), white)
            scr.refresh()
            return False
        box(scr, 0, 0, 9, 32, white)
        put(scr, 0, 2, " STATS ", white)
        put(scr, 2, 2, "HP / Health", white)
        bar(scr, 2, 14, hp, green)
        put(scr, 3, 2, "Hunger", white)
        bar(scr, 3, 14, hunger, brown)
        put(scr, 4, 2, "Thirst", white)
        bar(scr, 4, 14, thirst, blue)
        put(scr, 5, 2, "Radiation", white)
        bar(scr, 5, 14, radiation, yellow)
        box(scr, 0, 32, 17, 30, white)
        put(scr, 0, 34, " SCENE ", white)
        draw_map(scr, 2, 33, loc, location_items)
        put(scr, 12, 34, "Press 1-4 to move.", white)
        put(scr, 13, 34, "5-8 use, 9 dispose.", white)
        put(scr, 15, 34, "Here: " + names.get(loc, "?"), cyan)
        box(scr, 0, 62, 17, 18, white)
        put(scr, 0, 64, " ACTIONS ", white)
        put(scr, 2, 64, "1-4 Move", white)
        put(scr, 3, 64, "1 Base", white)
        put(scr, 4, 64, "2 Trash can", white)
        put(scr, 5, 64, "3 Warehouse", white)
        put(scr, 6, 64, "4 Store", white)
        put(scr, 8, 64, "5-8 Use/Toss", white)
        put(scr, 13, 64, "9 Dispose", white)
        put(scr, 9, 64, "5 [" + (items[0] if items[0] else " ") + "]", white)
        put(scr, 10, 64, "6 [" + (items[1] if items[1] else " ") + "]", white)
        put(scr, 11, 64, "7 [" + (items[2] if items[2] else " ") + "]", white)
        put(scr, 12, 64, "8 [" + (items[3] if items[3] else " ") + "]", white)
        box(scr, 17, 0, 7, 80, white)
        put(scr, 17, 2, " DIALOGUE / INPUT ", white)
        for i in range(len(dialogue_lines)):
            if i >= 4:
                break
            put(scr, 18 + i, 2, dialogue_lines[i][:76], white)
        put(scr, 22, 2, footer[:76], cyan)
        scr.refresh()
        return True

    def wait_key():
        while True:
            ch = scr.getch()
            if ch == ord("q") or ch == ord("Q"):
                return "q"
            if ch == 10 or ch == 13 or ch == curses.KEY_ENTER or ch == ord(" "):
                return "enter"

    if name == None or name == "":
        buf = ""
        curses.curs_set(1)
        while True:
            if not draw_frame(["Enter your name: " + buf], "Enter: confirm"):
                ch = scr.getch()
                if ch == ord("q") or ch == ord("Q"):
                    curses.curs_set(0)
                    init = True
                    return "You"
                continue
            ch = scr.getch()
            if ch == 10 or ch == 13 or ch == curses.KEY_ENTER:
                name = buf.strip()
                if name == "":
                    name = "You"
                break
            if ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8:
                buf = buf[:-1]
            elif ch >= 32 and ch <= 126 and len(buf) < 20:
                buf = buf + chr(ch)
        curses.curs_set(0)

    beats = load_intro_beats(name)
    for beat in beats:
        wrapped = []
        for line in beat:
            wrapped = wrapped + wrap_plot_line(line, 76)
        if wrapped == []:
            continue
        page = 0
        while page < len(wrapped):
            if not draw_frame(wrapped[page:page + 4]):
                ch = scr.getch()
                if ch == ord("q") or ch == ord("Q"):
                    init = True
                    return name
                continue
            action = wait_key()
            if action == "q":
                init = True
                return name
            page = page + 4

    init = True
    return name

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
    if location_items == None:
        location_items = {}

    def cell(n, width):
        item = location_items.get(n)
        if item == None and n in location_items:
            body = "-"
        elif item:
            body = item
        else:
            body = ""
        if loc == n:
            body = "@" + body
        if len(body) > width:
            body = body[:width - 1] + "."
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
    scr.move(12, 0)
    scr.clrtoeol()
    put(scr, 12, 0, "You found a " + str(item))
    put(scr, 13, 0, "Press Enter to pick it up or Space to skip:")
    scr.refresh()
    while True:
        key = scr.getkey()
        if key == "\n" or key == "\r" or key == "KEY_ENTER":
            return "You picked up the " + str(item), item
        if key == " ":
            return "You skipped", None

def restore_curses(scr):
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
    result = False
    if puzzle == "sliding_puzzle":
        result = sliding_puzzle(scr)
    elif puzzle == "circuit_puzzle":
        result = generate_circuit(5, 20, 10, scr)
    elif puzzle == "sokoban_puzzle":
        result = sokoban_puzzle(scr)
    else:
        return False
    restore_curses(scr)
    return result

LOCATION_PUZZLES = {
    2: "circuit_puzzle",
    3: "sliding_puzzle",
    4: "sokoban_puzzle"
}

def encounter(scr):
    scenario = random.choice(["scenario A", "scenario B", "scenario C"])
    puzzles = ["sliding_puzzle", "sokoban_puzzle", "circuit_puzzle"]
    put(scr, 12, 0, "You encountered " + scenario + "!")
    put(scr, 13, 0, "Press Enter to continue or Space to skip:")
    scr.refresh()
    while True:
        key = scr.getkey()
        if key == "\n" or key == "\r" or key == "KEY_ENTER":
            puzzle = random.choice(puzzles)
            put(scr, 12, 0, "Solve " + puzzle + " to pass.")
            scr.refresh()
            if run_game(scr, puzzle):
                return "You solved the puzzle", "Circuit Board"
            return "Puzzle failed", None
        if key == " ":
            return "You skipped", None

loot_table = [
    ["Circuit Board", 5],
    ["Battery", 5],
    ["Antenna", 5],
    ["Amplifier", 5],
    ["Tuner", 5],
    ["Water", 30],
    ["Canned Food", 10],
    ["Dog Food", 20],
    ["Medicine", 10],
    ["Event", 5]
]

def generate_loot():
    roll = random.randint(1, 100)
    total = 0
    for i in range(len(loot_table)):
        total = total + loot_table[i][1]
        if roll <= total:
            return loot_table[i][0]
    return "Event"

def generate_item(loc=None):
    item = generate_loot()
    while item == "Event":
        item = generate_loot()
    return item

def regen_map():
    new_items = {}
    for loc in [2, 3, 4]:
        new_items[loc] = generate_loot()
    return new_items

def hp_penalty(n):
    if n < 40:
        return 50
    elif n < 60:
        return 30
    elif n < 85:
        return 20
    else:
        return 0

def cap(n):
    if n < 0:
        return 0
    if n > 100:
        return 100
    return n

def dispose_item(items, slot):
    if slot < 0 or slot >= len(items):
        return "Bad slot."
    item = items[slot]
    if item == None:
        return "Slot " + str(slot + 5) + " empty."
    items[slot] = None
    return "Disposed " + item + "."

def loc_generation(scr, loc):
    loot = generate_loot()
    if loot == "Event":
        return encounter(scr)
    return pick_item(scr, loot)

def wait_dialogue(scr, lines, footer="Enter: continue"):
    white = curses.color_pair(5)
    cyan = curses.color_pair(6)
    box(scr, 17, 0, 7, 80, white)
    put(scr, 17, 2, " DIALOGUE / INPUT ", white)
    for i in range(4):
        put(scr, 18 + i, 2, " " * 76, white)
    for i in range(len(lines)):
        if i >= 4:
            break
        put(scr, 18 + i, 2, lines[i][:76], white)
    put(scr, 22, 2, footer[:76], cyan)
    scr.refresh()
    while True:
        ch = scr.getch()
        if ch == 10 or ch == 13 or ch == curses.KEY_ENTER or ch == ord(" "):
            return "enter"
        if ch == ord("q") or ch == ord("Q"):
            return "q"

def main(stdscr, hp=100, hunger=100, thirst=100, radiation=0, loc=1, items=None):
    if items == None:
        items = [None, None, None, None]
    visited = set()
    visited.add(loc)
    solved = set()
    location_items = regen_map()
    dispose_mode = False
    day = 1
    actions_left = ACTIONS
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
    status = "DAY 1. " + str(ACTIONS) + " actions left."
    stdscr.keypad(True)
    global init
    init = False
    player_name = init_gameplot(stdscr, hp=hp, hunger=hunger, thirst=thirst,
                                radiation=radiation, loc=loc, items=items,
                                location_items=location_items)
    status = "DAY 1. " + str(ACTIONS) + " actions left."

    def advance_day():
        nonlocal day, actions_left, location_items, visited
        nonlocal dispose_mode, status, hp, hunger, thirst
        dispose_mode = False
        lost = hp_penalty(hunger) + hp_penalty(thirst)
        hp = cap(hp - lost)
        msg = []
        msg.append("Day " + str(day) + " is over.")
        if hp_penalty(hunger) != 0 or hp_penalty(thirst) != 0:
            line = ""
            if hp_penalty(hunger) != 0:
                line = line + "Low hunger: HP -" + str(hp_penalty(hunger)) + "."
            if hp_penalty(thirst) != 0:
                if line != "":
                    line = line + " "
                line = line + "Low thirst: HP -" + str(hp_penalty(thirst)) + "."
            msg.append(line)
        if hp <= 0:
            msg.append("Your health reached 0.")
            msg.append("Press Enter to return to the menu.")
            wait_dialogue(stdscr, msg)
            return False
        if day >= DAYS:
            msg.append("You survived 7 days.")
            msg.append("Press Enter to return to the menu.")
            wait_dialogue(stdscr, msg)
            return False
        hunger = cap(hunger - 20)
        thirst = cap(thirst - 20)
        msg.append("Hunger -20. Thirst -20.")
        day = day + 1
        actions_left = ACTIONS
        location_items = regen_map()
        visited = set()
        msg.append("Press Enter to begin DAY " + str(day) + ".")
        result = wait_dialogue(stdscr, msg)
        if result == "q":
            return False
        status = "DAY " + str(day) + ". " + str(actions_left) + " actions left."
        return True

    def spend_action(message):
        nonlocal actions_left, status
        actions_left = actions_left - 1
        if actions_left < 0:
            actions_left = 0
        if actions_left == 0:
            status = message + " No actions left."
            return advance_day()
        status = message + " " + str(actions_left) + " action(s) left."
        return True

    def try_pickup():
        loot = location_items.get(loc)
        if loot == None or loot == "":
            visited.add(loc)
            return True, "Nothing left here."
        puzzle = LOCATION_PUZZLES.get(loc)
        if puzzle != None and loc not in solved:
            if not run_game(stdscr, puzzle):
                return True, "Puzzle failed. Come back to try again."
            solved.add(loc)
        if loot == "Event":
            message, reward = encounter(stdscr)
            restore_curses(stdscr)
            if message == "You skipped":
                return True, "You skipped the event."
            if reward == None:
                visited.add(loc)
                location_items[loc] = None
                return True, message
            loot = reward
        empty_slot = None
        for i in range(len(items)):
            if items[i] == None:
                empty_slot = i
                break
        if empty_slot == None:
            location_items[loc] = loot
            return True, "Found " + loot + ", but inventory is full."
        visited.add(loc)
        items[empty_slot] = loot
        location_items[loc] = None
        ok = spend_action("Found " + loot + ". Added to slot " + str(empty_slot + 5) + ".")
        return ok, None

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
            if ch == ord("q") or ch == ord("Q"):
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
        put(stdscr, 6, 2, "Day " + str(day) + " / " + str(DAYS), cyan)
        put(stdscr, 7, 2, "Actions " + str(actions_left) + " / " + str(ACTIONS), cyan)
        box(stdscr, 0, 32, 17, 30, white)
        put(stdscr, 0, 34, " SCENE ", white)
        draw_map(stdscr, 2, 33, loc, location_items)
        if dispose_mode:
            put(stdscr, 12, 34, "DISPOSE: press 5-8.", yellow)
            put(stdscr, 13, 34, "9 cancel dispose.", yellow)
        else:
            put(stdscr, 12, 34, "Press 1-4 to move.", white)
            put(stdscr, 13, 34, "5-8 use, 9 dispose.", white)
            put(stdscr, 14, 34, "0 end day / skip.", white)
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
        put(stdscr, 14, 64, "0 End day", white)
        put(stdscr, 9, 64, "5 [" + (items[0] if items[0] else " ") + "]", white)
        put(stdscr, 10, 64, "6 [" + (items[1] if items[1] else " ") + "]", white)
        put(stdscr, 11, 64, "7 [" + (items[2] if items[2] else " ") + "]", white)
        put(stdscr, 12, 64, "8 [" + (items[3] if items[3] else " ") + "]", white)
        box(stdscr, 17, 0, 7, 80, white)
        put(stdscr, 17, 2, " DIALOGUE / INPUT ", white)
        put(stdscr, 19, 2, ("> " + status)[:76], white)
        put(stdscr, 21, 2, "0 end day    Q quit", white)

        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord("q") or ch == ord("Q"):
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
            elif key == "5" or key == "6" or key == "7" or key == "8":
                slot = int(key) - 5
                item = items[slot]
                status = dispose_item(items, slot)
                dispose_mode = False
                if item != None:
                    if not spend_action("Disposed " + item + "."):
                        return
            else:
                status = "Dispose: press 5-8, or 9 to cancel."
            continue

        if key == "0":
            if not advance_day():
                return
            continue

        if key == "9":
            dispose_mode = True
            status = "Dispose mode: press 5-8 to toss."
            continue

        if key == "1":
            new_loc = 1
            moved_status = "Moved to Base."
        elif key == "2":
            new_loc = 2
            moved_status = "Moved to Trash can."
        elif key == "3":
            new_loc = 3
            moved_status = "Moved to Warehouse."
        elif key == "4":
            new_loc = 4
            moved_status = "Moved to Store."
        else:
            new_loc = None
            moved_status = ""

        if new_loc != None:
            if new_loc != loc:
                loc = new_loc
                status = moved_status
                if loc not in visited:
                    ok, leftover = try_pickup()
                    if leftover != None:
                        status = leftover
                    if not ok:
                        return
            elif loc not in visited and location_items.get(loc):
                ok, leftover = try_pickup()
                if leftover != None:
                    status = leftover
                if not ok:
                    return
            else:
                status = "You are already here."
        elif key == "5" or key == "6" or key == "7" or key == "8":
            slot = int(key) - 5
            used = items[slot]
            if used == None:
                status = "Slot " + key + " empty."
            elif used not in item_props:
                status = "Can't use " + used + "."
            else:
                effect = item_props[used]
                items[slot] = None
                hp = cap(hp + effect["health"])
                hunger = cap(hunger + effect["hunger"])
                thirst = cap(thirst + effect["thirst"])
                msg = "Used " + used + "."
                if effect["hunger"] != 0:
                    msg = msg + " Hunger +" + str(effect["hunger"]) + "."
                if effect["thirst"] != 0:
                    msg = msg + " Thirst +" + str(effect["thirst"]) + "."
                if effect["health"] != 0:
                    msg = msg + " HP +" + str(effect["health"]) + "."
                if not spend_action(msg):
                    return
        else:
            status = "Unknown key."

if __name__ == "__main__":
    curses.wrapper(main)