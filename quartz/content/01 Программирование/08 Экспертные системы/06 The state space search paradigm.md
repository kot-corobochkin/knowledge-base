## 1. The State Space Concept

The state space search paradigm was popularized by Newell and Simon with their General Problem Solver (GPS) in 1960.
- **State:** A configuration of the problem at a given point. For example, in the 8-puzzle, each arrangement of tiles is a state.
- **Operators (Actions):** Actions that transform one state into another (e.g., moving a tile into the blank space). Each operator has pre-conditions and effects.
- **Initial State:** The starting configuration of the agent.
- **Goal State:** The desired configuration that constitutes a solution.
- **State Space:** A graph representation where nodes represent states and arcs represent operators (actions). The graph is often undirected because moves are reversible.

## 2. The Search Problem Formally Defined

A search problem is represented as a 4-tuple: **{S, S0, A, G}**

| Component | Description |
| --- | --- |
| S | Full set of all possible states |
| S0 | The initial state |
| A | Set of operators (actions) that transform states: S → S |
| G | Set of goal states |

- **Solution Path:** A sequence of actions (plan) P = {a0, a1, a2, ..., aN} that transforms the agent from the initial state to a goal state.
- **Path Cost:** A positive number, often the sum of the costs of individual actions along the path.

## 3. The Searching Process

The basic search process follows these steps, repeated until a solution is found or the state space is exhausted:
- Check the current node.
- Execute an allowable action to find successor states.
- Pick one of the new states.
- Check if the new state is a goal state.
- If not, the new state becomes the current state and the process repeats.

The search tree is typically extended one node at a time, with the search strategy determining the order in which nodes are explored.

## 4. Examples of State Space Problems

## 4.1 Pegs and Disks (Tower of Hanoi)
- **Problem:** Three pegs and three disks. Operators allow moving the topmost disk from one peg to another.
- **Goal State:** All disks on peg B.
- **Solution:** A sequence of seven moves achieves the goal.

## 4.2 8-Puzzle
- **Problem:** A 3×3 board with eight numbered tiles and one blank. Tiles can slide into the blank position (or equivalently, the blank moves up, down, left, right).
- **State:** Description of the location of each tile.
- **Goal Test:** Current state matches a specified goal configuration.
- **Path Cost:** Each move costs 1.
## 5. Search Techniques: Key Concepts

Every AI program involves searching because solution steps are not explicit. The search technique helps find a feasible path efficiently.

**Search Algorithm:** Takes a problem as input and returns a solution after evaluating a number of possible solutions. The set of all possible solutions is called the **search space**.

**Basic Search Algorithm (Pseudocode):**
```

Let L be a list containing the initial state
Loop
    If L is empty, then return failure
    Node ← select(L)
    If node is a goal
        Then return node
    Else generate all successors of node and merge them into L
End loop
```

**Evaluation Criteria for Search Algorithms:**
- **Completeness:** Does the strategy guarantee finding a solution if one exists?
- **Optimality:** Does it find the solution with the lowest (minimal) cost?
- **Complexity:**

**Time Complexity:** Time taken to find a solution.
- **Space Complexity:** Memory used by the algorithm.

## 6. Types of Search Techniques

| Category                           | Description                                                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Uninformed Search (Blind Search)   | No domain-specific knowledge. Only uses initial state, goal state, and legal operators. Explores nodes in a predetermined order. |
| Informed Search (Heuristic Search) | Uses domain-specific knowledge (heuristics) to guide the search more efficiently toward the goal.                                |
## 7. Uninformed Search: Breadth-First Search (BFS)

**Concept:** Explores the search tree level by level. The root node is expanded first, then all its successors, then all successors of those nodes, and so on.

**Implementation:** Uses a FIFO (First-In-First-Out) queue. Nodes visited first are expanded first.

**Algorithm:**
- Set the initial node on list START.
- If START is empty or START equals goal, terminate.
- Remove the first node from START, call it A.
- If A equals goal, terminate with success.
- Else if A has successors, generate all of them and add them to the end of START.
- Go to step 2.

**Properties:**
- **Complete:** Yes (if the shallowest goal node is at finite depth)
- **Optimal:** Yes (if path cost is a non-decreasing function of depth; finds the shortest path in terms of number of steps)
- **Time Complexity:** O(b^d) — exponential
- **Space Complexity:** O(b^d) — exponential

**Advantages:**
- Finds the minimal solution (shortest path).
- Simple to implement.
- Works well for problems with a small state space (e.g., traveling salesman with few cities).

**Disadvantage:**
- Requires generation and storage of an exponentially large tree, leading to massive memory requirements for deep problems.
## 8. Uninformed Search: Uniform Cost Search

**Concept:** An extension of BFS that expands the node with the lowest path cost (g(n)) rather than the shallowest node. Each operator has an associated cost.

**Implementation:** Nodes are sorted in the OPEN list by increasing g(n) (cumulative cost from the start).

**Properties:**
- **Complete:** Yes
- **Optimal:** Yes
- **Complexity:** Exponential time and space

**Note:** If all step costs are equal, uniform cost search is identical to BFS.

## 9. Uninformed Search: Depth-First Search (DFS)

**Concept:** Explores the deepest node in the current fringe first. The search proceeds immediately to the deepest level of the tree until nodes have no successors, then backtracks.

**Implementation:** Uses a LIFO (Last-In-First-Out) stack. Only one path from root to leaf needs to be stored, along with unexpanded sibling nodes.

**Variant: Backtracking Search**
- Generates only one successor at a time rather than all.
- Modifies the current state description directly instead of copying.
- Memory requirement: O(m) where m is the maximum depth (compared to O(bm) for standard DFS).

**Algorithm:**
- Put the initial node on list START.
- If START is empty or START equals goal, terminate.
- Remove the first node from START, call it A.
- If A equals goal, terminate with success.
- Else if A has successors, generate all of them and add them to the beginning of START.
- Go to step 2.

**Properties:**
- **Complete:** No (may get stuck in infinite depth if the tree is unbounded)
- **Optimal:** No (does not guarantee the shortest path)
- **Time Complexity:** O(b^m) — exponential in the worst case
- **Space Complexity:** O(bm) — linear (significant advantage over BFS)

**Advantages:**
- Requires much less memory than BFS.
- More efficient for problems with deep solutions.

**Disadvantage:**
- May explore very deep paths unnecessarily and can get lost in infinite branches.

## 10. Comparison of BFS and DFS

| Feature | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| --- | --- | --- |
| Data Structure | FIFO Queue | LIFO Stack |
| Completeness | Complete | Incomplete (may go infinite) |
| Optimality | Yes (shortest path) | No |
| Time Complexity | O(b^d) | O(b^m) |
| Space Complexity | O(b^d) | O(bm) |
| Memory Usage | Very high | Moderate |
| Best For | Shallow solutions | Deep solutions, memory-constrained environments |

*(where b = branching factor, d = depth of shallowest goal, m = maximum depth of the search tree)*
## 11. Conclusion

State space search is a foundational technique in AI for problem-solving. The choice of search strategy involves trade-offs between completeness, optimality, time, and memory. Uninformed searches like BFS and DFS provide basic mechanisms for exploring state spaces without domain knowledge, with BFS guaranteeing the shortest path at the cost of high memory usage, and DFS offering memory efficiency at the risk of incompleteness and non-optimality.

Uninformed search strategies provide fundamental mechanisms for exploring state spaces without domain-specific knowledge. The choice of algorithm involves trade-offs between completeness, optimality, time, and memory:

- **BFS** guarantees the shortest path but requires exponential memory.
- **DFS** is memory-efficient but may not find a solution or may find a non-optimal one.
- **DLS** addresses DFS's infinite path issue but requires knowledge of a suitable depth limit.
- **IDDFS** combines the best properties of BFS and DFS—optimality and completeness with linear memory—making it the preferred uninformed search strategy for large state spaces where the solution depth is unknown.
