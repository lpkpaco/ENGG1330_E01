def sliding_game():
    import random
    number_list = ["00","01","02","03","04","05","06","07","08"]
    answer = ["01","02","03","04","05","06","07","08","00"]
    x = 0
    y = 0
    inversion_count = 0
    move_postion = ()
    random.shuffle(number_list)
    a = list(map(int,number_list))
    while inversion_count == 0 or inversion_count%2 != 0:
        for i in a:
            for k in a[i:]:
                if k < i:
                    inversion_count += 1
        if inversion_count % 2 != 0:
            random.shuffle(number_list)
            continue
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
        if move in ["0","1","2","3","4","5","6","7","8","9"]:
            move = "0" + move
        #out of range input
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
        zero_postion = (x,y)
        #non-adjacent
        if move_postion not in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
            print("Not adjacent to blank tile")
            continue
        if x == 0 and move_postion not in [(x+1,y),(x,y+1),(x,y-1)]:
            print("Not adjacent to blank tile")
            continue
        if x == 2 and move_postion not in[(x-1,y),(x,y+1),(x,y-1)]:
            print("Not adjacent to blank tile")
            continue
        if y == 0 and move_postion not in[(x,y+1),(x-1,y),(x+1,y)]:
            print("Not adjacent to blank tile")
            continue
        if y == 2 and move_postion not in[(x,y-1),(x-1,y),(x+1,y)]:
            print("Not adjacent to blank tile")
            continue
        original_position = number_list.index(move)
        number_list[number_list.index("00")] = move
        number_list[original_position] = "00"
        temp = number_list[:]
        matrix = []
        while number_list != []:
                matrix.append(number_list[:3])
                number_list = number_list[3:]
        #print(matrix)
        number_list = temp[:]
        #print(number_list)
    print("SOLVED")
    return True