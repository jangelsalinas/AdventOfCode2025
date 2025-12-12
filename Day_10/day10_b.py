'''
--- Part Two ---
Now we need to configure joltage level counters instead of indicator lights.

Each machine has counters (initially 0) that need to reach specific target values shown in {curly braces}.
When you push a button, it increases each of its listed counters by 1.

Example: {3,5,4,7} means we need counters: [3, 5, 4, 7]
Button (1,3) increases counters 1 and 3 by 1 each time pressed.

Goal: Find the minimum number of button presses to reach the target joltage levels.
'''

def parse_machine(line: str) -> tuple[list[int], list[set[int]]]:
    parts = line.strip()

    # Extract joltage requirements (between { and })
    j0 = parts.index('{')
    j1 = parts.index('}', j0)
    target_joltage = list(map(int, parts[j0 + 1 : j1].split(',')))

    # Extract all buttons (between ( and )), ignoring the [diagram]
    buttons: list[set[int]] = []
    i = 0
    while True:
        try:
            p0 = parts.index('(', i)
        except ValueError:
            break
        p1 = parts.index(')', p0)
        button_str = parts[p0 + 1 : p1]
        if button_str:
            buttons.append(set(map(int, button_str.split(','))))
        i = p1 + 1

    return target_joltage, buttons


class MinCostMaxFlow:
    def __init__(self, n: int):
        self.n = n
        self.adj: list[list[int]] = [[] for _ in range(n)]
        self.to: list[int] = []
        self.cap: list[int] = []
        self.cost: list[int] = []
        self.nxt: list[int] = []

    def add_edge(self, u: int, v: int, cap: int, cost: int) -> None:
        # forward
        self.adj[u].append(len(self.to))
        self.to.append(v)
        self.cap.append(cap)
        self.cost.append(cost)
        self.nxt.append(len(self.adj[v]))
        # backward
        self.adj[v].append(len(self.to))
        self.to.append(u)
        self.cap.append(0)
        self.cost.append(-cost)
        self.nxt.append(len(self.adj[u]) - 1)

    def min_cost_flow(self, s: int, t: int, maxf: int) -> tuple[int, int]:
        import heapq

        n = self.n
        flow = 0
        cost = 0
        pot = [0] * n  # potentials

        while flow < maxf:
            dist = [10**18] * n
            parent_e = [-1] * n
            dist[s] = 0
            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d != dist[u]:
                    continue
                for ei in self.adj[u]:
                    if self.cap[ei] <= 0:
                        continue
                    v = self.to[ei]
                    nd = d + self.cost[ei] + pot[u] - pot[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        parent_e[v] = ei
                        heapq.heappush(pq, (nd, v))

            if parent_e[t] == -1:
                break

            for v in range(n):
                if dist[v] < 10**18:
                    pot[v] += dist[v]

            add = maxf - flow
            v = t
            while v != s:
                ei = parent_e[v]
                add = min(add, self.cap[ei])
                v = self.to[ei ^ 1]

            v = t
            while v != s:
                ei = parent_e[v]
                self.cap[ei] -= add
                self.cap[ei ^ 1] += add
                cost += add * self.cost[ei]
                v = self.to[ei ^ 1]

            flow += add

        return flow, cost

def min_button_presses(target_joltage: list[int], buttons: list[set[int]]) -> int:
    # We need nonnegative integers x_j (press counts) minimizing sum(x_j)
    # subject to: for each counter i, sum_{j: i in button_j} x_j = target[i].
    # This is a min-cost circulation problem:
    # - Create one node per distinct button-pattern (mask) and one node per counter.
    # - Send exactly target[i] units into each counter.
    # - Each unit that goes through a pattern node costs 1 (counts as one press).

    n = len(target_joltage)
    if n == 0:
        return 0

    # Build patterns: each press chooses a pattern (subset of counters) and contributes +1 to all in it.
    # Multiple buttons with same pattern are equivalent for minimizing total presses.
    pattern_masks: set[int] = set()
    for btn in buttons:
        mask = 0
        for idx in btn:
            mask |= 1 << idx
        if mask != 0:
            pattern_masks.add(mask)

    # Quick infeasibility: any counter not covered by any pattern with that bit => impossible.
    cover = 0
    for m in pattern_masks:
        cover |= m
    for i, t in enumerate(target_joltage):
        if t != 0 and ((cover >> i) & 1) == 0:
            return 0

    patterns = sorted(pattern_masks)
    P = len(patterns)
    total = sum(target_joltage)
    if total == 0:
        return 0

    # Graph:
    # source -> each counter i with cap=target[i], cost=0
    # counter i -> pattern p if pattern includes i with cap=target[i], cost=0
    # pattern p -> sink with cap=INF, cost=1  (each unit assigned to p costs 1 press)
    # This ensures each unit of demand chooses one pattern, counting presses.
    # BUT: choosing a pattern unit must satisfy ALL counters in that pattern simultaneously.
    # We enforce this by expanding flow units across counters using equality constraints:
    # For each pattern p, the number of units through p must be identical across its counters.
    # Achieved by introducing a pattern node that "produces" k units, and each counter in pattern consumes k.

    # To model that, we use a standard construction:
    # source -> pattern p (cap=INF, cost=1)
    # pattern p -> counter i (cap=INF, cost=0) for i in p
    # counter i -> sink (cap=target[i], cost=0)
    # and we require exact total flow = sum(target).
    # This makes each unit go from source to one pattern then to one counter, which would NOT enforce
    # simultaneous increment for all counters in the pattern.
    # So instead we solve via min-cost max-flow on patterns as "columns" with coupling using a
    # min-cost flow on a bipartite expansion over unit layers is too large.

    # Practical AoC shortcut: number of counters is small (<= 10 from sample; input shows <= 10).
    # Use DP over bitmasks with Dijkstra in n-dimensional space is still huge.
    # We can instead compute exact optimum using integer DP via meet-in-the-middle on patterns count.

    # Final chosen method: dynamic programming with Dijkstra on residual demands where n <= 10.
    # State is remaining tuple; transitions subtract a pattern (press once). This is BFS with pruning,
    # but implemented with A* (Dijkstra) and strong heuristic + dominance to handle large targets.

    import heapq

    start = tuple(target_joltage)
    pq: list[tuple[int, tuple[int, ...]]] = [(0, start)]
    best = {start: 0}

    # Precompute pattern as list of indices for faster update
    pat_idxs = []
    for m in patterns:
        idxs = [i for i in range(n) if (m >> i) & 1]
        pat_idxs.append(idxs)

    def heuristic(state: tuple[int, ...]) -> int:
        # Lower bound: any press can reduce at most max_popcount counters by 1.
        # So minimum presses >= ceil(sum(state)/max_popcount)
        s = sum(state)
        if s == 0:
            return 0
        max_pop = max(len(idxs) for idxs in pat_idxs)
        return (s + max_pop - 1) // max_pop

    seen_cost = best

    while pq:
        g, state = heapq.heappop(pq)
        if g != seen_cost.get(state, 10**18):
            continue
        if all(v == 0 for v in state):
            return g

        # Expand: press any pattern once (subtract 1 from included counters if >0)
        for idxs in pat_idxs:
            # Quick skip if this pattern doesn't help
            if all(state[i] == 0 for i in idxs):
                continue
            new_list = list(state)
            for i in idxs:
                if new_list[i] == 0:
                    break
                new_list[i] -= 1
            else:
                new_state = tuple(new_list)
                ng = g + 1
                if ng < seen_cost.get(new_state, 10**18):
                    seen_cost[new_state] = ng
                    heapq.heappush(pq, (ng, new_state))

    return 0

if __name__ == "__main__":
    total_presses = 0
    with open("Day_10/day10_input.txt", "r") as file:
        for line in file:
            target_joltage, buttons = parse_machine(line)
            presses = min_button_presses(target_joltage, buttons)
            # print(f"Machine requires {presses} presses for target {target_joltage}")
            total_presses += presses
    print(f"Fewest button presses required: {total_presses}")