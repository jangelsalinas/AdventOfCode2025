'''
UPDATE: You'll need to keep connecting junction boxes together until they're all in one large circuit.

Continue connecting the closest unconnected pairs of junction boxes together until they're all in the same circuit. 
What do you get if you multiply together the X coordinates of the last two junction boxes you need to connect?

For example, the first connection which causes all of the junction boxes to form a single circuit is between 
the junction boxes at 216,146,977 and 117,168,530. Multiplying the X coordinates (216 and 117) produces 25272.
'''

import math

def calculate_distance(box1: tuple[int, int, int], box2: tuple[int, int, int]) -> float:
    return math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2)

def find_unifying_connection(junction_boxes: list[tuple[int, int, int]]) -> int:
    n = len(junction_boxes)
    parent = list(range(n))
    
    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        """Returns True if the union actually connected two different components"""
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootY] = rootX
            return True
        return False
    
    def count_circuits() -> int:
        """Count the number of separate circuits"""
        return len(set(find(i) for i in range(n)))

    # Calculate all distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_distance(junction_boxes[i], junction_boxes[j])
            distances.append((dist, i, j))

    distances.sort()

    # Connect boxes until all are in one circuit
    for dist, box1, box2 in distances:
        if union(box1, box2):
            # Check if all boxes are now connected
            if count_circuits() == 1:
                # This was the final connection!
                x1 = junction_boxes[box1][0]
                x2 = junction_boxes[box2][0]
                return x1 * x2
    
    return 0  # Should never reach here if input is valid

if __name__ == "__main__":
    with open("Day_08/day08_input.txt", "r") as file:
        junction_boxes = [tuple(map(int, line.strip().split(','))) for line in file.readlines()]
    result = find_unifying_connection(junction_boxes)
    print(f"Product of X coordinates of final connection: {result}")