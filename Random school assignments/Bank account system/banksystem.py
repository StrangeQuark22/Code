import random
from typing import TextIO
import json
from passlib.hash import argon2
from typing import Optional, TypedDict

class BankAccount:
    """
    A class that is essentially a datatype for bank account objects.
    
    Also holds many getting and setting functions for different attributes of the object.

    Instance attributes:
        data: dict --- All data of the account as a dict. The keys are the individual attributes
        balance: float --- The available money on the account
        number: int --- a 6 digit unique numerical identifier for the account
        holderName: str --- The name of the account holder
        maxCredit: int --- Maximum allowed credit on the account
        password: str --- The account password, stored as cleartext for now

    Methods:
        update(self, update: AccountData) -> None:
            Updates appropriate attributes by parsing a partial or full AccountData dict and
            updates itself in Bank.accounts

    Subclasses:
        AccountData(TypedDict):
            TypedDict which stores account data with proper typehints
    """

    class AccountData(TypedDict, total=False):
        """TypedDict for account data storage"""
        balance: float
        holderName: str
        number: int
        maxCredit: int
        hashedPassword: str

    # Constructor, skapar ett nytt konto med känd data. Används för filimport
    def __init__(self, holderName: str, hashedPassword: str, balance: float=0, maxCredit: int=5000, number: Optional[int]=None):
        self.data: BankAccount.AccountData = {
            "balance": balance,
            "holderName": holderName,
            "number": Bank.getAccountNumber() if number == None else number,
            "maxCredit": maxCredit,
            "hashedPassword": hashedPassword
        }
        self.balance: float = self.data["balance"]
        self.number: int = self.data["number"]
        self.holderName: str = self.data["holderName"]
        self.maxCredit: int = self.data["maxCredit"]
        self.password: str = self.data["hashedPassword"]
        
        Bank.addAccount(self)

    def update(self, update: AccountData) -> None:
        """Updates account data py parsing an AccountData dict into the appropriate attributes"""
        self.data.update(update)
        ogNum: int = self.number
        
        if "balance" in update and "balance" in self.data:
            self.balance = self.data["balance"]
        
        if "number" in update and "number" in self.data:
            self.number = self.data["number"]
        
        if "holderName" in update and "holderName" in self.data:
            self.holderName = self.data["holderName"]
        
        if "maxCredit" in update and "maxCredit" in self.data:
            self.maxCredit = self.data["maxCredit"]
        
        if "hashedPassword" in update and "hashedPassword" in self.data:
            self.password = self.data["hashedPassword"]

        try:
            Bank.updateAccount(self, ogNum)
        except ValueError:
            # TODO:
            # Add handling of improper account number selection
            pass
        except KeyError:
            # TODO:
            # Add handling of ogNum doesn't exist
            pass


class Bank:
    """
    Contains attributes of the whole bank as well as global bank functions

    Attributes:
        BANK_NAME: str --- The name of the bank
        accounts: dict[int, BankAccount] --- A dict of the accounts keyed by ther account number
    
    Methods:
        getAccountNumber(cls) -> int:
            returns a unique 6-digit account number that doesn't exist yet.
        
        addAccount(cls, account: BankAccount) -> None:
            Adds an account to the 'accounts' dict

        updateAccounts(cls, updatedAccount: BankAccount, originalAccountNum: int) -> None:
            overwrites the account with the number originalAccountNum with the data in updatedAccount

        save(cls, path: str) -> None:
            Serializes accounts to json att path
        
        load(cls, path: str) -> None:
            Loads serialized accounts from json att path
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
    def addAccount(cls, account: BankAccount) -> None:      
        """Adds an account to the class attribute storing all accounts"""
        cls.accounts.update({account.number: account})

    @classmethod
    def updateAccount(cls, updatedAccount: BankAccount, originalAccountNum: int) -> None:
        """
        Updates the 'accounts' attribute at index originalAccountNum with the updatedAccount object
        
        Exceptions:
            KeyError:
                raises KeyError if the key originalAccountNum doesn't exist in Bank.accounts
            ValueError:
                raises ValueError if the newly selected account number alreas exists in Bank.accounts

        Since exceptions stop excecution a try-except block is recommended with this method to preserve accounts in RAM
        """

        if updatedAccount.number not in cls.accounts:
            try:
                cls.accounts.pop(originalAccountNum)
            except KeyError:
                raise KeyError("Original account number does not exist in the ledger of accounts")
            else:
                cls.accounts.update({updatedAccount.number: updatedAccount})
        else:
            raise ValueError("Newly defined account number already exists, insertion impossible")

    @classmethod
    def save(cls, path: str) -> None:
        """Serialise accounts to json and save at path"""
        with open(path, "w") as file:
            json.dump({key: val.data for key, val in cls.accounts.items()}, file)
    
    @classmethod
    def load(cls, path: str) -> None:
        """Load serialized accounts from json at path"""
        with open(path, "r") as file:
            cls.accounts = {int(key): BankAccount(**val) for key, val in dict(json.load(file)).items()}
        