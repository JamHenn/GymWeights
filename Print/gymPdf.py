import pandas as pd
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


def sort_and_deduplicate(ls):
    """
    Sort a list (ascending), and remove duplicates
    """

    return list(unique(sorted(ls)))


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

    # Range: 40-120
    if (total < 40) or (total > 110):
        return False

    return True


def create_dfs(weight_combinations):
    barbell_table = []
    trapbar_table = []

    for combination in weight_combinations:
        total = combination[0]
        plates = combination[1]

        big_plates, small_plates = split_at(plates, 10.0)

        big_plate_string = "`"
        small_plate_string = " ".join(str(p) for p in small_plates)

        if is_barbell_weight(total, plates):
            # Unique big plates. Two 10s is accounted for below.
            all_big_plates = [15.9, 15.0, 11.3, 10.0]

            # Big weights (separated into columns)
            for p in all_big_plates:
                if p in big_plates:
                    # Write the plate (5 characters, right-aligned)
                    big_plate_string += f"{str(p):>5}" * big_plates.count(p)

                else:
                    # Leave a gap (5 characters)
                    big_plate_string += " "*5

            barbell_table.append([total, big_plate_string, small_plate_string])

        if is_trap_bar_weight(total+10, big_plates, small_plates):
            # Unique big plates. Two 10s is accounted for below.
            all_big_plates = [22.65, 20.0, 15.9, 15.0, 11.3, 10.0]

            # Big weights (separated into columns)
            for p in all_big_plates:
                if p in big_plates:
                    # Write the plate (5 characters, right-aligned)
                    big_plate_string += f"{str(p)[:4]:>5}" * big_plates.count(p)

                else:
                    # Leave a gap (5 characters)
                    big_plate_string += " "*5

            trapbar_table.append([total+10, big_plate_string, small_plate_string])

    barbell_df = pd.DataFrame(barbell_table, columns = ['Total', 'Big Plates', 'Small Plates'])
    trapbar_df = pd.DataFrame(trapbar_table, columns = ['Total', 'Big Plates', 'Small Plates'])

    return barbell_df, trapbar_df



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
print(f"Number of weight combinations: {len(all_weights)}")
# Sort by total weight & plates; Remove duplicates
all_weights = sort_and_deduplicate(all_weights)
print(f"Number after removing duplicates: {len(all_weights)}")

barbell_df, trapbar_df = create_dfs(all_weights)

print("\nBarbell Weights")
print(barbell_df.info())
print("\nTrap Bar Weights")
print(trapbar_df.info())

# trapbar_df.to_html('~/Documents/GymWeights/Print/trapbar.html', index=False)
barbell_df.to_csv('~/Documents/GymWeights/Print/barbell.csv', index=False)
trapbar_df.to_csv('~/Documents/GymWeights/Print/trapbar.csv', index=False)
