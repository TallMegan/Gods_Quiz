from tkinter import *


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

        self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                         width=20)

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
                # temporary success message, replace with call to PlayGame class
                self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"),
                                         text=f"You have chosen to play {q_wanted} round/s")
                Play(q_wanted)

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

            # display the error if necessary
        if has_errors == "yes":
            self.num_questions_entry.delete(0, END)
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.insert(0, "Please enter a whole number (>0)")

            # removes the placeholder
            self.on_click_id = self.num_questions_entry.bind('<Button-1>')


class Play:

    def __init__(self, q_num):
        self.quiz_frame = Frame(padx=10, pady=10)
        self.quiz_frame.grid()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
