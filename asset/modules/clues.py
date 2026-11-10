collected_clues = {}


def add_clue(clue_name, clue_text):
    # Save a clue only if it has not been collected before.
    if clue_name not in collected_clues:
        collected_clues[clue_name] = clue_text


def get_clues():
    # Return all collected clues.
    return collected_clues.copy()