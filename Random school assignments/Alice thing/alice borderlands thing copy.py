import itertools
# from numba import jit, njit
import numpy as np
# import sympy as sp
import matplotlib.pyplot as plt

nums: list[int] = list(range(1, 101))


# @jit(parallel=True)
def getCombs() -> np.ndarray:
    stuff: list[tuple] = []
    for i, item in enumerate(list(itertools.combinations(nums, 5))):
        stuff.append(item)
        if i % 1_000_000 == 0:
            print(item)
    return np.array(stuff, dtype=object)


combinations = getCombs()


# @jit(parallel=True)
def calcMeans(combs):
    means: np.ndarray = np.empty(len(combs), dtype=np.float64)

    for i, comb in enumerate(combs):
        means[i] = np.float64((sum(comb) / 5) * (4 / 5))
        if i % 1_000_000 == 0:
            print(comb)

    return means


results = calcMeans(combinations)

plt.hist(results, bins=250)
plt.show()
