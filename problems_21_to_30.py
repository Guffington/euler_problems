import numpy as np
from utils import aliquot_sum

def problem_twentyone(bound):
    """
    Return the sum of all amicable numbers under 'bound'
    """
    # Dictionary to hold the sums of divisors
    factor_sum_dict = {1: 1}
    # List of amicable numbers
    amicable_numbers = []
    
    for n in range(2, bound):
        # Calculate the sum of divisors of n
        sum_of_divisors = aliquot_sum(n)
        
        # Add sum of divisors to the dictionary
        factor_sum_dict[n] = sum_of_divisors
        # Check the dictionary see if the number is amicable; if so append the pair to 'amicable_numbers'
        if sum_of_divisors < n:
            if factor_sum_dict[sum_of_divisors] == n:
                amicable_numbers.extend([sum_of_divisors, n])
        
    return sum(amicable_numbers)
    
# print("The answer to problem twenty-one is: ", problem_twentyone(10000))



def problem_twentytwo():
    """
    Return the total name scores of all names in 'problem_twentytwo_names.txt'
    """

    # Import the file as a list of names
    with open("problem_twentytwo_names.txt", 'r') as n:
        names = n.read().split(",")
        # Remove unnecessary quotation marks; format and sort the names in alphabetical order
        names = [name.strip().strip('"').lower() for name in names]
        names = sorted(names)
        
    counter = 0
    for name in names:
        value = 0
        for letter in name:
            # The value of each letter can be calculated from its Unicode code point
            value += ord(letter) - ord('a') + 1
        # Total name score is the word value multiplied by its position in the list
        counter += value * (names.index(name) + 1)
        
    return counter
        
    
# print("The answer to problem twenty-two is: ", problem_twentytwo())


def problem_twentythree():
    """
    Find the sum of all numbers which cannot be written as the sum of two abundant numbers
    """
    abundant_numbers = []
    
    # Calculate all abundant numbers and store them in 'abundant_numbers'
    for n in range(12, 28183):
        if aliquot_sum(n) > n:
            abundant_numbers.append(n)
    
    # Calculate all possible sums of abundant numbers, store necessary ones inn 'sums_of_abundant_numbers'
    sums_of_abundant_numbers = set( )
    for i, n in enumerate(abundant_numbers):
        for m in abundant_numbers[i:]:
            if n + m < 28183:
                sums_of_abundant_numbers.add(n + m)
    
    # The numbers which can't be written are all the numbers *not* in sums of abundant numbers
    no_sum = set(np.arange(1, 28183, 1)) - sums_of_abundant_numbers
    
    # Sum the numbers not a sum of two abundant numbers
    return sum(list(no_sum))

    
# print("The answer to problem twenty-three is: ", problem_twentythree())



def problem_twentyfour(n):
    """
    Calculate the nth permutation in order of 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    """
    
    def tp(string, a, b):
        """
        Simple transposition: swap letters a and b in 'string'. Indexed from 1.
        """
        if a == b:
            return string
        
        i = min(a, b) - 1
        j = max(a, b) - 1
        
        return string[:i] + string[j] + string[i+1:j] + string[i] + string[j+1:]


    def tp_2(string, list, prepend = ""):
        """
        Transpose last two letters of string, append both permutations to list with a prepend if chosen
        """
        list.append(prepend + string)
        list.append(prepend + tp(string, len(string) - 1, len(string)))
        return list
        
    def tp_n(string, list, prepend = ""):
        """
        Calculate all permutations of all letters of 'string', and store each in 'list'
        This function works recursively: it builds up larger permutations from many smaller transpositions
        """
        if len(string) > 2:
            # For an n-letter string, calculate all permutations on the last (n-1)-letters. Then transpose the first letter with the second letter, and calculate all permutations again. Then transpose the first letter with the third letter etc.
            for i in range(1, len(string) + 1):
                new_string = tp(string, 1, i)
                # The first letter is cut-off and the algorithm is run again on the remaining (n-1)-letters. The first letter is stored in 'prepend' and re-attached to the beginning once all lower order permutations are calculated
                list = tp_n(new_string[1:], list, prepend + new_string[0])
        else:
            # Recursion stops when only swapping the last two letters. All permutations are built up from this.
            list = tp_2(string, list, prepend)
                
        return list
    
    permutations = tp_n("0123456789", [])
        
    return sorted(permutations)[n - 1]

    
print("The answer to problem twenty-four is: ", problem_twentyfour(10**6))