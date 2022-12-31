import warnings
import random

class BankAccount:
    """
    A class that is essentially a datatype for bank account objects.
    
    Also holds many getting and setting functions for different attributes of the object.

    Instance attributes:
        data (dict): All data of the account as a dict. The keys are the individual attributes
        balance (float): The available money on the account
        number (int): a 6 digit unique numerical identifier for the account
        holderName (str): The name of the account holder
        maxCredit (int): Maximum allowed credit on the account
        password (str): The account password, stored as cleartext for now

    Functions:

    """
    # Constructor, skapar ett nytt konto med känd data. Används för filimport
    def __init__(self, holderName: str, password: str, balance: float=0, maxCredit: int=5000):
        self.data: dict[str, int | float | str] = {
            "balance": balance, 
            "holderName": holderName,
            "number": Bank.getNumber(),
            "maxCredit": maxCredit,
            "password": password  
            }
        self.balance = self.data["balance"]
        self.number = self.data["number"]
        self.holderName = self.data["holderName"]
        self.maxCredit = self.data["maxCredit"]
        self.password = self.data["password"]

        Bank.addAccount(self)

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

    # Ändra maxCredit
    def changeMaxCredit(self):
        amount = float(input("Hur mycket?\n"))
        if amount >= 0:
            self.maxCredit = int(amount)
            self.data["maxCredit"] = self.maxCredit
            print(f"Din nya maximala kredit är {amount} kr")
        else:
            warnings.warn("Negativa kreditvärden är omöjliga!", Warning)


class Bank:
    """
    The container class for the overarching object with global bank functions

    Attributes:
        BANK_NAME (str) - The name of the bank
        accounts (dict[int, BankAccount]) - A dict of the accounts keyed by ther account number
    
    Methods:
        getAccountNumber(cls) -> int:
            returns a unique 6-digit account number that doesn't exist yet.
    """
    
    BANK_NAME: str = "Banken"
    accounts: dict[int, BankAccount] = {}

    @classmethod
    def getAccountNumber(cls) -> int:
        """Returns a 6-digit unique integer account number that doesn't exist yet"""
        num: int = random.randint(100000,999999)
        while num in cls.accounts:
            num = random.randint(100000,999999)
        return num
    # Lägger till ett konto i listan
    @classmethod
    def addAccount(cls, account: BankAccount):      
        cls.accounts.update({account.number: account})
