import curses #holy code ts so tuff
import json
import locale
import os
import random
locale.setlocale(locale.LC_ALL, "")

from asset.puzzles.circuit import generate_circuit
from asset.puzzles.sliding_puzzle_curses import sliding_puzzle
from asset.puzzles.sokoban_puzzle import sokoban_puzzle
from asset.puzzles.radio import radio_puzzle
from asset.modules.readplot import readplot
from asset.modules.calc import circuit_difficulty
from asset.modules.filehandle import writesave, loadsave, readsave, unused_save_name

init = False
DAYS = 7
ACTIONS = 4

prop_file = os.path.join(os.path.dirname(__file__), "asset", "modules", "properties.json")
f = open(prop_file, "r")
item_props = json.load(f)
f.close()

def put(scr, y, x, text, attr=0):
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass


def wait_for_size(scr, min_w=80, min_h=24):
    while True:
        h, w = scr.getmaxyx()
        if h >= min_h and w >= min_w:
            return True
        scr.erase()
        put(scr, 0, 0, "Window too small.")
        put(scr, 1, 0, "Resize to least " + str(min_w) + "x" + str(min_h) + ".")
        put(scr, 2, 0, "Now: " + str(w) + "x" + str(h))
        put(scr, 4, 0, "Waiting for resize and press Q to quit if u want")
        scr.refresh()
        scr.timeout(200)
        ch = scr.getch()
        scr.timeout(-1)
        if ch == ord("q") or ch == ord("Q"):
            return False


def item_slot(slot, item):
    name = item if item else " "
    text = str(slot) + " [" + name + "]"
    if len(text) > 16:
        text = str(slot) + "[" + name + "]"
    if len(text) > 16:
        text = text[:15] + "]"
    return text

def enter_ch(ch):
    if ch == 10 or ch == 13 or ch == curses.KEY_ENTER:
        return True
    if hasattr(curses, "PADENTER") and ch == curses.PADENTER:
        return True
    return False

def enter_key(key):
    return key == "\n" or key == "\r" or key == "KEY_ENTER" or key == "PADENTER"

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


def load_ending_beats(name, hidden):
    try:
        raw_lines = readplot()
    except OSError:
        if hidden:
            return [["You turned on the radio and escaped."]]
        return [["You survived 7 days."]]
    beats = []
    current = []
    started = False
    if hidden:
        start = "DAY 6 - hidden ending"
        stop = "DAY 6-7"
    else:
        start = "THE SEVENTH DAY"
        stop = "END"
    for line in raw_lines:
        stripped = line.strip()
        if started == False:
            if stripped.startswith(start):
                started = True
                if hidden:
                    continue
            else:
                continue
        if hidden:
            if stripped.startswith(stop):
                break
        else:
            if stripped == stop:
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
        if hidden:
            return [["You turned on the radio and escaped."]]
        return [["You survived 7 days."]]
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

    def draw_frame(dialogue_lines, footer="Enter: continue    Q: skip intro"): #blud this drawing code killing me imma killmyself
        if not wait_for_size(scr):
            return False
        scr.erase()
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
        put(scr, 9, 63, item_slot(5, items[0]), white)
        put(scr, 10, 63, item_slot(6, items[1]), white)
        put(scr, 11, 63, item_slot(7, items[2]), white)
        put(scr, 12, 63, item_slot(8, items[3]), white)
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
            if enter_ch(ch) or ch == ord(" "):
                return "enter"

    if name == None or name == "":
        buf = ""
        curses.curs_set(1)
        while True:
            if not draw_frame(["Enter your name: " + buf], "Enter: confirm"):
                curses.curs_set(0)
                init = True
                return "You"
            ch = scr.getch()
            if enter_ch(ch):
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
                init = True
                return name
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
        if enter_key(key):
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

def run_game(scr, puzzle, hp=100, radiation=0):
    result = False
    if puzzle == "sliding_puzzle":
        result = sliding_puzzle(scr)
    elif puzzle == "circuit_puzzle":
        blocked, width, height = circuit_difficulty(hp, radiation)
        result = generate_circuit(blocked, width, height, scr)
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

def encounter(scr, hp=100, radiation=0):
    scenario = random.choice(["scenario A", "scenario B", "scenario C"])
    puzzles = ["sliding_puzzle", "sokoban_puzzle", "circuit_puzzle"]
    put(scr, 12, 0, "You encountered " + scenario + "!")
    put(scr, 13, 0, "Press Enter to continue or Space to skip:")
    scr.refresh()
    while True:
        key = scr.getkey()
        if enter_key(key):
            puzzle = random.choice(puzzles)
            put(scr, 12, 0, "Solve " + puzzle + " to pass.")
            scr.refresh()
            if run_game(scr, puzzle, hp, radiation):
                return "You solved the puzzle", "Circuit Board"
            return "Puzzle failed", None
        if key == " ":
            return "You skipped", None

loot_table = [
    ["Circuit Board", 7.5],
    ["Battery", 7.5],
    ["Antenna", 7.5],
    ["Amplifier", 7.5],
    ["Water", 25],
    ["Canned Food", 10],
    ["Dog Food", 20],
    ["Medicine", 10],
    ["Event", 5]
]


radio_parts = ["Circuit Board", "Battery", "Antenna", "Amplifier"]

def generate_loot():
    roll = random.random() * 100
    total = 0
    for i in range(len(loot_table)):
        total = total + loot_table[i][1]
        if roll < total:
            return loot_table[i][0]
    return "Event"

def generate_item():
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
    if n < 25:
        return 35
    elif n < 50:
        return 20
    elif n < 75:
        return 10
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

def loc_generation(scr):
    loot = generate_loot()
    if loot == "Event":
        return encounter(scr)
    return pick_item(scr, loot)

def ask_save_name(scr, default=""):
    buf = default
    if buf.lower().endswith(".json"):
        buf = buf[:-5]
    curses.curs_set(1)
    white = curses.color_pair(5)
    cyan = curses.color_pair(6)
    while True:
        box(scr, 17, 0, 7, 80, white)
        put(scr, 17, 2, " SAVE GAME ", white)
        put(scr, 18, 2, " " * 76, white)
        put(scr, 19, 2, "Name this save: " + buf, white)
        put(scr, 20, 2, " " * 76, white)
        put(scr, 21, 2, " " * 76, white)
        put(scr, 22, 2, "Enter: save    Q: cancel", cyan)
        scr.refresh()
        ch = scr.getch()
        if ch == ord("q") or ch == ord("Q"):
            curses.curs_set(0)
            return None
        if enter_ch(ch):
            break
        if ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8:
            buf = buf[:-1]
        elif ch >= 32 and ch <= 126 and len(buf) < 40:
            buf = buf + chr(ch)
    curses.curs_set(0)
    name = buf.strip()
    if name == "":
        return default
    return name


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
        if enter_ch(ch) or ch == ord(" "):
            return "enter"
        if ch == ord("q") or ch == ord("Q"):
            return "q"


def play_ending(scr, name, hidden):
    beats = load_ending_beats(name, hidden)
    for beat in beats:
        wrapped = []
        for line in beat:
            wrapped = wrapped + wrap_plot_line(line, 76)
        if wrapped == []:
            continue
        page = 0
        while page < len(wrapped):
            chunk = wrapped[page:page + 4]
            result = wait_dialogue(scr, chunk, "Enter: continue    Q: skip")
            if result == "q":
                return
            page = page + 4
    wait_dialogue(scr, ["Press Enter to return to the menu."])

def main(stdscr, hp=100, hunger=100, thirst=100, radiation=0, loc=1, items=None, save=None):
    if items == None:
        items = [None, None, None, None]
    visited = set()
    visited.add(loc)
    solved = set()
    location_items = regen_map()
    dispose_mode = False
    radio_fixed = False
    radio_built = False
    day = 1
    actions_left = ACTIONS
    player_name = None
    skip_intro = False
    if save != None:
        hp = save.get("hp", hp)
        hunger = save.get("hunger", hunger)
        thirst = save.get("thirst", thirst)
        radiation = save.get("radiation", radiation)
        loc = save.get("loc", loc)
        if "items" in save and save["items"] != None:
            items = save["items"][:]
        if items == None:
            items = [None, None, None, None]
        while len(items) < 4:
            items.append(None)
        items = items[:4]
        day = save.get("day", 1)
        actions_left = save.get("actions_left", ACTIONS)
        radio_fixed = save.get("radio_fixed", False)
        radio_built = save.get("radio_built", False)
        player_name = save.get("player_name", "You")
        if player_name == None or player_name == "":
            player_name = "You"
        if "location_items" in save and save["location_items"] != None:
            location_items = {}
            for k in save["location_items"]:
                location_items[int(k)] = save["location_items"][k]
        if "visited" in save and save["visited"] != None:
            visited = set()
            for v in save["visited"]:
                visited.add(int(v))
        if "solved" in save and save["solved"] != None:
            solved = set()
            for v in save["solved"]:
                solved.add(int(v))
        skip_intro = True
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
    status = "DAY " + str(day) + ". " + str(actions_left) + " actions left."
    stdscr.keypad(True)
    global init
    if skip_intro:
        init = True
    else:
        init = False
        player_name = init_gameplot(stdscr, hp=hp, hunger=hunger, thirst=thirst,
                                    radiation=radiation, loc=loc, items=items,
                                    location_items=location_items)
        status = "DAY " + str(day) + ". " + str(actions_left) + " actions left."

    def advance_day():
        nonlocal day, actions_left, location_items, visited, solved
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
        if radio_fixed and day >= 6:
            msg.append("Press Enter to continue.")
            result = wait_dialogue(stdscr, msg)
            if result == "q":
                return False
            play_ending(stdscr, player_name, True)
            return False
        if day >= DAYS:
            msg.append("Press Enter to continue.")
            result = wait_dialogue(stdscr, msg)
            if result == "q":
                return False
            play_ending(stdscr, player_name, False)
            return False
        hunger = cap(hunger - 20)
        thirst = cap(thirst - 20)
        msg.append("Hunger -20. Thirst -20.")
        day = day + 1
        actions_left = ACTIONS
        location_items = regen_map()
        visited = set()
        solved = set()
        if radio_fixed and day >= 6:
            msg.append("Press Enter to continue.")
            result = wait_dialogue(stdscr, msg)
            if result == "q":
                return False
            play_ending(stdscr, player_name, True)
            return False
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
        nonlocal radiation
        loot = location_items.get(loc)
        if loot == None or loot == "":
            visited.add(loc)
            return True, "Nothing left here."
        puzzle = LOCATION_PUZZLES.get(loc)
        gained_rad = False
        if puzzle != None and loc not in solved:
            if not run_game(stdscr, puzzle, hp, radiation):
                return True, "Puzzle failed. Come back to try again."
            solved.add(loc)
            radiation = cap(radiation + 7)
            gained_rad = True
            if radiation >= 100:
                wait_dialogue(stdscr, ["Your radiation reached 100.", "Press Enter to return to the menu."])
                return False, None
        rad_note = ""
        if gained_rad:
            rad_note = " Radiation +7."
        if loot == "Event":
            message, reward = encounter(stdscr, hp, radiation)
            restore_curses(stdscr)
            if message == "You skipped":
                return True, "You skipped the event." + rad_note
            if reward == None:
                visited.add(loc)
                location_items[loc] = None
                return True, message + rad_note
            loot = reward
        empty_slot = None
        for i in range(len(items)):
            if items[i] == None:
                empty_slot = i
                break
        if empty_slot == None:
            location_items[loc] = loot
            return True, "Found " + loot + ", but inventory is full." + rad_note
        visited.add(loc)
        items[empty_slot] = loot
        location_items[loc] = None
        ok = spend_action("Found " + loot + ". Added to slot " + str(empty_slot + 5) + "." + rad_note)
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
        if not wait_for_size(stdscr):
            return
        stdscr.erase()
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
            put(stdscr, 14, 34, "0 end day, C craft, S save.", white)
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
        put(stdscr, 15, 64, "C Craft", white)
        put(stdscr, 9, 63, item_slot(5, items[0]), white)
        put(stdscr, 10, 63, item_slot(6, items[1]), white)
        put(stdscr, 11, 63, item_slot(7, items[2]), white)
        put(stdscr, 12, 63, item_slot(8, items[3]), white)
        box(stdscr, 17, 0, 7, 80, white)
        put(stdscr, 17, 2, " DIALOGUE / INPUT ", white)
        put(stdscr, 19, 2, ("> " + status)[:76], white)
        put(stdscr, 21, 2, "0 end day    C craft    S save    Q quit", white)

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

        if key == "s" or key == "S":
            default_name = unused_save_name()
            name = ask_save_name(stdscr, default_name)
            if name == None:
                status = "Save cancelled."
                continue
            progress = {
                "player_name": player_name,
                "day": day,
                "actions_left": actions_left,
                "hp": hp,
                "hunger": hunger,
                "thirst": thirst,
                "radiation": radiation,
                "loc": loc,
                "items": items,
                "location_items": {},
                "visited": list(visited),
                "solved": list(solved),
                "radio_fixed": radio_fixed,
                "radio_built": radio_built
            }
            for k in location_items:
                progress["location_items"][str(k)] = location_items[k]
            saved = writesave(progress, name)
            if saved:
                status = "Saved as " + saved + "."
            else:
                status = "Save failed."
            continue

        if key == "9":
            dispose_mode = True
            status = "Dispose mode: press 5-8 to toss."
            continue

        if key == "c" or key == "C":
            if radio_fixed:
                if day >= 6:
                    play_ending(stdscr, player_name, True)
                    return
                status = "The radio is already working."
            else:
                if radio_built == False:
                    missing = []
                    for part in radio_parts:
                        if part not in items:
                            missing.append(part)
                    if missing != []:
                        status = "Missing: " + ", ".join(missing) + "."
                        continue
                    for part in radio_parts:
                        for i in range(len(items)):
                            if items[i] == part:
                                items[i] = None
                                break
                    radio_built = True
                ok = radio_puzzle(stdscr, name=player_name, play_plot=False)
                restore_curses(stdscr)
                if ok:
                    radio_fixed = True
                    if day >= 6:
                        play_ending(stdscr, player_name, True)
                        return
                    status = "The radio is working. It may have more to say later."
                else:
                    status = "The tubes failed. Press C to try again."
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
                rad = 0
                if "radiation" in effect:
                    rad = effect["radiation"]
                radiation = cap(radiation + rad)
                msg = "Used " + used + "."
                if effect["hunger"] != 0:
                    msg = msg + " Hunger +" + str(effect["hunger"]) + "."
                if effect["thirst"] != 0:
                    msg = msg + " Thirst +" + str(effect["thirst"]) + "."
                if effect["health"] != 0:
                    msg = msg + " HP +" + str(effect["health"]) + "."
                if rad > 0:
                    msg = msg + " Radiation +" + str(rad) + "."
                elif rad < 0:
                    msg = msg + " Radiation " + str(rad) + "."
                if not spend_action(msg):
                    return
        else:
            status = "Unknown key."

if __name__ == "__main__":
    curses.wrapper(main)