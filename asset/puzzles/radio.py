import curses
from pathlib import Path


def _plot_path():
    here = Path(__file__).resolve().parent
    return here.parent / "modules" / "plot.txt"


def load_hidden_plot(name="You"):
    path = _plot_path()
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
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
        scr.addstr(y, 2, line[: max(0, width - 4)])
        y += 1
    scr.addstr(height - 2, 2, footer[: max(0, width - 4)])
    scr.refresh()
    while True:
        key = scr.getkey()
        if key in ("\n", "\r", "KEY_ENTER", "PADENTER", " "):
            return "enter"
        if key in ("q", "Q"):
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
    wait_lines(scr, ["Press Enter to return to the menu."], "Enter: continue")


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
            "The radio has been abandoned underground for a long time.",
            "The vacuum tubes are severely worn out.",
            "Try to keep them at a stable temperature so the fragile",
            "components do not burn out.",
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
            scr.addstr(1, 2, "VACUUM TUBE CONTROL SYSTEM", yellow)
            scr.addstr(3, 2, "BATTERY  " + battery_bar(battery), white)
            for i in range(3):
                marker = ">" if i == selected else " "
                color = green if i == selected else white
                if temperatures[i] >= 95:
                    color = red
                scr.addstr(5 + i, 2, marker + " Tube " + "ABC"[i] + "  " + temp_bar(temperatures[i]), color)
            scr.addstr(9, 2, "Target: ALL tubes exactly 85 C. Burnout: 100 C.", white)
            scr.addstr(11, 2, "Heating effects:   A     B     C", white)
            scr.addstr(12, 2, "Tube A:           +5     0    -5", white)
            scr.addstr(13, 2, "Tube B:           -5    +5     0", white)
            scr.addstr(14, 2, "Tube C:            0    -5   +10", white)
            scr.addstr(16, 2, "W/S or Up/Down: select tube", white)
            scr.addstr(17, 2, "A/D or Left/Right: cool / heat  (-5% battery)", white)
            scr.addstr(18, 2, "Q: quit", white)
            if status:
                scr.addstr(20, 2, status[:76], red)
            scr.refresh()
            key = scr.getkey()
            status = ""
            if key in ("q", "Q"):
                return False
            if key in ("w", "W", "KEY_UP"):
                selected = (selected - 1) % 3
            elif key in ("s", "S", "KEY_DOWN"):
                selected = (selected + 1) % 3
            elif key in ("a", "A", "d", "D", "KEY_LEFT", "KEY_RIGHT"):
                change = -1
                if key in ("d", "D", "KEY_RIGHT"):
                    change = 1
                next_temperatures = []
                for i in range(3):
                    next_temperatures.append(temperatures[i] + effects[selected][i] * change)
                if min(next_temperatures) < 0:
                    status = "Control rejected: temperature would fall below 0 C."
                    continue
                temperatures = next_temperatures
                battery -= 5
                if max(temperatures) >= 100:
                    wait_lines(scr, ["A tube burns out. Tonight's attempt has failed."])
                    return False
                if battery == 0:
                    break

        if battery < 10 or temperatures != [85, 85, 85]:
            wait_lines(scr, ["Not enough battery to keep the radio running. Tonight ends."])
            return False

        result = wait_lines(scr, [
            "Vacuum tube control system repaired.",
            "The radio is now operational.",
        ])
        if play_plot and result != "q":
            play_hidden_plot(scr, name)
        return True

    if stdscr is None:
        return curses.wrapper(game)
    return game(stdscr)


final_puzzle = radio_puzzle

if __name__ == "__main__":
    radio_puzzle(play_plot=True)
