from tkinter import *
from PIL import Image, ImageTk

root = Tk()

image = ImageTk.PhotoImage(Image.open("D:/MISC/Code/Random school assignments/Bank account system/icons/bank50.png"))

Label(root, text='Hello', image=image, compound='left').pack()

root.mainloop()