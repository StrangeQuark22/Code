from banksystem import Bank, BankAccount
from passlib.hash import argon2
import tkinter as tk
from tkinter import ttk


root = tk.Tk()

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0)

root2 = tk.Tk()
