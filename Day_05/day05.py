'''
The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs.
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.
How many of the available ingredient IDs are fresh
'''

def count_fresh_ingredients(fresh_ranges: list[str], available_ids: list[int]) -> int:
    # Parse ranges into list of tuples (start, end)
    ranges = []
    for range_str in fresh_ranges:
        start, end = map(int, range_str.split('-'))
        ranges.append((start, end))
    
    # Count how many available IDs fall within any range
    fresh_count = 0
    for ingredient_id in available_ids:
        # Check if this ID is in any range
        for start, end in ranges:
            if start <= ingredient_id <= end:
                fresh_count += 1
                break  # No need to check other ranges
    
    return fresh_count

if __name__ == "__main__":
    with open("Day_05/day05_input.txt", "r") as file:
        sections = file.read().strip().split('\n\n')
        fresh_ranges = sections[0].strip().splitlines()
        available_ids = list(map(int, sections[1].strip().splitlines()))
    
    result = count_fresh_ingredients(fresh_ranges, available_ids)
    print(f"Number of fresh ingredients available: {result}")