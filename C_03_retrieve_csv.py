import csv
import random


def get_gods():
    """
    Retrieves the gods and duties from a csv file
    and puts them into a list
    """

    # retrieves gods from csv file and put them in a list
    file = open("gods.csv", "r")
    all_gods = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_gods.pop(0)

    return all_gods


def get_question_gods():
    for item in range(0, 3):
        incorrect_duties = []
        gods = get_gods()

        god_selected = random.choice(gods)
        gods.remove(god_selected)

        for item in range(0, 2):
            random_duties = random.choice(gods)
            incorrect_duties.append(random_duties[1])
            gods.remove(random_duties)

        print(f"God Selected: {god_selected[0]}"
              f"\nCorrect Duty: {god_selected[1]}"
              f"\nIncorrect Duty 1: {incorrect_duties[0]}"
              f"\nIncorrect Duty 2: {incorrect_duties[1]}\n")


get_question_gods()
