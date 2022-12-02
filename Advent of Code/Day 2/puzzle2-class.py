import os
import logging as log

os.chdir("./Day 2")

try:
    with open("log3.log", "w") as logFile:
        logFile.truncate(0)
except FileNotFoundError:
    pass

log.basicConfig(
    filename="log3.log",
    level=log.INFO,
    format="%(levelname)s:%(asctime)s --- from %(filename)s in %(module)s >> %(funcName)s ln %(lineno)d: %(msg)s",
)


class Game:
    def __init__(self, game: list) -> None:
        self.opponentChoice = game[0]
        self.goal = game[1]
        self.score = 0 if self.goal == "X" else 3 if self.goal == "Y" else 6
        return

    def addScore(self, score: int) -> None:
        self.score += score
        return

    def answerChoiceScore(self) -> int:
        if self.goal == "X":
            return (
                1
                if self.opponentChoice == "B"
                else 2
                if self.opponentChoice == "C"
                else 3
            )
        elif self.goal == "Y":
            return (
                1
                if self.opponentChoice == "A"
                else 2
                if self.opponentChoice == "B"
                else 3
            )
        else:
            return (
                1
                if self.opponentChoice == "C"
                else 2
                if self.opponentChoice == "A"
                else 3
            )


scores = list()

with open("input.txt") as file:
    games = [Game(game.strip().split(" ")) for game in file.readlines()]

for game in games:
    game.addScore(game.answerChoiceScore())
    scores.append(game.score)

print(sum(scores))
