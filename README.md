# ENGG1330_E01
ENGG1330 Group E01

## TODO LIST

- [ ] Puzzle 1: Circuit Game:
    - [X] Basic coding
    
    #### How to call functions:

    `get_char([screen], [x], [y])`
    
    Usage: Returns the decoded utf-8 character at the target coordinates. Type: str
    - screen = Pass the current Curses screen to it. Type: Curses screen
    - x and y = Coordinates of the target position that you want to check. Type: int
    - `e.g. character_at_3_2 = get_char(stdscr, 3, 2)`

    `validate([screen], [character_list], [start_y], [end_y], [width], [height])`
    
    Usage: Returns the status of whether the circuit is complete from the starting point to the ending point. Type: bool
    - screen = Pass the current Curses screen to it. Type: Curses screen
    - character_list = Objects list is passed as the default character list in this script. <br>
    `objects = ["█", "↑", "↓", "←", "→", "☇", "⚑"]` <br>
    Type = list
    - start_y and end_y = The y-coordinates of the starting and ending point. Type = int
    - width and height = Dimensions of the rendered game screen. Type: int

    `e.g. if validate(stdscr, objects, 6, 7, 15, 10): #Returns True or False`

    `generate_circuit([difficulty], [width], [height])`
    
    Usage: Starts the circuit puzzle. Returns True if solved puzzle.
    - difficulty = Number of blocked tiles. Type: int
    - width and height = Dimensions of the rendered game screen. Type: int

    #### Todo:
    - [ ] Player need to complete the game within a timer

    #### Known bugs:
    - [ ] When revealing a tile and the tile is blocked, the item at the last position will be erased and replaced with a block
    - [ ] There is a chance where a stage without any solutions will be generated

- [ ] Puzzle 2: 3x3 Sliding game
    - [X] Basic coding

    #### How to call functions
    `sliding_puzzle()`

    Usage: Generates a 3x3 sliding puzzle game. Returns True if solved puzzle.

    #### Todo:
    - [X] Write the game with the Curses module for less repetitive output and easier integration flow

    #### Known bugs:
    - [X] Has anyone ever solved the puzzle (?)
    - [ ] The game hangs if the initial random shuffle results in an already solved state

- [ ] Puzzle 3: Sokoban puzzle
    - [X] Basic coding

    #### How to call functions
    `sokoban_puzzle()`

    Usage: Generates a 5x5 grid-based Sokoban puzzle. Returns True if solved puzzle.
    - controls: W/A/S/D to move, R to reset, Q to quit.

    #### Known bugs:
    - [ ] None at the moment (Tested locally, movement and reset logic work).

- [ ] Puzzle 4: Shortwave Radio Tuning
- [X] Plot + Hidden Ending
- [ ] Inventory/status mechanism
- [ ] Map Function
- [ ] Save/load game functionality
- [ ] Game menu
- [ ] Puzzle-main game integration
