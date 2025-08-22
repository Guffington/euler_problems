print("Loading packages...", end = "")
from utils import timer, find_all_factors, sieve_primes
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

# answer, time = problem_thirtyone()
# print(f"The answer to problem thirty-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirtytwo():
    """
    Find the sum of all pandigital products
    """
    
    def digits(n):
        """
        Return the set of unique digits which feature in n
        """
        digit_set = set()
        for digit in str(n):
            digit_set.add(int(digit))
        return digit_set

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
    
    
# answer, time = problem_thirtytwo()
# print(f"The answer to problem thirty-two is: {answer}    (Run in {time:.5f} s)")


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


# answer, time = problem_thirtythree()
# print(f"The answer to problem thirty-three is: {answer}    (Run in {time:.5f} s)")


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
    
    
# answer, time = problem_thirtyfour()
# print(f"The answer to problem thirty-four is: {answer}    (Run in {time:.5f} s)")



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
    
    
# answer, time = problem_thirtyfive(10 ** 6)
# print(f"The answer to problem thirty-four is: {answer}    (Run in {time:.5f} s)")