import logging as log

try:
    with open("log1.log", "w") as file:
        file.truncate(0)
except FileNotFoundError:
    pass

log.basicConfig(
    filename="log1.log",
    level=log.DEBUG,
    format="%(levelname)s:%(asctime)s --- from %(filename)s in %(module)s >> %(funcName)s ln %(lineno)d: %(msg)s" # NOQA
)

with open("input.txt") as f:
    bags = [line.strip() for line in f.readlines()]
    log.debug(str(bags))

prio = lambda letter: " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index( # NOQA
    letter
)  # NOQA

# print(bags)

total = 0

log.debug(f"There are {len(bags)} bags to check")

for i, bag in enumerate(bags, start=1):
    left, right = bag[: int(len(bag) / 2)], bag[int(len(bag) / 2):]
    log.debug(f"Contents of bag {i}: {bag}    Left: {left}, Right: {right}")
    for letter in set(left):
        if letter in right:
            log.debug(f"Found shared letter \'{letter}\' worth {prio(letter)} points")
            total += prio(letter)

print(total)
