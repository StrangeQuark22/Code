from banksystem import BankAccount, Bank
from passlib.hash import argon2

Bank.load("test.json")

acc = Bank.accounts[499040]

print(acc.data)
print(acc.number)

acc.update({"number": 255355})

print(acc.data)
print(acc.number)
print(Bank.accounts[acc.number].data)
print(Bank.accounts[acc.number].number)