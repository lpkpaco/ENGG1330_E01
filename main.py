from title_menu import load_main_menu
from asset.puzzles.circuit import generate_circuit
from asset.puzzles.filehandle import readsave
from asset.puzzles.sliding_puzzle_curses import sliding_puzzle
from asset.puzzles.sokoban_puzzle import sokoban_puzzle
from title_menu import load_main_menu
import curses, locale
locale.setlocale(locale.LC_ALL, "")

if __name__ == "__main__":
    curses.wrapper(load_main_menu)