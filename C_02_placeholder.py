from tkinter import *

root = Tk()

my_entry = Entry(root, width=50)
my_entry.pack()
my_entry.insert(0, "Place Holder")
my_entry.configure(state=DISABLED)


def on_click(event):
    my_entry.configure(state=NORMAL)
    my_entry.delete(0, END)

    # make the callback only work once
    my_entry.unbind('<Button-1>', on_click_id)


on_click_id = my_entry.bind('<Button-1>', on_click)

root.mainloop()
