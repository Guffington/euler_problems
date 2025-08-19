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
    
    # Load the big number from file
    with open("problem_eight_number.txt", 'r') as num:
        number = num.read().split()
        
    # Add the lists together, storing the number in one big list
    big_number = []
    for line in number:
        for letter in line:
            big_number.append(letter)
    
    # Search though the number to find the largest product of n successive digits
    largest_product = 0
    for num in range(1000 - (n-1)):
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