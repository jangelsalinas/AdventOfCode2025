'''
The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).
you can find the invalid IDs by looking for any ID which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.
None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)
Your job is to find all of the invalid IDs that appear in the given ranges.

Response = Adding up all the invalid IDs
'''

def is_invalid_id(num):
    s = str(num)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:] and not s.startswith('0')
def sum_invalid_ids(ranges):
    total = 0
    for r in ranges:
        start, end = map(int, r.split('-'))
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num
    return total

if __name__ == "__main__":
    with open("Day_02/day02_input.txt", "r") as file:
        line = file.readline().strip()
        ranges = line.split(',')
        result = sum_invalid_ids(ranges)
        print("Sum of invalid IDs:", result)
