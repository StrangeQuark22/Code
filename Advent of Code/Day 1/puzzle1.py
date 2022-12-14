
import numpy as np

allData = ""
with open("./Day 1/input1.txt", "r", encoding="utf-8") as file:
    for line in file:
        allData += line

elfs = np.array(
    [np.array(bundle.split("\n")).astype(int) for bundle in allData.split("\n\n")]
)
print(elfs)

sums = []

for elf in elfs:
    sums.append(sum(elf))
print("\n\n largest: ", max(sums))
