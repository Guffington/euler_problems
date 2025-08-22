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