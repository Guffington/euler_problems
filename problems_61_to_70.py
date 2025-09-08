print("\rLoading packages...", end = "")
from utils import timer, prime_factors_dict, sieve_primes
from fractions import Fraction
import math
print("\rAll packages loaded")


@timer
def problem_sixtyone():
    """
    Return then sum of the only sequence of six 4-digit numbers, one from each of the triangular, pentagonal, hexagonal, heptagonal and octagonal sets, which are cyclic in their first two and last two digits
    """
    # Generate a list of triangular, pentagonal, hexagonal and heptagonal sets, each number has the digit 3, 4, 5, 6, or 7 attached for set identification
    lists = [[((n * (n + 1)) // 2, 3) for n in range(1, 150) if 10 ** 3 <= (n * (n + 1)) // 2 < 10 ** 4], 
            [(n ** 2, 4) for n in range(1, 100) if 10 ** 3 <= n ** 2 < 10 ** 4],
            [((n * (3*n - 1)) // 2, 5) for n in range(1, 100) if 10 ** 3 <= (n * (3*n - 1)) // 2 < 10 ** 4],
            [((n * (2*n - 1)), 6) for n in range(1, 100) if 10 ** 3 <= (n * (2*n - 1)) < 10 ** 4],
            [((n * (5*n - 3)) // 2, 7) for n in range(1, 100) if 10 ** 3 <= (n * (5*n - 3)) // 2 < 10 ** 4]]
    
    # Create a dictionary of octagonal numbers, the value sets will contain all compatible elements from other sets; we build up beginning with the octagonal numbers because there are fewer of them
    p8 = {((n * (3*n - 2),), (8,)): set() for n in range(1, 100) if 10 ** 3 <= (n * (3*n - 2)) < 10 ** 4}

    # Find all numbers in all other number sets which are cyclic compatible for each number in the octagonal numbers.
    for number_list in lists:
        for num in number_list:
            for key in p8.keys():
                # Compare the last two digits of the octagonal number and the first two of the other number
                if key[0][0] % 100 == num[0] // 100:
                    # If compatible, add it to the set of compatible numbers for that octagonal number
                    p8[key].add(num)
                    
    old_dict = p8
    # We're looking for a set of six numbers, so we begin chaining numbers together to build possible sequences
    for _ in range(5):
        new_dict = {}
        for key, value_set in old_dict.items():
            # The chain is the sequence of numbers, whereas the tracker will keep track that each number comes from a seperate set
            chain, tracker = key
            # If a chain has no more compatible numbers, no longer consider it
            if len(value_set) > 0:
                # For each compatible number, we add it to the chain and then re-compute the set of compatible numbers for this new chain
                for num, identifier in value_set:
                    # Make sure the identifier (which set the number comes from) hasn't already been used in the chain
                    if identifier not in tracker:
                        new_chain = chain + (num,)
                        new_tracker = tracker + (identifier,)
                        new_dict[(new_chain, new_tracker)] = set()
                        # Check all numbers for compatible numbers
                        for number_list in lists:
                            for element in number_list:
                                if element[1] not in new_tracker and num % 100 == element[0] // 100:
                                    new_dict[(new_chain, new_tracker)].add(element)
        old_dict = new_dict
    
    # After the previous loop we have a dictionary of chains of six number from different sets which are cyclic, all except the first and last number; if we enforce that last condition we find the unique element and can take its sum
    for chain, _ in new_dict.keys():
        first = chain[0]
        last = chain[-1]
        if last % 100 == first // 100:
            return sum(chain)
    

# answer, time = problem_sixtyone()
# print(f"The answer to problem sixty-one is: {answer}    (Run in {time:.5f} s)")  


@timer
def problem_sixtytwo(n):
    """
    Find the smallest cube such that n permutations of its digits are also cubes
    """
    # Dictionary to store each tuple of digits, along with the cubes for which it appears
    cube_digits = {0: []}
    i = 3
    # Check to see whether the maximal length of digits has surpased n
    while len(max(cube_digits.values(), key = len)) < n:
        # The digits of i ** 3 are stored in a tuple, ordered from smallest to largest for comparison
        digits = tuple(sorted(str(i ** 3)))
        # Append the digits and its associated cube root to the dictionary
        if digits in cube_digits:
            cube_digits[digits].append(i)
        else:
            cube_digits[digits] = [i]
        # Move to the next number
        i += 1

    # For the digits which have n associated cubes, return the cube of the smallest value
    return max(cube_digits.values(), key = len)[0] ** 3

# answer, time = problem_sixtytwo(5)
# print(f"The answer to problem sixty-two is: {answer}    (Run in {time:.5f} s)") 



@timer
def problem_sixtythree():
    """
    Return the number of positive integers n which can be written as n = a ** b, where b is the number of digits in n
    """
    number_counter = 0
    # 10 ** n has n + 1 digits, therefore 9 ** n is the largest power which can have n digits; it can be checked that this holds up to n = 21 and fails for n = 22, which places the upper bound on numbers we need to check
    for exp in range(1, 21 + 1):
        # Check all bases counting backwards from 9
        for base in range(9, 1 - 1, -1):
            number = base ** exp
            # If we encounter less digits than exp, move to the next exponent, since all smaller values will have just as few digits
            if number < 10 ** (exp - 1):
                break
            else:
                number_counter += 1
                
    return number_counter
    

# answer, time = problem_sixtythree()
# print(f"The answer to problem sixty-three is: {answer}    (Run in {time:.5f} s)") 


@timer
def problem_sixtyfour(m):
    """
    Return the number integers less than or equal to m for which the continued fraction of sqrt(m) has an odd period
    """
    # Calculate all squares up to m, to filter out
    squares = set([n ** 2 for n in range(2, int(math.sqrt(m)) + 1)])
    
    # Variable to track the number of odd periods
    odd_periods = 0
    for sq in range(2, m + 1):
        if sq not in squares:
            # base is the integer part of sqrt(m)
            base = int(math.sqrt(sq))

            # Store the continued fraction expansion
            cont_frac = [base, ()]
            # Store the decomposition into numerator, denominator and integer part, to detect when the continued fraction begins repeating
            repetitions = set()
            # Initialise values of numerator, denominator and integer part for the first run
            num, denom, integer = -base, 1, 0
            
            while 1 > 0:
                # From the previous step, the numerator is achieved by subtracting the integer part multiplied by the denominator, renormalised to be made positive
                num -= integer * denom
                num *= -1
                # The denominator is  from 'rationalising the denominator'
                denom = (sq - (num ** 2)) // denom
                # The integer part is the largest integer that can be subtracted leaving the fraction part positive
                integer = int((num + base) / denom)
                # Check if we've already seen this decomposition; if so, the continued fraction is repeating
                if (integer, num, denom) in repetitions:
                    if len(cont_frac[1]) % 2 == 1:
                        # Once we have a continued fraction calculated, check for an even or odd period, and update the counter and move to the next value of sq
                        odd_periods += 1
                    break
                else:
                    # If the continued fraction is not yet repeating, add the current decomposition to the set and add the integer part to the continued fraction representation.
                    repetitions.add((integer, num, denom))
                    cont_frac[1] += (integer,)
        
    return odd_periods
    
# answer, time = problem_sixtyfour(10 ** 4)
# print(f"The answer to problem sixty-four is: {answer}    (Run in {time:.5f} s)") 
    
    
@timer
def problem_sixtyfive(n):
    """
    Return the sum of the digits of the numerator of the nth convergent in the simple continued expansion of e
    """
    # Create the continued fraction list for e
    e = [2,1,2]
    k = 2
    for digit in range(n):
        # Append 2 * k to the continued fraction for every third time, otherwise append
        if digit % 3 == 2:
            e.append(2 * k)
            k += 1
        else:
            e.append(1)
            
    # Use the recurrence relation to determine the numerators: p_n  = a_n * p_{n-1} + p_{n-2}
    p = [0, 1]
    for digit in range(n):
        p.append(e[digit] * p[-1] + p[-2])
    
    # Perform the digit sum of the 100th convergent
    return sum(int(d) for d in str(p[n + 1]))
        
        
# answer, time = problem_sixtyfive(100)
# print(f"The answer to problem sixty-five is: {answer}    (Run in {time:.5f} s)") 


def problem_sixtysix():
    """
    COMMENT
    """
    def check_x(x, d):
        """
        COMMENT
        """
        x_sq = x ** 2
        y_sq = int(math.sqrt(x_sq // d))
        lower_bound = max(0, y_sq - 2)
        for y in range(lower_bound, y_sq + 2 + 1):
            if x_sq - d * (y ** 2) == 1:
                return y
            elif y == y_sq + 2:
                return False
            
    squares = set([x ** 2 for x in range(35) if x ** 2 <= 1000])
    largest = 0
    for d in range(61, 61 + 1):
        if d not in squares:
            x = int(math.sqrt(d))
            while 1 > 0:
                result = check_x(x, d)
                if result != False:
                    if x > largest:
                        largest = x
                    break
                else:
                    x += 1
                    print(x)
    return largest
            
    
# print(problem_sixtysix())
# print(f"The answer to problem sixty-six is: {answer}    (Run in {time:.5f} s)") 


@timer
def problem_sixtyseven():
    """
    Find the route through the triangle with the largest sum
    NOTE: This is the same code as for problem 18.
    """
    triangle_matrix = []
    
    def make_list(item):
        """
        Return 'item' converted to an integer and placed into a list
        """
        return [int(item)]
    
    # Import the triangle from file
    with open("problem_sixtyseven_triangle.txt") as t:
        for line in t:
            triangle_matrix.append(list(map(make_list, line.split()))) # Each number in the triangle is made into a list, so the paths can be built up by appending the largest child
    
    # Begin from the bottom, and finish with the second row from the top
    for level, row in enumerate(reversed(triangle_matrix[1:])):
        for i in range(len(row) - 1):
            # Compute the largest sum of the paths of the two decedenents for each element in each row
            largest = max(row[i], row[i + 1], key = sum)
            # Append the largest path to its ancestor
            triangle_matrix[-(level + 2)][i].extend(largest)
                
    # The top entry will now contain the largest possible path all the way to the bottom. Return the top entry
    return sum(triangle_matrix[0][0])


# answer, time = problem_sixtyseven()
# print(f"The answer to problem sixty-seven is: {answer}    (Run in {time:.5f} s)") 

@timer
def problem_seventy():
    """
    Return the number n between 1 and 10 ** 7 which minimises n / phi(n), where phi is the euler totient function, subject to the constraint that phi(n) must consist of precisely the same digits as n
    """
    # Use a sieve method to generate phi(n) up to 10 ** 7
    # First generate a list of all integers
    tot = [i for i in range(10 ** 7)]
    for p in range(2, 10 ** 7):
        # If tot[index] == index the number must be prime, since composite numbers will be reduced
        if tot[p] == p:
            # For each multiple of each prime, multiply that entry in tot by (1 - 1 / prime)
            for n in range(p, 10 ** 7, p):
                tot[n] -= (tot[n] // p)
    
    # Now filter out those n for which phi(n) and n do not use the same digits
    successful_numbers = []
    current_min = 2
    for k in range(2, 10 ** 7):
        tot_k = tot[k]
        if k / tot_k < current_min:
            if sorted(str(k)) == sorted(str(tot_k)):
                # For applicable numbers, append not only i but i / number to the sucess list
                successful_numbers.append((k / tot[k], k))
                current_min = k / tot_k
    
    # The minimise function automatically minimises over the first entry in a tuple, which will minimise n / phi(n); after this select n (2nd entry) from the tupe
    return min(successful_numbers)[1]
    
    
# answer, time = problem_seventy()
# print(f"The answer to problem seventy is: {answer}    (Run in {time:.5f} s)")