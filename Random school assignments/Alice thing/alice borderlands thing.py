import numpy as np
import matplotlib.pyplot as plt
from numba import jit
import itertools
import sys

# nums = [num for num in range(1,101)]

# with open("nums.bin", "wb") as file:
#     for i, item in enumerate(itertools.combinations(nums, 5)):
#         for num in item:
#             file.write(num.to_bytes(length=1, byteorder=sys.byteorder, signed=False))
#         if i % 1_000_000 == 0:
#             print(item)

# results: np.ndarray = np.empty(75_287_520, dtype=np.float64)

# with open("nums.bin", "rb") as file:
#     i = 0
#     while numSet := file.read(5):
#         results[i] = (sum(tuple(numSet)) / 5) * 0.8
#         i+=1
#         if i % 1_000_000 == 0:
#             print(tuple(numSet))

# results.tofile("results.bin")

# print(results)

results: np.ndarray = np.fromfile("results.bin", dtype=np.float64)


# @jit(parallel=True, nopython=True)
# def normalFunc(xValues) -> np.ndarray:
#     result: np.ndarray = np.empty(len(xValues), dtype=np.float64)
#     for i, val in enumerate(xValues):
#         result[i] = (1 / (results.std() * np.sqrt(2 * np.pi))) * np.exp(
#             -(np.int8(1) / np.int8(2))
#             * np.power((val - results.mean()) / results.std(), 2)
#         )
#         print(val)
#     return result


# x = np.linspace(0, 80, 50)

# y = normalFunc(x)


plt.hist(results, bins=250)
# plt.plot(x, y)
plt.show()
