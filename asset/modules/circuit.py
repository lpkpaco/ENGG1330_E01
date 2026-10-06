def generate_circuit():
    import curses
    def main(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()