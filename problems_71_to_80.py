print("\rLoading packages...", end = "")
from utils import timer, euclid, totient
from fractions import Fraction
import math
print("\rAll packages loaded")

@timer
def problem_seventyone():
    """
    Return the numerator of the fraction immediately before 3/7, if listing all fractions of the form a / b where a < b <= 10 ** 6, in ascending order
    """
    # We want to find the a/b that minimises 3/7 - a/b, with the restrictions that a < b < 10 ** 6 and 3/7 - a/b > 0. This is equivalent to minimising (3b - 7a) / 7b. This is minimised by finding a solution to 3b - 7a = 1 that maximises b < 10 ** 6. An obvious solution is b = -2 and 7 = -1: other solutions can be found by translating: b = -2 + 7*n; a = -1 + 3*n for integer values of n.
    
    n = (10 ** 6 + 2) // 7
            
    return  -1 + 3*n

    
# answer, time = problem_seventyone()
# print(f"The answer to problem seventy-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventytwo(n):
    """
    Return the number of unique fractions less than one, with a denominator less than n
    """
    # Use a sieve method to find euler's totient function up to n
    tot = totient(n)
    
    # The number of unqiue fractions of each denominator will be the number of positive integers co-prime to that denominator
    return sum(tot[2:])
    
    
# answer, time = problem_seventytwo(12 * (10 ** 3))
# print(f"The answer to problem seventy-two is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventythree(bound):
    """
    Return the number of fractions between 1/3 and 1/2 with denominator no larger (in smallest terms) than bound
    """
    # We use a Farey sequences method with denominator, summing them together is effectively taking a mediant of the denominators.
    stack = [(3, 2)]
    # Counter counts how many mediants we perform
    counter = 0
    
    # Use a stack, "First-In-Last-Out" approach
    while stack:
        x, y = stack.pop()
        if x + y <= bound:
            # If a median is computed, increase the counter by 1
            stack.append((x, x + y))
            stack.append((x + y, y))
            counter += 1
    
    return counter
    
# answer, time = problem_seventythree(12000)
# print(f"The answer to problem seventy-three is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventyfour(n):
    """
    Return the number of chains of length sixty, beginning with a number below n and repeatedly performing a digit factorisation sum
    """
    # Compute factorials of digits up front so it doesn't have to be done every cycle
    factorials = [math.factorial(i) for i in range(9 + 1)]
    # Count the number of chains of length sixty
    sixty_chains = 0
    # Put all the data from the problem into a dictionary to avoid unncessary computation; the key is each number and its value is its chain length
    seen = {1: 1,
            2: 1,
            69: 5,
            78: 4,
            145: 1,
            169: 3,
            540: 2,
            871: 2,
            872: 2,
            1454: 3,
            45360: 3,
            363600: 4,
            363601: 3
            }
    
    for i in range(3, n):
        current = i
        if i not in seen:
            # Build the chain using a tuple
            current = i
            chain = (current,)
            
            while 1 > 0:
                # Calculate the sum of factorials of digits
                summand = current
                fact_sum = 0
                while summand > 0:
                    fact_sum += factorials[summand % 10]
                    summand //= 10
                    
                # The three non-trivial loops are already in the dictionary, so either the chain will hit one of them, or encounter a trivial loop
                if fact_sum == current:
                    length = len(chain)
                    # If we encounter a trivial loop, add all chain elements to the dictionary with an increasing number (in reverse order)
                    for index, element in enumerate(chain):
                        seen[element] = length - index
                    break
                
                elif fact_sum in seen:
                    length = len(chain)
                    # If we hit a number already seen, add all chain elements to the dictionary with an increasing number in reverse order, adding the chain length of the number we hit in the dictionary
                    for index, element in enumerate(chain):
                        seen[element] = (length - index) + seen[fact_sum]
                    # Only the first element of the chain can have a length of sixty
                    if seen[i] == 60:
                        sixty_chains += 1
                    break
                else:
                    # If we have not hit anything, continue
                    chain += (fact_sum,)
                    current = fact_sum
    
    return sixty_chains
    
# answer, time = problem_seventyfour(10 ** 6)
# print(f"The answer to problem seventy-four is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventysix(n):
    """
    Return the number of decompositions of n into a sum of at least two terms
    """
    # Compute the number of decompositions of n into a sum of at least two terms only using 1 or 2 for all integers from 1 to n
    current_list = [ (i // 2) + 1 for i in range(0, n + 1)]
    
    # Compute the number of decompositions when using numbers 1, ... , m
    for m in range(3, n):
        next_list = []
        for total in range(0, n + 1):
            # The number of ways of decomposing 'total' into  sums using 1, ... , m is summing the decompositions of 'total - r' using 1, ... , m - 1, over r, where runs over each multiple of m
            total = sum( current_list[total - j] for j in range(0, total + 1, m) )
            next_list.append(total)
        # Replace the old list with the newly constructed list
        current_list = next_list
            
    
    return current_list[-1]

    
# answer, time = problem_seventysix(100)
# print(f"The answer to problem seventy-six is: {answer}    (Run in {time:.5f} s)")