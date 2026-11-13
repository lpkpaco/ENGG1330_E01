import curses, locale
from game import main
locale.setlocale(locale.LC_ALL, "")
def load_main_menu(menuscr):
    curses.start_color()
    #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    #curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    #color_normal = curses.color_pair(1)
    #color_selected = curses.color_pair(2)
    menuscr.clear()
    import pyfiglet
    titletbd = "ENGG1330-E01\nRadiation Doom"
    title = pyfiglet.figlet_format(titletbd, font="big", justify = "center", width = 80)
    for i, line in enumerate(title.splitlines()):
        menuscr.addstr(i, 0, line)
    menuscr.refresh()
    newgame = curses.newwin(5, 20, 9, 30)
    newgame.box()
    newgame.addstr(2, 4, "1. New Game")
    newgame.refresh()
    loadgame = curses.newwin(5, 20, 14, 30)
    loadgame.box()
    loadgame.addstr(2, 4, "2. Load Game")
    loadgame.refresh()
    menuscr.keypad(True)
    while True:
        ch = menuscr.getch()
        if ch in (ord("q"), ord("Q")):
            return
        if ch == ord("1"):
            main(menuscr)
            menuscr.clear()
            for i, line in enumerate(title.splitlines()):
                menuscr.addstr(i, 0, line)
            menuscr.refresh()
            newgame = curses.newwin(5, 20, 9, 30)
            newgame.box()
            newgame.addstr(2, 4, "1. New Game")
            newgame.refresh()
            loadgame = curses.newwin(5, 20, 14, 30)
            loadgame.box()
            loadgame.addstr(2, 4, "2. Load Game")
            loadgame.refresh()
        elif ch == ord("2"):
            pass
if __name__ == "__main__":
    curses.wrapper(load_main_menu)
