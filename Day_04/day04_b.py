'''
The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.
The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions.

UPDATE: Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper is removed, the forklifts might be able to access more rolls of paper, which they might also be able to remove.

Discover how many rolls of paper are accessible on the grid.
'''


def count_accessible_rolls(grid: list[str]) -> int:
    grid = [list(row) for row in grid]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    accessible_count = 0
    
    while True:
        found = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    # Check adjacent positions
                    adjacent_rolls = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                                adjacent_rolls += 1
                    if adjacent_rolls < 4:
                        grid[r][c] = '.'
                        accessible_count += 1
                        found = True
        if not found:
            break
    
    return accessible_count


if __name__ == "__main__":
    with open("Day_04/day04_input.txt", "r") as file:
        grid = file.read().strip().splitlines()
    result = count_accessible_rolls(grid)
    print(f"Number of accessible rolls of paper: {result}")