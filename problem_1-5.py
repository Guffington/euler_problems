def prime_factors_list(n):
    test = 2
    factors = []
    
    while test ** 2 <= n:
        if n % test == 0:
            factors.append(test)
            n //= test
        else:
            test += 1           
    factors.append(n)
    
    return factors
    

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

# Euler problem 1: Sum of all multiples of 3 and 5 for all natural numbers below 1000 
# print("The answer to problem one is: ", problem_one(1000))

def problem_two(n):
    """
    Returns the sum of all even Fibonacci numbers below n.
    """
    a = 1
    b = 2
    counter = 2
    while a + b <= n:
        if (a + b) % 2 == 0:
            counter += a + b
        a, b = b, a + b
    return counter

# print("The answer to problem two is: ", problem_two(4 * 10**6))

def problem_three(n):
    """
    Returns the largest prime factor of n.
    """
    factors = prime_factors_list(n)
    
    return max(factors)

# print("The answer to problem three is: ", problem_three(600851475143))

def problem_four(n):
    """
    Return
    """
    n_nines = int("9" * n)
    
    for i in reversed(range(10 ** (2*n - 2), (n_nines ** 2) + 1)):
        if str(i)[::-1] == str(i):
            # print(i)
            for factor in reversed(range(10 ** (n-1), n_nines + 1)):
                if i % factor == 0 and len(str(i // factor)) == n:
                    return i
        
# print("The answer to problem four is: ", problem_four(3))


def problem_five(n):
    """
    Return
    """
    
    factors_dict = {}
    
    for i in range(2, n + 1):
        factors = prime_factors_list(i)
        for factor in set(factors):
            if factor in factors_dict:
                if factors.count(factor) > factors_dict[factor]:
                    factors_dict[factor] = factors.count(factor)
            else:
                factors_dict[factor] = factors.count(factor)
    
    total = 1
    for base, power in factors_dict.items():
        total *= base ** power
    
    return total
        
    
print("The answer to problem five is: ", problem_five(19))