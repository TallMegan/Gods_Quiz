from tkinter import *
from functools import partial

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
        self.num_questions_entry.config(state=DISABLED)

        # removes the placeholder
        self.on_click_id = self.num_questions_entry.bind('<Button-1>', on_click)

        self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)

        # creates play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
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
                # temporary success message, replace with call to PlayGame class
                self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"),
                                         text=f"You have chosen to play {q_wanted} question/s")
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
                                     text="How many questions would you like?")
            self.num_questions_entry.delete(0, END)
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.insert(0, "Please enter a whole number (>0)")

            # removes the placeholder
            self.on_click_id = self.num_questions_entry.bind('<Button-1>')

class Play:
    """
    Super summarised play class to just focus on the help button
    """

    def __init__(self, q_wanted):

        # self.correct_answers = IntVar()
        self.q_answered = 10
        self.correct_answers = 6

        self.q_wanted = q_wanted

        self.quiz_box = Toplevel()

        self.quiz_frame = Frame(self.quiz_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # creates the to_stats button
        self.stats_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=partial(self.to_stats, q_wanted))
        self.stats_button.grid()

    def __getitem__(self, key):
        """
        Makes the all_stats_info retrievable
        """
        all_stats_info = [self.q_answered, self.correct_answers]

        return all_stats_info

    def to_stats(self, all_stats_info):
        # correct_answers = self.correct_answers.get
        Stats(self)

class Stats:

    def __init__(self, partner):

        all_stats_info = [self.q_answered, self.correct_answers]

        # retrieves the stats info
        q_answered = all_stats_info[0][0]
        correct_answers = all_stats_info[0][1]

        # partner.stats_button.config(state=DISABLED)

        self.stats_box = Toplevel()

        # if users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid(padx=10, pady=10)

        self.stats_heading_label = Label(self.stats_frame, text="Quiz Statistics",
                                         font=("Arial", 18, "bold"))
        self.stats_heading_label.grid(row=0)

        stats_text = (f"\nQuestions Correct: {correct_answers} / {q_answered} \n\n"
                      f"Correct Percentage: {correct_answers / q_answered * 100}% \n\n"
                      f"Highest Streak: #\n\n")

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
        """
        # partner.stats_button.config(state=NORMAL)

        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
