'''
The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs.

UPDATE: Now, the second section of the database (the available ingredient IDs) is irrelevant

The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.
How many ingredient IDs are considered to be fresh according to the fresh ingredient ID ranges?
'''

def count_fresh_ingredients(fresh_ranges: list[str]) -> int:
    # Parse ranges into list of tuples (start, end)
    ranges = []
    for range_str in fresh_ranges:
        start, end = map(int, range_str.split('-'))
        ranges.append((start, end))
    
    # Sort ranges by start position
    ranges.sort()
    
    # Merge overlapping ranges
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlapping or adjacent - merge with the last range
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # No overlap - add as new range
            merged.append((start, end))
    
    # Calculate total count from merged ranges
    total_count = sum(end - start + 1 for start, end in merged)
    
    return total_count

if __name__ == "__main__":
    with open("Day_05/day05_input.txt", "r") as file:
        sections = file.read().strip().split('\n\n')
        fresh_ranges = sections[0].strip().splitlines()
        # available_ids section is ignored as per the update
    
    result = count_fresh_ingredients(fresh_ranges)
    print(f"Number of fresh ingredient IDs: {result}")