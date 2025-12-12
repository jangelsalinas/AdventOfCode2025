'''
Read a file
Each line contains a single indicator light diagram in [square brackets], one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.
To start a machine, its indicator lights must match those shown in the diagram, where . means off and # means on. The machine has the number of indicator lights shown, but its indicator lights are all initially off.
So, an indicator light diagram like [.##.] means that the machine has four indicator lights which are initially off and that the goal is to simultaneously configure the first light to be off, the second light to be on, the third to be on, and the fourth to be off.
You can toggle the state of indicator lights by pushing any of the listed buttons. Each button lists which indicator lights it toggles, where 0 means the first light, 1 means the second light, and so on. When you push a button, each listed indicator light either turns on (if it was off) or turns off (if it was on). You have to push each button an integer number of times; there's no such thing as "0.5 presses" (nor can you push a button a negative number of times).
So, a button wiring schematic like (0,3,4) means that each time you push that button, the first, fourth, and fifth indicator lights would all toggle between on and off. If the indicator lights were [#.....], pushing the button would change them to be [...##.] instead.
Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.
You can push each button as many times as you like. However, to save on time, you will need to determine the fewest total presses required to correctly configure all indicator lights for all machines in your list.
There are a few ways to correctly configure the first machine:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
You could press the first three buttons once each, a total of 3 button presses.
You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button presses.
You could press all of the buttons except (1,3) once each, a total of 5 button presses.

However, the fewest button presses required is 2. One way to do this is by pressing the last two buttons ((0,2) and (0,1)) once each.

In the input test
So, the fewest button presses required to correctly configure the indicator lights on all of the machines is 2 + 3 + 2 = 7.

What is the fewest button presses required to correctly configure the indicator lights on all of the machines?
'''

def parse_machine(line: str) -> tuple[str, list[set[int]]]:
    # Split by brackets, parentheses to find diagram and buttons
    parts = line.strip()
    
    # Extract diagram (between [ and ])
    diagram_start = parts.index('[')
    diagram_end = parts.index(']')
    diagram = parts[diagram_start+1:diagram_end]
    
    # Extract all buttons (between ( and ))
    buttons = []
    rest = parts[diagram_end+1:]
    
    while '(' in rest:
        btn_start = rest.index('(')
        btn_end = rest.index(')')
        button_str = rest[btn_start+1:btn_end]
        
        # Skip if it's the joltage requirement (starts with number followed by comma and more numbers after })
        if '{' not in rest[:btn_start]:  # Not inside curly braces
            if button_str:  # Not empty
                buttons.append(set(map(int, button_str.split(','))))
        
        rest = rest[btn_end+1:]
    
    return diagram, buttons

def min_button_presses(diagram: str, buttons: list[set[int]]) -> int:
    from itertools import product

    n = len(buttons)
    min_presses = float('inf')

    # Try all combinations of button presses (0 or 1 times)
    for presses in product([0, 1], repeat=n):
        lights = ['.'] * len(diagram)
        for btn_index, press in enumerate(presses):
            if press == 1:
                for light_index in buttons[btn_index]:
                    lights[light_index] = '#' if lights[light_index] == '.' else '.'
        if ''.join(lights) == diagram:
            total_presses = sum(presses)
            min_presses = min(min_presses, total_presses)

    return min_presses if min_presses != float('inf') else 0

if __name__ == "__main__":
    total_presses = 0
    with open("Day_10/day10_input.txt", "r") as file:
        for line in file:
            diagram, buttons = parse_machine(line)
            presses = min_button_presses(diagram, buttons)
            total_presses += presses
    print(f"Fewest button presses required: {total_presses}")