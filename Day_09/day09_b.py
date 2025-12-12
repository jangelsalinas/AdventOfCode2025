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

def fill_polygon_fast(red_tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """Fast polygon fill using scanline algorithm"""
    if len(red_tiles) < 3:
        return set()
    
    filled = set()
    min_y = min(t[1] for t in red_tiles)
    max_y = max(t[1] for t in red_tiles)
    
    n = len(red_tiles)
    
    # For each horizontal scanline
    for y in range(min_y, max_y + 1):
        intersections = []
        
        # Find all edge intersections with this scanline
        for i in range(n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[(i + 1) % n]
            
            # Check if edge crosses scanline
            if y1 == y2:  # Horizontal edge
                continue
            
            if min(y1, y2) <= y <= max(y1, y2):
                # Calculate x intersection
                if y1 != y2:
                    x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(x)
        
        # Sort intersections
        intersections.sort()
        
        # Fill between pairs of intersections
        for i in range(0, len(intersections) - 1, 2):
            x_start = int(intersections[i])
            x_end = int(intersections[i + 1])
            for x in range(x_start, x_end + 1):
                filled.add((x, y))
    
    return filled

def is_rect_valid(min_x, min_y, max_x, max_y, red_tiles, green_and_red_set):
    """Check if all 4 corners and edges of rectangle are valid"""
    # Must have red tiles at the two opposite corners we're checking
    # All 4 corners must be inside the valid area
    corners = [(min_x, min_y), (max_x, max_y), (min_x, max_y), (max_x, min_y)]
    for corner in corners:
        if corner not in green_and_red_set and not point_in_polygon(corner, red_tiles):
            return False
    
    # Check all edges must be valid
    # Top and bottom edges
    for x in range(min_x, max_x + 1):
        if (x, min_y) not in green_and_red_set and not point_in_polygon((x, min_y), red_tiles):
            return False
        if (x, max_y) not in green_and_red_set and not point_in_polygon((x, max_y), red_tiles):
            return False
    
    # Left and right edges
    for y in range(min_y, max_y + 1):
        if (min_x, y) not in green_and_red_set and not point_in_polygon((min_x, y), red_tiles):
            return False
        if (max_x, y) not in green_and_red_set and not point_in_polygon((max_x, y), red_tiles):
            return False
    
    # If all edges are valid, the interior must be valid too (convexity property)
    return True

def calculate_largest_rectangle(red_tiles: list[tuple[int, int]]) -> int:
    n = len(red_tiles)
    
    # Build set of tiles on the perimeter (red + green connections)
    perimeter_tiles = set(red_tiles)
    
    # Add green tiles between consecutive red tiles (perimeter only)
    for i in range(n):
        next_i = (i + 1) % n
        tiles_between = get_tiles_between(red_tiles[i], red_tiles[next_i])
        perimeter_tiles.update(tiles_between)
    
    # Don't fill the entire polygon - too expensive
    # Instead, check rectangles on-demand
    
    max_area = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # They must have different x and y coordinates to form a rectangle
            if x1 != x2 and y1 != y2:
                min_x, max_x = min(x1, x2), max(x1, x2)
                min_y, max_y = min(y1, y2), max(y1, y2)
                
                area = (max_x - min_x + 1) * (max_y - min_y + 1)
                
                # Skip if can't beat current max
                if area <= max_area:
                    continue
                
                # Check if rectangle is valid
                if is_rect_valid(min_x, min_y, max_x, max_y, red_tiles, perimeter_tiles):
                    max_area = area
    
    return max_area

if __name__ == "__main__":
    with open("Day_09/day09_input.txt", "r") as file:
        red_tiles = [tuple(map(int, line.strip().split(','))) for line in file.readlines()]
    result = calculate_largest_rectangle(red_tiles)
    print(f"Largest rectangle area: {result}")