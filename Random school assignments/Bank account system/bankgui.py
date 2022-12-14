"""GUI implementation of the bank system from school using my banksystem.py as backend"""
import os
import sys
import string
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as msgbox
import tkinter.filedialog as filedlg
from tkinter import ttk
from banksystem import Bank, BankAccount
from passlib.hash import argon2
from typing import NoReturn

os.chdir("Random school assignments/Bank account system")


class App(tk.Tk):
    """The main app class"""

    def __init__(self) -> None:
        super().__init__()

        # Inital setup
        self.title(Bank.BANK_NAME)
        self.geometry("400x450")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.font = tkfont.Font(family="Roboto")

        # Style setup
        self.style = ttk.Style(self)
        self.style.layout("Tabless.TNotebook.Tab", [])
        self.style.configure("Header.TFrame", background="#66e64c")
        self.style.configure(
            "BorderedHeader.TFrame",
            background="#66e64c",
            borderwidth=4,
            relief="groove",
        )
        self.style.configure("Header.TLabel", background="#66e64c")
        self.style.configure("AccountInfo.TFrame", borderwidth=4, relief="groove")

        # Main notebook
        self.main_note = MainNotebook(self)
        self.main_note.grid(row=0, column=0, sticky="nsew")

        # Creates info splashscreen
        self.info_frame = InfoFrame(self)
        self.main_note.add(self.info_frame)
        self.info_frame.login_button.focus()
        self.info_frame.bind(
            "<FocusIn>", lambda e: self.info_frame.login_button.focus()
        )

        # Creates account screen
        self.account_frame = AccountFrame(self)
        self.main_note.add(self.account_frame)

        # Window close protocol
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def switch_to(self, tab: int) -> None:
        """Switch to tab of main notebook"""
        self.main_note.select(tab)

    def login(self) -> None:
        """What to do when login is successful"""
        self.switch_to(1)
        self.geometry("800x450")

    def on_close(self) -> None | NoReturn:
        """Proper closing procedure"""
        answer: bool | None = msgbox.askyesnocancel(
            "L??mna", "Vill du spara konton till en fil innan du l??mnar?"
        )

        if answer is None:
            return

        if answer:
            save_path = filedlg.asksaveasfilename(filetypes=[("JSON Files", ".json")])
            Bank.save(save_path)

        self.quit()
        sys.exit()


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
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.header = AccountFrame.Header(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.account_info_frame = AccountFrame.AccountInfoFrame(self)
        self.account_info_frame.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=5)

        self.buttons_frame = AccountFrame.AccountButtonsFrame(self)
        self.buttons_frame.grid(row=2, column=0, sticky="nsew")
        self.rowconfigure(2, weight=5)

        self.history_frame = AccountFrame.HistoryFrame(self)
        self.history_frame.grid(row=1, rowspan=2, column=1, sticky="nsew")

        self.account: BankAccount

    class Header(ttk.Frame):
        """Header for account screen"""

        def __init__(self, container) -> None:
            super().__init__(container, style="BorderedHeader.TFrame")

            # Welcome text
            self.name: str = "Name"
            self.header_text = tk.StringVar(value=f"V??lkommen {self.name}!")
            self.welcome_text = ttk.Label(
                self,
                textvariable=self.header_text,
                font=("Roboto", 20),
                style="Header.TLabel",
            )
            self.welcome_text.grid(row=0, column=0, sticky="w", padx=5)
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=3)

            # Bank watermark
            # Logo var
            self.logo = tk.PhotoImage(file="icons/bank50.png")
            # Frame for logo and text
            self.logo_frame = ttk.Frame(self, style="Header.TFrame")
            self.logo_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            self.columnconfigure(1, weight=1)

            # Image part of logo label
            self.logo_image_label = ttk.Label(
                self.logo_frame, image=self.logo, style="Header.TLabel"
            )
            self.logo_image_label.image = self.logo  # type: ignore
            self.logo_image_label.grid(row=0, column=0, sticky="e")
            self.logo_frame.rowconfigure(0, weight=1)
            self.logo_frame.columnconfigure(0, weight=5)

            # Text part of logo label
            self.logo_text_label = ttk.Label(
                self.logo_frame,
                text=Bank.BANK_NAME,
                font=("Roboto", 20, "bold"),
                style="Header.TLabel",
            )
            self.logo_text_label.grid(row=0, column=1, sticky="w")
            self.logo_frame.columnconfigure(1, weight=1)

            for logo_part in (self.logo_image_label, self.logo_text_label):
                logo_part.grid_configure(padx=10)

    class AccountInfoFrame(ttk.Frame):
        """Frame for holding account info like acc num, balance and max credit"""

        def __init__(self, container) -> None:
            super().__init__(container, style="AccountInfo.TFrame")
            # Initial setup
            # self.columnconfigure(0, weight=1)
            # self.columnconfigure(1, weight=1)

            # [ACCOUNT NUM SECTION]
            self.rowconfigure(0, weight=1)
            # Account num image and label
            self.account_number_icon = tk.PhotoImage(file="icons/hashtag25.png")
            self.account_number_icon_label = ttk.Label(
                self, image=self.account_number_icon
            )
            self.account_number_icon_label.image = self.account_number_icon  # type: ignore
            self.account_number_icon_label.grid(row=0, column=0)

            # Account num text and label
            self.account_number: str = "123456"
            self.account_number_text = tk.StringVar(
                value=f"Kontonummer: {self.account_number}"
            )
            self.account_number_text_label = ttk.Label(
                self,
                textvariable=self.account_number_text,
                font=("Roboto", 16),
                justify="left",
                anchor="w",
            )
            self.account_number_text_label.grid(row=0, column=1, sticky="w")

            # [ACCOUNT BALANCE SECTION]
            self.rowconfigure(1, weight=1)
            # Account balance icon
            self.balance_icon = tk.PhotoImage(file="icons/wallet25.png")
            self.balance_icon_label = ttk.Label(self, image=self.balance_icon)
            self.balance_icon_label.image = self.balance_icon  # type: ignore
            self.balance_icon_label.grid(row=1, column=0)

            # Account balance text and label
            self.balance: str = "10000"
            self.balance_text = tk.StringVar(value=f"Saldo: {self.balance}")
            self.balance_text_label = ttk.Label(
                self,
                textvariable=self.balance_text,
                font=("Roboto", 16),
                justify="left",
                anchor="w",
            )
            self.balance_text_label.grid(row=1, column=1, sticky="w")

            # [ACCOUNT CREDIT SECTION]
            self.rowconfigure(2, weight=1)
            # Credit icon and label
            self.credit_icon = tk.PhotoImage(file="icons/credit_card25.png")
            self.credit_icon_label = ttk.Label(self, image=self.credit_icon)
            self.credit_icon_label.image = self.credit_icon  # type: ignore
            self.credit_icon_label.grid(row=2, column=0)

            # Credit text and label
            self.max_credit: str = "5000"
            self.credit_text = tk.StringVar(value=f"Maximal kredit: {self.max_credit}")
            self.credit_text_label = ttk.Label(
                self,
                textvariable=self.credit_text,
                font=("Roboto", 16),
                justify="left",
                anchor="w",
            )
            self.credit_text_label.grid(row=2, column=1, sticky="w")

            for child in self.winfo_children():
                child.grid_configure(padx=5, pady=5)

    class AccountButtonsFrame(ttk.Frame):
        """Frame for all buttons in account info pane"""

        def __init__(self, container) -> None:
            super().__init__(container, style="AccountInfo.TFrame")

            # Initial config
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.rowconfigure(2, weight=1)

            # Add money button
            self.add_money_button = ttk.Button(
                self, text="S??tt in pengar", command=self.make_add_money_window
            )
            self.add_money_button.grid(row=0, column=0, rowspan=2, sticky="nsew")

            # Withdraw money button
            self.withdraw_money_button = ttk.Button(
                self, text="Ta ut pengar", command=self.make_withdraw_money_window
            )
            self.withdraw_money_button.grid(row=2, column=0, sticky="nsew")

            # Change max credit button
            self.change_credit_button = ttk.Button(
                self, text="??ndra max. kredit", command=self.make_change_credit_window
            )
            self.change_credit_button.grid(row=0, column=1, sticky="nsew")

            # Change name button
            self.change_name_button = ttk.Button(
                self, text="??ndra namn", command=self.make_change_name_window
            )
            self.change_name_button.grid(row=1, column=1, sticky="nsew")

            # Change pass button
            self.change_pass_button = ttk.Button(self, text="??ndra l??senord")
            self.change_pass_button.grid(row=2, column=1, sticky="nsew")

            # Log out button
            self.logout_button = ttk.Button(self, text="Logga ut", command=self.logout)
            self.logout_button.grid(row=0, column=2, rowspan=3, sticky="nsew")

            for child in self.winfo_children():
                child.grid_configure(padx=5, pady=5)

        class AddMoneyPrompt(tk.Toplevel):
            """Creates a popup to add money to the account"""

            def __init__(self, container):
                super().__init__(container)
                # Initial setup
                self.geometry("250x300")
                self.rowconfigure(0, weight=1)
                self.columnconfigure(0, weight=1)

                # Main content frame
                self.main_frame = ttk.Frame(self)
                self.main_frame.grid(column=0, row=0)
                self.main_frame.columnconfigure(0, weight=1)

                # Add money text
                self.add_money_label = ttk.Label(
                    self.main_frame, text="S??tt in pengar", font=("Roboto", 24)
                )
                self.add_money_label.grid(row=0, column=0, padx=5, pady=10)
                self.main_frame.rowconfigure(0, weight=3)

                # Amount entry and label:
                self.entry_label = ttk.Label(self.main_frame, text="M??ngd:")
                self.entry_label.grid(row=1, column=0, sticky="w", padx=5)
                self.main_frame.rowconfigure(1, weight=1)
                self.amount = tk.StringVar()
                self.entry = ttk.Entry(self.main_frame, textvariable=self.amount)
                self.entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
                self.main_frame.rowconfigure(2, weight=1)
                self.entry.bind("<Return>", lambda e: self.confirm_button.invoke())
                self.entry.focus()

                # Confirm and cancel button frame
                self.button_frame = ttk.Frame(self.main_frame)
                self.button_frame.grid(row=3, column=0, sticky="nsew")
                self.main_frame.rowconfigure(3, weight=2)
                self.button_frame.rowconfigure(0, weight=1)

                # Confirm button
                self.confirm_button = ttk.Button(
                    self.button_frame, text="S??tt in", command=self.confirm
                )
                self.confirm_button.grid(row=0, column=1)
                self.button_frame.columnconfigure(1, weight=1)

                # Cancel button
                self.cancel_button = ttk.Button(
                    self.button_frame,
                    text="Tillbaka",
                    command=self.winfo_toplevel().destroy,
                )
                self.cancel_button.grid(row=0, column=0)
                self.button_frame.columnconfigure(0, weight=1)

            def confirm(self) -> None:
                """what to do when confirm button is pressed"""
                account: BankAccount = self.winfo_toplevel().master.master.account  # type: ignore

                try:
                    amount = float(self.amount.get())
                except ValueError:
                    msgbox.showerror("Fel", "Summa ej ett flyttal")
                    return

                if float(self.amount.get()) < 0:
                    msgbox.showerror(
                        "Fel", "Ogiltigt summa (antagligen negativ eller 0)"
                    )
                    return

                try:
                    account.update({"balance": account.balance + amount})
                except KeyError:
                    msgbox.showerror(
                        "Fel",
                        "Kontot existerar inte i den globala databasen. Detta ska vara om??jligt s?? grattis, du har pajat min kod! (Det ??r antagligen Pythons GC som f??rst??r, men ingen aning) Skapa om kontot om det ska anv??ndas igen.",  # NOQA
                    )
                    return
                self.winfo_toplevel().master.master.load_account(account)  # type: ignore
                self.winfo_toplevel().destroy()

        class WithdrawMoneyPrompt(tk.Toplevel):
            """Popup to withdraw money"""

            def __init__(self, container):
                super().__init__(container)
                # Initial setup
                self.geometry("250x300")
                self.rowconfigure(0, weight=1)
                self.columnconfigure(0, weight=1)

                # Main content frame
                self.main_frame = ttk.Frame(self)
                self.main_frame.grid(column=0, row=0)
                self.main_frame.columnconfigure(0, weight=1)

                # withdraw money text
                self.withdraw_money_label = ttk.Label(
                    self.main_frame, text="Ta ut pengar", font=("Roboto", 24)
                )
                self.withdraw_money_label.grid(row=0, column=0, padx=5, pady=10)
                self.main_frame.rowconfigure(0, weight=3)

                # Amount entry and label:
                self.entry_label = ttk.Label(self.main_frame, text="M??ngd:")
                self.entry_label.grid(row=1, column=0, sticky="w", padx=5)
                self.main_frame.rowconfigure(1, weight=1)
                self.amount = tk.StringVar()
                self.entry = ttk.Entry(self.main_frame, textvariable=self.amount)
                self.entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
                self.main_frame.rowconfigure(2, weight=1)
                self.entry.bind("<Return>", lambda e: self.confirm_button.invoke())
                self.entry.focus()

                # Confirm and cancel button frame
                self.button_frame = ttk.Frame(self.main_frame)
                self.button_frame.grid(row=3, column=0, sticky="nsew")
                self.main_frame.rowconfigure(3, weight=2)
                self.button_frame.rowconfigure(0, weight=1)

                # Confirm button
                self.confirm_button = ttk.Button(
                    self.button_frame, text="Ta ut", command=self.confirm
                )
                self.confirm_button.grid(row=0, column=1)
                self.button_frame.columnconfigure(1, weight=1)

                # Cancel button
                self.cancel_button = ttk.Button(
                    self.button_frame,
                    text="Tillbaka",
                    command=self.winfo_toplevel().destroy,
                )
                self.cancel_button.grid(row=0, column=0)
                self.button_frame.columnconfigure(0, weight=1)

            def confirm(self) -> None:
                """what to do when confirm button is pressed"""
                account: BankAccount = self.winfo_toplevel().master.master.account  # type: ignore

                try:
                    amount = float(self.amount.get())
                except ValueError:
                    msgbox.showerror("Fel", "Summa ej ett flyttal")
                    return

                if amount <= 0:
                    msgbox.showerror(
                        "Fel", "Ogiltig summa (antagligen negativ eller 0)"
                    )
                    return
                if account.balance - amount < 0:
                    msgbox.showerror(
                        "Otillr??ckligt saldo",
                        f"Pengarna p?? ditt saldo r??cker inte till.\nDu kan som mest ta ut {account.balance} kr",
                    )
                    return

                try:
                    account.update({"balance": account.balance - amount})
                except KeyError:
                    msgbox.showerror(
                        "Fel",
                        "Kontot existerar inte i den globala databasen. Detta ska vara om??jligt s?? grattis, du har pajat min kod! (Det ??r antagligen Pythons GC som f??rst??r, men ingen aning) Skapa om kontot om det ska anv??ndas igen.",  # NOQA
                    )
                    return
                self.winfo_toplevel().master.master.load_account(account)  # type: ignore
                self.winfo_toplevel().destroy()

        class ChangeCreditPrompt(tk.Toplevel):
            """Popup to change max credit"""

            def __init__(self, container):
                super().__init__(container)
                # Initial setup
                self.geometry("250x300")
                self.rowconfigure(0, weight=1)
                self.columnconfigure(0, weight=1)

                # Main content frame
                self.main_frame = ttk.Frame(self)
                self.main_frame.grid(column=0, row=0)
                self.main_frame.columnconfigure(0, weight=1)

                # withdraw money text
                self.change_credit_label = ttk.Label(
                    self.main_frame,
                    text="??ndra\nmaximal kredit",
                    font=("Roboto", 24),
                    justify="center",
                )
                self.change_credit_label.grid(row=0, column=0, padx=5, pady=10)
                self.main_frame.rowconfigure(0, weight=3)

                # Amount entry and label:
                self.entry_label = ttk.Label(self.main_frame, text="Ny m??ngd:")
                self.entry_label.grid(row=1, column=0, sticky="w", padx=5)
                self.main_frame.rowconfigure(1, weight=1)
                self.amount = tk.StringVar()
                self.entry = ttk.Entry(self.main_frame, textvariable=self.amount)
                self.entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
                self.main_frame.rowconfigure(2, weight=1)
                self.entry.bind("<Return>", lambda e: self.confirm_button.invoke())
                self.entry.focus()

                # Confirm and cancel button frame
                self.button_frame = ttk.Frame(self.main_frame)
                self.button_frame.grid(row=3, column=0, sticky="nsew")
                self.main_frame.rowconfigure(3, weight=2)
                self.button_frame.rowconfigure(0, weight=1)

                # Confirm button
                self.confirm_button = ttk.Button(
                    self.button_frame, text="??ndra", command=self.confirm
                )
                self.confirm_button.grid(row=0, column=1)
                self.button_frame.columnconfigure(1, weight=1)

                # Cancel button
                self.cancel_button = ttk.Button(
                    self.button_frame,
                    text="Tillbaka",
                    command=self.winfo_toplevel().destroy,
                )
                self.cancel_button.grid(row=0, column=0)
                self.button_frame.columnconfigure(0, weight=1)

            def confirm(self) -> None:
                """what to do when confirm button is pressed"""
                account: BankAccount = self.winfo_toplevel().master.master.account  # type: ignore

                try:
                    amount = int(self.amount.get())
                except ValueError:
                    msgbox.showerror("Fel", "Summa ej ett giltigt heltal")
                    return

                if amount <= 0:
                    msgbox.showerror(
                        "Fel", "Ogiltig summa (antagligen negativ eller 0)"
                    )
                    return

                try:
                    account.update({"max_credit": amount})
                except KeyError:
                    msgbox.showerror(
                        "Fel",
                        "Kontot existerar inte i den globala databasen. Detta ska vara om??jligt s?? grattis, du har pajat min kod! (Det ??r antagligen Pythons GC som f??rst??r, men ingen aning) Skapa om kontot om det ska anv??ndas igen.",  # NOQA
                    )
                    return

                self.winfo_toplevel().master.master.load_account(account)  # type: ignore
                self.winfo_toplevel().destroy()

        class ChangeNamePrompt(tk.Toplevel):
            """Prompt to change name on account"""

            def __init__(self, container) -> None:
                super().__init__(container)
                # Initial setup
                self.columnconfigure(0, weight=1)
                self.rowconfigure(0, weight=1)

                # Main frame
                self.main_frame = ttk.Frame(self)
                self.main_frame.grid(row=0, column=0, sticky="nsew")
                self.main_frame.columnconfigure(0, weight=1)

                # Change name label
                self.change_name_label = ttk.Label(
                    self.main_frame, text="??ndra namn", font=("Roboto", 24)
                )
                self.change_name_label.grid(row=0, column=0)
                self.main_frame.rowconfigure(0, weight=3)

                # New name entry and label
                self.entry_label = ttk.Label(self.main_frame, text="Nytt namn:")
                self.entry_label.grid(row=1, column=0, sticky="w")
                self.main_frame.rowconfigure(1, weight=1)
                self.new_val = tk.StringVar()
                self.entry = ttk.Entry(self.main_frame, textvariable=self.new_val)
                self.entry.grid(row=2, column=0)
                self.rowconfigure(2, weight=1)
                self.entry.focus()
                self.entry.bind("<Return>", lambda e: self.confirm_button.invoke())

                # Confirm and cancel button frame
                self.button_frame = ttk.Frame(self.main_frame)
                self.button_frame.grid(row=3, column=0, sticky="nsew")
                self.main_frame.rowconfigure(3, weight=2)
                self.button_frame.rowconfigure(0, weight=1)

                # Confirm button
                self.confirm_button = ttk.Button(
                    self.button_frame, text="??ndra", command=self.confirm
                )
                self.confirm_button.grid(row=0, column=1)
                self.button_frame.columnconfigure(1, weight=1)

                # Cancel button
                self.cancel_button = ttk.Button(
                    self.button_frame,
                    text="Tillbaka",
                    command=self.winfo_toplevel().destroy,
                )
                self.cancel_button.grid(row=0, column=0)
                self.button_frame.columnconfigure(0, weight=1)

            def confirm(self) -> None:
                """Commit the proposed change"""

                new_val: str = (
                    self.new_val.get().strip().replace('"', "").replace("'", "")
                )
                account: BankAccount = self.winfo_toplevel().master.master.account  # type: ignore

                if new_val in string.digits.join(string.punctuation):
                    msgbox.showerror(
                        "Fel",
                        f"Namnet f??r inte inneh??lla siffror ({string.digits}) eller specialkarat??rer ({string.punctuation})",
                    )
                    return

                new_val = new_val.title()

                if not msgbox.askyesno(
                    "Korrekt?", f"??r du n??jd med detta namn:\n{new_val}"
                ):
                    if not msgbox.askretrycancel(
                        "F??rs??k igen?", "Vill du f??rs??ka igen eller avbryta?"
                    ):
                        self.winfo_toplevel().destroy()
                    return

                try:
                    account.update({"holder_name": new_val})
                except KeyError:
                    msgbox.showerror(
                        "Fel",
                        "Kontot existerar inte i den globala databasen. Detta ska vara om??jligt s?? grattis, du har pajat min kod! (Det ??r antagligen Pythons GC som f??rst??r, men ingen aning) Skapa om kontot om det ska anv??ndas igen.",  # NOQA
                    )
                    return
                except ValueError:
                    msgbox.showerror(
                        "Fel", "Namnet tillh??r redan ett annat konto, v??lj ett annat"
                    )

                self.winfo_toplevel().master.master.load_account(account)  # type: ignore
                self.winfo_toplevel().destroy()

        def make_add_money_window(self) -> None:
            """Creates add money popup"""
            add_money_window = AccountFrame.AccountButtonsFrame.AddMoneyPrompt(self)
            add_money_window.grab_set()

        def make_withdraw_money_window(self) -> None:
            """Creates withdraw money popup"""
            withdraw_money_window = (
                AccountFrame.AccountButtonsFrame.WithdrawMoneyPrompt(self)
            )
            withdraw_money_window.grab_set()

        def make_change_credit_window(self) -> None:
            """Create change credit prompt"""
            credit_window = AccountFrame.AccountButtonsFrame.ChangeCreditPrompt(self)
            credit_window.grab_set()

        def make_change_name_window(self) -> None:
            name_window = AccountFrame.AccountButtonsFrame.ChangeNamePrompt(self)
            name_window.grab_set()

        def logout(self) -> None:
            """Log the user out"""
            self.winfo_toplevel().switch_to(0)  # type: ignore
            self.winfo_toplevel().geometry("400x450")

    class HistoryFrame(ttk.Frame):
        """Frame for account transaction history"""

        def __init__(self, container):
            super().__init__(container, style="AccountInfo.TFrame")

            self.placeholder = ttk.Label(self, text="Historik (WIP)")
            self.placeholder.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def load_account(self, account: BankAccount) -> None:
        """Updates all text to match new account"""
        self.header.header_text.set(f"V??lkommer {account.holder_name}!")
        self.account_info_frame.account_number_text.set(
            f"Kontonummer: {account.number}"
        )
        self.account_info_frame.balance_text.set(f"Saldo: {account.balance}")
        self.account_info_frame.credit_text.set(f"Maximal kredit: {account.max_credit}")
        self.account = account


class InfoFrame(ttk.Frame):
    """Class containing the frame that is the info splashscreen at first open"""

    def __init__(self, container):
        super().__init__(container)
        # Initial setup
        self.columnconfigure(0, weight=1)

        # Welcome text
        self.welcome_text = ttk.Label(
            self, text=f"V??lkommen till {Bank.BANK_NAME}!", font=("Roboto", 24)
        )
        self.welcome_text.grid(row=0, column=0, sticky="n")
        self.rowconfigure(0, weight=2)

        # Create and place logo widget at the top
        logo = tk.PhotoImage(file="icons/bank250.png")
        self.logo_label = ttk.Label(self, image=logo)
        self.logo_label.image = logo  # type: ignore
        self.logo_label.grid(row=1, column=0, padx=5, pady=10)
        self.rowconfigure(1, weight=3)

        # Login button
        self.login_button = ttk.Button(
            self, text="Logga in", command=self.open_login_prompt
        )
        self.login_button.grid(row=2, column=0, sticky="ew")
        self.rowconfigure(2, weight=2)
        self.login_button.bind("<Return>", lambda e: self.login_button.invoke())

        # Create account button
        self.signup_button = ttk.Button(self, text="??ppna konto")
        self.signup_button.grid(row=3, column=0, sticky="ew")
        self.rowconfigure(3, weight=2)
        self.signup_button.bind("<Return>", lambda e: print("test"))

        # Quit button
        self.quit_button = ttk.Button(self, text="L??mna banken", command=self.winfo_toplevel().on_close)  # type: ignore
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
            self.username_label = ttk.Label(self, text="Anv??ndarnamn:")
            self.username_label.grid(row=1, column=0, sticky="w", columnspan=2)
            self.rowconfigure(1, weight=1)

            # Username entry and StringVar
            self.username = tk.StringVar()
            self.username_entry = ttk.Entry(self, textvariable=self.username)
            self.username_entry.grid(row=2, column=0, columnspan=2, sticky="ew")
            self.rowconfigure(2, weight=1)
            self.username_entry.focus()

            # Password entry text
            self.password_label = ttk.Label(self, text="L??senord:")
            self.password_label.grid(row=3, column=0, sticky="w", columnspan=2)
            self.rowconfigure(3, weight=1)

            # Password entry and StringVar
            self.password = tk.StringVar()
            self.password_entry = ttk.Entry(self, textvariable=self.password, show="*")
            self.password_entry.grid(row=4, column=0, columnspan=2, sticky="ew")
            self.rowconfigure(4, weight=1)

            # Login button
            self.login_button = ttk.Button(
                self,
                text="Logga in",
                command=lambda: self.login(self.username.get(), self.password.get()),
            )
            self.login_button.grid(row=5, column=1)
            self.rowconfigure(5, weight=1)
            self.columnconfigure(1, weight=1)

            # Back button
            self.back_button = ttk.Button(
                self, text="Tillbaka", command=self.winfo_toplevel().destroy
            )
            self.back_button.grid(row=5, column=0)

            for button in (self.login_button, self.back_button):
                button.grid_configure(padx=5, pady=7)

        def login(self, username: str, password: str) -> None:
            """The function of the login button. It stores login data and flips pages in main app and quits popup"""
            # msgbox.showinfo("Nice", f"login: user: {username} pass: {password}")
            try:
                acc = Bank.accounts[username.title()]
            except KeyError:
                msgbox.showerror("Fel", "Ogiltigt anv??ndarnamn")
                return

            if argon2.verify(password, acc.hashed_password):
                self.password.set("")
                msgbox.showinfo("Login succes!", str(acc.data))
            else:
                msgbox.showerror("Fel", "Felaktigt l??senord")
                return

            self.winfo_toplevel().master.login()  # type: ignore
            self.winfo_toplevel().master.account_frame.load_account(Bank.accounts[username.title()])  # type: ignore
            self.winfo_toplevel().destroy()


if __name__ == "__main__":
    app = App()
    if msgbox.askyesno("Ladda konton", "Vill du ladda sparade konton fr??n fil?"):
        load_path = filedlg.askopenfilename(filetypes=[("JSON File", ".json")])
        Bank.load(load_path)
    app.mainloop()
