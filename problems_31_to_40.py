print("\rLoading packages...", end = "")
from utils import timer, find_all_factors, sieve_primes, is_prime, digits
from fractions import Fraction
import math
print("\rAll packages loaded")

@timer
def problem_thirtyone():
    """
    Calculate how many different ways of decomposing two-pounds into lesser coins
    """
    list_of_dicts = []
    
    # Build up from 1p, 2p coins; the number of different decompositions is trivial in this case
    new_dict = {0 : 1}
    for i in range(1, 200 + 1):
        # if i is even, the number of decompositions is i/2 + 1
        if i % 2 == 0:
            new_dict[i] = (i // 2) + 1
        # if i is odd, the number of decompositions is the same as i - 1
        else:
            new_dict[i] = new_dict[i-1]
    list_of_dicts.append(new_dict)
    
    # Build up combinations by adding in each coin
    for coin in [5, 10, 20, 50, 100, 200]:
        # Dictionary to contain the number of combinations for each number up to 200p.
        new_dict = {0 : 1}
        prev_dict = list_of_dicts[-1]
        for i in range(1, 200 + 1):
            divides = i // coin
            # 'coin' can go into 'i' 'divides' many times; for each time we sum the number of ways of making the remainder with lesser coins, using the previous dictionary
            new_dict[i] = sum(prev_dict[i - coin * j] for j in range(divides + 1))
        list_of_dicts.append(new_dict)
        
    # Return the number of ways of making 200p from the most recent dictionary, which includes all coins
    return list_of_dicts[-1][200]

answer, time = problem_thirtyone()
print(f"The answer to problem thirty-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtytwo():
    """
    Find the sum of all pandigital products
    """

    def factor_pairs(n):
        """
        Return all factors of n in pairs, which together multiply to give n
        """
        factors = find_all_factors(n)
        factor_pairs = []
        # find_all_factors returns a list of all factors in asending order; pair them off by linearly searching through the list in both directions
        for index in range(len(factors) // 2):
            factor_pairs.append((factors[index], factors[-(index + 1)]))
        return factor_pairs
    
    pandigital_numbers = []

    # Pandigital numbers can only have 4 digits, otherwise no such mutiplicand/multiplier/product identity is possible
    for number in range(1000, 10000):
        # Only proceed if 'number' has no repeated digits
        if len(digits(number)) == len(str(number)):
            # Find the decompositions of 'number' into multiplicant/multiplier pairs
            factors = factor_pairs(number)
            for factor in factors:
                # Amalgamate all digits into one set
                all_digits = digits(factor[0]) | digits(factor[1]) | digits(number)
                if all_digits == set([1,2,3,4,5,6,7,8,9]):
                    pandigital_numbers.append(number)        
    
    return sum(set(pandigital_numbers))
    
    
answer, time = problem_thirtytwo()
print(f"The answer to problem thirty-two is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtythree():
    """
    Return the denominator of the product of all four non-trivial fractions which have naive cancellation
    """
    naive_fractions = []
    for i in range(1, 9 + 1):
        for j in range(1, 9 + 1):
            for k in range(1, 9 + 1):
                # Consider all fractions of the form ij/ki
                numerator = int(str(i) + str(j))
                denominator = int(str(k) + str(i))
                if numerator < denominator and numerator / denominator == j/k:
                    naive_fractions.append(Fraction(j, k))
                # Consider all fractions of the form ij/ki
                numerator = int(str(j) + str(i))
                denominator = int(str(i) + str(k))
                if numerator < denominator and numerator / denominator == j/k:
                    naive_fractions.append(Fraction(j, k))
                    
    # Take the product of all such naive fractions
    product = Fraction(1, 1)
    for fraction in naive_fractions:
        product *= fraction
        
    return product.denominator


answer, time = problem_thirtythree()
print(f"The answer to problem thirty-three is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtyfour():
    """
    Find the sum of all numbers which are the sum of the factorials of their digits.
    """
    # The sum of the factorial of 7 digit numbers can be at most the following bound. This implies that no higher number could be the sum for the factorials of its digits
    bound = 2540160
    
    factorial_numbers = []
    for i in range(10, bound):
        factorial_sum = sum(math.factorial(int(digit)) for digit in str(i))
        if factorial_sum == i:
            factorial_numbers.append(i)

    return sum(factorial_numbers)
    
    
answer, time = problem_thirtyfour()
print(f"The answer to problem thirty-four is: {answer}    (Run in {time:.5f} s)")



@timer
def problem_thirtyfive(n):
    """
    Calculate the number circular primes below one n
    """
    def digit_rotation(number):
        """
        Circularly rotate the digits of 'number'; putting the first digit at the end
        """
        string = str(number)
        string = string[1:] + string[0]
        return string
    
    # Find all primes up to n
    primes = set(sieve_primes(n))
    
    circular_primes = []
    for prime in primes:
        for i in range(len(str(prime))):
            prime_copy = prime
            # Consider all circular rotations of i and check if they're all prime
            for _ in range(i):
                prime_copy = digit_rotation(prime_copy)
            # As soon as one is found to be not prime, move on
            if int(prime_copy) not in primes:
                break
            # Only add the prime to the list once all of its circular rotations have been considered
            if i == len(str(prime)) - 1:
                circular_primes.append(prime)
            
    return len(circular_primes)
    
    
answer, time = problem_thirtyfive(10 ** 6)
print(f"The answer to problem thirty-five is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtysix(n):
    """
    Return the sum of all numbers less than one million which are palindromic in both decimal and binary systems
    """
    palindromes = []
    for i in range(n):
        # Use the bin() function to calculate the binary version of 'i'; need to cut off the '0b' string
        if str(i) == str(i)[::-1] and bin(i)[2:] == bin(i)[:1:-1]:
            palindromes.append(i)

    return sum(palindromes)
    
answer, time = problem_thirtysix(10 ** 6)
print(f"The answer to problem thirty-six is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtyseven():
    """
    Find the sum of all eleven left/right truncatable primes
    """
    # We can deduce the following facts:
    # - Last digit must be 3, 5, 7
    # - 4, 6, 8 cannot feature in the number
    # - 2, 5 can only be the first digit of a number
    
    last_digits = [3, 5, 7]
    possible_digits = [1, 2, 3, 5, 7, 9]
    
    # First construct all two-digit left-truncatable numbers
    left_truncatable = []
    truncatable = set()
    for last_digit in last_digits:
        for first_digit in possible_digits:
            number = int(str(first_digit) + str(last_digit))
            if is_prime(number):
                left_truncatable.append(number)
                # If the first digit is prime then it is also right tuncatable
                if first_digit in [2, 3, 5, 7]:
                    truncatable.add(number)
    
    # From the two digit left-truncatable numbers, build up (mostly) all left truncatable numbers. This loop keeps adding numbers to the 'left_truncatable' list, and then builds off those until no more left-truncatable numbers exist
    for number in left_truncatable:
        # Don't build on any numbers beginning with a 2 or a 5 since they will obviously get excluded later
        if str(number)[0] not in ["2", "5"]:
            for digit in possible_digits:
                new_number = int(str(digit) + str(number))
                if is_prime(new_number) and new_number not in left_truncatable:
                    left_truncatable.append(new_number)
    
    # Now check the right truncatability of each of the left-truncatable numbers
    for number in left_truncatable:
        for i in range(1, len(str(number))):
            # Start with the first digit then add a digit each time, checking each round if the number is prime
            new_number = int(str(number)[:i])
            if not is_prime(new_number): 
                break
            if i == len(str(number)) - 1:
                truncatable.add(number)
                
    # Sum all the left and right truncatable numbers
    return sum(truncatable)
    
answer, time = problem_thirtyseven()
print(f"The answer to problem thirty-seven is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtyeight():
    """
    Find the longest panditigal number which can be expressed as a concatenated product
    """
    all_digits = set('123456789')
    
    pandigitals = []
    # Given 918273645 was mentioned in the problem, to find a larger solution the original number being multiplied must begin with at least '92'.
    for num in range(92, 10000):
        pandigital = str(num)
        if int(pandigital[:2]) >= 92 and len(set(pandigital)) == len(pandigital):
            # Multiply by each digit from 1 to 9
            for n in range(2, 9 + 1):
                pandigital += str(num * n)
                # Check that each multiplication doesn't add any repeated digits
                if len(set(pandigital)) == len(pandigital) and set(pandigital) == all_digits:
                    pandigitals.append(pandigital)
                    break
                # Break if a repeated digit is found at any stage
                elif len(set(pandigital)) < len(pandigital):
                    break
                
    return max(pandigitals)
    
answer, time = problem_thirtyeight()
print(f"The answer to problem thirty-eight is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtynine():
    """
    Find the perimeter less than 1000 of a right angle triangle which has the most decompositions into integral side lengths
    """
    # All pythagorean triples can be written in the form k * (m**2 - n**2), k * (2*m*n), k*(m**2 + n**2) where k, m, n are positive integers and m > n
    
    # Initialise a dictionary to track the counts of different perimeters that come up and a set to store each triple so as to not double count
    triples_counter = {}
    triples_set = set()
    # Since m, n are squared, they only need to be checked up to sqrt(1000)
    bound = int(math.sqrt(1000))
    for n in range(1, bound + 1):
        for m in range(n + 1, bound + 1):
            for k in range(1, 1000):
                a, b, c = sorted([k * (m**2 - n**2), k * (2*m*n), k*(m**2 + n**2)])
                p = a + b + c
                if p > 1000:
                    # As soon as the perimeter is reached we can stop searching through k
                    break
                else:
                    if (p, a, b, c) in triples_set:
                        # Move on if we have already seen this triple
                        break
                    else:
                        triples_set.add((p, a, b, c))
                        # If this is a unique triple add it to the count
                        if p in triples_counter:
                            triples_counter[p] += 1
                        else:
                            triples_counter[p] = 1
    
    return max(triples_counter, key = triples_counter.get)
    
answer, time = problem_thirtynine()
print(f"The answer to problem thirty-nine is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_forty():
    """
    Find the product of various digits of Champernowne's Constant
    """
    # List of digits we want to find.
    milestones = [10 ** n for n in range(6 + 1)]
    
    # List of digits we care about
    d_list = []
    # Track the length of Champernowne's Constant as we progress
    length_counter = 0
    # We add each integer to the end of Champernowne's Constant
    number = 1
    # For each milestone digit, we wait until the number of digits build beyond it, then add that digit to 'd_list'
    for milestone in milestones:
        while length_counter < milestone:
            if length_counter + len(str(number)) >= milestone:
                diff = (length_counter + len(str(number))) - milestone
                # As the length exceeds each digit milestone backtrack by 'diff' and add the digit of interest as a tuple along with the milestone
                d_list.append((milestone, int(str(number)[-diff - 1])))
            # Add 'number' to Champernowne's Constant and count the increase in digit length
            length_counter += len(str(number))
            number += 1
        
    # Take the product of all digits of interest
    product = 1
    for digit in d_list:
        product *= digit[1]
    
    return product

    
answer, time = problem_forty()
print(f"The answer to problem forty is: {answer}    (Run in {time:.5f} s)")