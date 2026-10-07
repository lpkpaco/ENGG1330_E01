# ENGG1330_E01
ENGG1330 Group E01

## TODO LIST

- [ ] Puzzle 1: Circuit Game:
    - [X] Basic coding
    
    #### How to call functions:

    **get_char([screen], [x], [y])**
    
    Usage: Returns the decoded utf-8 character at the target coordinates. Type: Str
    - screen = Pass the current Curses screen to it. Type: Curses screen
    - x and y = Coordinates of the target position that you want to check. Type: Int
    - `e.g. character_at_3_2 = get_char(stdscr, 3, 2)`

    #### Features:
    - [ ] Player need to complete the game within a timer

    #### Known bugs:
    - [ ] When revealing a tile and the tile is blocked, the item at the last position will be erased and replaced with a block
    - [ ] There is a chance where a stage without any solutions will be generated

- [ ] Puzzle 2: TBD
- [ ] Puzzle 3: TBD
- [ ] Puzzle 4: TBD
- [ ] Plot + hidden ending
- [ ] Round-based mechanism and inventory/status mechanism
- [ ] Save/load game functionality
- [ ] Game menu
- [ ] Puzzle-main game integration