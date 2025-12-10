'''
You quickly locate a diagram of the tachyon manifold (your puzzle input). A tachyon beam enters the manifold at the location marked S; tachyon beams always move downward. Tachyon beams pass freely through empty space (.). However, if a tachyon beam encounters a splitter (^), the beam is stopped; instead, a new tachyon beam continues from the immediate left and from the immediate right of the splitter.
Find How many times will the beam be split
If 2 splitters split the beam into the same spot it counts as one split only.
'''

def count_splits(manifold_text: str) -> int:
    lines = manifold_text.strip().splitlines()
    width = len(lines[0])
    height = len(lines)
    
    # Starting position of the beam (find 'S')
    start_x = lines[0].index('S')
    
    # Track active beams and splits
    active_beams = {start_x}  # Set of x positions where beams are at current y level
    split_count = 0
    
    # Process each row
    for y in range(height):
        next_beams = set()
        
        for x in active_beams:
            if x < 0 or x >= width:
                continue
                
            char = lines[y][x]
            
            if char == '^':
                # Beam splits
                split_count += 1
                # Create two new beams going left and right
                if x > 0:
                    next_beams.add(x - 1)
                if x < width - 1:
                    next_beams.add(x + 1)
            else:  # char == '.' or 'S'
                # Beam continues straight down
                next_beams.add(x)
        
        active_beams = next_beams
    
    return split_count

if __name__ == "__main__":
    with open("Day_07/day07_input.txt", "r") as file:
        manifold = file.read().strip()
    result = count_splits(manifold)
    print(f"Number of splits: {result}")