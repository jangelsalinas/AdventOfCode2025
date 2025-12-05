'''
The batteries are each labeled with their joltage rating, a value from 1 to 9.
The batteries are arranged into banks; each line of digits in your input corresponds to a single bank of batteries.
Within each bank, you need to turn on exactly two batteries
the joltage that the bank produces is equal to the number formed by the digits on the batteries you've turned on
For example, if you have a bank like 12345 and you turn on batteries 2 and 4, the bank would produce 24 jolts
You'll need to find the largest possible joltage each bank can produce.

In the above example:

In 987654321111111, you can make the largest joltage possible, 98, by turning on the first two batteries.
In 811111111111119, you can make the largest joltage possible by turning on the batteries labeled 8 and 9, producing 89 jolts.
In 234234234234278, you can make 78 by turning on the last two batteries (marked 7 and 8).
In 818181911112111, the largest joltage you can produce is 92.

The maximun number is gotten by turning on the two batteries with the highest digits in each bank. In order, so if you have 818181911112111 you turn on the batteries labeled 9 and 2, producing 92 jolts.∫

The total output joltage is the sum of the maximum joltage from each bank,

UPDATE:Now, you need to make the largest joltage by turning on exactly twelve batteries within each bank.
'''

def calculate_max_joltage(banks: list[str]) -> int:
    total_joltage = 0
    for bank in banks:
        # Greedy approach: select the 12 largest digits maintaining order
        result = []
        remaining_needed = 12
        start_pos = 0
        
        while remaining_needed > 0:
            # Calculate how many positions we can search
            # We need to leave enough digits after this selection
            search_end = len(bank) - remaining_needed + 1
            
            # Find the maximum digit in the valid range
            max_digit = max(bank[start_pos:search_end])
            
            # Find the position of this max digit in the valid range
            for i in range(start_pos, search_end):
                if bank[i] == max_digit:
                    max_pos = i
                    break
            
            # Add this digit to result
            result.append(max_digit)
            
            # Update for next iteration
            start_pos = max_pos + 1
            remaining_needed -= 1
        
        # Convert result to integer
        max_joltage = int(''.join(result))
        total_joltage += max_joltage
    return total_joltage

if __name__ == "__main__":
    with open("Day_03/day03_input.txt", "r") as file:
        banks = file.read().strip().splitlines()
    result = calculate_max_joltage(banks)
    print(f"Total maximum joltage: {result}")