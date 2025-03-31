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


gods = get_gods()

print(gods)
