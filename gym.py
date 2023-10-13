from itertools import chain
from list_module import sort_and_deduplicate, split_at
from barbell_module import total_barbell_weight, is_barbell_weight, is_trap_bar_weight
from combination_module import weight_combinations, plate_combination_string


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


combinations = list(chain(weight_combinations(plates),
                          weight_combinations(plates10, [10.0]),
                          weight_combinations(plates15, [5.0, 10.0]),
                          weight_combinations(plates22, [22.65]),
                          weight_combinations(plates32, [10.0, 22.65])))

# Find the total weight of each combination
all_weights = [(total_barbell_weight(combo), combo) for combo in combinations]
# Sort by total weight; Remove duplicates
#all_weights = sort_and_deduplicate2(all_weights)#, key = lambda tup: tup[0])
all_weights = sort_and_deduplicate(all_weights, key = lambda t: (-t[0], t[1]), reverseFlag=True)

print(f"Number of weight combinations: {len(all_weights)}")


# Write to .txt file
barbell_file = 'output/BarbellWeights.txt'
trapbar_file = 'output/TrapBarWeights.txt'
with open(barbell_file, 'w') as bfile, open(trapbar_file, 'w') as tfile:
    for total, weights in all_weights:
        big_plates, small_plates = split_at(weights, 10.0)

        # Standard barbell weights
        if is_barbell_weight(total, weights):
            bfile.write(plate_combination_string(False, total, big_plates, small_plates))

        # Trap bar deadlift weights
        if is_trap_bar_weight(total+10, big_plates, small_plates):
            tfile.write(plate_combination_string(True, total, big_plates, small_plates))
