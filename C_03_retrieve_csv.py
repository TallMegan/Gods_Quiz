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

gods = [[0, "Zeus", "Lightning"],
        [1, "Poseidon", "Ocean"],
        [2, "Hades", "Underworld"]]

possible_gods = gods
incorrect_duties = []
random_duties = []

while len(incorrect_duties) < 3:
    god_selected = random.choice(gods)
    god_name = god_selected[1]
    correct_duty = god_selected[2]
    incorrect_duties = []

    random_duties = random.choice(possible_gods)
    incorrect_duties.append(random_duties[2])

    for item in incorrect_duties:

        if random_duties[2] in incorrect_duties:
            random

    print(f"God Selected: {god_name}"
          f"\nCorrect Duty: {correct_duty}"
          f"\nIncorrect Duty 1: {incorrect_duties[0]}"
          f"\nIncorrect Duty 2: {incorrect_duties[0]}\n")
