import os
import numpy as np

os.chdir("D:/MISC/Code/Advent of Code/Day 4")

with open("input.txt", "r") as file:
    data: list[str] = [line.strip() for line in file.readlines()]

pairs: np.ndarray = np.array([line.split(",") for line in data], dtype=str)

matches = 0
print(pairs)
print(type(pairs))

for pair in pairs:
    elf1 = [int(item) for item in pair[0].split("-")]
    elf2 = [int(item) for item in pair[1].split("-")]
    print(elf1, elf2)
    if max(elf1) - min(elf1) > max(elf2) - min(elf2):
        isOverlap: list[bool] = []
        elf1Range = list(range(min(elf1), max(elf1) + 1))
        for i in range(min(elf2), max(elf2) + 1):
            if i in elf1Range:
                isOverlap.append(True)
            else:
                isOverlap.append(False)
        if False in isOverlap:
            continue
        else:
            matches += 1
            continue
    else:
        isOverlap: list[bool] = []
        elf2Range = list(range(min(elf2), max(elf2) + 1))
        for i in range(min(elf1), max(elf1) + 1):
            if i in elf2Range:
                isOverlap.append(True)
            else:
                isOverlap.append(False)
        if False in isOverlap:
            continue
        else:
            matches += 1
            continue

print(matches)
