def count_paths(manifold_text: str) -> int:
    lines = manifold_text.strip().splitlines()
    width = len(lines[0])
    height = len(lines)
    
    # Find starting position
    start_x = lines[0].index('S')
    
    # Track all possible states: (x, y) -> count of paths reaching that state
    current_states = {start_x: 1}  # {x_position: number_of_paths}
    
    # Process each row
    for y in range(height):
        next_states = {}
        
        for x, path_count in current_states.items():
            if x < 0 or x >= width:
                continue
            
            char = lines[y][x]
            
            if char == '^':
                # Beam splits into two paths
                if x > 0:
                    next_states[x - 1] = next_states.get(x - 1, 0) + path_count
                if x < width - 1:
                    next_states[x + 1] = next_states.get(x + 1, 0) + path_count
            else:  # char == '.' or 'S'
                # Beam continues straight down
                next_states[x] = next_states.get(x, 0) + path_count
        
        current_states = next_states
    
    # Sum all paths that reach the bottom
    return sum(current_states.values())

if __name__ == "__main__":
    with open("Day_07/day07_input.txt", "r") as file:
        manifold = file.read().strip()
    result = count_paths(manifold)
    print(f"Number of paths: {result}")
