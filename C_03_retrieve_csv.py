import csv
import random


# def get_gods():
#     """
#     Retrieves the gods and duties from a csv file
#     and puts them into a list
#     """
#
#     # retrieves gods from csv file and put them in a list
#     file = open("gods.csv", "r")
#     all_gods = list(csv.reader(file, delimiter=","))
#     file.close()
#
#     # remove the first row
#     all_gods.pop(0)
#
#     return all_gods
#
#
# gods = get_gods()

gods = [["Zeus", "Lightning"], ["Poseidon", "Ocean"], ["Hades", "Underworld"]]

for item in range(0, 3):
    god_selected = random.choice(gods)
    god_name = god_selected[0]
    correct_duty = god_selected[1]

    incorrect_duties = []
    cycles = 0
    while cycles < 2:
        random_duties = random.choice(gods)
        if random_duties[1] not in incorrect_duties:
            incorrect_duties.append(random_duties[1])
            cycles += 1
        else:
            continue

    print(f"God Selected: {god_name}"
          f"\nCorrect Duty: {correct_duty}"
          f"\nIncorrect Duty 1: {incorrect_duties[0]}"
          f"\nIncorrect Duty 2: {incorrect_duties[1]}\n")
