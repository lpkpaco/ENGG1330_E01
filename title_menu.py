import curses, locale
from game import main, wait_for_size
from asset.modules.filehandle import readsave, loadsave, deletesaves
locale.setlocale(locale.LC_ALL, "")

def draw_main_menu(menuscr, title):
    menuscr.clear()
    import pyfiglet
    titletbd = "7 DAYS"
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

def pick_save(menuscr):
    while True:
        if not wait_for_size(menuscr):
            return None
        files = readsave()
        menuscr.clear()
        menuscr.addstr(1, 2, "LOAD GAME")
        if files == []:
            menuscr.addstr(3, 2, "No saves found.")
            menuscr.addstr(5, 2, "Press any key to go back.")
            menuscr.refresh()
            menuscr.getch()
            return None
        shown = files[::-1][:9]
        for i in range(len(shown)):
            menuscr.addstr(3 + i, 2, str(i + 1) + ". " + shown[i])
        menuscr.addstr(14, 2, "Press 1-9 to load, D to delete all saves, Q to go back.")
        menuscr.refresh()
        ch = menuscr.getch()
        if ch in (ord("q"), ord("Q")):
            return None
        if ch in (ord("d"), ord("D")):
            menuscr.addstr(16, 2, "Delete ALL saves? Y to confirm, N to cancel.")
            menuscr.refresh()
            while True:
                confirm = menuscr.getch()
                if confirm in (ord("y"), ord("Y")):
                    deletesaves()
                    menuscr.clear()
                    menuscr.addstr(3, 2, "All saves deleted.")
                    menuscr.addstr(5, 2, "Press any key to go back.")
                    menuscr.refresh()
                    menuscr.getch()
                    return None
                if confirm in (ord("n"), ord("N"), ord("q"), ord("Q")):
                    break
            continue
        if ch >= ord("1") and ch <= ord("9"):
            idx = ch - ord("1")
            if idx < len(shown):
                data = loadsave(shown[idx])
                if data == None:
                    menuscr.addstr(16, 2, "Could not read that save.")
                    menuscr.refresh()
                    menuscr.getch()
                    continue
                return data

def load_main_menu(menuscr):
    curses.start_color()
    menuscr.keypad(True)
    import pyfiglet
    titletbd = "7 Days"
    title = pyfiglet.figlet_format(titletbd, font="big", justify="center", width=80)
    while True:
        if not wait_for_size(menuscr):
            return
        draw_main_menu(menuscr, title)
        ch = menuscr.getch()
        if ch in (ord("q"), ord("Q")):
            return
        if ch == curses.KEY_RESIZE:
            continue
        if ch == ord("1"):
            main(menuscr)
        elif ch == ord("2"):
            data = pick_save(menuscr)
            if data != None:
                main(menuscr, save=data)

if __name__ == "__main__":
    curses.wrapper(load_main_menu)
