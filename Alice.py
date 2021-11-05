import sys
from typing import *


class Grid:
    def __init__(self):
        self.role = "normal"
        self.color = "Black"
        self.NW = False
        self.N = False
        self.NE = False
        self.W = False
        self.E = False
        self.SW = False
        self.S = False
        self.SE = False

    def _print_directions(self) -> str:  # for testing
        result = ""
        if self.NW:
            result += "nw "
        if self.N:
            result += "n "
        if self.NE:
            result += "ne "
        if self.W:
            result += "w "
        if self.E:
            result += "e "
        if self.SW:
            result += "sw "
        if self.S:
            result += "s "
        if self.SE:
            result += "se "
        return result

    def __str__(self):  # for testing
        return "role: {0}, color: {1}, directions: {2}". \
            format(self.role, self.color, self._print_directions())

    def assign_role(self, r: str):
        if r == "?":
            self.role = "start"
        elif r == "!":
            self.role = "goal"
        else:
            self.role = "normal"

    def assign_color(self, c: str):
        if c == "b":
            self.color = "Black"
        elif c == "r":
            self.color = "Red"
        else:
            self.color = "Yellow"

    def assign_directions(self, directions: List[str]):
        for d in directions:
            if d == "":
                break
            if d == "nw":
                self.NW = True
            elif d == "n":
                self.N = True
            elif d == "ne":
                self.NE = True
            elif d == "w":
                self.W = True
            elif d == "e":
                self.E = True
            elif d == "sw":
                self.SW = True
            elif d == "s":
                self.S = True
            else:
                self.SE = True

    def blank(self) -> bool:
        return not (
                self.E or self.N or self.NE or self.NW or
                self.S or self.SE or self.SW or self.W)


class Maze:
    # top left corner is (0, 0)
    # bottom right corner is (width - 1, height - 1)
    def __init__(self, width: int, height: int):
        self.starting_point = (0, 0)
        self.width = width
        self.height = height
        self.data = []
        for i in range(0, height):
            self.data.append([])

    def print_maze(self):  # for testing
        print("The starting point is " + str(self.starting_point))
        for i in range(0, self.height):
            for j in range(0, self.width):
                print(self.data[i][j])
            print("=========")

    def get_grid(self, point: Tuple[int, int]) -> Grid:
        return self.data[point[1]][point[0]]


class Node:
    def __init__(self):
        self.coordinate = (0, 0)
        self.step_size = 1
        self.children = []
        self.parent = None


class Queue:

    def __init__(self):
        self.data = []

    def enqueue(self, a):
        self.data.append(a)

    def dequeue(self) -> Node:
        return self.data.pop(0)

    def is_empty(self) -> bool:
        return len(self.data) == 0


# def built_tree(node: Node, maze: Maze, at_grid: Grid, all_past_node: List):
#     if(node.coordinate)


def main() -> None:
    # You do NOT need to include any error checking. I found this particular
    # check personally helpful, when I forgot to provide a filename.
    if len(sys.argv) != 2:
        print("Usage: python3 Alice.py <inputfilename>")
        sys.exit()

    # Here is how you open a file whose name is given as the first argument
    f = open(sys.argv[1])

    # readline returns the next line from the file reader as a string
    # including the linefeed
    grid_dim = f.readline().strip().split(" ")  # [width, height]
    width = int(grid_dim[0])
    height = int(grid_dim[1])
    maze = Maze(width, height)
    for i in range(0, height):
        input_arr = f.readline().strip().split(" ")  # a row of Grids
        for j in range(0, width):
            g = Grid()
            grid_arr = input_arr[j].split(",")  # [role, color, directions]
            g.assign_role(grid_arr[0])  # add role to a grid
            g.assign_color(grid_arr[1])  # add color to a grid
            directions = grid_arr[2].split("_")
            g.assign_directions(directions)  # add directions to a grid
            if grid_arr[0] == "?":
                maze.starting_point = (j, i)
            maze.data[i].append(g)

    # above is the code for loading Maze into the program
    root = Node()
    root.coordinate = maze.starting_point
    all_past_node = []
    for i in range(maze.height):
        all_past_node.append([])
        for j in range(maze.height):
            all_past_node[i].append([])

    queue = Queue()

    queue.enqueue(root)
    all_past_node[root.coordinate[0]][root.coordinate[1]].append(root.step_size)

    goal = None
    while not queue.is_empty():
        focus_node = queue.dequeue()
        if focus_node.step_size == 0:
            continue
        # check the direction
        current_grid = maze.get_grid(focus_node.coordinate)
        if current_grid.NW:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0] - focus_node.step_size,
                              focus_node.coordinate[1] - focus_node.step_size)
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.N:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0],
                              focus_node.coordinate[1] - focus_node.step_size)
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.NE:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0] + focus_node.step_size,
                              focus_node.coordinate[1] - focus_node.step_size)
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.W:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0] - focus_node.step_size,
                              focus_node.coordinate[1])
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.E:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0] + focus_node.step_size,
                              focus_node.coordinate[1])
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.SW:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0] - focus_node.step_size,
                              focus_node.coordinate[1] + focus_node.step_size)
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.S:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0],
                              focus_node.coordinate[1] + focus_node.step_size)
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to
                        # the queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)
        if current_grid.SE:
            # find out the children's coordinate
            new_coordinate = (focus_node.coordinate[0] + focus_node.step_size,
                              focus_node.coordinate[1] + focus_node.step_size)
            # check if children is out of bound
            if not (new_coordinate[0] < 0 or new_coordinate[0] >= height or
                    new_coordinate[1] < 0 or new_coordinate[1] >= height):
                new_grid = maze.get_grid(new_coordinate)
                # create the node
                new_node = Node()
                new_node.parent = focus_node
                new_node.coordinate = new_coordinate
                if new_grid.color == 'Red':
                    new_node.step_size = focus_node.step_size + 1
                elif new_grid.color == 'Yellow':
                    new_node.step_size = focus_node.step_size - 1
                else:
                    new_node.step_size = focus_node.step_size
                # check if it is goal
                if new_grid.role == 'goal':
                    # finish
                    goal = new_node
                    break
                # check if it is blank
                if not new_grid.blank():
                    # check if it is already have
                    if new_node.step_size not in \
                            all_past_node[new_coordinate[0]][new_coordinate[1]]:
                        # connect children to the parent and add children to the
                        #  queue and add children to the all_past_node
                        focus_node.children.append(new_node)
                        queue.enqueue(new_node)
                        all_past_node[new_coordinate[0]][
                            new_coordinate[1]].append(new_node.step_size)

    if goal is None:
        print("No solution.")
    else:
        length = 0

        result = "(" + str(goal.coordinate[0]) + "," + str(
            goal.coordinate[1]) + ")"

        current_node = goal

        while current_node.parent is not None:
            current_node = current_node.parent
            length += 1
            result = "(" + str(current_node.coordinate[0]) + "," + str(
                current_node.coordinate[1]) + ")->" + result

        print(result)
        print("length is " + str(length))


if __name__ == "__main__":

    main()
