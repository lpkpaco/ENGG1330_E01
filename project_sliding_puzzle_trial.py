#This code is likely deprecated btw
#use sliding_game_3x3.py
import random
number_list = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
answer = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
#shuffle
random.shuffle(number_list)
print("\n"*2)
matrix = []
temp = number_list[:]
while number_list != []:
    matrix.append(number_list[:4])
    number_list = number_list[4:]
        #print(matrix)
        #print(number_list)
number_list = temp[:]
for i in matrix:
    print(f"|{i[0]}|{i[1]}|{i[2]}|{i[3]}|")
    #print(number_list)

while number_list != answer:
    try:
        move = input("Move a tile:")
        original_position = number_list.index(move)
    except ValueError:
        print("Input not in number list")
        continue
    number_list[number_list.index("00")] = move
    number_list[original_position] = "00"
    temp = number_list[:]
    matrix = []
    while number_list != []:
            matrix.append(number_list[:4])
            number_list = number_list[4:]
    print(matrix)
    number_list = temp[:]
    print(number_list)

    for i in matrix:
        print(f"|{i[0]}|{i[1]}|{i[2]}|{i[3]}|")

