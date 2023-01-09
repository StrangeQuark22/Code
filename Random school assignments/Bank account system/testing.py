import tkinter as tk
from tkinter import ttk
import os

os.chdir("D:/MISC/Code/Random school assignments/Bank account system")

root = tk.Tk()

style = ttk.Style()
style.configure("Tabless.TNotebook", tabmargins=[0, 0, 0, 0])
style.layout("Tabless.TNotebook.Tab", [])

note = ttk.Notebook(root, style="Tabless.TNotebook")
note.grid(row=0, column=0)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
label = ttk.Label(note, text="test")
note.add(label)
root.mainloop()