print("Loading packages...", end = "")
import numpy as np
from utils import timer, aliquot_sum, sieve_primes, is_prime, permutations
print("\rAll packages loaded")


@timer
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
    
answer, time = problem_twentyone(10000)
print(f"The answer to problem twenty-one is: {answer}    (Run in {time:.5f} s)")


@timer
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
        
    
answer, time = problem_twentytwo()
print(f"The answer to problem twenty-two is: {answer}    (Run in {time:.5f} s)")


@timer
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

    
answer, time = problem_twentythree()
print(f"The answer to problem twenty-three is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_twentyfour(n):
    """
    Calculate the nth permutation in order of 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    """
    
    permutation_list = permutations("0123456789")
        
    return sorted(permutation_list)[n - 1]

    
answer, time = problem_twentyfour(10**6)
print(f"The answer to problem twenty-four is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_twentyfive(n):
    """
    Find the index of the first Fibonacci number with n digits
    """
    Fib = [1, 1]
    step = 1
    # Calculate the Fibonacci sequence by brute force until a number with n digits appears
    while len(str(Fib[step])) < n:
        Fib.append(Fib[step - 1] + Fib[step])
        step += 1
        
    return len(Fib) 
    
    
answer, time = problem_twentyfive(10**3)
print(f"The answer to problem twenty-five is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_twentysix(n):
    """
    Calculate the d < n  such that 1 / d has the largest repeating cycle of digits
    """
    def division(d):
        """
        Calculate the repeating cycle of 1 / d
        """
        remainders = [10]
        # Repeat division algorithm, appending the remainders with every iteration. Once a remainder recurs, the number of iterations since it last occured is returned
        while 1 > 0:
            next = (remainders[-1] % d) * 10
            if next in remainders:
                return len(remainders) - remainders.index(next)
            else:
                remainders.append(next)
                
    cycles = []
    # Compute the cycle lengths for all integers from 1 up to 1000
    for i in range(1, n):
        cycles.append(division(i))
    
    return cycles.index(max(cycles)) + 1
        
    
answer, time = problem_twentysix(1000)
print(f"The answer to problem twenty-six is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_twentyseven():
    """
    Compute the product a * b where n**2 + a*n + b = 0 produces the most number of consecutive primes for beginning with n = 0, for |a| < 1000 and |b| <= 1000
    """

    def quadratic_zeros(a: int, b: int):
        """
        Returns the number of consecutive integers, beginning with 0, for which the quadratic equation with coefficients a and b is prime
        """
        n = 0
        while is_prime(n**2 + a*n + b):
            n += 1
        return n
    
    zeros_list = []
    
    # b is the qudratic evaluated at 0, so b must be a prime number less than 1000.
    b_values = np.array(sieve_primes(1000))
    
    for b in b_values:
        # The quadratic evaluated at 1 is 1 + a + b, so for a to be prime, it must be of the form a = prime - b - 1
        a_values = b_values - b - 1
        for a in a_values:
            # Create a list of tuples with coefficients a, b and the number of consecutive primes.
            zeros_list.append((quadratic_zeros(a, b), a, b))
    
    # Find the best quadratic equation
    best_quadeatic = max(zeros_list)
    
    # Calculate the product of the coefficients
    return best_quadeatic[1] * best_quadeatic[2]

    
answer, time = problem_twentyseven()
print(f"The answer to problem twenty-seven is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_twentyeight(n):
    """
    Calculate the sum of of the diagonals of an n x n spiral grid
    """
    
    # For an n x n spiral grid, the top-right diagonal is given by (2k + 1) ** 2, where k runs from 0 to (n - 1)/2. For each layer, the other four corners are found from the top right corner by subtracting 2k, 4k and 8k.
    
    if n % 2 == 0 or n <= 2 or type(n) != int:
        raise ValueError("n must be an odd integer greater than or equal to 3." )
    
    diagonal_sum = 0
    
    for k in range(1, ((n-1) // 2) + 1):
        for i in range(4):
            diagonal_sum += (2*k + 1) ** 2 - 2 * k * i
            
    # Add in the centre '1'
    return diagonal_sum + 1

    
answer, time = problem_twentyeight(1001)
print(f"The answer to problem twenty-eight is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_twentynine(n):
    """
    Compute the number of distinct terms generated by terms of the form a ** b, where 2 <= a <= 100 and 2 <= b <= 100
    """
    distinct_values = set()
    
    for a in range(2, n + 1):
        for b in range(2, n + 1):
            distinct_values.add(a ** b)
            
    return len(distinct_values)
    

answer, time = problem_twentynine(100)
print(f"The answer to problem twenty-nine is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_thirty():
    """
    Sum all numbers which can be written as the sum of the fifth powers of their digits
    """
    
    # The largest the fifth powers of the digits of a 7-digit number can sum to is 413343, which means no 7 digit number (or higher) can be the sum of the fifth power of its digits
    # The largest the fifth powers of the digits of a 6-digit number can sum to is 354294, putting an upper bound on the numbers we need to check
    
    fifth_power = []

    # Begin at 10 since single digits don't have sums
    for number in range(10, 354294):
        sum_of_powers = 0
        for digit in str(number):
            sum_of_powers += int(digit) ** 5
        if number == sum_of_powers:
            fifth_power.append(number)
        
    return sum(fifth_power)
    
answer, time = problem_thirty()
print(f"The answer to problem thirty is: {answer}    (Run in {time:.5f} s)")