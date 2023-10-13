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


def sort_and_deduplicate(l, key, reverseFlag=False):
    """ Sort a list with the given key, and remove duplicates """
    return list(unique(sorted(l, key=key, reverse=reverseFlag)))
