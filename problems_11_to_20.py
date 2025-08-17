import numpy as np
from problems_1_to_10 import prime_factors_list

### USEFUL FUNCTIONS ###

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


### EULER PROBLEMS BEGIN HERE ###


def problem_eleven():
    """
    Return the largest product of four adjacent numbers in any direction from the 20x20 matrix
    """
    # Import the matrix from the .txt file
    matrix = np.array(np.loadtxt("problem_eleven_number.txt", dtype = int))
    
    # Create a matrix reflected along the x-axis, useful for calculating anti-diagonal sequences
    matrix_reflected = []
    for row in matrix:
        matrix_reflected.append(list(row[::-1]))
    matrix_reflected = np.array(matrix_reflected)
    
    largest_product = 0
    
    # Scan over columns of the matrix and its transpose (which effects a sum over the rows)
    for grid in [matrix, matrix.T]:
        for row in range(20):
            for column in range(20 - 3):
                product = grid[row, column] * grid[row, column + 1] * grid[row, column + 2] * grid[row, column + 3]
                if product > largest_product:
                    largest_product = product
        
    # Scan through the diagonals
    for grid in [matrix, matrix_reflected]:    
        for diagonal in range(-16, 16 + 1):
            for element in range(16 - np.abs(diagonal) + 1):
                # Deduce the row and column from the diagonal
                if diagonal < 0:
                    row = element + np.abs(diagonal)
                    column = element
                else:
                    row = element
                    column = element + np.abs(diagonal)
                    
                product = grid[row, column] * grid[row + 1, column + 1] * grid[row + 2, column + 2] * grid[row + 3, column + 3]
                if product > largest_product:
                    largest_product = product

    return largest_product

# print("The answer to problem eleven is: ", problem_eleven())



def problem_twelve(n):
    """
    Calculate the first triangle number to have at least n divisors
    """
    
    counter = 1
    
    while 1 > 0:
        # Using Euler's formula for the nth triangle number: is n * (n+1) / 2
        counter_plus_one = counter + 1
        
        prime_factors_c = prime_factors_dict(counter)
        prime_factors_cp1 = prime_factors_dict(counter_plus_one)
        
        # The division by two in Euler's formula requires removing a factor of two from one of the prime list dictionaries
        if counter % 2 == 0:
            prime_factors_c[2] -= 1
        else:
            prime_factors_cp1[2] -= 1
        
        # The number of distinct factors is the product of each multiplicity value plus one
        product = 1
        for multiplicity in prime_factors_c.values():
            product *= multiplicity + 1
        for multiplicity in prime_factors_cp1.values():
            product *= multiplicity + 1
        
        if product >= n:
            return int(counter * (counter + 1) / 2) 
        
        # If we haven't reached n factors, continue with counter increased by 1
        counter += 1
        

# print("The answer to problem twelve is: ", problem_twelve(500))


def problem_thirteen():
    """
    Return the first 10-digits of a sum of 100 different 50-digit numbers 
    Python can easily do this sum itself trivially
    More interesting to create my own addition algorithm
    """
    large_numbers = np.loadtxt("problem_thirteen_numbers.txt", dtype = str)
    
    # Store each 50-digit number as a list of digits
    large_numbers = [list(number) for number in large_numbers]
    
    # Variable to store the carry to the next digit
    carry = 0
    # Initialize list to contain the current summation
    summation = ['0'] * 50
    
    for number in [number for number in large_numbers[:i]]:
        
        # Prepend zeros to each number so that the two numbers have the same number of digits
        number = ['0'] * (len(summation) - len(number)) + number
        
        if len(summation) != len(number):
            raise IndexError("Summation and current number do not have the same length")
        
        for backward_index, digit in enumerate(reversed(number)):
            # Compute correct index from enumerated idex
            index = len(number) -  1 - backward_index
            
            # Sum each digit, leave the last remainder and carry the rest to the next digit
            digit_sum = int(digit) + int(summation[index]) + carry
            remainder = digit_sum % 10
            carry = digit_sum // 10
            
            summation[index] = str(remainder)
            
            # If there are carries left over, prepend them to the total sum
            if index == 0 and carry != 0:
                summation = [str(carry)] + summation
                carry = 0
                
    # Return only the first 10 digits
    first_10 = int("".join(summation[0:10]))
    
    return first_10
    
# print("The answer to problem thirteen is: ", problem_thirteen())




def problem_fourteen():
    """
    Find the longest collatz sequence beginning with a number less than one million
    """
    
    def collatz_sequence(n):
        """
        Creates a collatz sequence beginning with n, returns length of that sequence
        """
        sequence = [n]
        
        number = n
        while number != 1:
            if number % 2 == 0:
                number //= 2
                sequence.append(number)
            else:
                sequence.append(3 * number + 1)
                number = (3 * number + 1) // 2
                sequence.append(number)
                
        return len(sequence)
    
    # Collatze dictionary of thelength of the collatz sequence beginning with each number.
    collatz = {
        1: 1,
        2: 2,
        4: 3,
        8: 4,
        16: 5,
        5: 6,
        10: 7,
        20: 8,
        40: 9,
        13: 10,
    }
    
    # Search through numbers up to one million
    for i in range(3, 10 ** 6):
        if i not in collatz:
            # If i is not already in the collatz dictionary, we need to create a new collatz sequence
            sequence = [i]
            num = i
            
            # Generate new terms in the collatz sequence until we hit a number already in the collatz dictionary
            while num not in collatz:
                if num % 2 == 0:
                    num = num // 2
                else:
                    num = 3*num + 1
                    
                if num not in collatz:
                    sequence.append(num)
                else:
                    # Once the squence hits a number already in the dictionary, add each element of the sequence hitherto generated into the dictionary
                    counter = collatz[num]
                    for number in reversed(sequence):
                        counter += 1
                        collatz[number] = counter
        
    largest = max(collatz, key = collatz.get)
    
    return largest
        
        
# print("The answer to problem fourteen is: ", problem_fourteen())


def problem_fifteen():
    1
    
print("The answer to problem fifteen is: ", problem_fifteen())