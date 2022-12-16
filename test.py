import json

with open("accounts.json", "r") as file:
    accounts = json.load(file)

print(accounts)
