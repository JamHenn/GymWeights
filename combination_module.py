from list_module import powerset


def weight_combinations(optional, must_include = []):
    """
    Generate every possible combination of weights, given
    a list of optional plates (to take combinations of)
    and a list of mandatory plates (which must be included).
    """
    # Find every combination of the optional plates
    combos = powerset(optional)

    # Sort the plates in descending order for each combination
    return [sorted(combo + tuple(must_include), reverse = True) for combo in combos]


def plate_combination_string(is_trap_bar, total, big_plates, small_plates):
    """
    Write formatted text to display the given weight combination.

    Barbell line length:  6 (total) + 6*5 (6 big plates) = 36 characters
    Trap bar line length: 6 (total) + 7*5 (7 big plates) = 41 characters
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
