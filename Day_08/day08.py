'''
The plan is to connect the junction boxes with long strings of lights. Most of the junction boxes don't provide electricity; however, when two junction boxes are connected by a string of lights, electricity can pass between those two junction boxes.
Your input is  a list of all of the junction boxes' positions in 3D space
Each position is given as X,Y,Z coordinates.
You have to focus on connecting pairs of junction boxes that are as close together as possible according to straight-line distance.
To save on string lights, the Elves would like to focus on connecting pairs of junction boxes that are as close together as possible according to straight-line distance. In this example, the two junction boxes which are closest together are 162,817,812 and 425,690,689.

By connecting these two junction boxes together, because electricity can flow between them, they become part of the same circuit. After connecting them, there is a single circuit which contains two junction boxes, and the remaining 18 junction boxes remain in their own individual circuits.

Now, the two junction boxes which are closest together but aren't already directly connected are 162,817,812 and 431,825,988. After connecting them, since 162,817,812 is already connected to another junction box, there is now a single circuit which contains three junction boxes and an additional 17 circuits which contain one junction box each.

The next two junction boxes to connect are 906,360,560 and 805,96,715. After connecting them, there is a circuit containing 3 junction boxes, a circuit containing 2 junction boxes, and 15 circuits which contain one junction box each.

The next two junction boxes are 431,825,988 and 425,690,689. Because these two junction boxes were already in the same circuit, nothing happens!

This process continues for a while, and the Elves are concerned that they don't have enough extension cables for all these circuits. They would like to know how big the circuits will be.

After making the ten shortest connections, there are 11 circuits: one circuit which contains 5 junction boxes, one circuit which contains 4 junction boxes, two circuits which contain 2 junction boxes each, and seven circuits which each contain a single junction box. Multiplying together the sizes of the three largest circuits (5, 4, and one of the circuits of size 2) produces 40.

Your list contains many junction boxes; connect together the 1000 pairs of junction boxes which are closest together. Afterward, what do you get if you multiply together the sizes of the three largest circuits?
'''

import math

def calculate_distance(box1: tuple[int, int, int], box2: tuple[int, int, int]) -> float:
    return math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2)

def find_largest_circuits_product(junction_boxes: list[tuple[int, int, int]], connections: int) -> int:
    n = len(junction_boxes)
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if size[rootX] < size[rootY]:
                rootX, rootY = rootY, rootX
            parent[rootY] = rootX
            size[rootX] += size[rootY]

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_distance(junction_boxes[i], junction_boxes[j])
            distances.append((dist, i, j))

    distances.sort()

    # Limit connections to available pairs
    max_connections = min(connections, len(distances))
    
    for k in range(max_connections):
        _, box1, box2 = distances[k]
        union(box1, box2)

    # Find unique circuits and their sizes
    circuit_sizes = {}
    for i in range(n):
        root = find(i)
        circuit_sizes[root] = size[root]
    
    # Get the three largest circuit sizes
    largest_sizes = sorted(circuit_sizes.values(), reverse=True)[:3]
    
    # Calculate product
    product = 1
    for s in largest_sizes:
        product *= s

    return product

if __name__ == "__main__":
    with open("Day_08/day08_input.txt", "r") as file:
        junction_boxes = [tuple(map(int, line.strip().split(','))) for line in file.readlines()]
    result = find_largest_circuits_product(junction_boxes, 1000)  # 1000 connections for real input
    print(f"Product of the sizes of the three largest circuits: {result}")