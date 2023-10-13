from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def split_at(ls, value):
    """ Spilt a list at the given value """
    above, below = [], []
    for element in ls:
        if element < value: below.append(element)
        else: above.append(element)

    return above, below


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
    """ Sort a list with the given key, and remove duplicates """

    # combos are sorted by total weight, but not by plate configuration
    # So 2 identical combinations could be separated by a third combination
    # with the same total weight.
    # Since the list is not fully sorted, some duplicates will remain
    return list(unique(sorted(l, key = key)))
