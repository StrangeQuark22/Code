import os
import logging as log

os.chdir("./Day 2")

try:
    with open("log1.log", "w") as logFile:
        logFile.truncate(0)
except FileNotFoundError:
    pass

log.basicConfig(
    filename="log1.log",
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


def result(game: tuple, num: int) -> int:
    if game[1] == game[0]:
        log.debug(
            f"Resut of game {num}: Player chose {'ROCK' if game[1] == 'A' else 'PAPER' if game[1] == 'B' else 'SCISSORS'} and opponent chose {'ROCK' if game[0] == 'A' else 'PAPER' if game[0] == 'B' else 'SCISSORS'} - draw"
        )
        return 3
    elif (
        (game[1] == "A" and game[0] == "C")
        or (game[1] == "B" and game[0] == "A")
        or (game[1] == "C" and game[0] == "B")
    ):
        log.debug(
            f"Resut of game {num}: Player chose {'ROCK' if game[1] == 'A' else 'PAPER' if game[1] == 'B' else 'SCISSORS'} and opponent chose {'ROCK' if game[0] == 'A' else 'PAPER' if game[0] == 'B' else 'SCISSORS'} - win"
        )
        return 6
    else:
        log.debug(
            f"Resut of game {num}: Player chose {'ROCK' if game[1] == 'A' else 'PAPER' if game[1] == 'B' else 'SCISSORS'} and opponent chose {'ROCK' if game[0] == 'A' else 'PAPER' if game[0] == 'B' else 'SCISSORS'} - loss"
        )
        return 0


for i, game in enumerate(games):
    score = 0
    if game[1] == "A":
        score += result(game, i) + 1
    elif game[1] == "B":
        score += result(game, i) + 2
    elif game[1] == "C":
        score += result(game, i) + 3
    scores.append(score)

print(sum(scores))
