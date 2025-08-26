print("\rLoading packages...", end = "")
from utils import timer, sieve_primes
import math
from fractions import Fraction
print("\rAll packages loaded")


@timer
def problem_fiftyone(n):
    """
    Return the smallest prime which can make n other primes by replacing digits
    """
    # First considering all 2 digit numbers
    num_of_digits = 2
    # Set of all primes already checked, to avoid double checking
    checked = set()

    while 1 > 0:
        # Generate all primes with at most 'num_of_digits' digits
        primes = sieve_primes(10 ** num_of_digits)
        # Filter primes for primes only with 'num_of_digits' digits
        relevant_primes = [prime for prime in primes if prime >= 10 ** (num_of_digits - 1)]
        # Create a prime set for easy lookup
        primes_set = set(relevant_primes)
        
        for prime in relevant_primes:
            if prime not in checked:
                # Replace each unique digit
                for digit in set(str(prime)):
                    numbers = [str(prime).replace(digit, str(i)) for i in range(10)]
                    # Check how many digit replacements result in prime numbers
                    prime_numbers = [int(number) for number in numbers if int(number) in primes_set]
                    # Add them all to the checked set so as to not revisit them
                    checked.update(prime_numbers)
                    
                    if len(prime_numbers) >= n:
                        return prime_numbers[0]
        # If no prime set of length n is found, increase the number of digits considered 
        num_of_digits += 1

    
# answer, time = problem_fiftyone(8)
# print(f"The answer to problem fifty-one is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftytwo(n):
    """
    Return the smallest number x for which x, 2x, 3x, ..., n * x all contain the same digits
    """
    # Begin searching through two digit numbers
    num_of_digits = 2
    while 1 > 0:
        # For the number of digits to be the same, only need to search up to (10 ** num_of_digits) // n to avoid increasing number of digits
        for number in range(10 ** (num_of_digits - 1), ((10 ** num_of_digits) // n) + 1):
            # Compute list of digits for comparison
            digit_list = sorted(str(number))
            for multiple in range(2, n + 1):
                # For each multiple of n check whether it has the same digits as the original
                if sorted(str(number * multiple)) != digit_list:
                    # If not, move to the next number
                    break
                # If we've checked through all n multiples and all have the same digits, return the number
                if multiple == n:
                    return number
        # If we haven't found such a number with the current number of digitis, increase the number of digits
        num_of_digits += 1

# answer, time = problem_fiftytwo(6)
# print(f"The answer to problem fifty-two is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftythree():
    """
    Return the number of times n choose k is greater than 10 ** 6 for 1 <= n <= 100.
    """
    million_counter = 0
    for n in range(23, 100 + 1):
        # No need to consider n choose 0, 1, n or n-1 as these are guaranteed to be less than 10 ** 6
        for k in range(2, n - 1):
            if math.comb(n, k) > 10 ** 6:
                million_counter += 1
                
    return million_counter
    
    
# answer, time = problem_fiftythree()
# print(f"The answer to problem fifty-three is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftyfour():
    """
    Return the number of player one wins in problem_fiftyfour_poker.txt
    """
    # Import the file
    with open("problem_fiftyfour_poker.txt", 'r') as t:
        hands = t.read().split("\n")
        
    # Separate the hands into player one and player two
    person_one = []
    person_two = []
    for pair in hands:
        cards = pair.split()
        first = cards[:5]
        second = cards[5:]
        
        person_one.append(first)
        person_two.append(second)

    # Converting cards and hands to numerical values for the purposes of comparison
    card_value = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    hand_value = {"High Card": 1, "One Pair": 2, "Two Pair": 3, "Three of a Kind": 4, "Straight": 5, "Flush": 6, "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9, "Royal Flush": 10}
    
    def hand(hand):
        """
        Return the name of 'hand' and the numerical values of the hand decomposition
        """
        # List of suits in the hand
        suits = [card[-1] for card in hand]
        # List of numbers in the hand
        numbers = sorted([card_value[card[0]] for card in hand])
        # Create a dictionary to count multiplicity of each card
        numbers_dict = {}
        for number in numbers:
            numbers_dict[number] = numbers.count(number)
        
        # List of distinct card number values, sorted in decending order by multiplicity, then by card value itself. This will be used to compare the 'next highest card' if two hands are equal
        card_list = sorted(numbers_dict, key=lambda k: (numbers_dict[k], k), reverse=True)
        
        # First check for flushes and straights; if a hand contains any kind of flush or straight, it cannot have any kind of pair
        if len(set(suits)) == 1:
            flush = True
        else:
            flush = False
        # Straights have 5 consecutive numbers
        if len(set(numbers)) == 5 and max(numbers) - min(numbers) == 4:
            straight = True
        else: 
            straight = False
        if flush == True:
            if straight == True:
                # A royal flush is a straight flush beginning at 10
                if min(numbers_dict.keys()) == 10:
                    return "Royal Flush", card_list
                else:
                    return "Straight Flush", card_list
            else:
                return "Flush", card_list
        elif straight == True:
            return "Straight", card_list
        
        # If no flushes or straights were found, look for pairs
        if max(numbers_dict.values()) == 4:
            return "Four of a Kind", max(numbers_dict, key = numbers_dict.get)
        elif max(numbers_dict.values()) == 3:
            if min(numbers_dict.values()) == 2:
                return "Full House", card_list
            else:
                return "Three of a Kind", card_list
        elif max(numbers_dict.values()) == 2:
            # Two determine whether there is two pairs or only one pair, count the number of 2s in the numbers_dict
            pair_count = [value for value in numbers_dict.values()].count(2)
            if pair_count == 2:
                return "Two Pair", card_list
            else:
                return "One Pair", card_list
        else:
            return "High Card", card_list
        
    def compare_hands(first_hand, second_hand):
        """
        Compare two hands and return the winner
        """
        hand_one = hand(first_hand)
        hand_two = hand(second_hand)
        
        if hand_value[hand_one[0]] > hand_value[hand_two[0]]:
            return 1
        elif hand_value[hand_one[0]] < hand_value[hand_two[0]]:
            return 2
        else:
            # If the two hands have the same hand description, compare the quality of each hand numerically, by moving along card_list
            list_one = hand_one[1]
            list_two = hand_two[1]
            for i in range(len(list_one)):
                if list_one[i] > list_two[i]:
                    return 1
                elif list_one[i] < list_two[i]:
                    return 2
        # If both hands are identically valued, it's a draw
        return 0
    
    # Count the number of player one wins
    person_one_score = 0
    # Compare every hand between player one and player two
    for hand_number in range(len(person_one)):
       result = compare_hands(person_one[hand_number], person_two[hand_number])
       if result == 1:
           person_one_score += 1
       elif result == 0:
           # There should be no draws, any draw is an indication of a bug i coding
           raise ValueError(f"Draw found on hand number {hand_number + 1}")                
    
    return person_one_score

# answer, time = problem_fiftyfour()
# print(f"The answer to problem fifty-four is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftyfive(n):
    """
    Return the number of Lychrel numbers below n
    """
    lychrel = []
    # Search through all number up to n
    for number in range(n):
        new_number = number
        # Perform 50 iterations per number to find a palindrome
        for iteration in range(50):
            new_number += int(str(new_number)[::-1])
            if new_number == int(str(new_number)[::-1]):
                # Move to next number if a palindrome is found
                break
            # If no palindrome is found after 50 iterations, we have found a Lychrel number
            if iteration == 50 - 1:
                lychrel.append(number)
                
    return len(lychrel)
    

# answer, time = problem_fiftyfive(10 ** 4)
# print(f"The answer to problem fifty-five is: {answer}    (Run in {time:.5f} s)")


@timer
def problem_fiftysix(n):
    """
    Find the maximal digit sub of any number of the form a ** b where a, b < n
    """
    maximum = 0
    for a in range(n):
        for b in range(n):
            number = pow(a, b)
            # Sum the digits of a ** b
            digit_sum = sum([int(i) for i in str(number)])
            if digit_sum > maximum:
                maximum = digit_sum
    
    return maximum
    
# answer, time = problem_fiftysix(100)
# print(f"The answer to problem fifty-six is: {answer}    (Run in {time:.5f} s)")



def problem_fiftyseven():
    """
    
    """
    print(Fraction(1 + 1/2))
    
    
print(problem_fiftyseven())
# print(f"The answer to problem fifty-seven is: {answer}    (Run in {time:.5f} s)")