def total_barbell_weight(plates):
    """
    Calculate the total weight of a barbell with the given list of plates
    on both sides
    """
    return round(20.0 + 2 * sum(plates), 1)


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
