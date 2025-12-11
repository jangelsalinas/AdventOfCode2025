'''
The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have a list of where the red tiles are located in the grid
your goal is to find the largest rectangle possible and return its area.
You can choose any two red tiles as the opposite corners of your rectangle
'''

def calculate_largest_rectangle(red_tiles: list[tuple[int, int]]) -> int:
    max_area = 0
    n = len(red_tiles)
    
    # Check all pairs of red tiles as opposite corners
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # They must have different x and y coordinates to form a rectangle
            if x1 != x2 and y1 != y2:
                # Calculate area including the tiles at the corners
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                max_area = max(max_area, area)
    
    return max_area

if __name__ == "__main__":
    with open("Day_09/day09_input.txt", "r") as file:
        red_tiles = [tuple(map(int, line.strip().split(','))) for line in file.readlines()]
    result = calculate_largest_rectangle(red_tiles)
    print(f"Largest rectangle area: {result}")