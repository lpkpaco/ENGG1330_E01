from pathlib import Path

def _plot_path():
    here = Path(__file__).resolve().parent
    for candidate in (here / "plot.txt", here.parent / "puzzles" / "plot.txt"):
        if candidate.is_file():
            return candidate
    return here / "plot.txt"

def readplot(linenumber=None):
    with open(_plot_path(), "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f]
    if linenumber is None:
        return lines
    if 0 <= linenumber < len(lines):
        return lines[linenumber].strip()
    return ""
