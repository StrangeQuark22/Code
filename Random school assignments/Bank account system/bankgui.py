import os
import sys
from typing import NoReturn
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as msgbox
from tkinter import ttk
from banksystem import Bank, BankAccount
from passlib.hash import argon2

os.chdir("D:/MISC/Code/Random school assignments/Bank account system")


class App(tk.Tk):
    """The main app class"""

    def __init__(self) -> None:
        super().__init__()

        # Inital setup
        self.title(Bank.BANK_NAME)
        self.geometry("400x450")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.font = tkfont.Font(family="Roboto")

        # Style setup
        self.style = ttk.Style(self)
        self.style.layout("Tabless.TNotebook.Tab", [])

        # Main notebook
        self.main_note = MainNotebook(self)
        self.main_note.grid(row=0, column=0, sticky="nsew")

        # Creates info splashscreen
        self.info_frame = InfoFrame(self)
        self.main_note.add(self.info_frame)

        # Creates account screen
        self.account_frame = AccountFrame(self)
        self.main_note.add(self.account_frame)

    def switch_to(self, tab: int) -> None:
        """Switch to tab of main notebook"""
        self.main_note.select(tab)

    def login(self) -> None:
        """What to do when login is successful"""
        self.switch_to(1)

class MainNotebook(ttk.Notebook):
    """The main views of the app"""

    def __init__(self, container) -> None:
        super().__init__(
            container,
            style="Tabless.TNotebook",
        )


class AccountFrame(ttk.Frame):
    """The frame conataining the account view"""

    def __init__(self, container) -> None:
        super().__init__(container)
        # Initial setup
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Test label
        test = ttk.Label(self, text="test")
        test.grid(row=0, column=0)


class InfoFrame(ttk.Frame):
    """Class containing the frame that is the info splashscreen at first open"""

    def __init__(self, container):
        super().__init__(container)
        # Initial setup
        self.columnconfigure(0, weight=1)

        # Welcome text
        self.welcome_text = ttk.Label(self, text=f"Välkommen till {Bank.BANK_NAME}!", font=("Roboto", 24))
        self.welcome_text.grid(row=0, column=0, sticky="n")
        self.rowconfigure(0, weight=2)

        # Create and place logo widget at the top
        logo = tk.PhotoImage(file="icons/bank250.png")
        self.logo_label = ttk.Label(self, image=logo)
        self.logo_label.image = logo  # type: ignore
        self.logo_label.grid(row=1, column=0, padx=5, pady=10)
        self.rowconfigure(1, weight=3)

        # Login button
        self.login_button = ttk.Button(self, text="Logga in", command=self.open_login_prompt)
        self.login_button.grid(row=2, column=0, sticky="ew")
        self.rowconfigure(2, weight=2)

        # Create account button
        self.signup_button = ttk.Button(self, text="Öppna konto")
        self.signup_button.grid(row=3, column=0, sticky="ew")
        self.rowconfigure(3, weight=2)

        # Quit button
        self.quit_button = ttk.Button(self, text="Lämna banken", command=self.winfo_toplevel().quit)
        self.quit_button.grid(row=4, column=0, sticky="ew")
        self.rowconfigure(4, weight=2)

        for button in (self.login_button, self.signup_button, self.quit_button):
            button.grid_configure(padx=5, pady=5)

    def open_login_prompt(self) -> None:
        """Opens the login popup and grabs forced focus for it"""
        login_window = LoginWindow(self.winfo_toplevel())
        login_window.grab_set()


class LoginWindow(tk.Toplevel):
    """A login popup"""

    def __init__(self, container) -> None:
        super().__init__(container)
        # Initial setup
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.geometry("250x300")

        # Login frame
        self.login_frame = LoginWindow.LoginFrame(self)
        self.login_frame.grid(row=0, column=0)
        self.bind("<Return>", lambda e: self.login_frame.login_button.invoke())

    class LoginFrame(ttk.Frame):
        """Frame for entering login info"""

        def __init__(self, container) -> None:
            super().__init__(container)
            # Initial setup
            self.columnconfigure(0, weight=1)

            # Login text
            self.login_label = ttk.Label(self, text="Logga in", font=("Roboto", 24))
            self.login_label.grid(row=0, column=0, columnspan=2)
            self.rowconfigure(0, weight=2)

            # Usename entry text
            self.username_label = ttk.Label(self, text="Användarnamn:")
            self.username_label.grid(row=1, column=0, sticky="w", columnspan=2)
            self.rowconfigure(1, weight=1)

            # Username entry and StringVar
            self.username = tk.StringVar()
            self.username_entry = ttk.Entry(self, textvariable=self.username)
            self.username_entry.grid(row=2, column=0, columnspan=2)
            self.rowconfigure(2, weight=1)

            # Password entry text
            self.password_label = ttk.Label(self, text="Lösenord:")
            self.password_label.grid(row=3, column=0, sticky="w", columnspan=2)
            self.rowconfigure(3, weight=1)

            # Password entry and StringVar
            self.password = tk.StringVar()
            self.password_entry = ttk.Entry(self, textvariable=self.password, show="*")
            self.password_entry.grid(row=4, column=0, columnspan=2)
            self.rowconfigure(4, weight=1)

            # Login button
            self.login_button = ttk.Button(self, text="Logga in", command=lambda: self.login(self.username.get(), self.password.get()))
            self.login_button.grid(row=5, column=1)
            self.rowconfigure(5, weight=1)
            self.columnconfigure(1, weight=1)

            # Back button
            self.back_button = ttk.Button(self, text="Tillbaka", command=self.winfo_toplevel().destroy)
            self.back_button.grid(row=5, column=0)

            for button in (self.login_button, self.back_button):
                button.grid_configure(padx=5, pady=7)

        def login(self, username: str, password: str) -> None:
            """The function of the login button. It stores login data and flips pages in main app and quits popup"""
            msgbox.showinfo("Nice", f"login: user: {username} pass: {password}")
            self.winfo_toplevel().master.login() # type: ignore
            self.winfo_toplevel().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
