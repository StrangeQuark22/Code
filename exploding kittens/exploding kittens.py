from numba import njit, jit
import random
import matplotlib.pyplot as plt
import numpy as np
import sys

players: int = 5
initialExplosion: int = 4
cards: int = 56

initialIsBoom: list[bool] = [False] * (cards - (players * 5)) + [True] * initialExplosion

def do(amount: int):
    cardsInDeck: int = len(initialIsBoom)
    for _ in range(amount):
        tempIsBoom: list[bool] = [False] * (cards - (players * 5)) + [True] * initialExplosion
        isBoom = np.empty(shape=len(initialIsBoom))
        for i in range(len(isBoom)):
            isBoom[i] = tempIsBoom.pop(random.randint(0,len(tempIsBoom)-1))
        explosions: int = 4
        chances: list[float] = [explosions / cardsInDeck]
        for i, draw in enumerate(isBoom, start=1):
            if draw:
                explosions -= 1
            
            if explosions <= 0:
                break
            
            chances.append(explosions / (cardsInDeck - i))
        plt.plot(chances)
        if _ % 100 == 0 and _ != 0:
            sys.stdout.write(f"\rNumber {_} done")
            sys.stdout.flush()
    else:
        sys.stdout.write(f"\rNumber {amount} done")
        sys.stdout.flush()

do(10_000)
plt.show()
# print(chances)