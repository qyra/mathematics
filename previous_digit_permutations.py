from scipy.special import comb
from multiset import Multiset
import sys
import operator as op
from functools import reduce
"""
Calculates how many previous (smaller) unique numbers there are which use
the same set of digits as the input.

For example, if the input was 4212, then the following options are smaller:
0: 1224
1: 1242
2: 1422
3: 2124
4: 2142
5: 2214
6: 2241
7: 2412
8: 2421
9: 4122

So there are 10 options which are smaller than 4212 
"""

def n_choose_k(n, k):
    k = min(k, n-k)
    if k == 0:
        return 1
    numer = reduce(op.mul, range(n, n-k, -1))
    denom = reduce(op.mul, range(1, k+1))
    return numer//denom


def unique_permutations(n, digits):
    total_arrangements = 1
    for _, count in digits.items():
        arrangements = n_choose_k(n, count)
        total_arrangements = total_arrangements * arrangements
        n = n - count

    return total_arrangements


DEBUG = False


def count_preceding(str_number):
    number = [int(x) for x in list(str_number)]
    all_preceding_options = 0

    for i, curr in enumerate(number):
        if DEBUG:
            print("{0}Position: {1}".format('   '*i, i))
            
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

                if DEBUG:
                    print("{0}Using {1} instead results in {2} options".format('   '*i, digit, up))

                preceding_options = preceding_options + up
            else:
                break
        
        all_preceding_options = all_preceding_options + preceding_options

    return all_preceding_options


def run_tests():
    tests = {
        1224: 0, 
        1242: 1,
        1422: 2,
        2124: 3,
        2142: 4, 
        2214: 5,
        2241: 6, 
        2412: 7, 
        2421: 8, 
        4122: 9,

        123: 0,
        132: 1,
        213: 2,
        231: 3,
        312: 4,
        321: 5
    }

    for test_num, prev_count in tests.items():
        res = count_preceding(str(test_num))
        print("Input {0}: Result {1} == Expected {2}? {3}".format(test_num, res, prev_count, res == prev_count))
        assert(prev_count == res)


if __name__ == "__main__":
    assert(type(sys.argv[1]) == str)

    if sys.argv[1] == "test":
        run_tests()
    else:
        print("Lower unique arrangements: {0}".format(count_preceding(sys.argv[1])))