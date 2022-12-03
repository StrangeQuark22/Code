import logging as log

try:
    with open("log2.log", "w") as file:
        file.truncate(0)
except FileNotFoundError:
    pass

log.basicConfig(
    filename="log2.log",
    level=log.DEBUG,
    format="%(levelname)s:%(asctime)s --- from %(filename)s in %(module)s >> %(funcName)s ln %(lineno)d: %(msg)s",  # NOQA
)

with open("input.txt", "r") as f:
    bags = [bag.strip() for bag in f.readlines()]
    groups = []
    while len(bags) > 0:
        groups.append([bags.pop(0) for i in range(3)])
    # log.debug(str(groups))

# fmt: off
prio = lambda letter: " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(letter) # NOQA
# fmt: on

total = 0

log.debug(f"There are {len(groups)} groups to check")

for i, group in enumerate(groups, start=1):
    log.debug(f"Checking group {i}: {group}")
    bag1 = set(group[0])
    log.debug(f"Selected bag: {bag1}    Remaining bags: {[group[1], group[2]]}")
    for letter in bag1:
        log.debug(f"Checking letter '{letter}'")
        if (letter in set(group[1])) and (letter in set(group[2])):
            log.debug(f"Matching letter '{letter}' found")
            total += prio(letter)
        else:
            log.debug("No match")

print(total)
