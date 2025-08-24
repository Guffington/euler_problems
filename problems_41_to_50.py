print("\rLoading packages...", end = "")
from utils import timer, permutations, miller_rabin
import math
print("\rAll packages loaded")


@timer
def problem_fortyone():
    """
    Return the largest pandigital prime
    """
    # Checking all n! 9-digit pandigital numbers will be difficult with standard sieve methods. Use the Miller-Rabin test instead, which can be deterministic up to 10 ** 10 using [2, 3, 5, 7, 11] as bases
    pandigital_number = "123456789"
    
    for i in range(9):
        if i == 0:
            number = pandigital_number
        else:
            # With each iteration remove the last digit from the pandigital number
            number = pandigital_number[:-i]
        # Calculate all permutations of the pandigital number
        permutation_list = sorted(permutations(number))
        # Process numbers from largest to smallest
        for permutation in reversed(permutation_list):
            # Miller-Rabin test only applies to odd numbers, which are the only prime candidates anyway
            if int(permutation[-1]) not in [2, 4, 5, 6, 8]:
                if miller_rabin(int(permutation), [2, 3, 5, 7, 11]):
                    # As soon as a prime number is found, it must be the largest, so return it
                    return permutation
                
    # If no number is found, there must not be a pandigitial prime
    return None

# answer, time = problem_fortyone()
# print(f"The answer to problem forty-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortytwo():
    """
    Calculate the number of words in problem_fortytwo_words.txt have a value which is a triangle number
    """
    # Read in the file, formatting the words into a standard form
    with open("problem_fortytwo_words.txt", 'r') as w:
        words = w.read().split(",")
        words = [word.strip().strip('"').lower() for word in words]
        words = sorted(words)
        
    # Calculate the first 50 triangle numbers, which should contain large enough numbers to cover the value of any word in the file. A word would need to have a minimum of 48 letters to possibly have more a value larger than the 50th triangle number
    triangle_numbers = set([n * (n + 1) / 2 for n in range(50)])
    triangle_counter = 0
    for word in words:
        # Use ord to calculate the value of each letter, summing the result
        word_value = sum(ord(letter) - ord('a') + 1 for letter in word)
        # Put in a warning for the small chance in which we haven't listed enough triangle numbers
        if word_value > max(triangle_numbers):
            print("Warning: Word found with value larger than all computed triangle numbers. Increase set of triangle numers!")
        if word_value in triangle_numbers:
            triangle_counter += 1
    
    return triangle_counter

# answer, time = problem_fortytwo()
# print(f"The answer to problem forty-two is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortythree():
    """
    Find the sum of all 0 to 9 pandigital numbers with the divisibility property
    """
    permutation_list = permutations("0123456789")
    # Remove numbers beginning with zero, not considered 0 to 9 pandigital
    permutation_list = sorted([permutation for permutation in permutation_list if permutation[0] != "0"])
    # List of primes to test
    primes = [2, 3, 5, 7, 11, 13, 17]
    
    divisible = []
    for permutation in permutation_list:
        # Loop through all the 3-digit combinations
        for i in range(1, 8):
            number = int(permutation[i:i + 3])
            # Move on if one divisibility criterion fails
            if number % primes[i - 1] != 0:
                break
            # If it passes all the divisibility criteria then add the number to the list
            if i == 7:
                divisible.append(int(permutation))
            
    return sum(divisible)

# answer, time = problem_fortythree()
# print(f"The answer to problem forty-three is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortyfour():
    """
    Find the minimal difference between pairs of pentagonal numbers whose sum and difference is also pentagonal
    """
    
    # Create a very large set of pentagonal numbers to check. Use a set rather than a list for fast lookup
    pentagonal_numbers = set([(n * (3*n - 1)) // 2 for n in range(1, 10 ** 5 + 1)])
    
    for x in range(len(pentagonal_numbers)):
        # Make sure y < x
        for y in range(1, x):
            # Generate two pentagonal numbers
            p1 = (x * (3 * x - 1)) // 2
            p2 = (y * (3 * y - 1)) // 2
            # Check their sum and difference
            if p1 + p2  in pentagonal_numbers:
                if p1 - p2 in pentagonal_numbers:
                    # As soon as one is found it will be the solution, since the pentagonal numbers grow monotonically, all smaller differences will have been checked
                    return p1 - p2
    
    
# answer, time = problem_fortyfour()
# print(f"The answer to problem forty-four is: {answer}    (Run in {time:.5f} s)")