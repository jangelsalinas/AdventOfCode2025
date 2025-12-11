'''
UPDATE: The Elves just remembered: they can only switch out tiles that are red or green.

Every red tile is connected to the red tile before and after it by a straight line of green tiles. 
The list wraps, so the first red tile is also connected to the last red tile.
All tiles inside the loop of red and green tiles are also green.

The rectangle you choose must have red tiles in opposite corners, but any other tiles it includes 
must be red or green.
'''

def get_tiles_between(p1: tuple[int, int], p2: tuple[int, int]) -> set[tuple[int, int]]:
    """Get all tiles on a straight line between two points (horizontal or vertical)"""
    x1, y1 = p1
    x2, y2 = p2
    tiles = set()
    
    if x1 == x2:  # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x1, y))
    elif y1 == y2:  # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y1))
    
    return tiles

def point_in_polygon(point: tuple[int, int], polygon: list[tuple[int, int]]) -> bool:
    """Ray casting algorithm to check if point is inside polygon"""
    x, y = point
    n = len(polygon)
    inside = False
    
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    
    return inside

def calculate_largest_rectangle(red_tiles: list[tuple[int, int]]) -> int:
    n = len(red_tiles)
    
    # Build the set of green and red tiles
    # Red tiles form a closed loop, green tiles connect consecutive red tiles
    green_and_red_tiles = set(red_tiles)
    
    # Add green tiles between consecutive red tiles (including wrap-around)
    for i in range(n):
        next_i = (i + 1) % n
        tiles_between = get_tiles_between(red_tiles[i], red_tiles[next_i])
        green_and_red_tiles.update(tiles_between)
    
    # Add tiles inside the polygon formed by red tiles
    if n >= 3:
        # Find bounding box
        min_x = min(t[0] for t in red_tiles)
        max_x = max(t[0] for t in red_tiles)
        min_y = min(t[1] for t in red_tiles)
        max_y = max(t[1] for t in red_tiles)
        
        # Check all points inside bounding box
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if point_in_polygon((x, y), red_tiles):
                    green_and_red_tiles.add((x, y))
    
    # Now find the largest rectangle using only red/green tiles
    max_area = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # They must have different x and y coordinates to form a rectangle
            if x1 != x2 and y1 != y2:
                # Check if all tiles in this rectangle are red or green
                min_x, max_x = min(x1, x2), max(x1, x2)
                min_y, max_y = min(y1, y2), max(y1, y2)
                
                all_valid = True
                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        if (x, y) not in green_and_red_tiles:
                            all_valid = False
                            break
                    if not all_valid:
                        break
                
                if all_valid:
                    area = (max_x - min_x + 1) * (max_y - min_y + 1)
                    max_area = max(max_area, area)
    
    return max_area

if __name__ == "__main__":
    with open("Day_09/day09_input.txt", "r") as file:
        red_tiles = [tuple(map(int, line.strip().split(','))) for line in file.readlines()]
    result = calculate_largest_rectangle(red_tiles)
    print(f"Largest rectangle area: {result}")