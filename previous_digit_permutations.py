from scipy.special import comb
from pprint import pprint
from multiset import Multiset
import sys

def unique_permutations(n, digits):
    total_arrangements = 1
    for _, count in digits.items():
        arrangements = comb(n, count, exact=True)
        total_arrangements = total_arrangements * arrangements
        n = n - count

    return total_arrangements


if __name__ == "__main__":
    assert(type(sys.argv[1]) == str)
    number = [int(x) for x in list(sys.argv[1])]
    all_preceding_options = 0

    for i, curr in enumerate(number):
        full_sequence = number[i:]
        rem_sequence = number[i+1:]
        
        n = len(rem_sequence)
        full_digits = Multiset(full_sequence)
        rem_digits = Multiset(rem_sequence)

        preceding_options = 0

        for digit in sorted(rem_digits.distinct_elements()):
            if digit < curr:
                # If this digit had been used first, how many 
                # possibilities would there have been?
                new_digits = full_digits.copy()
                new_digits[digit] = new_digits[digit] - 1
                up = unique_permutations(n, new_digits)
                preceding_options = preceding_options + up
            else:
                break
        
        all_preceding_options = all_preceding_options + preceding_options

    print('Previous unique arrangements: ', all_preceding_options)
