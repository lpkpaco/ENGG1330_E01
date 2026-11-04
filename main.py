from title_menu import load_main_menu
from asset.modules.circuit import generate_circuit
from asset.modules.filehandle import readsave
from asset.modules.sliding_puzzle_curses import sliding_puzzle
from asset.modules.sokoban_puzzle import sokoban_puzzle
from title_menu import load_main_menu
import curses, locale
locale.setlocale(locale.LC_ALL, "")

if __name__ == "__main__":
    curses.wrapper(load_main_menu)