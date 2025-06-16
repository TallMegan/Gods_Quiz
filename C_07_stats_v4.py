import random
from tkinter import *
from functools import partial


class Play:

    def __init__(self, q_num):

        self.length_of_streaks = []
        self.correct_streak_list = []
        self.quiz_frame = Frame()
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
        self.misc_button_frame = Frame(self.quiz_frame)
        self.misc_button_frame.grid(padx=10, pady=10, row=2)

        # the list of misc buttons e.g. next question/help
        # frame | button | bg | command
        misc_buttons = [
            [self.misc_button_frame, "Next Question", "#add8e6", self.new_question],
            [self.misc_button_frame, "Stats", "#FF8000", partial(self.to_stats, self.q_wanted)]
        ]

        misc_button_ref = []

        # makes the buttons for the duties
        for count, item in enumerate(misc_buttons):
            misc_button = Button(item[0], text=item[1], font=("Arial", 16, "bold"),
                                 bg=item[2], pady=10, padx=10, justify="left",
                                 wraplength=350, command=item[3])
            misc_button.grid(row=0, column=count, padx=5, pady=5)
            misc_button_ref.append(misc_button)

        # assigns the next question button to a variable and disables it
        # so the user has to answer the question first before pressing "next question"
        self.next_question = misc_button_ref[0]
        self.next_question.config(state=DISABLED)
        self.buttons_to_be_disabled.append(self.next_question)

        # assigns the stats button to a variable
        self.stats_button = misc_button_ref[1]
        self.stats_button.config(state=DISABLED)

        # sets up the first question
        self.new_question()

    def __getitem__(self, key):
        """
        Makes the all_stats_info retrievable
        """

        q_answered = self.q_answered.get()
        correct_answers = self.correct_answers.get()

        all_stats_info = [q_answered, correct_answers, self.highest_streak, self.stats_button]

        return all_stats_info

    def new_question(self):
        """
        Changes the question and selects a new god and two new duties when the user
        presses "next question"
        """

        # gets the gods name, duties and two incorrect duties
        god_name, correct_duty, incorrect_1, incorrect_2 = ["test", 1, 2, 3]

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
        compares the current streak to the highest streak
        if the current streak is higher than the highest streak
        then it changes the highest streak to the current streak
        otherwise highest streak will remain the same
        """

        if current > highest:
            highest = current
        else:
            highest = highest

        return highest


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

    def to_stats(self, stats_bundle):
        """
        Invokes the stats class
        """
        Stats(self, stats_bundle)


class Stats:

    def __init__(self, stats_bundle, partner):

        # retrieves the stats info
        q_answered = stats_bundle[0][0]
        correct_answers = stats_bundle[0][1]
        highest_streak = stats_bundle[0][2]
        self.stats_button = stats_bundle[0][3]

        # prevents the user from being able
        # to open multiple stats windows
        self.stats_button.config(state=DISABLED)

        self.stats_box = Toplevel()

        # if users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', self.close_stats)

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid(padx=10, pady=10)

        self.stats_heading_label = Label(self.stats_frame, text="Quiz Statistics",
                                         font=("Arial", 18, "bold"))
        self.stats_heading_label.grid(row=0)

        stats_text = (f"\nQuestions Answered: {q_answered}\n\n"
                      f"Questions Correct: {correct_answers} / {q_answered} \n\n"
                      f"Correct Percentage: {correct_answers / q_answered * 100}% \n\n"
                      f"Highest Streak: {highest_streak}\n\n")

        self.stats_text_label = Label(self.stats_frame, text=stats_text,
                                      font=("Arial", 12), wraplength=350,
                                      justify="left")
        self.stats_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=self.close_stats, height=2, width=20)
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.stats_frame, self.stats_heading_label,
                         self.stats_text_label, self.stats_box]

        background = "#FFE6CC"

        for item in recolour_list:
            item.config(bg=background)

    def close_stats(self):
        """
        Closes stats dialogue box
        and enables the stats button
        """
        self.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Gods Quiz")
    Play(8)
    root.mainloop()