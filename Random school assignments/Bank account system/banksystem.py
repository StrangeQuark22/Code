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
        holder_name: str --- The name of the account holder
        max_credit: int --- Maximum allowed credit on the account
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
        holder_name: str
        number: int
        max_credit: int
        hashed_password: str

    # Constructor, skapar ett nytt konto med känd data. Används för filimport
    def __init__(self, holder_name: str, hashed_password: str, balance: float = 0, max_credit: int = 5000, number: Optional[int] = None):
        self.data: BankAccount.AccountData = {
            "balance": balance,
            "holder_name": holder_name,
            "number": Bank.get_account_number() if number is None else number,
            "max_credit": max_credit,
            "hashed_password": hashed_password
        }
        self.balance: float = self.data["balance"]
        self.number: int = self.data["number"]
        self.holder_name: str = self.data["holder_name"]
        self.max_credit: int = self.data["max_credit"]
        self.hashed_password: str = self.data["hashed_password"]

        Bank.add_account(self)

    def update(self, update: AccountData) -> None:
        """Updates account data py parsing an AccountData dict into the appropriate attributes"""
        self.data.update(update)
        og_name: str = self.holder_name

        if "balance" in update and "balance" in self.data:
            self.balance = self.data["balance"]

        if "number" in update and "number" in self.data:
            self.number = self.data["number"]

        if "holder_name" in update and "holder_name" in self.data:
            self.holder_name = self.data["holder_name"]

        if "max_credit" in update and "max_credit" in self.data:
            self.max_credit = self.data["max_credit"]

        if "hashed_password" in update and "hashed_password" in self.data:
            self.hashed_password = self.data["hashed_password"]

        try:
            Bank.update_account(self, og_name)
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
        get_account_number(cls) -> int:
            returns a unique 6-digit account number that doesn't exist yet.
        
        add_account(cls, account: BankAccount) -> None:
            Adds an account to the 'accounts' dict

        update_account(cls, updated_account: BankAccount, original_account_num: int) -> None:
            overwrites the account with the number originalAccountNum with the data in updatedAccount

        save(cls, path: str) -> None:
            Serializes accounts to json att path
        
        load(cls, path: str) -> None:
            Loads serialized accounts from json att path
    """

    BANK_NAME: str = "Banken"
    accounts: dict[str, BankAccount] = {}

    @classmethod
    def get_account_number(cls) -> int:
        """Returns a 6-digit unique integer account number that doesn't exist yet"""
        num: int = random.randint(100000, 999999)
        while num in [acc.number for _, acc in cls.accounts.items()]:
            num = random.randint(100000, 999999)
        return num

    @classmethod
    def add_account(cls, account: BankAccount) -> None:
        """Adds an account to the class attribute storing all accounts. Raises ValueError of name already exists"""
        if account.holder_name not in [acc.number for _, acc in cls.accounts.items()]:
            cls.accounts.update({account.holder_name: account})
        else:
            raise ValueError("Name already exists, choose another one")

    @classmethod
    def update_account(cls, updated_account: BankAccount, og_holder_name: str) -> None:
        """
        Updates the 'accounts' attribute at index originalAccountNum with the updatedAccount object
        
        Exceptions:
            KeyError:
                raises KeyError if the key originalAccountNum doesn't exist in Bank.accounts
            ValueError:
                raises ValueError if the newly selected account number alreas exists in Bank.accounts

        Since exceptions stop excecution a try-except block is recommended with this method to preserve accounts in RAM
        """

        if updated_account.holder_name not in [acc.number for _, acc in cls.accounts.items()]:
            try:
                cls.accounts.pop(og_holder_name)
            except KeyError as exc:
                raise KeyError("Original account number does not exist in the ledger of accounts") from exc
            else:
                cls.accounts.update({updated_account.holder_name: updated_account})
        else:
            raise ValueError("Newly defined account name already exists, insertion impossible")

    @classmethod
    def save(cls, path: str) -> None:
        """Serialise accounts to json and save at path"""
        with open(path, "w", encoding="utf-8") as file:
            json.dump({key: val.data for key, val in cls.accounts.items()}, file)

    @classmethod
    def load(cls, path: str) -> None:
        """Load serialized accounts from json at path"""
        with open(path, "r", encoding="utf-8") as file:
            cls.accounts = {str(key): BankAccount(**val) for key, val in dict(json.load(file)).items()}
