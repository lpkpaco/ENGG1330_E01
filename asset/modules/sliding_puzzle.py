def sliding_puzzle(): 
    import random
    number_list = ["00","01","02","03","04","05","06","07","08"]
    answer = ["01","02","03","04","05","06","07","08","00"]
    x = 0
    y = 0
    inversion_count = 0
    move_postion = ()
    random.shuffle(number_list)
    #inversion test for solvability
    while inversion_count == 0 or inversion_count%2 != 0:
        a = number_list[:]
        a.remove("00")
        a = list(map(int,a))
        for i in a[:len(a)-1]:
            for k in a[a.index(i)+1:]:
                if k < i:
                    inversion_count += 1
        if inversion_count % 2 != 0:
            random.shuffle(number_list)
            inversion_count = 0
    print("\n"*2)
    matrix = []
    temp = number_list[:]
    while number_list != []:
        matrix.append(number_list[:3])
        number_list = number_list[3:]
    number_list = temp[:]


    while number_list != answer:
        for i in matrix:
            print(f"|{i[0]}|{i[1]}|{i[2]}|")
        move = input("Move a tile:")
        #fix single digit input
        if move in ["0","1","2","3","4","5","6","7","8","9"]:
            move = "0" + move
        #out of range
        if move not in number_list:
            print("Tile not found")
            continue
        for i in matrix:
            if move in i:
                y = matrix.index(i)
                for k in i:
                    if move == k:
                        x = i.index(k)
        move_postion = (x,y) #(columns,row)
        for i in matrix:
                if "00" in i:
                    y = matrix.index(i)
                    for k in i:
                        if "00" == k:
                            x = i.index(k)
        #eliminate non-adjacent
        if move_postion not in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
            print("Tile not adjacent to blank")
            continue
        if x == 0 and move_postion not in [(x+1,y),(x,y+1),(x,y-1)]:
            print("Tile not adjacent to blank")
            continue
        if x == 2 and move_postion not in[(x-1,y),(x,y+1),(x,y-1)]:
            print("Tile not adjacent to blank")
            continue
        if y == 0 and move_postion not in[(x,y+1),(x-1,y),(x+1,y)]:
            print("Tile not adjacent to blank")
            continue
        if y == 2 and move_postion not in[(x,y-1),(x-1,y),(x+1,y)]:
                print("Tile not adjacent to blank")
                continue
        original_position = number_list.index(move)
        number_list[number_list.index("00")] = move
        number_list[original_position] = "00"
        temp = number_list[:]
        matrix = []
        while number_list != []:
                matrix.append(number_list[:3])
                number_list = number_list[3:]
        number_list = temp[:]
    print("SOLVED")
    for i in matrix:
        print(f"|{i[0]}|{i[1]}|{i[2]}|")
    return True

if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    sliding_puzzle()