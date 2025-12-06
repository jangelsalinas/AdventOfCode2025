'''
The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers that need to be either added (+) or multiplied (*) together.
Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. Problems are separated by a full column of only spaces. The left/right alignment of numbers within each problem can be ignored.

Result is he grand total of adding together all of the answers to the individual problems.
'''

def calculate_total(worksheet_text: str) -> int:
    lines = worksheet_text.strip().splitlines()
    
    # Last line contains operations
    operations_line = lines[-1]
    # Other lines contain numbers
    number_lines = lines[:-1]
    
    # Split each line into tokens (preserving positions)
    # Find column positions by splitting and tracking indices
    split_lines = [line.split() for line in number_lines]
    operations = operations_line.split()
    
    # Transpose: convert rows to columns
    # Each column represents one problem
    num_problems = len(operations)
    
    total = 0
    for col_idx in range(num_problems):
        # Extract numbers from this column
        numbers = []
        for row in split_lines:
            if col_idx < len(row):
                numbers.append(int(row[col_idx]))
        
        # Get the operation for this column
        operation = operations[col_idx]
        
        # Calculate result
        if operation == '+':
            result = sum(numbers)
        elif operation == '*':
            result = 1
            for number in numbers:
                result *= number
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        total += result
    
    return total

if __name__ == "__main__":
    with open("Day_06/day06_input.txt", "r") as file:
        worksheet = file.read().strip()
    result = calculate_total(worksheet)
    print(f"Total of all problems: {result}")