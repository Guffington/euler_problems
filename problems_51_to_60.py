print("\rLoading packages...", end = "")
from utils import timer, sieve_primes
import math
print("\rAll packages loaded")


@timer
def problem_fiftyone(n):
    """
    Return the smallest prime which can make n other primes by replacing digits
    """
    # First considering all 2 digit numbers
    num_of_digits = 2
    # Set of all primes already checked, to avoid double checking
    checked = set()

    while 1 > 0:
        # Generate all primes with at most 'num_of_digits' digits
        primes = sieve_primes(10 ** num_of_digits)
        # Filter primes for primes only with 'num_of_digits' digits
        relevant_primes = [prime for prime in primes if prime >= 10 ** (num_of_digits - 1)]
        # Create a prime set for easy lookup
        primes_set = set(relevant_primes)
        
        for prime in relevant_primes:
            if prime not in checked:
                # Replace each unique digit
                for digit in set(str(prime)):
                    numbers = [str(prime).replace(digit, str(i)) for i in range(10)]
                    # Check how many digit replacements result in prime numbers
                    prime_numbers = [int(number) for number in numbers if int(number) in primes_set]
                    # Add them all to the checked set so as to not revisit them
                    checked.update(prime_numbers)
                    
                    if len(prime_numbers) >= n:
                        return prime_numbers[0]
        # If no prime set of length n is found, increase the number of digits considered 
        num_of_digits += 1

    
# answer, time = problem_fiftyone(8)
# print(f"The answer to problem fifty-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftytwo(n):
    """
    Return the smallest number x for which x, 2x, 3x, ..., n * x all contain the same digits
    """
    # Begin searching through two digit numbers
    num_of_digits = 2
    while 1 > 0:
        # For the number of digits to be the same, only need to search up to (10 ** num_of_digits) // n to avoid increasing number of digits
        for number in range(10 ** (num_of_digits - 1), ((10 ** num_of_digits) // n) + 1):
            # Compute list of digits for comparison
            digit_list = sorted(str(number))
            for multiple in range(2, n + 1):
                # For each multiple of n check whether it has the same digits as the original
                if sorted(str(number * multiple)) != digit_list:
                    # If not, move to the next number
                    break
                # If we've checked through all n multiples and all have the same digits, return the number
                if multiple == n:
                    return number
        # If we haven't found such a number with the current number of digitis, increase the number of digits
        num_of_digits += 1

# answer, time = problem_fiftytwo(6)
# print(f"The answer to problem fifty-two is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftythree():
    """
    Return the number of times n choose k is greater than 10 ** 6 for 1 <= n <= 100.
    """
    million_counter = 0
    for n in range(23, 100 + 1):
        # No need to consider n choose 0, 1, n or n-1 as these are guaranteed to be less than 10 ** 6
        for k in range(2, n - 1):
            if math.comb(n, k) > 10 ** 6:
                million_counter += 1
                
    return million_counter
    
    
# answer, time = problem_fiftythree()
# print(f"The answer to problem fifty-three is: {answer}    (Run in {time:.5f} s)")



def problem_fiftyfour():
    """
    
    """
    
    
print(problem_fiftyfour())
# print(f"The answer to problem fifty-four is: {answer}    (Run in {time:.5f} s)")