import csv
import random
from tkinter import *
from functools import partial


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
    gets the gods and sorts them into their correct lists
    and what button they should be allocated to
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

def recolour(list, colour):
    """
    recolours all the components inside
    the list to a specific colour
    """

    recolour_list = list
    background = colour

    # recolours all the components
    for item in recolour_list:
        item.config(bg=background)

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
            self.num_questions_entry.config(state="normal")
            self.num_questions_entry.delete(0, END)

            # make the callback only work once
            self.num_questions_entry.unbind('<Button-1>', self.on_click_id)

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = "Welcome to my quiz about Greek and Roman Gods!" \
                       " Every round there will be a randomly selected god and 3 buttons" \
                       " will appear, 2 of them will be 2 random god's" \
                       " jobs/duties and 1 will be the correct one for the god that was " \
                       "randomly selected. Your job is to select the right one.\n\n" \
                       "Good Luck!\n\n" \
                       "To begin, enter how many questions you'd like into the text box below."

        choose_question = "How many questions?"

        # list of the main menu labels and their specifications (mm means main menu)
        # text | font | justify
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

        self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                         width=20)
        self.num_questions_entry.config(bg="#a9a9a9")

        # inserts the placeholder
        self.num_questions_entry.pack()
        self.num_questions_entry.insert(0, "How many questions would you like?")
        self.num_questions_entry.config(state="normal")

        # removes the placeholder
        self.on_click_id = self.num_questions_entry.bind('<Button-1>', on_click)

        self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)

        # creates play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_question)

        self.play_button.grid(row=1)

        # recolours everything to have a background colour
        recolour_list = [self.start_frame, self.choose_label, self.entry_area_frame,
                         mm_labels_ref[0], mm_labels_ref[1]]

        recolour(recolour_list, "#DAE8FC")

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

                # makes the start menu disappear
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

            # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(fg="#000000", font=("Arial", "12", "bold"),
                                     text="How many questions?")
            self.num_questions_entry.delete(0, END)
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.insert(0, "Please enter a num (>0)")

            # removes the placeholder
            self.on_click_id = self.num_questions_entry.bind('<Button-1>')

class Play:

    """
    main part of the game
    """

    def __init__(self, q_num):

        # creates the play window
        self.quiz_box = Toplevel()
        self.quiz_frame = Frame(self.quiz_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # stores the variables
        # basically allows it to be passed between functions by using "(variable).get()"
        self.correct_answer = StringVar()

        self.q_wanted = IntVar()
        self.q_wanted.set(q_num)

        self.q_answered = IntVar()
        self.q_answered.set(0)

        self.correct_answers = IntVar()
        self.correct_answers.set(0)

        # sets up the correct answer streak stat
        self.correct_streak = IntVar()
        self.correct_streak.set(0)

        # sets up streaks
        self.first_streak = "yes"
        self.correct_streak = 0
        self.highest_streak = 0

        # creates the label frame
        self.label_frame = Frame(self.quiz_frame)
        self.label_frame.grid(padx=10, pady=10, row=0)

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

        # creates the list for the buttons to be disabled later
        # on once the game is completed
        self.buttons_to_be_disabled = []

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
            self.buttons_to_be_disabled.append(option_label)

            # removes it from the possible columns list, so there are
            # no buttons that stack on top of each other
            possible_columns.remove(column)

        # assigns each button a variable
        self.button_1 = self.option_labels_ref[0]
        self.button_2 = self.option_labels_ref[1]
        self.button_3 = self.option_labels_ref[2]

        # creating the frame
        self.help_stats_frame = Frame(self.quiz_frame)
        self.help_stats_frame.grid(padx=5, pady=10, row=3)

        # the list of misc buttons e.g. next question/help
        # frame | button | bg | command | row | column | width
        misc_buttons = [
            [self.quiz_frame, "Next Question", "#add8e6", self.new_question, 2, 0, 21],
            [self.help_stats_frame, "Help", "#FF8000", self.to_help, 0, 0, 9],
            [self.help_stats_frame, "Stats", "#FF8000", self.to_stats, 0, 1, 9],
            [self.quiz_frame, "To Start", "#FF7F7F", self.to_start, 4, 0, 21]
        ]

        misc_button_ref = []

        # makes the buttons for the duties
        for count, item in enumerate(misc_buttons):
            misc_button = Button(item[0], text=item[1], font=("Arial", 16, "bold"),
                                 bg=item[2], pady=10, padx=10, justify="left",
                                 wraplength=350, width=item[6], command=item[3])
            misc_button.grid(row=item[4], column=item[5], padx=5, pady=5)
            misc_button_ref.append(misc_button)

        # assigns the next question button to a variable and disables it
        # so the user has to answer the question first before pressing "next question"
        self.next_question = misc_button_ref[0]
        self.next_question.config(state=DISABLED)
        self.buttons_to_be_disabled.append(self.next_question)

        # assigns the help button to a variable
        self.help_button = misc_button_ref[1]

        # assigns the stats button to a variable
        self.stats_button = misc_button_ref[2]
        self.stats_button.config(state=DISABLED)

        self.to_start_button = misc_button_ref[3]

        # creates a list of buttons to recolour to have an orange background
        recolour_list = [self.quiz_frame, self.label_frame, self.help_stats_frame,
                         self.options_frame, self.heading_label, self.quiz_box,
                         self.answer_label, self.god_label]

        # recolours the buttons
        recolour(recolour_list, "#DAE8FC")

        # sets up the first question
        self.new_question()


    def new_question(self):
        """
        Changes the question and selects a new god and two new duties when the user
        presses "next question"
        """

        # gets the gods name, duties and two incorrect duties
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

        # gets the correct answer
        self.correct_answer.set(correct_duty)

        # the buttons and possible columns
        columns = [1, 2, 3]
        buttons = [self.button_1, self.button_2, self.button_3]

        # configures the pre-made buttons and adds the answer checker command
        # it also re-randomizes the button layout so they correct answer
        # will always be in a random spot
        for count, item in enumerate(buttons):
            new_duty = random.choice(options)
            column = random.choice(columns)

            buttons[count].config(text=new_duty[0], command=partial(self.answer_checker, new_duty[0]))
            buttons[count].grid(column=column)

            options.remove(new_duty)
            columns.remove(column)

        if q_answered >= 1:
            # enables the stats button as
            # there is now data to work with
            self.stats_button.config(state=NORMAL)

        print(f"{correct_duty}")

    def best_streak(self, current, highest):
        """
        compares the current streak to the highest streak,
        whichever one is higher, it will return that one
        """

        return max(current, highest)

    def answer_checker(self, button_pressed):
        """
        Gets the answer that was set in the new_question function and then
        compares it to the button that was pressed and updates how many
        questions the user has already answered
        """

        # gets the correct answer and
        # num of correct answers so far
        correct_answer = self.correct_answer.get()
        correct_answers = self.correct_answers.get()

        # compares the answer based on their ids
        if button_pressed == correct_answer:
            self.god_label.configure(text="Correct!", fg="#009900")

            # adds 1 to correct answers for stats purposes
            correct_answers += 1
            self.correct_answers.set(correct_answers)

            # adds 1 to the correct answer streak
            self.correct_streak += 1

            self.highest_streak = self.best_streak(self.correct_streak, self.highest_streak)

        else:
            self.god_label.configure(text="Incorrect!", fg="#990000")

            # resets the correct streak but adds it to a list
            # makes it, so I can sort from highest to lowest to find
            # the highest streak the user had done

            self.first_streak = "no"

            self.correct_streak = 0

            self.highest_streak = self.best_streak(self.correct_streak, self.highest_streak)

        # disables all the buttons after a button was pressed/answer
        # was checked to prevent cheating
        for item in self.option_labels_ref:
            item.config(state=DISABLED)

        self.next_question.config(state=NORMAL)

        # adds one to the questions answered
        q_answered = self.q_answered.get()
        q_wanted = self.q_wanted.get()
        q_answered += 1
        self.q_answered.set(q_answered)

        # disables all the buttons once the user
        # has answered all the questions they wanted
        if q_answered == q_wanted:
            for item in self.buttons_to_be_disabled:
                item.config(state=DISABLED)

            self.heading_label.config(text="You made it to the End!")

    def to_help(self):
        """
        Invokes the help class
        """
        Help(self)

    def to_stats(self):
        """
        Invokes the stats class
        """
        Stats(self)

    def to_start(self):
        # reshow root and end current
        # game / allow new game to start
        root.deiconify()
        self.quiz_box.destroy()


class Help:

    """
    Re-displays the introduction info with
    some extra bits to help the user if they're stuck
    """

    def __init__(self, partner):

        # disables the help button
        # prevents the user from creating multiple help button windows
        partner.help_button.config(state=DISABLED)

        # disable button to prevent program crashing
        partner.to_start_button.config(state=DISABLED)

        self.help_box = Toplevel()

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # creates the help / info window
        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid(padx=10, pady=10)

        self.help_heading_label = Label(self.help_frame, text="Help / Info",
                                        font=("Arial", 18, "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("- There will be a randomly selected god and 3 buttons will appear\n\n"
                     "- 2 of them will be 2 random god's jobs/duties and 1 will be the correct one for the god "
                     " that was randomly selected.\n\n"
                     "- Your job is to select the right one.\n\n"
                     "- Then press the next question button and we will randomly select another god and 3 duties.\n\n"
                     "- Once it has been however many questions you had wanted, the game will end and you can see your "
                     " stats by pressing the stats button "
                     "")

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     font=("Arial", 12), wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        # creates the dismiss button
        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner), height=2, width=20)
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # creates a list of buttons to recolour to have an orange background
        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label, self.help_box]

        # recolours the buttons
        recolour(recolour_list, "#FFE6CC")

    # closes help window
    def close_help(self, partner):
        """
        Closes help dialogue box
        """

        # enables the help/to start button again
        partner.help_button.config(state=NORMAL)
        partner.to_start_button.config(state=NORMAL)

        # destroys the help window
        self.help_box.destroy()

class Stats:

    """
    Displays the stats for
    the gods quiz
    """

    def __init__(self, partner):

        self.partner = partner

        partner.to_start_button.config(state=DISABLED)

        # retrieves the stats info
        q_answered = partner.q_answered.get()
        correct_answers = partner.correct_answers.get()
        highest_streak = partner.highest_streak
        self.stats_button = partner.stats_button

        # prevents the user from being able
        # to open multiple stats windows
        self.stats_button.config(state=DISABLED)

        self.stats_box = Toplevel()

        # if users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid(padx=10, pady=10)

        self.stats_heading_label = Label(self.stats_frame, text="Quiz Statistics",
                                         font=("Arial", 18, "bold"))
        self.stats_heading_label.grid(row=0)

        stats_text = (f"\nQuestions Answered: {q_answered}\n\n"
                      f"Questions Correct: {correct_answers} / {q_answered} \n\n"
                      f"Correct Percentage: {correct_answers / q_answered * 100:.2f}% \n\n"
                      f"Highest Streak: {highest_streak}\n\n")

        self.stats_text_label = Label(self.stats_frame, text=stats_text,
                                      font=("Arial", 12), wraplength=350,
                                      justify="left")
        self.stats_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats, partner), height=2, width=20)
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.stats_frame, self.stats_heading_label,
                         self.stats_text_label, self.stats_box]

        background = "#FFE6CC"

        for item in recolour_list:
            item.config(bg=background)

    def close_stats(self, partner):
        """
        Closes stats dialogue box
        and enables the stats button
        and to start button
        """
        partner.to_start_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Gods Quiz")
    StartGame()
    root.mainloop()