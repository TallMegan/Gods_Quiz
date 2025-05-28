from tkinter import *

class Play:
    """
    Super summarised play class to just focus on the help button
    """

    def __init__(self):

        self.quiz_frame = Frame()
        self.quiz_frame.grid(padx=10, pady=10)

        # creates the to_help button
        self.help_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                     text="Hints", width=15, fg="#FFFFFF",
                                     bg="#FF8000", padx=10, pady=10, command=self.to_help)
        self.help_button.grid()


    def to_help(self):

        Help()


class Help:

    def __init__(self):
        self.help_box = Toplevel()
        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid(padx=10, pady=10)

        self.help_heading_label = Label(self.help_frame, text="Help / Info",
                                        font=("Arial", 18, "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("There will be a randomly selected god and 3 buttons will appear, 2 of them "
                     "will be 2 random god's jobs/duties and 1 will be the correct one for the god "
                     "that was randomly selected. Your job is to select the right one. After you select "
                     "an option, we will let you know if you got it right or not. Then press the next question "
                     "button and we will randomly select another god and 3 duties. Once it has been however many "
                     "rounds you have selected, the game will end and you can see your stats by pressing the stats "
                     "button")

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     font=("Arial", 12), wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Play()
    root.mainloop()
