import curses
from pathlib import Path


def load_hidden_plot(name="You"):
    here = Path(__file__).resolve().parent
    path = here.parent / "modules" / "plot.txt"
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except:
        return [
            ["Radio: If anyone is listening, the radiation and the nuclear war are fake!"],
            [name + ": I have to leave and escape from this lie."],
            ["GAME OVER - SURVIVED"],
            ["HIDDEN ENDING : THE LAMB ESCAPES SLAUGHTER"],
        ]
    beats = []
    current = []
    started = False
    start = "DAY 6 - hidden ending"
    stop = "DAY 6-7"
    for line in raw_lines:
        stripped = line.strip()
        if started == False:
            if stripped.startswith(start):
                started = True
                continue
            else:
                continue
        if stripped.startswith(stop):
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
        return [["You turned on the radio and escaped."]]
    return beats


def wait_lines(scr, lines, footer="Enter: continue    Q: skip"):
    height, width = scr.getmaxyx()
    scr.erase()
    y = 2
    for line in lines:
        if y >= height - 3:
            break
        if width - 4 < 0:
            text = ""
        else:
            text = line[:width - 4]
        scr.addstr(y, 2, text)
        y = y + 1
    if width - 4 < 0:
        foot = ""
    else:
        foot = footer[:width - 4]
    scr.addstr(height - 2, 2, foot)
    scr.refresh()
    while True:
        key = scr.getkey()
        if key == "\n" or key == "\r" or key == "KEY_ENTER" or key == "PADENTER" or key == " ":
            return "enter"
        if key == "q" or key == "Q":
            return "q"


def play_hidden_plot(scr, name="You"):
    beats = load_hidden_plot(name)
    for beat in beats:
        lines = []
        for line in beat:
            width = 76
            words = line.split(" ")
            current = ""
            for word in words:
                if current == "":
                    current = word
                elif len(current) + 1 + len(word) <= width:
                    current = current + " " + word
                else:
                    lines.append(current)
                    current = word
            if current != "":
                lines.append(current)
        page = 0
        while page < len(lines):
            chunk = lines[page:page + 4]
            result = wait_lines(scr, chunk)
            if result == "q":
                return
            page = page + 4
    wait_lines(scr, ["Press Enter to go back."], "Enter: continue")


def battery_bar(battery):
    filled = battery // 5
    if filled < 0:
        filled = 0
    if filled > 20:
        filled = 20
    return "[" + "#" * filled + "." * (20 - filled) + "]  " + str(battery) + "%"


def temp_bar(temp):
    filled = temp // 5
    if filled < 0:
        filled = 0
    if filled > 20:
        filled = 20
    return "[" + "#" * filled + "." * (20 - filled) + "]  " + str(temp) + " C"


def radio_puzzle(stdscr=None, name="You", play_plot=False):
    def game(scr):
        curses.start_color()
        curses.curs_set(0)
        scr.keypad(True)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        white = curses.color_pair(1)
        green = curses.color_pair(2)
        red = curses.color_pair(3)
        yellow = curses.color_pair(4)

        intro = [
            "This radio has been left underground for a long time.",
            "The vacuum tubes are pretty worn out.",
            "Keep all of them at 85 C. If one hits 100 C it burns out.",
        ]
        if wait_lines(scr, intro) == "q":
            return False

        battery = 100
        temperatures = [80, 85, 80]
        selected = 0
        effects = [(5, -5, 0), (0, 5, -5), (-5, 0, 10)]
        status = ""

        while temperatures != [85, 85, 85]:
            scr.erase()
            scr.addstr(1, 2, "VACUUM TUBES", yellow)
            scr.addstr(3, 2, "BATTERY  " + battery_bar(battery), white)
            i = 0
            while i < 3:
                if i == selected:
                    marker = ">"
                    color = green
                else:
                    marker = " "
                    color = white
                if temperatures[i] >= 95:
                    color = red
                scr.addstr(5 + i, 2, marker + " Tube " + "ABC"[i] + "  " + temp_bar(temperatures[i]), color)
                i = i + 1
            scr.addstr(9, 2, "Target: all tubes at 85 C. Burnout at 100 C.", white)
            scr.addstr(11, 2, "Heating effects:   A     B     C", white)
            scr.addstr(12, 2, "Tube A:           +5     0    -5", white)
            scr.addstr(13, 2, "Tube B:           -5    +5     0", white)
            scr.addstr(14, 2, "Tube C:            0    -5   +10", white)
            scr.addstr(16, 2, "W/S or Up/Down: select tube", white)
            scr.addstr(17, 2, "A/D or Left/Right: cool / heat  (-5% battery)", white)
            scr.addstr(18, 2, "Q: quit", white)
            if status != "":
                scr.addstr(20, 2, status[:76], red)
            scr.refresh()
            key = scr.getkey()
            status = ""
            if key == "q" or key == "Q":
                return False
            if key == "w" or key == "W" or key == "KEY_UP":
                selected = (selected - 1) % 3
            elif key == "s" or key == "S" or key == "KEY_DOWN":
                selected = (selected + 1) % 3
            elif key == "a" or key == "A" or key == "d" or key == "D" or key == "KEY_LEFT" or key == "KEY_RIGHT":
                change = -1
                if key == "d" or key == "D" or key == "KEY_RIGHT":
                    change = 1
                nxt = []
                i = 0
                while i < 3:
                    nxt.append(temperatures[i] + effects[selected][i] * change)
                    i = i + 1
                if min(nxt) < 0:
                    status = "Too cold, that would go below 0 C."
                    continue
                temperatures = nxt
                battery = battery - 5
                if max(temperatures) >= 100:
                    wait_lines(scr, ["One of the tubes burned out. The radio failed."])
                    return False
                if battery == 0:
                    break

        if battery < 10 or temperatures != [85, 85, 85]:
            wait_lines(scr, ["Battery too low. The radio died."])
            return False

        result = wait_lines(scr, [
            "The tubes are stable now.",
            "The radio works.",
        ])
        if play_plot and result != "q":
            play_hidden_plot(scr, name)
        return True

    if stdscr == None:
        return curses.wrapper(game)
    return game(stdscr)


final_puzzle = radio_puzzle

if __name__ == "__main__":
    radio_puzzle(play_plot=True)
