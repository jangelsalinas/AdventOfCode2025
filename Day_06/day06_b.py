'''
The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers that need to be either added (+) or multiplied (*) together.
Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. Problems are separated by a full column of only spaces. The left/right alignment of numbers within each problem can be ignored.

UPDATE:Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant digit at the bottom. (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem is still the operator to use.)

Result is he grand total of adding together all of the answers to the individual problems.
'''

def calculate_total(worksheet_text: str) -> int:
    lines = worksheet_text.splitlines()
    
    # Ensure all lines have the same length by padding with spaces
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]
    
    # Last line contains operations
    operations_line = lines[-1]
    # Other lines contain digit characters
    number_lines = lines[:-1]
    
    # Process character by character (column by column)
    problems = []
    current_number = []
    
    for col_idx in range(max_len):
        # Get all characters in this column
        column_chars = [line[col_idx] for line in number_lines]
        operation_char = operations_line[col_idx]
        
        # Check if this column is all spaces (separator between problems)
        if all(c == ' ' for c in column_chars) and operation_char == ' ':
            # This is a separator - save current problem if any
            if current_number:
                problems.append(current_number)
                current_number = []
        else:
            # This column is part of a number
            # Read digits vertically to form a number
            digit_str = ''.join(c if c.isdigit() else '' for c in column_chars)
            if digit_str:  # Only add if there are actual digits
                num = int(digit_str)
                current_number.append((num, operation_char))
    
    # Don't forget the last problem
    if current_number:
        problems.append(current_number)
    
    # Calculate total
    total = 0
    for problem in problems:
        # All numbers in a problem share the same operation (from the last one)
        operation = problem[0][1]  # Get operation from first number
        numbers = [num for num, _ in problem]
        
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
        worksheet = file.read().rstrip('\n')  # Remove trailing newline but keep internal structure
    result = calculate_total(worksheet)
    print(f"Total of all problems: {result}")