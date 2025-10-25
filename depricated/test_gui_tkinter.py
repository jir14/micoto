from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from db import Database


def fileopen():
    return askopenfilename()


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

db = Database("db.db")
a=0
for rec in db.getLevelDirs(0):
    if rec == "":
        continue
    ttk.Button(frm, text=rec, ).grid(column=0, row=a)
    a+=1

ttk.Button(frm, text="Quit", command=fileopen()).grid(column=1, row=0)
root.mainloop()