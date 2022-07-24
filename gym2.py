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
    above, below = [], []

    for element in ls:
        if element < value:
            below.append(element)
        else:
            above.append(element)

    above.sort(reverse=True)
    below.sort(reverse=True)

    return above, below


def sorted_combinations(combinations):
    """
    Generate every possible combination of weights

    Input:
        optional (list): plates that can go on each side of the barbell.
                         There is just one number for each pair of plates.

        must_include (list): plates that must be on the barbell


    Output: (total weight, list of plates)
    sorted by total weight DESC, list of plates ASC
    """
    '''
    # Sort plates in descending order
    # itertools.combinations will then sort the plate combinations
    # in descending order too
    optional.sort(reverse = True)
    '''

    unique_combos = list(set(powerset(combinations)))

    # Find the total weight of each combination
    all_weights = [(weight(combo), combo) for combo in unique_combos]

    # Sort the combinations by the total weight
    all_weights.sort(key = lambda tup: tup[0])

    return all_weights


all_big_plates = [22.65, 15.9, 15.0, 11.3, 10.0]
all_plates = all_big_plates + [5.0, 4.5, 2.5, 2.2, 1.25, 1.25, 1.1]

all_weights = sorted_combinations(all_plates)

# Write to .txt file
with open('GymWeights.txt', 'w') as f:
    for total, weights in all_weights:
        # Total value
        line = f"{total:>5}:"
        '''
        # Weights (separated into columns)
        for p in all_plates:
            if p in weights:
                line += "{0:>5}".format(str(p)[:4])
            else:
                line += "     "
        line += "\n"
        f.write(line)
        '''
        big_plates, small_plates = split_at(weights, 10.0)

        # Big weights (separated into columns)
        if big_plates == []:
            pass
        else:
            for p in all_big_plates:
                if p in big_plates:
                    # Write the plate (5 characters, right-aligned)
                    line += f"{str(p)[:4]:>5}"
                else:
                    # Leave a gap (5 characters)
                    line += " "*5
            #line += "\n" + " "*8 + "+ "
            #line += "\n"

        # Small weights
        line += "\n" + " "*7


        line += "{0:>29}".format(" ".join(str(p) for p in small_plates))
        line += "\n"
        '''
        for w in weights:
            line += f" {w}"
            if w < 10.0:
                line += "\n"
        '''
        #line += f"{big_plates} {small_plates}"
        line += "-"*36
        line += "\n"

        f.write(line)
