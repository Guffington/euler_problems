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

answer, time = problem_fortyone()
print(f"The answer to problem thirty-one is: {answer}    (Run in {time:.5f} s)")