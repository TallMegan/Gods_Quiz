from tkinter import *
from functools import partial

class Play:
    """
    Super summarised play class to just focus on the help button
    """

    def __init__(self):

        self.quiz_frame = Frame()
        self.quiz_frame.grid(padx=10, pady=10)

        # creates the to_help button
        self.help_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                     text="Help / Info", width=15, fg="#FFFFFF",
                                     bg="#FF8000", padx=10, pady=10, command=self.to_help)
        self.help_button.grid()


    def to_help(self):

        Help(self)


class Help:

    def __init__(self, partner):

        partner.help_button.config(state=DISABLED)

        self.help_box = Toplevel()

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

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

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner), height=2, width=20)
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label, self.help_box]

        background = "#FFE6CC"

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Closes help dialogue box
        """
        partner.help_button.config(state=NORMAL)

        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Play()
    root.mainloop()
