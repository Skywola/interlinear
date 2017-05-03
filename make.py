import codecs
import os
from tkinter import filedialog
import Interlinear as Itl
import tkinter as tk
from tkinter import Label
from tkinter import Button
from tkinter import mainloop
from tkinter import Text

def center(top_level):
    top_level.update_idletasks()
    w = 578  # width for the Tk root
    h = 372  # height for the Tk root
    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def get_path1():
    text1.delete("1.0", "end")
    text1.insert("1.0", filedialog.askopenfilename())
    return 0

def get_path2():
    text2.delete("1.0", "end")
    text2.insert("1.0", filedialog.askopenfilename())
    return 0

def make_it():
    Itl.create(text1.get("1.0", "end"), text2.get("1.0", "end"))
    return 0

# NEED ERROR HANDLERS
root = tk.Tk()
#root.withdraw()
root.wm_title("Interlinear Subtitle Creator    Beta Version 1.0     Created 03-2017")
message = '''To create an interlinear subtitle file, select the subtitle file with the first language, then the subtitle
file with the second language. Note that the time-lines and numbers must correspond between them.
Both files you select must be saved in UTF-8 format beforehand!  (Notepad can do this.)  The
first file you select will be the language displayed on the top line of the subtitle. The second
file you select will be the language displayed on the bottom line of the subtitle.'''
root.grid_columnconfigure(0, weight=1)

label1 = Label(root, text=message).grid(row=0, column=0, padx=16, pady=4, sticky='w')
text1 = Text(root, height=2, width=70)
text1.insert("1.0", '') # "C:/AVideo/AAMovies/ARussian Movies/Ballad Of The Bomber/English/Ballad Of The Bomber-01.srt")
text1.grid(row=1, column=0, padx=6, pady=4, sticky='w')

text2 = Text(root, height=2, width=70)
text2.insert("1.0", '') # C:/AVideo/AAMovies/ARussian Movies/Ballad Of The Bomber/Баллада о бомбере-01.srt")
text2.grid(row=2, column=0, pady=4, padx=6, sticky='w')

Button(root, text='Click to get the top Subtitle', command=get_path1).grid(row=3, column=0, padx=6, pady=4, sticky='w')
Button(root, text='Click to get the bottom Subtitle', command=get_path2).grid(row=3, column=0, padx=180, pady=4, sticky='w')
Button(root, text=' Create and Close', command=make_it).grid(row=3, column=0, padx=86, pady=4, sticky='e')
Button(root, text=' Close ', command=root.quit).grid(row=3, column=0, padx=10, pady=4, sticky='e')

lab_message = '''OUTPUT: Interlinear subtitle file - Interlinear-Vol01.srt - and any sequential files will be placed in
the same directory as the first file you select.  You can create a new directory for them, or just
remove the old files, and leave the interlinear subtitle in place.

- - - - - - - - - - - - - - - - - - - - - - - - - -

For more information on creating interlinear subtitle files and playing them back, visit

       www.tachufind.com '''

label2 = Label(root, text=lab_message).grid(row=5, column=0, padx=16, pady=6, sticky='w')

center(root)

mainloop()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



'''
import sys, os                                    # platform, args, run tools
from tkinter import *                             # base widgets, constants
from tkinter.filedialog   import Open, SaveAs     # standard dialogs
from tkinter.messagebox   import showinfo, showerror, askyesno
from tkinter.simpledialog import askstring, askinteger
from tkinter.colorchooser import askcolor
'''
