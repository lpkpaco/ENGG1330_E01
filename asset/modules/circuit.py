def generate_circuit(difficulty):
    import curses, secrets, locale
    locale.setlocale(locale.LC_ALL, "")
    def main(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()
        objects = ["█", "◯", "⊖", "⌽", "☇", "⚑"]
        marked = []
        for y in range(4, 20):
            for x in range(0, 80):
                stdscr.addstr(y, x, objects[0])
        start_y = secrets.SystemRandom().randint(4, 20)
        end_y = secrets.SystemRandom().randint(4, 20)
        stdscr.addstr(start_y, 0, objects[4])
        stdscr.addstr(end_y, 79, objects[5])
        blocked_coor = []
        for i in range(0, difficulty):
            while True:
                y = secrets.SystemRandom().randint(4, 20)
                if y != start_y and y != end_y:
                    break
                else:
                    continue
            x = secrets.SystemRandom().randint(4, 20)
            blocked_coor.append((x, y))
        if __name__ == "__main__":
            print(blocked_coor)
        stdscr.refresh()
        stdscr.getch()
    curses.wrapper(main)

if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    generate_circuit(100)