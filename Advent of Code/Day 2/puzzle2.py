import os
import logging as log

os.chdir("./Day 2")

try:
    with open("log2.log", "w") as logFile:
        logFile.truncate(0)
except FileNotFoundError:
    pass

log.basicConfig(
    filename="log2.log",
    level=log.INFO,
    format="%(levelname)s:%(asctime)s --- from %(filename)s in %(module)s >> %(funcName)s ln %(lineno)d: %(msg)s",
)

scores = list()


def convert(game: list) -> tuple:
    if game[1] == "X":
        return (game[0], "A")
    elif game[1] == "Y":
        return (game[0], "B")
    elif game[1] == "Z":
        return (game[0], "C")
    else:
        raise ValueError("Invalid game")


with open("input.txt") as file:
    games = [convert(game.strip().split(" ")) for game in file.readlines()]

# print(games)


def answer(game: tuple) -> int:
    if game[0] == "A":
        return 2
    if game[0] == "B":
        return 3
    if game[0] == "C":
        return 1
    else:
        raise ValueError("Invalid game input")


def lose(game: tuple) -> int:
    if game[0] == "A":
        return 3
    if game[0] == "B":
        return 1
    if game[0] == "C":
        return 2
    else:
        raise ValueError("Invalid game input")


def draw(game: tuple) -> int:
    if game[0] == "A":
        return 1
    if game[0] == "B":
        return 2
    if game[0] == "C":
        return 3
    else:
        raise ValueError("Invalid game input")


for game in games:
    score = (
        0 + lose(game)
        if game[1] == "A"
        else 3 + draw(game)
        if game[1] == "B"
        else 6 + answer(game)
    )
    scores.append(score)

print(sum(scores))
