import csv
import random
from tkinter import *


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


class StartGame:
    """
    gods quiz main menu
    """

    def __init__(self):
        """
        gets the number of questions from the user
        """

        # upon user clicking the entry box,
        # it removes the placeholder
        def on_click(event):
            self.num_questions_entry.configure(state=NORMAL)
            self.num_questions_entry.delete(0, END)

            # make the callback only work once
            self.num_questions_entry.unbind('<Button-1>', self.on_click_id)

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = "Welcome to my quiz about Green and Roman Gods!" \
                       " Every round there will be a randomly selected god and 3 buttons" \
                       " will appear, 2 of them will be 2 random god's" \
                       " jobs/duties and 1 will be the correct one for the god that was " \
                       "randomly selected. Your job is to select the right one.\n\n" \
                       "Good Luck!\n\n" \
                       "To begin, enter how many questions you'd like into the text box below."

        choose_question = "How many questions would you like?"

        # list of the main menu labels and their specifications (mm means main menu)
        # text | font
        mm_labels = [
            ["Gods Quiz", ("Arial", "16", "bold")],
            [intro_string, ("Arial", "12")],
            [choose_question, ("Arial", "12", "bold")]
        ]

        # create labels and add them to a reference list (mm means main menu)
        mm_labels_ref = []
        for count, item in enumerate(mm_labels):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               pady=10, padx=10, justify="left",
                               wraplength=350)
            make_label.grid(row=count)

            mm_labels_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = mm_labels_ref[2]

        # frame so that entry box and button ca be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                         width=20)
        self.num_questions_entry.config(bg="#a9a9a9")

        # inserts the placeholder
        self.num_questions_entry.pack()
        self.num_questions_entry.insert(0, "How many questions would you like?")
        self.num_questions_entry.configure(state=DISABLED)

        # removes the placeholder
        self.on_click_id = self.num_questions_entry.bind('<Button-1>', on_click)

        self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)

        # creates play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_question)

        self.play_button.grid(row=1)

    def check_question(self):
        """
        checks that the number of questions
        is valid (above 0 and an integer, not a letter)
        """
        q_wanted = self.num_questions_entry.get()

        has_errors = "no"

        # reset label and entry box (for when users come back to home screen)
        try:
            q_wanted = int(q_wanted)

            if q_wanted > 0:
                self.num_questions_entry.delete(0, END)
                self.num_questions_entry.config(bg="#a9a9a9")
                Play(q_wanted)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

            # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(fg="#000000", font=("Arial", "12", "bold"),
                                     text="How many questions would you like?")
            self.num_questions_entry.delete(0, END)
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.insert(0, "Please enter a whole number (>0)")

            # removes the placeholder
            self.on_click_id = self.num_questions_entry.bind('<Button-1>')


class Play:

    def __init__(self, q_num):

        self.quiz_box = Toplevel()

        self.quiz_frame = Frame(self.quiz_box)
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

        # makes the three option boxes
        self.options_frame = Frame(self.quiz_frame)
        self.options_frame.grid(padx=10, pady=10)

        # text | font
        option_labels = [
            [f"{correct_duty}", ("Arial", "12")],
            [f"{incorrect_1}", ("Arial", "12")],
            [f"{incorrect_2}", ("Arial", "12")],
        ]

        # the possible columns the buttons could be in
        possible_columns = [0, 1, 2]

        # create labels and add them to a reference list
        option_labels_ref = []
        for count, item in enumerate(option_labels):
            option_label = Button(self.options_frame, text=item[0], font=item[1],
                                  pady=10, padx=10, justify="left",
                                  wraplength=350)

            # randomises the column so that the correct button will appear
            # in different places instead of just the left most place
            column = random.choice(possible_columns)

            option_label.grid(row=0, column=column, pady=5, padx=5)

            option_labels_ref.append(option_label)

            # removes it from the possible columns list, so there are
            # no buttons that stack on top of each other
            possible_columns.remove(column)

        correct_button = option_labels_ref[0]
        incorrect_button1 = option_labels_ref[1]
        incorrect_button2 = option_labels_ref[2]


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
