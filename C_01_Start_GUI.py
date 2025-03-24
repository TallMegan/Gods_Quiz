from tkinter import *


class StartGame:
    """
    gods quiz main menu
    """

    def __init__(self):
        """
        gets the number of questions from the user
        """

        self.start_frame = Frame(padx=10, pady=10, bg="#6C8EBF")
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
            # [choose_question, ("Arial", "12", "bold")]
        ]

        # create labels and add them to a reference list (mm means main menu)
        mm_labels_ref = []

        for count, item in enumerate(mm_labels):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               justify="left", pady=10, padx=10, bg="#add8e6",
                               wraplength=350)
            make_label.grid(row=count)

            mm_labels_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary
        # self.choose_label = mm_labels_ref[2]
        #
        # # frame so that entry box and button ca be in the same row
        # self.entry_area_frame = Frame(self.start_frame)
        # self.entry_area_frame.grid(row=3)
        #
        # self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
        #                                  width=20, bg="#6C8EBF")
        # self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
