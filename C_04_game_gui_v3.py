import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


def get_gods():
    """
    Retrieves the gods and duties from a csv file
    and puts them into a list
    """

    # retrieve gods from csv file and put them in a list
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

        god_name = god_selected[0]
        correct_duty = god_selected[1]
        incorrect_duty_1 = incorrect_duties[0]
        incorrect_duty_2 = incorrect_duties[1]

        return god_name, correct_duty, incorrect_duty_1, incorrect_duty_2


class Play:

    def __init__(self, q_num):

        self.quiz_frame = Frame()
        self.quiz_frame.grid(padx=10, pady=10)

        # stores the q_wanted and sets it to the q_num
        # basically allows it to be passed between functions by using "(variable).get()"
        q_wanted = IntVar()
        q_wanted.set(q_num)

        god_name, correct_duty, incorrect_1, incorrect_2 = get_question_gods()

        # list of the game menu labels and their specifications (gm means game menu)
        # text | font | justify
        gm_labels = [
            [f"{god_name}", ("Arial", "18", "bold")],
            ["Select an Option below:", ("Arial", "14")],
        ]

        # create labels and add them to a reference list (mm means main menu)
        gm_labels_ref = []
        for count, item in enumerate(gm_labels):
            make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                               pady=10, padx=10, justify="left",
                               wraplength=350)
            make_label.grid(row=count)

            gm_labels_ref.append(make_label)

        self.answer_label = gm_labels_ref[1]

        # makes the three option boxes
        self.options_frame = Frame(self.quiz_frame)
        self.options_frame.grid(padx=10, pady=10)

        # text | font | id
        options = [
            [f"{correct_duty}", ("Arial", "12"), "1"],
            [f"{incorrect_1}", ("Arial", "12"), "2"],
            [f"{incorrect_2}", ("Arial", "12"), "3"],
        ]

        # stores the correct answer
        self.correct_answer = StringVar()
        self.correct_answer.set("1")

        # the possible columns the buttons could be in
        possible_columns = [0, 1, 2]

        # create labels and add them to a reference list
        option_labels_ref = []

        # checks the answer
        def answer_checker(button_pressed):
            self.correct_answer = self.correct_answer.get()
            if button_pressed == self.correct_answer:
                self.answer_label.configure(text="Correct!", fg="#009900")
            else:
                self.answer_label.configure(text="Incorrect!", fg="#990000")

        # makes the buttons for the duties
        for count, item in enumerate(options):
            option_label = Button(self.options_frame, text=item[0], font=item[1],
                                  pady=10, padx=10, justify="left",
                                  wraplength=350, command=partial(answer_checker, item[2]))

            # randomises the column so that the correct button will appear
            # in different places instead of just the left most place
            column = random.choice(possible_columns)

            option_label.grid(row=0, column=column, pady=5, padx=5)

            option_labels_ref.append(option_label)

            # removes it from the possible columns list, so there are
            # no buttons that stack on top of each other
            possible_columns.remove(column)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Play(5)
    root.mainloop()
