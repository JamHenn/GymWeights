from itertools import chain, combinations


def weight(plates):
    """
    Calculate the total weight of a barbell with the given list of plates
    on both sides
    """

    return round(20.0 + 2 * sum(plates), 1)


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def split_at(ls, value):
    """
    Spilt a list at the given value
    """

    above, below = [], []

    for element in ls:
        if element < value:
            below.append(element)
        else:
            above.append(element)

    return above, below


def possible_combinations(optional, must_include = []):
    """
    Generate every possible combination of weights

    Input:
        optional (list): plates that can go on each side of the barbell.
                         There is just one number for each pair of plates.

        must_include (list): plates that must be on the barbell


    Output: (total weight, list of plates)
    sorted by total weight DESC, list of plates ASC
    """

    # Find every combination of the optional plates
    combos = powerset(optional)

    # Sort the plates in descending order for each combination
    return [sorted(combo + tuple(must_include), reverse = True) for combo in combos]


def unique(lst):
    """
    Return the unique elements of an ordered list

    Input: An ordered list
    """

    last = object()

    for item in lst:
        if item == last:
            continue
        yield item
        last = item


def sort_and_deduplicate(l, key):
    """
    Sort a list with the given key, and remove duplicates
    """

    # combos are sorted by total weight, but not by plate configuration
    # So 2 identical combinations could be separated by a third combination
    # with the same total weight.
    # Since the list is not fully sorted, some duplicates will remain
    return list(unique(sorted(l, key = key)))


def is_trap_bar_weight(total, big_plates, small_plates):
    # Total weight on 30kg trap bar exceeds 120
    # 22.65 and 20.0 plates are used
    if (total > 120) and ({20.0, 22.65} <= set(big_plates)):
        # If 5 big plates are used, no more than 6 plates total can fit
        if len(big_plates) >= 5:
            return len(big_plates) + len(small_plates) <= 6

        # If 4 big plates are used, no more than 7 plates total can fit
        if len(big_plates) == 4:
            # Can replace with 2.5 on the shorter side
            if small_plates.count(1.25) == 2:
                return len(small_plates) <= 4;
            return len(small_plates) <= 3

        return True
    return False


def is_barbell_weight(total, plates):
    # Don't use 22.65 plates
    if (22.65 in plates) or (20.0 in plates):
        return False

    # Don't use 20.0 on a weight less than 80
    #if (total < 120) and (20.0 in plates):
    #    return False

    # Cut off at 145
    if (total > 145):
        return False

    return True


def barbell_section_string(big_plates, small_plates):
    """
    Write a section of the BarbellWeights.txt file

    Line length is:
    6 (total) + 6*5 (6 big plates) = 36 characters

    Small plates (7): Up to 29 characters
    """
    section = ""

    # Unique big plates. Two 10s is accounted for below.
    all_big_plates = [15.9, 15.0, 11.3, 10.0]

    # Big weights (separated into columns)
    for p in all_big_plates:
        if p in big_plates:
            # Write the plate (5 characters, right-aligned)
            section += f"{str(p):>5}" * big_plates.count(p)

        else:
            # Leave a gap (5 characters)
            section += " "*5

    # 2nd line: Leave gap under total
    section += "\n" + " "*7

    # Small weights (29 characters, right-justified)
    section += "{0:>29}".format(" ".join(str(p) for p in small_plates))

    # Line of dashes
    section += "\n" + "-"*36 + "\n"

    return section


def trap_bar_section_string(big_plates, small_plates):
    """
    Write a section of the .txt file

    Line length is:
    6 (total) + 7*5 (7 big plates) = 41 characters

    Small plates (7): Up to 29 characters
    """
    section = ""

    all_big_plates = [22.65, 20.0, 15.9, 15.0, 11.3, 10.0]

    # Big weights (separated into columns)
    for p in all_big_plates:
        if p in big_plates:
            # Write the plate (5 characters, right-aligned)
            section += f"{str(p)[:4]:>5}" * big_plates.count(p)

        else:
            # Leave a gap (5 characters)
            section += " "*5

    # 2nd line: Leave gap under total
    section += "\n" + " "*12

    # Small weights (29 characters, right-justified)
    section += "{0:>29}".format(" ".join(str(p) for p in small_plates))

    # Line of dashes
    section += "\n" + "-"*41 + "\n"

    return section


# Weights that come in pairs
plates = [1.1, 1.25, 1.25, 2.2, 2.5, 4.5, 5.0, 10.0, 11.3, 15.0, 15.9, 20.0]
# Use 10 and (two 5s)
plates10 = [1.1, 1.25, 1.25, 2.2, 2.5, 4.5, 10.0, 11.3, 15.0, 15.9, 20.0]
# Use (10 + two 2.5s) and (three 5s)
plates15 = [1.1, 1.25, 1.25, 2.2, 4.5, 11.3, 10.0, 15.0, 15.9, 20.0]
# Use 22.7 kg and (20.1 + 2.5)
plates22 = [1.1, 1.25, 1.25, 2.2, 4.5, 5.0, 10.0, 11.3, 15.0, 15.9, 20.0]
# Use (22.7 + two 5s) and (20.1 + 2.5 + 10)
plates32 = [1.1, 1.25, 1.25, 2.2, 4.5, 10.0, 11.3, 15.0, 15.9, 20.0]


combinations = list(chain(possible_combinations(plates),
                          possible_combinations(plates10, [10.0]),
                          possible_combinations(plates15, [5.0, 10.0]),
                          possible_combinations(plates22, [22.65]),
                          possible_combinations(plates32, [10.0, 22.65])))

# Find the total weight of each combination
all_weights = [(weight(combo), combo) for combo in combinations]
# Sort by total weight; Remove duplicates
all_weights = sort_and_deduplicate(all_weights, key = lambda tup: tup[0])

print(f"Number of weight combinations: {len(all_weights)}")


# Write to .txt file
with open('BarbellWeights_June2021.txt', 'w') as f1, open('TrapBarWeights_June2021.txt', 'w') as f2:
    for total, weights in all_weights:

        big_plates, small_plates = split_at(weights, 10.0)

        # Standard barbell weights
        if is_barbell_weight(total, weights):
            # Total value
            f1.write(f"{total:>5}:")
            # Plate breakdown
            f1.write(barbell_section_string(big_plates, small_plates))


        # Trap bar deadlift weights
        if is_trap_bar_weight(total+10, big_plates, small_plates):
            # Total value (30 kg trap bar)
            f2.write(f"{total+10:>5}:")
            # Plate breakdown
            f2.write(trap_bar_section_string(big_plates, small_plates))
