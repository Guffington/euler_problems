print("\rLoading packages...", end = "")
from utils import timer, permutations, miller_rabin, sieve_primes, is_prime, prime_factors_dict
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

answer, time = problem_fortyone()
print(f"The answer to problem forty-one is: {answer}    (Run in {time:.5f} s)")


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

answer, time = problem_fortytwo()
print(f"The answer to problem forty-two is: {answer}    (Run in {time:.5f} s)")


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

answer, time = problem_fortythree()
print(f"The answer to problem forty-three is: {answer}    (Run in {time:.5f} s)")


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
    
    
answer, time = problem_fortyfour()
print(f"The answer to problem forty-four is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortyfive():
    """
    Return the next number after 40755 which is triangular, pentagonal and hexagonal
    """
    # Initialise sets and n
    triangle, pentagonal, hexagonal, n = set(), set(), set(), 3
    
    # Compute all three sets of numbers up to 10 ** n until their intersection contains a new element
    while len(triangle & pentagonal & hexagonal) <= 2:
        triangle = set([(n * (n + 1)) // 2 for n in range(1, 10 ** n)])
        pentagonal = set([(n * (3*n - 1)) // 2 for n in range(1, 10 ** n)])
        hexagonal = set([(n * (2*n - 1)) for n in range(1, 10 ** n)])
        n += 1
    
    # Return the next number after 40755, which will be the smallest element after 1 and 40755 are removed from the sets.
    return min((triangle & pentagonal & hexagonal) - set([1, 40755]))
    
    
answer, time = problem_fortyfive()
print(f"The answer to problem forty-five is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortysix():
    """
    Return the smallest odd composite number which cannot be written as the sum of a prime and twice a square
    """
    def squares(n):
        """
        Return all square numbers up to n
        """
        return set([n ** 2 for n in range(1, int(math.sqrt(n)))])
    
    # Smallest odd composite number
    n = 9
    while 1 > 0:
        # Filter number for odd composite numbers
        if n % 2 == 1 and not is_prime(n):
            # Find all primes below n (not including 2)
            lower_primes = sieve_primes(n)[1:]
            # Find all squares below n
            squares_set = squares(n)
            for prime in lower_primes:
                if (n - prime) // 2 in squares_set:
                    # If a decomposition is found, move on to next n
                    break
                # If all primes have been tested an no decomposition has been found, n must be the soluton
                if prime == max(lower_primes):
                    return n
        n += 1


answer, time = problem_fortysix()
print(f"The answer to problem forty-six is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortyseven(n):
    """
    Return the first, of the first four consecutive numbers to have four distinct prime factors (including multiplicity)
    """
    number = 6
    while 1 > 0:
        decomposition_set = set()
        for i in range(n):
            dict_items = prime_factors_dict(number + i).items()
            for item in dict_items:
                decomposition_set.add(item)
        if len(decomposition_set) == n ** 2:
            return number
        number += 1
    

answer, time = problem_fortyseven(4)
print(f"The answer to problem forty-seven is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fortyeight(n):
    """
    Return the sum of 1 ** 1 + 2 ** 2 + ... + n ** n
    """
    # Use efficent pow function to do multiplication with modulo
    digits = str(sum(pow(i, i, 10 ** 10) for i in range(1, n + 1)) % (10 ** 10))
    
    # If the last ten digits begin with zeros we need to re-append them at the beginning for display
    if len(digits) < 10:
        digits = ("0" * (10 - len(digits))) + digits
    
    return digits
    
    
answer, time = problem_fortyeight(1000)
print(f"The answer to problem forty-eight is: {answer}    (Run in {time:.5f} s)")
    
    
@timer
def problem_fortynine():
    """
    Find the only 4-digit arithmetic sequence  of three primes which are all permutations of each other, other than (1487, 4817, 8147)
    """
    # Generate all primes with up to 4 digits
    primes = sieve_primes(10 ** 4)
    # Remove any primes with less than 4 digits
    primes = [prime for prime in primes if prime > 10 ** 3]
    # Create a set of primes for easy look-up
    primes_set = set(primes)
    
    # The set 'checked' will contain all 4 digit numbers considered thus far
    checked = set()
    # The list 'found' will contain all successful arthimetic permutation prime 4-digit sequences
    found = []
    
    for prime in primes:
        # Don't bother if we've already seen a number
        if prime not in checked:
            # Remove any duplicates that can arise during permuting. This can happen if digits are repeated
            permutation_list = sorted(list(set(permutations(str(prime)))))
            # Create a version of the permutation list with integers rather than strings
            permutation_list_int = list(map(int, permutation_list))
            # Filter out all permutations which which are not prime or don't have 4 digits; the latter can occur when a 4 digit number contains a 0 digit
            prime_permutations = [permutation  for permutation in permutation_list_int if permutation in primes_set and len(str(permutation)) == 4]
            # Only continue if there are at least 3 primes remaining, the minimal number required for an arithmetic sequence
            if len(prime_permutations) >= 3:
                # Find any possible arithmetic sequences: search through differences between any two numbers, and see if theres a third number with the same difference with the second
                for i in range(len(prime_permutations) - 2):
                    for j in range(i + 1, len(prime_permutations) - 1):
                        difference = prime_permutations[j] - prime_permutations[i]
                        number = prime_permutations[j] + difference
                        if number in prime_permutations:
                            found.append((prime_permutations[i], prime_permutations[j], number))
            # Add all numbers seen to the checked set, so as to not consider them again
            checked = checked | set(permutation_list_int)
                
            # We know there are only two arithmetic sequences, stop searching once they're found
            if len(found) >= 2:
                break
    
    for sequence in found:
        # Filter out the sequence already given in the problem
        if sequence != (1487, 4817, 8147):
            # Concatenate the numbers of the remaining sequence; return the concatenation
            concatenation = ""
            for number in sequence:
                concatenation += str(number)
            return concatenation

answer, time = problem_fortynine()
print(f"The answer to problem forty-nine is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fifty(bound):
    """
    Find the largest sequence of primes numbers which sum up to a prime below 'bound'
    """
    # Generate a list of all primes up to 'bound'
    primes = sieve_primes(bound)
    # Create a set of primes for easy lookup
    prime_set = set(primes)
    
    # We can find an upper bound on the possible sequence lengths of primes by summing the smallest primes until we exceed bound
    counter = 0
    total = 0
    for prime in primes:
        total += prime
        counter += 1
        if total > primes[-1]:
            sequence_bound = counter - 1
            break
    
    
    largest = 0
    # Search sequence lengths backwards from the largest sequence length
    for length in reversed(range(1, sequence_bound + 1)):
        for i, prime in enumerate(primes):
            # Find the sum of the sequence of 'length' consecutive primes beginning with 'prime'
            sequence_sum = sum([primes[i + j] for j in range(length)])
            if sequence_sum in prime_set and sequence_sum > largest:
                largest = sequence_sum
            # We can stop searching through sequences of length 'length' once the sums are exceeding the bound.
            if sequence_sum >= primes[-1]:
                if largest > 0:
                    # If we have found a prime sequence, it must be the largest possible since we are searching in reverse length order
                    return largest
                else:
                    break
    
    
answer, time = problem_fifty(10 ** 6)
print(f"The answer to problem fifty is: {answer}    (Run in {time:.5f} s)")