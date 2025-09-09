print("\rLoading packages...", end = "")
from utils import timer
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
    
    
# answer, time = problem_seventytwo(10 ** 6)
# print(f"The answer to problem seventy-two is: {answer}    (Run in {time:.5f} s)")