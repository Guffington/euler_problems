def problem_one(n):
    counter = 0
    for i in range(n):
        if i % 3 == 0:
            counter += i
        elif i % 5 == 0:
            counter += i
    return counter
        
print(problem_one(1000))