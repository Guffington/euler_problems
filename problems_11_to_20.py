print("Loading packages...", end = "")
import numpy as np
import math
from utils import timer, prime_factors_dict 
print("\rAll packages loaded")


@timer
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

answer, time = problem_eleven()
print(f"The answer to problem eleven is: {answer}    (Run in {time:.5f} s)")


@timer
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
        

answer, time = problem_twelve(500)
print(f"The answer to problem twelve is: {answer}    (Run in {time:.5f} s)")


@timer
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
    
    for number in large_numbers:
        
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
    
    
answer, time = problem_thirteen()
print(f"The answer to problem thirteen is: {answer}    (Run in {time:.5f} s)")



@timer
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
        
        
answer, time = problem_fourteen()
print(f"The answer to problem fourteen is: {answer}    (Run in {time:.5f} s)")

@timer
def problem_fifteen(n):
    """
    How many routes from the top left to the top right in a n x n grid.
    """
    
    # To get to the bottom right one needs to go 'right' n times and 'down' n times. The total number of combinations of these are (2n!) /( n! * n!)
    
    return math.comb(2*n, n)
    

answer, time = problem_fifteen(20)
print(f"The answer to problem fifteen is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_sixteen(n):
    """
    Return the sum of the digits of 2 ** n in decimal
    """
    
    return sum([int(num) for num in str(2 ** n)])    


answer, time = problem_sixteen(1000)
print(f"The answer to problem sixteen is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_seventeen():
    """
    Return the number of letters used to write out all numbers from one to one thousand
    """
    
    # Write down the building blocks of each number
    ones = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    
    tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    
    # From 20 to 999 the numbers can be assembled algorithmically
    up_to_ninety_nine = []
    for ten in tens:
        up_to_ninety_nine.append(ten)
        for one in ones:
            up_to_ninety_nine.append(ten + one)
    
    up_to_ninety_nine = ones + teens + up_to_ninety_nine
    
    hundreds = []
    for one in ones:
        hundreds.append(one + "hundred")
        for number in up_to_ninety_nine:
            hundreds.append(one + "hundredand" + number)
    
    # Full list of all numbers written in words (no spaces or hyphens)
    full_list = up_to_ninety_nine + hundreds + ['onethousand']
    
    # Count the letters in each word
    letter_counter = 0
    for number in full_list:
        letter_counter += len(number)
    
    return letter_counter
    
answer, time = problem_seventeen()
print(f"The answer to problem seventeen is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_eighteen():
    """
    Find the route through the triangle with the largest sum
    """
    triangle_matrix = []
    
    def make_list(item):
        """
        Return 'item' converted to an integer and placed into a list
        """
        return [int(item)]
    
    # Import the triangle from file
    with open("problem_eighteen_triangle.txt") as t:
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
 
 
answer, time = problem_eighteen()
print(f"The answer to problem eighteen is: {answer}    (Run in {time:.5f} s)")



@timer
def problem_nineteen():
    """
    Return how many Sundays fell on the first of the month between 1 Jan 1901 and Dec 31 2000
    """
    def is_leap(year: int):
        """
        Return True if 'year' is a leap year. Return 
        """
        if type(year) != int:
            raise ValueError("Year must be an integer")
        
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False
    
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # 1 Jan 1901 begins on a Tuesday (2)
    day = 2
    sunday_counter = 0
    for year in range(1901, 2000 + 1):
        for days in days_per_month:
            if is_leap(year) and days == 28: # Implement leap-year if necessary
                days = 29
            day = (days + day) % 7
            if day == 0:
                sunday_counter += 1
                
    # Note, this calculation actually includes 1 January 2001, but since this fell on a Monday this does not impact the result
    
    return sunday_counter
    
    
answer, time = problem_nineteen()
print(f"The answer to problem nineteen is: {answer}    (Run in {time:.5f} s)")



@timer
def problem_twenty(n):
    """
    Return is the digit sum of n!
    """
    return sum(map(int,list(str(math.factorial(n)))))
    
    
answer, time = problem_twenty(100)
print(f"The answer to problem twenty is: {answer}    (Run in {time:.5f} s)")