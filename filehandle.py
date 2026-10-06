def readsave():
    from os import listdir
    from contextlib import chdir
    with chdir('saves'):
        filelist = listdir()
        is_save = []
        for file in filelist:
            if file.endswith('.json'):
                is_save.append(file)
        return is_save

def writesave(progress):
    from contextlib import chdir
    from pathlib import Path
    try:
        with chdir("saves"):
            prefix = "save"
            i = 1
            while True:
                tmp = Path(prefix + str(i) + ".json")
                if tmp.exists():
                    i += 1
                    continue
                else:
                    filename = prefix + str(i) + ".json"
                    break
            f = open(filename, "w+")
            f.write("{" + compile(progress) + "}")
            f.close()
            print("File saved")
            return True
    except:
        from os import mkdir
        mkdir("saves")
        print("saves/ directory not found. Created new saves/ directory. Try rewriting save again.")
        return False

def compile(progress):
    pass