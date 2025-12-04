"""
Need to solve passowrd
The safe has a dial with only an arrow on it; around the dial are the numbers 0 through 99 in order. As you turn the dial, it makes a small click noise as it reaches each number.

The attached document (your puzzle input) contains a sequence of rotations, one per line, which tell you how to open the safe. A rotation starts with an L or R which indicates whether the rotation should be to the left (toward lower numbers) or to the right (toward higher numbers). Then, the rotation has a distance value which indicates how many clicks the dial should be rotated in that direction.

So, if the dial were pointing at 11, a rotation of R8 would cause the dial to point at 19. After that, a rotation of L19 would cause it to point at 0.

The dial starts by pointing at 50.

You could follow the instructions, but your recent required official North Pole secret entrance security training seminar taught you that the safe is actually a decoy. The actual password is the number of times the dial is left pointing at 0 after any rotation in the sequence.
"""

def count_zero_positions(rotations):
    position = 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'R':
            position = (position + distance) % 100
        elif direction == 'L':
            position = (position - distance) % 100

        if position == 0:
            zero_count += 1

    return zero_count

if __name__ == "__main__":
    with open("Day_01/day01_input.txt") as f:
        rotations = f.read().strip().splitlines()

    result = count_zero_positions(rotations)
    print(f"The dial points at 0 a total of {result} times.")
    