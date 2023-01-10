import random
import warnings
import sys
import json
import os

os.chdir("Random school assignments/Bank account system")


class BankAccount:

    # Constructor, skapar ett nytt konto med känd data. Används för filimport
    def __init__(self, accountDict: dict):
        self.data = accountDict

        self.balance = self.data["balance"]
        self.number = self.data["number"]
        self.holderName = self.data["name"]
        self.maxCredit = self.data["maxCredit"]
        self.password = self.data["password"]

    # Skapa ett nytt konto utan känd data
    @staticmethod
    def createNewAccount():
        print(f"Tack för att du vill skapa ett konto hos {Bank.BANK_NAME}!")
        data = {"name": input("Vad heter du?\n"), "number": BankAccount.getAccountNumber(), "balance": 0.0, "maxCredit": 5000, "password": BankAccount.getPassword()}
        Bank.addAccount(BankAccount(data))
        Menu.getMainMenu()

    # kolla om angivet lösen stämmer med lösen för angivet konto
    @staticmethod
    def checkPassword(password: str, accountNum: int) -> bool:
        # Kolla om konto existerar
        while accountNum not in Bank.accounts.keys():
            warnings.warn("Kontot existerar inte!", Warning)
            accountNum = int(input("Ange kontonummer igen: "))

        if password == Bank.accounts[accountNum].password:
            return True
        else:
            return False

    # Fråga efter ett värdet för ett nytt lösenord
    @staticmethod
    def promptPassword() -> str:
        return input("Välj lösenord: ")

    # Skaffa ett nytt lösenord
    @staticmethod
    def getPassword() -> str:
        password = BankAccount.promptPassword()
        while input("Bekräfta lösenord: ") != password:
            print("Lösenorden matchar inte!")
            if input("Välj annat lösenord (y/n)? ") in ("y", "Y"):
                password = BankAccount.promptPassword()
        return password

    # Ändra lösenord
    def changePassword(self):
        if BankAccount.checkPassword(input("Ange ditt gamla lösenord: "), self.number):
            print("VARNING! Ändring av lösenord går ej att ångra!")
            if input("Vill du fortfarande fortsätta (y/n)?") in ("y", "Y"):
                self.password = BankAccount.getPassword()
            else:
                return
        else:
            print("Fel lösenord, försök igen!")
            self.changePassword()

    # Generera ett kontonummer
    @staticmethod
    def getAccountNumber() -> int:
        num = 0
        while num == 0:
            rand = random.randint(0, 999999)
            if rand not in Bank.accounts.keys():
                num = rand

        return num

    # addera pengar till kontot
    def addMoney(self):
        amount = float(input("Hur mycket?\n"))
        if amount > 0:
            self.balance += amount
            self.balance = round(self.balance, 2)
            self.data["balance"] = self.balance
            print(f"{amount} kr har lagts till på ditt konto\nDitt nya saldo är {self.balance} kr")
        else:
            warnings.warn("Negativ pengsumma eller pengasumma som är 0 är inte tillåtet!", Warning)
        Menu.getAccountMenu(self.number)

    # dra ut pengar, kolla om det är möjligt
    def withdrawMoney(self):
        amount = float(input("Hur mycket?\n"))
        if amount <= self.balance:
            self.balance -= amount
            self.balance = round(self.balance, 2)
            self.data["balance"] = self.balance
            print(f"{amount} kr har tagits ut ur ditt konto.\nDitt nya saldo är {self.balance} kr")
        else:
            warnings.warn("Inte nog med pengar på kontot!", Warning)
        Menu.getAccountMenu(self.number)

    # Ändra maxCredit
    def changeMaxCredit(self):
        amount = float(input("Hur mycket?\n"))
        if amount >= 0:
            self.maxCredit = int(amount)
            self.data["maxCredit"] = self.maxCredit
            print(f"Din nya maximala kredit är {amount} kr")
        else:
            warnings.warn("Negativa kreditvärden är omöjliga!", Warning)
        Menu.getAccountMenu(self.number)


class Bank:
    # Bankens namn
    BANK_NAME = "Banken"

    # Dict med att konto där index är kontonr och värde är kontoobjektet
    accounts: dict[int, BankAccount] = {}

    # Lägger till ett konto i listan
    @classmethod
    def addAccount(cls, account: BankAccount):
        cls.accounts.update({account.number: account})

    # Loggar in en användare
    @staticmethod
    def login():
        if input("Kan du ditt kontonummer (y/n)?\n") in ("y", "Y"):
            num = int(input("Ange ditt kontonummer: "))
        else:
            name = input("Ange namnet på kontoinnehavaren: ")
            num = int()
            for accountNum, account in Bank.accounts.items():
                if name == account.holderName:
                    num = accountNum
                    break
            print(f"För framtida referens är ditt kontonummer '{num}'")

        password = input("Ange ditt lösenord: ")

        if BankAccount.checkPassword(password, num):
            Menu.getAccountMenu(num)
        else:
            print("Fel lösenord, försök igen!")
            Bank.login()


def exitProgram():
    output = []
    for key, val in Bank.accounts.items():
        output.append(val.data)
    with open("accounts.json", "w") as file:
        file.truncate(0)
        json.dump(output, file)
        sys.exit()


class Menu:
    # Möjliga alternativ för huvudmenyn som en tuple av namn och motsvarande funktion
    MAIN_OPTIONS = {1: (Bank.login, "Logga in"), 2: (BankAccount.createNewAccount, "Öppna konto"), 3: (exitProgram, "Dra")}

    # Möjliga alternativ i menyn för ett konto
    ACCOUNT_OPTIONS = {
        1: (BankAccount.addMoney, "Sätt in pengar"),
        2: (BankAccount.withdrawMoney, "Ta ut pengar"),
        3: (BankAccount.changeMaxCredit, "Ändra maximala kredit"),
        4: (BankAccount.changePassword, "Ändra lösenord"),
        5: (None, "Huvudmenyn"),
    }

    # Rita och hantera valet av alternativ i huvudmenyn
    @classmethod
    def getMainMenu(cls):
        print(f"Välkommen till {Bank.BANK_NAME}!\nVälj ett alternativ:")
        for key, val in cls.MAIN_OPTIONS.items():
            print(f"{key}: {val[1]}")

        print("-" * 50)
        selection = int(input("Val: "))
        # Kallar motsvarande funktion för alternativet utan alternativ
        cls.MAIN_OPTIONS[selection][0]()

    # Rita och hantera val i den inloggade menyn
    @classmethod
    def getAccountMenu(cls, accountNum):
        account = Bank.accounts[accountNum]

        print(f"Välkommen {account.holderName}! (konto nr. {account.number})\nVad vill du göra idag?")
        print("-" * 50)
        line = f"| Saldo: {account.balance}   Maximal kredit: {account.maxCredit}"
        while len(line) < 49:
            line += " "
        line += "|"
        print(line)
        print("-" * 50)

        for key, val in cls.ACCOUNT_OPTIONS.items():
            print(f"{key}: {val[1]}")

        selection = int(input("Val: "))
        if selection != max(cls.ACCOUNT_OPTIONS.keys()):
            cls.ACCOUNT_OPTIONS[selection][0](self=account)
        else:
            Menu.getMainMenu()


def parseFile(path: str):
    with open(path, "r") as file:
        accounts = json.load(file)
    return accounts


# Main metod
if __name__ == "__main__":
    # importData = parseFile("accounts.json")
    # if type(importData) is list:
    #     for account in importData:
    #         Bank.addAccount(BankAccount(account))
    # else:
    #     Bank.addAccount(importData)

    Menu.getMainMenu()
