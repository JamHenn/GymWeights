from itertools import chain
from list_module import powerset, sort_and_deduplicate, split_at
from barbell_module import total_barbell_weight, is_barbell_weight, is_trap_bar_weight


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
all_weights = [(total_barbell_weight(combo), combo) for combo in combinations]
# Sort by total weight; Remove duplicates
all_weights = sort_and_deduplicate(all_weights, key = lambda tup: tup[0])

print(f"Number of weight combinations: {len(all_weights)}")


# Write to .txt file
with open('BarbellWeights_2023.txt', 'w') as f1, open('TrapBarWeights_2023.txt', 'w') as f2:
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
