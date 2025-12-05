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
'''

def calculate_max_joltage(banks: list[str]) -> int:
    total_joltage = 0
    for bank in banks:
        # Find the two largest digits preserving their order
        max_joltage = 0
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)):
                # Form a number from digits at positions i and j
                joltage = int(bank[i]) * 10 + int(bank[j])
                max_joltage = max(max_joltage, joltage)
        # Add to the total joltage
        total_joltage += max_joltage
    return total_joltage

if __name__ == "__main__":
    with open("Day_03/day03_input.txt", "r") as file:
        banks = file.read().strip().splitlines()
    result = calculate_max_joltage(banks)
    print(f"Total maximum joltage: {result}")