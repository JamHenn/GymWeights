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


def plate_combination_string(is_trap_bar, total, big_plates, small_plates):
    """
    Barbell line length is:
    6 (total) + 6*5 (6 big plates) = 36 characters

    Trap bar line length is:
    6 (total) + 7*5 (7 big plates) = 41 characters
    """
    line_length = 41 if is_trap_bar else 36

    # Unique big plates
    if is_trap_bar: all_big_plates = [22.65, 20.0, 15.9, 15.0, 11.3, 10.0]
    else: all_big_plates = [15.9, 15.0, 11.3, 10.0]

    # Write total weight (+10kg for trap bar)
    text = f"{total+10:>5}:" if is_trap_bar else f"{total:>5}:"

    # Write big weights (separated into columns)
    for p in all_big_plates:
        if p in big_plates:
            # Write the plate (5 characters, right-aligned)
            text += f"{str(p)[:4]:>5}" * big_plates.count(p)

        else: text += " "*5 # Leave a gap (5 characters)

    # Write small weights (right-justified)
    if is_trap_bar:
        text += "\n{0:>41}".format(" ".join(str(p) for p in small_plates))
    else:
        text += "\n{0:>36}".format(" ".join(str(p) for p in small_plates))

    # Write line of dashes
    text += "\n" + "-"*line_length + "\n"

    return text


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
with open('BarbellWeights.txt', 'w') as f1, open('TrapBarWeights.txt', 'w') as f2:
    for total, weights in all_weights:
        big_plates, small_plates = split_at(weights, 10.0)

        # Standard barbell weights
        if is_barbell_weight(total, weights):
            f1.write(plate_combination_string(False, total, big_plates, small_plates))

        # Trap bar deadlift weights
        if is_trap_bar_weight(total+10, big_plates, small_plates):
            f2.write(plate_combination_string(True, total, big_plates, small_plates))
