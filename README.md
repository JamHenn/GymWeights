# Home Gym Barbell Weights
This project came about during the Covid pandemic, while I was exercising in a home gym.

The goal was to calculate every possible combination of weights that could be used on the barbell,
sort them, and display them in an easily readable format.

## Background
The gym had two main sets of weights: One based in kilograms, and one based in pounds.
Adding up a weight combination using the kilogram-weights is fairly easy to do in your head.
However, the imperial (pound) weights have values like this when converted to kilograms (values rounded):

| Pounds (lb) | Kilograms (kg) |
| -------- | ------- |
| 2.5 | 1.1 |
| 5 | 2.2 |
| 10 | 4.5 |
| 25 | 11.3 |
| 35 | 15.9 |
| ... | ... |

These weights, converted to kilograms, are harder to add up in your head.

Additionally, the smallest kilogram-weight in the gym was 1.25 kg, which meant that the smallest increment on the barbell, using only kilogram-weights, would be 2.5 kg (by using a 1.25 kg plate on side side).

However, using a mixture of lb- and kg-plates allows for many more combinations.
This facilitates using smaller weight increments week-to-week. For example, here's a 0.5 kg jump from 72.5 kg to 73 kg:

| Total Weight (kg) | Plates |
| -------- | ------- |
| 72.5 | 15.0, 10.0, 1.25 |
| 73.0 | 15.9, 5.0, 4.5, 1.1 |

The total weight is the sum of the plates times two (since they're on each side of the barbell), plus 20 kg for the barbell itself.

Note that the two combinations above are completely different.
This illustrates the main utility of this program:
0.5 kg is a common increment between workouts when doing strength training,
but finding the next weight combination is difficult to do in your head,
since:
1. there are so many combinations of plates, and
2. the next combination is often completely different to the previous one (as shown in the example).

So, having every combination calculated and sorted turned out to be very useful for this gym.


## The Code

### Basic Algorithm
I wrote the first iteration of this program in late 2020.

The basic algorithm is to take the full list of plates, and then get every combination via the power set (technically not a set, since plates can appear more than once).

### Restrictions on Available Plates
There are some weights in the gym that did not come in pairs.
For example, there were three 10 kg plates.
However, these could still be used together, since there were also two 5 kg plates,
which could be used together with the 3rd 10 kg plate.

For example, here's a combination for 60 kg:

| Left side | Right side |
| -------- | ------- |
| 10.0, 10.0 | 10.0, 5.0, 5.0 |

So for these combinations that use all three 10 kg plates:
The 5 kg plates will not be available for weight combinations,
since must both be used on one side to balance the barbell.

Another example is a 22.65 kg plate, whose pair is unbalanced (it weighs about 20 kg).
This can be balanced by using a single 2.5 kg plate.
So when this 22.65 kg plate is used, the 2.5 kg plates will not be available for combinations.

**In summary:** Since adding some plates will restrict the use of others,
there are actually multiple lists of available plates.

This means a bit more logic is needed to find all combinations.

### Additional Logic
The gym also has a 30 kg trap (hex) bar. The program also gives combinations for this.

With the trap bar, we would always use the 22.65 kg plates (and a 2.5 kg plate for balance, as described above). Also, since the bar itself was shorter, there was a limit on how many plates could fit onto it. These conditions, along with a few others, are used to restrict the combinations in the output files.

### Output

The program writes all the weight combinations into two text files: one for the barbell, and one for the trap bar.
It does some work to format the combinations based on total weight,
large plates required (with _large_ meaning 10 kg or more),
and small plates required.
