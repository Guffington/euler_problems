import math
from utils import prime_factors_list, primes_up_to_n, sieve_primes
    
def problem_one(n):
    """
    Returns the sum of all multiples of 3 or 5 below n.
    """
    
    counter = 0
    for i in range(n):
        # If the number is a multiple of 3, add it to the counter
        if i % 3 == 0:
            counter += i
        # If the number is not a multiple of 3 but is a multiple of 5, add it to the counter
        elif i % 5 == 0:
            counter += i
    return counter

print("The answer to problem one is: ", problem_one(1000))



def problem_two(n):
    """
    Returns the sum of all even Fibonacci numbers below n.
    """
    a = 1
    b = 2
    counter = b
    while a + b <= n:
        if (a + b) % 2 == 0:
            counter += a + b
        a, b = b, a + b #Update the Fibonacci sequence
    return counter

print("The answer to problem two is: ", problem_two(4 * 10**6))



def problem_three(n):
    """
    Returns the largest prime factor of n.
    """
    factors = prime_factors_list(n)
    
    return max(factors)

print("The answer to problem three is: ", problem_three(600851475143))



def problem_four(n):
    """
    Return the largest palendromic number that is the product of two n-digit numbers 
    """
    # Create an n-digit number of nines.
    n_nines = int("9" * n)
    
    # Search backwards through the product of all products of n-digit numbers, beginning with n_nines * n_nines
    for i in reversed(range(10 ** (2*n - 2), (n_nines ** 2) + 1)):
        if str(i)[::-1] == str(i): #Check if i is palendromic
            
            #Check backwards to see if i has an n-digit factor; return i if it does
            for factor in reversed(range(10 ** (n-1), n_nines + 1)):
                if i % factor == 0 and len(str(i // factor)) == n:
                    return i
        
print("The answer to problem four is: ", problem_four(3))


def problem_five(n):
    """
    Return the integer which is the smallest multiple of the integers from 1 to n
    """
    
    # Dictionary to store the factors of each number, paired with the largest index in any decomposition
    factors_dict = {}
    
    # For each integer from 2 to n generate its prime factors.
    for i in range(2, n + 1):
        factors = prime_factors_list(i)
        for factor in set(factors):
            # If the prime factor has already been seen, only update the multiplicity if the prime factor has a larger multuplicity for i than for any previous number
            if factor in factors_dict:
                if factors.count(factor) > factors_dict[factor]:
                    factors_dict[factor] = factors.count(factor)
            else:
                # If the prime factor hasn't been seen, add it to the dictionary with the factor multiplicity
                factors_dict[factor] = factors.count(factor)
    
    # Multiply together all the prime factors
    total = 1
    for base, power in factors_dict.items():
        total *= base ** power
    
    return total
        
    
print("The answer to problem five is: ", problem_five(19))



def problem_six(n):
    """
    Calculate the difference between the square of the sum of the first n integers, and the sum of the squares of the first n integers
    """
    
    # The difference is the sum of twice the cross terms
    counter = 0
    for i in range(1, n + 1):
        for j in range(1, i):
            counter += 2 * i * j
            
    return counter
    
    
print("The answer to problem six is: ", problem_six(100))



def problem_seven(n):
    """
    Return the nth prime number
    """
        
    return primes_up_to_n(n)[n-1]
    
print("The answer to problem seven is: ", problem_seven(10001))


def problem_eight(n):
    """
    Find the largest product of n successive digits in the 1000-digit number given
    """
    
    # Load the big number, into 10 lists
    big_number_dict = { 1: list(str(73167176531330624919225119674426574742355349194934)),
    2: list(str(96983520312774506326239578318016984801869478851843)),
    3: list(str(85861560789112949495459501737958331952853208805511)),
    4: list(str(12540698747158523863050715693290963295227443043557)),
    5: list(str(66896648950445244523161731856403098711121722383113)),
    6: list(str(62229893423380308135336276614282806444486645238749)),
    7: list(str(30358907296290491560440772390713810515859307960866)),
    8: list(str(70172427121883998797908792274921901699720888093776)),
    9: list(str(65727333001053367881220235421809751254540594752243)),
    10: list(str(52584907711670556013604839586446706324415722155397)),
    11: list(str(53697817977846174064955149290862569321978468622482)),
    12: list(str(83972241375657056057490261407972968652414535100474)),
    13: list(str(82166370484403199890008895243450658541227588666881)),
    14: list(str(16427171479924442928230863465674813919123162824586)),
    15: list(str(17866458359124566529476545682848912883142607690042)),
    16: list(str(242190226710556263211111093705442175069416589604080)),
    17: list(str(7198403850962455444362981230987879927244284909188)),
    18: list(str(845801561660979191338754992005240636899125607176060)),
    19: list(str(5886116467109405077541002256983155200055935729725)),
    20: list(str(71636269561882670428252483600823257530420752963450)) }
    
    # Add the lists together, storing the number in one big list
    big_number = []
    for _, number in big_number_dict.items():
        big_number.extend(number)
    
    # Search though the number to find the largest product of n successive digits
    largest_product = 0
    for num in range(1000 - (n - 1)):
        total = 1
        for i in range(n): #Calculate the product of n sucessive numbers after digit 'num'
            total *= int(big_number[num + i]) 
        if total > largest_product:
            largest_product = total #Update 'largest_product' if a new largest product is found
            
    return largest_product
    
print("The answer to problem eight is: ", problem_eight(13))



def problem_nine():
    """
    Return the product a * b * c, where a < b < c is the unqiue Pythagorean triple which sum to 1000.
    """
    
    # Generate a half-grid of numbers; first index is used to sort the list
    list_of_pairs = [ (m + n, m, n) for m in range(1, 20 + 1) for n in range(1, m) ]
    
    
    def generate_pyth(a, b):
        """
        Return a pythagorean triple from two integers with a < b
        """
        if b <= a:
            raise ValueError("Second argument must be strictly greater than the first")
        else:
            # Use Euclid's method
            return b ** 2 - a ** 2, 2 * a * b, a ** 2 + b ** 2
        
    
    for _, m, n in sorted(list_of_pairs):
        a, b, c = generate_pyth(n, m)
        if a + b + c == 1000:
            return a * b * c
        
    return "Not found."
    
print("The answer to problem nine is: ", problem_nine())



def problem_ten(n):
    """
    Return the sum of all primes up to n
    """
    
    return sum(sieve_primes(n))


print("The answer to problem ten is: ", problem_ten(2 * 10 ** 6))