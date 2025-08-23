print("\rLoading packages...", end = "")
from utils import timer, permutations, miller_rabin
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