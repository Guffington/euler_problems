print("\rLoading packages...", end = "")
from utils import timer, euclid, totient, sieve_primes
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

    
answer, time = problem_seventyone()
print(f"The answer to problem seventy-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventytwo(n):
    """
    Return the number of unique fractions less than one, with a denominator less than n
    """
    # Use a sieve method to find euler's totient function up to n
    tot = totient(n)
    
    # The number of unqiue fractions of each denominator will be the number of positive integers co-prime to that denominator
    return sum(tot[2:])
    
    
answer, time = problem_seventytwo(10 ** 6)
print(f"The answer to problem seventy-two is: {answer}    (Run in {time:.5f} s)")


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
    
answer, time = problem_seventythree(12000)
print(f"The answer to problem seventy-three is: {answer}    (Run in {time:.5f} s)")


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
    
answer, time = problem_seventyfour(10 ** 6)
print(f"The answer to problem seventy-four is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventyfive(max):
    """
    Return the number of lengths less than or equal to 'max' which have exactly 1 decomposition into pythagorean triples
    """
    # List to contain the tally for each possible length
    perimeters = [0] * (max + 1)

    # Calculate a bound on the value on 'm', the first number to generate primitive triples
    bound = int(math.sqrt(max))
    for m in range(2, bound):
        # Calculate a bound on 'n'
        n_bound = int(math.sqrt(max - m ** 2))
        # Enforce the bound and the restriction m > n
        for n in range(1, min(m, n_bound)):
            # Primititve triplets are generated from m > n where m and n are coprime and not both odd
            if m % 2 == 0 or n % 2 == 0:
                if euclid(m, n) == 1:
                    a, b, c = m ** 2 - n ** 2, 2 * m * n, m ** 2 + n ** 2
                    l = a + b + c
                    # Non-primitive triplets (and perimeters) can be found by scaling
                    if l <= max:
                        k = l
                        while k <= max:
                            perimeters[k] += 1
                            k += l
            
    # Count the number of entries in the list which are 1
    return sum(1 for count in perimeters if count == 1)
        
answer, time = problem_seventyfive(1500000)
print(f"The answer to problem seventy-five is: {answer}    (Run in {time:.5f} s)")



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

    
answer, time = problem_seventysix(100)
print(f"The answer to problem seventy-six is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventyseven(number_of_ways):
    """
    Return the least positive integer that can be written as the sum of primes in at least 'number_of_ways' different ways
    """
    
    # Use a sieve to generate a list of many primes
    primes = sieve_primes(10 ** 3)
    # Create a dictionary of the previous prime to each prime, for fast lookup
    previous_prime = {primes[i]: primes[i - 1] for i in range(1, len(primes))}
    # Turn the list of primes into a set for fast lookup
    primes = set(primes)
    # Dictionary to contain the number of ways of partitioning each integer into primes. Each key-value pair is of the form prime_key: value_set, where value_set[i] is the number of partitions of i using all primes up to and including prime_key
    partitions = {2: [1, 0, 1, 0, 1],
                  3: [1, 0, 1, 1, 1],}
    
    # Begin with 5
    n = 5
    while True:
        # Since each list is built from the previous, we append the nth entry onto each list
        for number, plist in partitions.items():
            # Using only the prime 2, n can be built from 2's if and only if n is even
            if number == 2:
                if n % 2 == 0:
                    plist.append(1)
                else:
                    plist.append(0)
            else:
                # Build the nth entry using a sum of entries from the previous entry
                p = previous_prime[number]
                s = sum(partitions[p][n - k] for k in range(0, n + 1, number))
                # If we encounter a partition greater than 'number_of_ways', end here
                if s > number_of_ways:
                    return n
                plist.append(s)
        if n in primes:
            # If n is prime, create a whole new dictionary entry and build that up
            partitions[n] = [1, 0, 1, 1, 1]
            for m in range(5, n + 1):
                p = previous_prime[n]
                s = sum(partitions[p][m - k] for k in range(0, m + 1, n))
                if s > number_of_ways:
                    return m
                partitions[n].append(s)
        n += 1
        
        
answer, time = problem_seventyseven(5000)
print(f"The answer to problem seventy-seven is: {answer}    (Run in {time:.5f} s)")



@timer
def problem_seventyeight():
    """
    Return the first number n such that the number of partitions of n is divisible by 1 million.
    """
    # Compute a large number of pentagonal numbers
    pentagonal = [(k*(3 * k - 1)) // 2 for k in range(0, (10 ** 3) + 1)]
    # Compute a large number of pentagonal numbers with a negative index
    pentagonal_m = [(k*(3 * k + 1)) // 2 for k in range(0, (10 ** 3) + 1)]
    
    # Compute a large number of powers of -1, for easy access
    signs = [(-1) ** (k + 1) for k in range(0, 10 ** 6)]

    # Initialise partitions with partitions[0] = 1
    partitions = [1]
    
    # Compute the number of partitions for each 'n' using the pentagonal number recurrance relation
    for n in range(1, 10 ** 6 + 1):
        total = 0
        ind = 1
        # Sum over all pentagonal numbers which are less than or equal to 'n'
        while pentagonal[ind] <= n:
            total += signs[ind] * partitions[n - pentagonal[ind]]
            if pentagonal_m[ind] <= n:
                total += signs[ind] * partitions[n - pentagonal_m[ind]]
            ind += 1
        # Reduce modulo 10 ** 6 at each stage to keep numbers below 10 ** 6
        if total % (10 ** 6) == 0:
            return n
        partitions.append(total % (10 ** 6))
        
    return "None Found"
    
answer, time = problem_seventyeight()
print(f"The answer to problem seventy-eight is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventynine():
    """
    Return the shortest secret passcode satisfying all the attempts in problem_seventynine_keylog.txt
    """
    
    with open("problem_seventynine_keylog.txt", 'r') as k:
        # Password attempts are sorted and duplicates are eliminated
        attempts = sorted(set(k.read().split("\n")))

    # Initialise the list containing the full password with the first clue
    password = list(attempts[0])
    
    # Before implementing the latest clue, the code goes back over all other clues to make sure they're still satisfied
    for end in range(1, len(attempts) + 1):
        for attempt in attempts[: end]:
            # For each 'digit' in the clue check if the next digit exists in the password to the right of 'digit'
            for i, digit in enumerate(attempt[:-1]):
                next_digit = attempt[i + 1]
                if digit in password:
                    ind = password.index(digit)
                    if next_digit in password[ind:]:
                        # If 'next_digit' already is to the right of 'digit', no need to do anything
                        continue
                    elif next_digit in password[: ind]:
                        # If 'next_digit' is actually before digit in the password, move it to the right of 'digit'
                        password.remove(next_digit)
                        ind = password.index(digit)
                        password.insert(ind + 1, next_digit)
                    else:
                        # If next_digit doesn't exist at all in the the password, then insert it right after 'digit'
                        password.insert(ind + 1, next_digit)
                # If 'digit' doesn't even exist in password, but 'next_digit' does, then insert 'digit' before 'next_digit'
                elif next_digit in password:
                    ind = password.index(next_digit)
                    password.insert(ind, digit)
                
    # Join the list together into a single string
    return "".join(password)


answer, time = problem_seventynine()
print(f"The answer to problem seventy-nine is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_eighty(m):
    """
    Return the total of the first 100 digits of the first m natural numbers
    """
    # Create a set of squares to ignore
    squares = set([n ** 2 for n in range(2, int(math.sqrt(m)) + 1)])
    # Count the sum of the first 100 digits
    total = 0
    
    for n in range(2, m + 1):
        if n not in squares:
            # First digit is the integer part of the square root
            digits = [int(math.sqrt(n))]
            while len(digits) < 100:
                # Search through digits one to 9 to find the next digit which best approximates the root
                for i in range(1, 9 + 1):
                    l = len(digits)
                    # Add i to the last digit, scaling by powers of 10 enough to make the number an integer
                    s = sum(digits[i] * (10 ** (l - i)) for i in range(0, l)) + i
                    # Check if we have exceeded the square root of 2 (suitably scaled). If, so the previous number was correct digit approximation
                    if s ** 2 > n * (10 ** (2 * l)):
                        digits.append(i - 1)
                        break
                    # If we get to 9 and haven't exceeded the root, then 9 is the appropriate digit
                    if i == 9:
                        digits.append(9)
            # Sum the first 100 digits and add it to the total
            total += sum(digits)
    
    return total
    
answer, time = problem_eighty(100)
print(f"The answer to problem eighty is: {answer}    (Run in {time:.5f} s)")