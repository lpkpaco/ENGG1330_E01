import json
from pathlib import Path

MAX_SAVES = 9


def _project_root():
    return Path(__file__).resolve().parents[2]


def _saves_dir():
    path = _project_root() / "saves"
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_save_name(name):
    if name == None:
        return None
    name = str(name).strip()
    if name.lower().endswith(".json"):
        name = name[:-5]
    cleaned = ""
    for ch in name:
        if ch in '<>:"/\\|?*':
            cleaned = cleaned + "_"
        elif ord(ch) >= 32:
            cleaned = cleaned + ch
    name = cleaned.strip(" .")
    if name == "":
        return None
    if len(name) > 40:
        name = name[:40].strip()
    return name + ".json"


def readsave():
    files = []
    folder = _saves_dir()
    items = []
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() == ".json":
            items.append(item)
    items.sort(key=lambda p: p.stat().st_mtime)
    for item in items:
        files.append(item.name)
    return files


def _oldest_save():
    files = readsave()
    if files == []:
        return None
    return files[0]


def unused_save_name():
    existing = set(readsave())
    i = 1
    while True:
        name = "save" + str(i) + ".json"
        if name not in existing:
            return name
        i = i + 1


def writesave(progress, filename=None):
    try:
        folder = _saves_dir()
        filename = clean_save_name(filename)
        if filename == None:
            filename = unused_save_name()
        path = folder / Path(filename).name
        existing = readsave()
        if (not path.exists()) and len(existing) >= MAX_SAVES:
            oldest = _oldest_save()
            if oldest != None and oldest != filename:
                old_path = folder / oldest
                if old_path.exists():
                    old_path.unlink()
        f = open(path, "w", encoding="utf-8")
        json.dump(progress, f, indent=4, ensure_ascii=False)
        f.close()
        return filename
    except OSError:
        return None


def deletesaves():
    count = 0
    folder = _saves_dir()
    for item in list(folder.iterdir()):
        if item.is_file() and item.suffix.lower() == ".json":
            item.unlink()
            count = count + 1
    return count


def loadsave(filename):
    try:
        path = _saves_dir() / Path(filename).name
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data
    except (OSError, json.JSONDecodeError, TypeError):
        return None


if __name__ == "__main__":
    import pyfiglet
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    print(writesave({"day": 1, "hp": 100}))
    print(readsave())
