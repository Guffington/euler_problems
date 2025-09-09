import numpy as np
import math
import time

def timer(func):
   """
   Timer decorator function to calculate the runtime of a function
   """ 
   def wrapper(*args, **kwargs):
       start = time.perf_counter()
       result = func(*args, **kwargs)
       end = time.perf_counter()
       return result, end - start
   
   return wrapper

def sieve_primes(bound):
    """
    Use the Sieve of Erathosthenes to find all primes up to but not including 'bound'
    """
    if bound < 2:
        raise ValueError("Integer must be greater than or equal to 2")
    
    # Create the sieve
    sieve = [True] * (bound + 1)
    sieve[0] = False
    sieve[1] = False
    
    # For each number up until sqrt(bound) remove all multiples of each number, leaving only prime numbers
    for num in range(2, int(bound ** 0.5) + 1):
        if sieve[num] == True:
            for multiple in range(num * num, bound + 1, num):
                sieve[multiple] = False
        
    # Sieve out the composite numbers
    return [p for p, is_prime in enumerate(sieve) if is_prime]


def prime_factors_list(n):
    """
    Return all prime factors of n
    """
    factors = []
    # Create a list of all primes up to (sqrt) n
    prime_list = sieve_primes(int(n ** 0.5) + 1)
    
    index = 0
    test = prime_list[index]
    
    # Test whether each prime is a a factor. If it is, append it to the factors list
    while test ** 2 <= n:
        if n % test == 0:
            factors.append(test)
            n //= test
        else:
            index += 1
            try:
                test = prime_list[index]
            except:
                test = n
    factors.append(n)
    
    return factors


def is_prime(n):
    """
    Return True if n is prime, False i fit is not prime
    """
    
    if n < 2:
        return False
    
    if len(prime_factors_list(n)) == 1:
        return True
    else:
        return False



def primes_up_to_n(n):
    """
    Return the first n primes
    """
    
    # The nth prime is approximately n * log(n)
    guess = int(n * math.log(n)) + 1
    
    # Return the first 'guess'-many primes
    prime_list = sieve_primes(guess)
    
    # Continually add more prime numbers until the list is at least n elements long
    while len(prime_list) < n:
        guess += n
        prime_list = sieve_primes(guess)
        
    # Return only the first n primes
    return prime_list[:n]

def find_all_factors(n):
    """
    Find all factors of n by brute force
    """
    factors = [1, n]
    
    for i in range(2, int(n/2)):
        if n % i == 0:
            factors.append(i)
            factors.append(n // i)
            
    return sorted(list(set(factors)))

def prime_factors_dict(n):
    """
    Convert prime factors list into a dictionary showing the multiplicity of each distinct factor
    """
    factors_dict = {}
    prime_factors = prime_factors_list(n)
    
    for factor in prime_factors:
        if factor in factors_dict:
            factors_dict[factor] += 1
        else:
            factors_dict[factor] = 1
    
    return factors_dict

def aliquot_sum(n):
    """
    Calculate the aliquot sum of n (the sum of all proper divisors)
    """
    prime_factors = prime_factors_dict(n)

    # Use geometric series formula to calculate the sum of the divisors involving each prime factor and its multiplicity
    sum_of_divisors = 1
    for factor, multiplicity in prime_factors.items():
        quotient = (factor ** (multiplicity + 1) - 1) // (factor - 1)
        sum_of_divisors *= quotient
    # Remove one copy of n to get the sum of the *proper* divisors
    sum_of_divisors -= n
    
    return sum_of_divisors

def digits(n):
        """
        Return the set of unique digits which feature in n
        """
        digit_set = set()
        for digit in str(n):
            digit_set.add(int(digit))
        return digit_set
    
def permutations(string):
    """
    Calculate all permutations of the letters in string, and return them all in a list
    """
    
    def tp(string: str, a: int, b: int):
        """
        Simple transposition: swap letters a and b in 'string'. Indexed from 1.
        """
        if a == b:
            return string
        
        i = min(a, b) - 1
        j = max(a, b) - 1
        
        return string[:i] + string[j] + string[i+1:j] + string[i] + string[j+1:]


    def tp_2(string: str, list: list, prepend = ""):
        """
        Transpose last two letters of string, append both permutations to list with a prepend if chosen
        """
        list.append(prepend + string)
        list.append(prepend + tp(string, len(string) - 1, len(string)))
        return list
        
    def tp_n(string: str, list: list, prepend = ""):
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
    
    return tp_n(string, [])

def miller_rabin(n: int, bases: list = [2, 3, 5, 7, 11, 13]):
    """
    Perform the Miller-Rabin test for probable primality for all bases in 'bases'
    """

    if n < 2 or type(n) != int or n % 2 == 0:
        raise ValueError("First argument must be an odd integer greater than or equal to two")
    elif n in bases:
        return True
    elif n % 2 == 0:
        return False
    
    def factorise(n):
        """
        Write n - 1 in the form (2 ** r) * d, where d is an odd integer
        """
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
            
        return d, r

    def test(n, base):
        """
        Miller-Rabin test with a single base
        """
        d, r = factorise(n)
        first_test = pow(base, d, n)
        if first_test == 1 or first_test == n - 1:
            return True
        
        for exp in range(1, r):
            test = pow(base, (2 ** exp) * d, n)
            if test == n - 1:
                return True
        return False
        
    
    for base in bases:
        if test(n, base) == False:
            return False
    
    return True

def totient(n):
    """
    Use a sieve method to generate a list of phi(m) for m from 2 up to and including n.
    Tot[0] = 0 and tot[1] = 1 by convention, so that phi(m) = tot[m].
    """
    # First generate a list of all integers
    tot = [i for i in range(n + 1)]
    for p in range(2, n + 1):
        # If tot[index] == index the number must be prime, since composite numbers will be reduced
        if tot[p] == p:
            # For each multiple of each prime, multiply that entry in tot by (1 - 1 / prime)
            for m in range(p, n + 1, p):
                tot[m] -= (tot[m] // p)
    
    return tot

def euclid(a, b):
    """
    Returns the greatest common divisor of a and b using Euclid's algorithm
    """
    m = max(a,b)
    n = min(a,b)
    
    while 1 > 0:
        q = m // n
        r = m - q * n
        if r == 0:
            return n
        m = n
        n = r


def continuing_fraction(n):
    """
    Return the continuing fracion representation of sqrt(num)
    """
    if type(n) != int or n < 1:
        raise ValueError("Argument must be a positive integer")
    
    # Check if the number is a square, and return immediately if so
    base = int(math.sqrt(n))
    if base ** 2 == n:
        return [base, (0,)]
    
    cont_frac = [base, ()]
    # Repetitions will keep track of the decompositons we've seen, to spot when the continued fraction decomposition begins to repeat
    repetitions = set()
    
    # Initialise the numerator and denominator
    num, denom = base, 1
    while 1 > 0:
        # Calculate the new denominator using 'rationalising the denominator'
        denom = (n - num ** 2) // denom
        # Extract the integer part from the radical fraction
        m = (base + num) // denom
        # Reduce the numerator accordingly, and normlise to make it positive
        num = -(num -  m * denom)
        # Check if we've seen this combination of numerator, denominator and integer part before
        if (m, num, denom) not in repetitions:
            # If not, add it to the list and append m to the continued fraction decomposition
            repetitions.add((m, num, denom))
            cont_frac[1] += (m,)
        else:
            # If we've seen this combination already, the continued fraction is repeating so we stop
            return cont_frac
        