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
print(problem_one(1000))