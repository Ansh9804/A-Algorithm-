#Name: - Ansh Tandale
#PRN: - 1032220887
#PANEL- B Roll No. 08
#AIES ASSIGNMENT-1 
# A* ALGORITHM Implementation
# f(n) = g(n) + h(n)
# g(n) = cost of path from start to node n
# h(n) = estimated cost of path from node n to goal
# min max algorithm

import heapq

class Node:
    def __init__(self, state, goal_state, parent=None, action=None, depth=0, use_manhattan=False):
        self.state = state
        self.goal_state = goal_state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.use_manhattan = use_manhattan
        self.heuristic = self.calculate_heuristic()
        self.f = self.depth + self.heuristic

    def calculate_heuristic(self):
        if self.use_manhattan:
            return self.calculate_manhattan_distance()
        else:
            return self.calculate_hamming_distance()

    def calculate_hamming_distance(self):
        return sum(self.state[i][j] != self.goal_state[i][j] and self.state[i][j] != '_'
                   for i in range(3) for j in range(3))

    def calculate_manhattan_distance(self):
        flat_goal = [tile for row in self.goal_state for tile in row]
        distance = 0
        for i in range(3):
            for j in range(3):
                tile = self.state[i][j]
                if tile != '_':
                    goal_index = flat_goal.index(tile)
                    goal_i, goal_j = divmod(goal_index, 3)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == '_':
                    return i, j
        return None

    def generate_children(self):
        children = []
        x, y = self.find_blank()
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        
        valid_moves = []
        for new_x, new_y in moves:
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                valid_moves.append((new_x, new_y))
        
        # Limit to a maximum of 2 moves
        for new_x, new_y in valid_moves[:2]:
            new_state = [row[:] for row in self.state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            children.append(Node(new_state, self.goal_state, self, action=(x, y, new_x, new_y), depth=self.depth + 1, use_manhattan=self.use_manhattan))

        return children

    def __lt__(self, other):
        return self.f < other.f

class Puzzle:
    def __init__(self, start_state, goal_state, use_manhattan=False):
        self.start_state = start_state
        self.goal_state = goal_state
        self.use_manhattan = use_manhattan

    def a_star_search(self, start_node):
        open_list = []
        heapq.heappush(open_list, start_node)
        closed_list = set()
        nodes_explored = 0

        while open_list:
            current_node = heapq.heappop(open_list)
            nodes_explored += 1

            # Internal traversal output
            print(f"Exploring Node at Depth {current_node.depth} with State:")
            self.print_state(current_node.state)
            print(f"Heuristic value (h): {current_node.heuristic}")
            print(f"Total cost (f = g + h): {current_node.f}")
            print("Generating Children (up to 2 moves):")

            if current_node.state == self.goal_state:
                self.print_solution(current_node)
                print(f"\nNumber of nodes explored: {nodes_explored}")
                return

            closed_list.add(tuple(map(tuple, current_node.state)))

            for child in current_node.generate_children():
                print("Possible Move to:")
                self.print_state(child.state)
                if tuple(map(tuple, child.state)) not in closed_list:
                    heapq.heappush(open_list, child)

        print("No solution found.")

    def print_solution(self, node):
        path = []
        while node:
            path.append(node)
            node = node.parent
        path.reverse()

        for step in path:
            self.print_state(step.state)
            print(f"Heuristic value (h): {step.heuristic}")
            print(f"Depth (g): {step.depth}")
            print(f"Total cost (f = g + h): {step.f}")
            print()

    @staticmethod
    def print_state(state):
        for row in state:
            print(" ".join(str(x) if x != '_' else ' ' for x in row))
        print()

def get_state_input(prompt):
    state = []
    print(prompt)
    for i in range(3):
        while True:
            row = input(f"Enter row {i+1} (space-separated values): ").strip().split()
            if len(row) == 3:
                state.append(row)
                break
            else:
                print("Each row must have exactly 3 elements. Please try again.")
    return state

def choose_initial_move(initial_state, goal_state, use_manhattan):
    initial_node = Node(initial_state, goal_state, use_manhattan=use_manhattan)
    children = initial_node.generate_children()
    
    if not children:
        print("No possible moves from the initial state.")
        return initial_node
    
    print("Possible moves from the initial state:")
    for idx, child in enumerate(children):
        print(f"Move {idx + 1}:")
        Puzzle.print_state(child.state)
    
    choice = -1
    while choice < 0 or choice >= len(children):
        choice = int(input(f"Choose a move (1 or {len(children)}): ")) - 1
        if choice < 0 or choice >= len(children):
            print(f"Invalid choice. Please choose a number between 1 and {len(children)}.")
    
    chosen_node = children[choice]
    
    print("You chose the following move:")
    Puzzle.print_state(chosen_node.state)
    
    return chosen_node

if __name__ == "__main__":
    print("Enter the initial state:")
    initial_state = get_state_input("Use '_' for the blank space.")
    
    print("Enter the goal state:")
    goal_state = get_state_input("Use '_' for the blank space.")

    print("Initial State:")
    Puzzle.print_state(initial_state)
    
    print("Goal State:")
    Puzzle.print_state(goal_state)
    
    use_manhattan = input("Use Manhattan distance heuristic? (yes/no): ").strip().lower() == 'yes'

    chosen_node = choose_initial_move(initial_state, goal_state, use_manhattan)

    print("Solving the Puzzle with the chosen move...")
    Puzzle(initial_state, goal_state, use_manhattan).a_star_search(chosen_node)