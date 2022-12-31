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
            "number": Bank.getAccountNumber(),
            "maxCredit": maxCredit,
            "password": password  
            }
        self.balance: float = float(self.data["balance"])
        self.number: int = int(self.data["number"])
        self.holderName: str = str(self.data["holderName"])
        self.maxCredit: int = int(self.data["maxCredit"])
        self.password: str = str(self.data["password"])
        
        Bank.addAccount(self)


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
    
    @classmethod
    def addAccount(cls, account: BankAccount):      
        """Adds an account to the class attribute storing all accounts"""
        cls.accounts.update({account.number: account})
