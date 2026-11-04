def get_char(stdscr, currenty, currentx):
    height, width = stdscr.getmaxyx()
    if currenty < 0 or currenty >= height or currentx < 0 or currentx >= width:
        return " "
    try:
        stdscr.addstr(2, 0, f"{currentx} {currenty}")
        raw_char = stdscr.instr(currenty, currentx, 4).split(b"\x00", 1)[0]
        decoded = raw_char.decode("utf-8", errors="ignore")
        if decoded:
            return decoded[0]
        else:
            return " "
    except:
        return " "

def validate(stdscr, objects, start_y, end_y, renderx, rendery):
    directions = {objects[1]: (-1, 0), objects[2]: (1, 0), objects[3]: (0, -1), objects[4]: (0, 1)} #yx
    inverse_directions = {(-1, 0): objects[1], (1, 0): objects[2], (0, -1): objects[3], (0, 1): objects[4]} #yx as well
    y, x = start_y, 0
    found = False
    for dx, dy in ((0, -1), (0, 1), (1, 0), (-1, 0)):
        newx, newy = x + dx, y + dy
        if not (0 <= newx <= renderx and 4 <= newy <= 4 + rendery):
            continue
        if get_char(stdscr, newy, newx) == inverse_directions[(dy, dx)]:
            x, y = newx, newy
            found = True
            break
    if not found:
        return False
    seen = set()
    while True:
        if (x, y) in seen:
            return False
        seen.add((x, y))
        char = get_char(stdscr, y, x)
        if char not in directions:
            return False
        dy, dx = directions[char]
        x += dx
        y += dy
        if (x, y) == (renderx - 1, end_y):
            return True
        if not (0 <= x <= renderx and 4 <= y <= 4 + rendery):
            return False

def generate_circuit(difficulty, renderx, rendery, stdscr=None):
    import curses, secrets, locale
    locale.setlocale(locale.LC_ALL, "")
    def circuit_game(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        color_normal = curses.color_pair(1)
        color_selected = curses.color_pair(2)
        color_blocked = curses.color_pair(3)
        stdscr.clear()
        objects = ["█", "↑", "↓", "←", "→", "☇", "⚑"]
        for y in range(4, 4 + rendery):
            for x in range(0, renderx):
                stdscr.addstr(y, x, objects[0])
        start_y = secrets.SystemRandom().randint(4, 4 + rendery - 1)
        end_y = secrets.SystemRandom().randint(4, 4 + rendery - 1)
        stdscr.addstr(start_y, 0, objects[5])
        stdscr.addstr(end_y, renderx-1, objects[6])
        blocked_coor = []
        for i in range(0, difficulty):
            while True:
                y = secrets.SystemRandom().randint(4, 4 + rendery)
                if y == start_y and y == end_y:
                    continue
                x = secrets.SystemRandom().randint(1, 1 + renderx)
                if (x, y) not in blocked_coor:
                    blocked_coor.append((x, y))
                    break
                else:
                    continue
        if __name__ == "__main__":
            print(blocked_coor)
            print(len(blocked_coor))
        stdscr.refresh()
        currentx, currenty = 0, start_y
        lastx, lasty = 0, start_y
        while True:
            key = stdscr.getkey()
            if key == "KEY_UP":
                if currenty - 1 < 4:
                    stdscr.addstr(0, 0, "Cannot move out of boundary".ljust(40))
                    continue
                elif get_char(stdscr, currenty - 1, currentx) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions".ljust(40))
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currenty -= 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
                    stdscr.refresh()
            elif key == "KEY_DOWN":
                if currenty + 1 > 3 + rendery:
                    stdscr.addstr(0, 0, "Cannot move out of boundary".ljust(40))
                    continue
                elif get_char(stdscr, currenty + 1, currentx) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions".ljust(40))
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currenty += 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
                    stdscr.refresh()
            elif key == "KEY_LEFT":
                if currentx - 1 < 0:
                    stdscr.addstr(0, 0, "Cannot move out of boundary".ljust(40))
                    continue
                elif get_char(stdscr, currenty, currentx - 1) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions".ljust(40))
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currentx -= 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
                    stdscr.refresh()
            elif key == "KEY_RIGHT":
                if currentx + 1 > renderx - 1:
                    stdscr.addstr(0, 0, "Cannot move out of boundary".ljust(40))
                    continue
                elif get_char(stdscr, currenty, currentx + 1) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions".ljust(40))
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currentx += 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
                    stdscr.refresh()
            elif key == "\n":
                if validate(stdscr, objects, start_y, end_y, renderx, rendery):
                    stdscr.addstr(0, 0, "Success".ljust(40))
                    stdscr.refresh()
                    return True
                else:
                    stdscr.addstr(0, 0, "Failed".ljust(40))
                    stdscr.refresh()
            elif key == " ":
                decoded_char = get_char(stdscr, currenty, currentx)
                if (currentx, currenty) not in blocked_coor:
                    stdscr.addstr(1, 0, "Not blocked")
                    if decoded_char == objects[0] or decoded_char == objects[4]:
                        stdscr.addstr(currenty, currentx, objects[1], color_selected)
                    elif decoded_char in objects[1:4]:
                        index = objects.index(decoded_char)
                        stdscr.addstr(currenty, currentx, objects[index + 1], color_selected)
                    else:
                        stdscr.addstr(0, 0, "Unexpected Exception")
                    stdscr.refresh()
                else:
                    stdscr.addstr(1, 0, "Blocked")
                    stdscr.addstr(currenty, currentx, "X", color_blocked)
                    currentx, currenty = lastx, lasty
                    stdscr.addstr(currenty, currentx, decoded_char, color_selected)
                    stdscr.refresh()
    if stdscr is None:
        return curses.wrapper(circuit_game)
    return circuit_game(stdscr)

if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    generate_circuit(10, 10, 5)