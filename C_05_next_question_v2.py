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
    """
    Gets the gods and assigns them to what they are meant for
    God name to god name
    Correct God Duty to Correct God Duty
    etc
    """

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

        # stores the variables
        # basically allows it to be passed between functions by using "(variable).get()"
        self.q_wanted = IntVar()
        self.q_wanted.set(q_num)

        self.q_answered = IntVar()
        self.q_answered.set(0)

        self.label_frame = Frame(self.quiz_frame)
        self.label_frame.grid(padx=10, pady=10, row=0)

        self.correct_answer = StringVar()

        # list of the game menu labels and their specifications (gm means game menu)
        # text | font | row
        gm_labels = [
            [f"Question x / y", ("Arial", "18", "bold")],
            [f"god name", ("Arial", "18", "bold")],
            ["Select an Option below:", ("Arial", "14")],
        ]

        # create labels and add them to a reference list (mm means main menu)
        gm_labels_ref = []

        for count, item in enumerate(gm_labels):
            make_label = Label(self.label_frame, text=item[0], font=item[1],
                               pady=10, padx=10, justify="left",
                               wraplength=350)
            make_label.grid(row=count, pady=10, padx=10)

            gm_labels_ref.append(make_label)

        self.heading_label = gm_labels_ref[0]
        self.god_label = gm_labels_ref[1]
        self.answer_label = gm_labels_ref[2]

        # makes the three option boxes
        self.options_frame = Frame(self.quiz_frame)
        self.options_frame.grid(padx=10, pady=10)

        # placeholder text / id
        options = [
            [f"correct_duty"],
            [f"incorrect_1"],
            [f"incorrect_2"],
        ]

        # the possible columns the buttons could be in
        possible_columns = [0, 1, 2]

        # create labels and add them to a reference list
        self.option_labels_ref = []

        # makes the buttons for the duties
        for count, item in enumerate(options):
            option_label = Button(self.options_frame, text=item[0], font=("Arial", 12),
                                  pady=10, padx=10, justify="left",
                                  wraplength=350)
            # randomises the column so that the correct button will appear
            # in different places instead of just the left most place
            column = random.choice(possible_columns)

            option_label.grid(row=0, column=column, pady=5, padx=5)

            self.option_labels_ref.append(option_label)

            # removes it from the possible columns list, so there are
            # no buttons that stack on top of each other
            possible_columns.remove(column)

        self.button_1 = self.option_labels_ref[0]
        self.button_2 = self.option_labels_ref[1]
        self.button_3 = self.option_labels_ref[2]


        # creating the frame
        self.misc_button_frame = Frame(self.quiz_frame)
        self.misc_button_frame.grid(padx=10, pady=10, row=2)

        # frame | button | bg | command
        misc_buttons = [
            [self.misc_button_frame, "Next Question", "#add8e6", self.new_question]
        ]

        misc_button_ref = []

        # makes the buttons for the duties
        for item in misc_buttons:
            misc_button = Button(item[0], text=item[1], font=("Arial", 16, "bold"),
                                 bg=item[2], pady=10, padx=10, justify="left",
                                 wraplength=350, command=item[3])
            misc_button.grid(row=1, column=0, padx=5, pady=5)

            misc_button_ref.append(misc_button)

        # assigns the next question button to a variable and disables it
        # so the user has to answer the question first before pressing "next question"
        self.next_question = misc_button_ref[0]
        self.next_question.config(state=DISABLED)


        # sets up the first question
        self.new_question()

    def new_question(self):
        """
        Changes the question and selects a new god and two new duties when the user
        presses "next question"
        """

        god_name, correct_duty, incorrect_1, incorrect_2 = get_question_gods()

        self.next_question.config(state=DISABLED)
        for item in self.option_labels_ref:
            item.config(state=NORMAL)

        # retrieves the amount of questions the user has answered and played
        q_wanted = self.q_wanted.get()
        self.q_wanted.set(q_wanted)

        q_answered = self.q_answered.get()
        self.q_answered.set(q_answered)

        # update heading
        self.heading_label.config(text=f"Question {q_answered + 1} of {q_wanted}")
        self.god_label.config(text=f"{god_name}", fg="#000000")

        # the duties that have been selected
        options = [
            [f"{correct_duty}"],
            [f"{incorrect_1}"],
            [f"{incorrect_2}"],
        ]

        self.correct_answer.set(correct_duty)

        columns = [1, 2, 3]

        buttons = [self.button_1, self.button_2, self.button_3]

        for count, item in enumerate(buttons):
            new_duty = random.choice(options)
            # print(f"selected: {new_duty}")
            column = random.choice(columns)
            # print(f"column: {column}")
            buttons[count].config(text=new_duty[0], command=partial(self.answer_checker, new_duty[0]))
            buttons[count].grid(column=column)
            # print(f"{count}")

            options.remove(new_duty)
            columns.remove(column)

        print(f"{correct_duty}")

    # checks the answer
    def answer_checker(self, button_pressed):
        """

        """

        correct_answer = self.correct_answer.get()

        # compares the answer based on their ids
        if button_pressed == correct_answer:
            self.god_label.configure(text="Correct!", fg="#009900")
        else:
            self.god_label.configure(text="Incorrect!", fg="#990000")

        # disables all the buttons after a button was pressed/answer
        # was checked to prevent cheating
        for item in self.option_labels_ref:
            item.config(state=DISABLED)

        self.next_question.config(state=NORMAL)

        # adds one to the questions answered
        q_answered = self.q_answered.get()
        q_answered += 1
        self.q_answered.set(q_answered)

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Play(5)
    root.mainloop()
