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


def generate_circuit(difficulty):
    import curses, secrets, locale
    locale.setlocale(locale.LC_ALL, "")
    def circuit_game(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        color_normal = curses.color_pair(1)
        color_selected = curses.color_pair(2)
        stdscr.clear()
        objects = ["█", "↑", "↓", "←", "→", "☇", "⚑"]
        marked = []
        for y in range(4, 20):
            for x in range(0, 80):
                stdscr.addstr(y, x, objects[0])
        start_y = secrets.SystemRandom().randint(4, 19)
        end_y = secrets.SystemRandom().randint(4, 19)
        stdscr.addstr(start_y, 0, objects[5])
        stdscr.addstr(end_y, 79, objects[6])
        blocked_coor = []
        for i in range(0, difficulty):
            while True:
                y = secrets.SystemRandom().randint(4, 19)
                if y == start_y and y == end_y:
                    continue
                x = secrets.SystemRandom().randint(1, 78)
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
                    stdscr.addstr(0, 0, "Cannot move out of boundary or move onto blocked positions")
                    continue
                elif get_char(stdscr, currenty - 1, currentx) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions")
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currenty -= 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
                    stdscr.refresh()
            elif key == "KEY_DOWN":
                if currenty + 1 > 19:
                    stdscr.addstr(0, 0, "Cannot move out of boundary")
                    continue
                elif get_char(stdscr, currenty + 1, currentx) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions")
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
                    stdscr.addstr(0, 0, "Cannot move out of boundary")
                    continue
                elif get_char(stdscr, currenty, currentx - 1) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions")
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currentx -= 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
                    stdscr.refresh()
            elif key == "KEY_RIGHT":
                if currentx + 1 > 79:
                    stdscr.addstr(0, 0, "Cannot move out of boundary")
                    continue
                elif get_char(stdscr, currenty, currentx + 1) == "X":
                    stdscr.addstr(0, 0, "Cannot move onto blocked positions")
                    continue
                else:
                    stdscr.chgat(currenty, currentx, 1, color_normal)
                    lastx = currentx
                    lasty = currenty
                    currentx += 1
                    stdscr.chgat(currenty, currentx, 1, color_selected)
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
                    stdscr.addstr(currenty, currentx, "X", color_normal)
                    currentx, currenty = lastx, lasty
                    stdscr.addstr(currenty, currentx, decoded_char, color_selected)
                    stdscr.refresh()
    curses.wrapper(circuit_game)

if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    generate_circuit(1000)