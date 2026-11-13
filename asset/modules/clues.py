collected_clues = {}


def add_clue(clue_name, clue_text):
    if clue_name not in collected_clues:
        collected_clues[clue_name] = clue_text


def get_clues():
    return collected_clues.copy()