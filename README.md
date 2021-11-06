# Alice Maze

Contributors: Luke Ren([Luke9248](https://github.com/Luke9248)), Steven Yuan([vesteny77](https://github.com/vesteny77))



## Background

Based on Lewis Carroll’s Alice In Wonderland, [Alice Mazes](http://www.logicmazes.com/alice.html) are puzzles created by Robert Abbott.

Unfortunately, Abbott passed away and the code for the mazes on his website are not maintained due to the deprecation of Java Applet.

The good news is that the mazes can be rendered using Java 7 on Internet Explorer 8. I've included the png files of all 20 mazes in the `mazes` folder.



## Rules

You start this maze on the red square, and your current position is always shown in red. You must make a series of moves that will take you to the goal. Begin each move by following one of the arrows in the red square, travel in a straight line for a distance equal to ***d***, and then click on the square where your move ends.

When the maze begins, ***d*** equals 1. When you land on a square with a red arrow, 1 is added to ***d***. When you land on a square with a yellow arrow, 1 is subtracted from ***d***. Two of these mazes have blank squares, which you may not land on.

(*Extracted from "http://www.logicmazes.com/alice.html"*)



## Input Setup

In order to implement a console-based Python program, we have to design a concise text that represents a human-readable representation of the maze:

Each grid in the maze is represented by a string containing 3 components separated by commas:

1. The first component is a symbol: `’?’` means that the grid is the starting grid; `’!’` means that the grid is the goal; `’#’` means that grid is neither a starting grid nor the goal.
2. The second component is an English letter: `’b’` stands for black, `’r’` stands for red, and `’y’` stands for yellow. If the grid is white, we place an empty string.
3. The third component contains directions separated by underscores. Each direction is abbreviated by a letter (eg: `s` -> south, `se` -> southeast). If there are no directions in the grid, we place an empty string.

Before the string representation for grids, we include the dimensions(width, height) of the maze. Following that, we place each grid row by row from the top left to the bottom right of the maze. So, the string representation of the example maze is

3 3

\#,r,e_se_s  !„  #,y,sw

#,b,n  #,b,n  #,b,sw

?,b,n_e  #,b,e  #,b,n



## Implementation Details

We will use an algorithm similar to the BFS.

We will label the grids of the maze by their coordinate, and construct a tree while going through the maze to show all possible non-duplicate paths the player could choose. We will denote the step size as d. We will treat the grid on the top left corner as coordinate (0,0) and the grid on the right bottom corner as coordinate (width - 1, height - 1).

Here is the **algorithm**:
When tracking through the maze starting from the starting position (red grid), the player can create a tree. The vertices of the tree not only represents the grid of the maze, but also contains the step size d when the player lands on the grid. Using the example maze, if the player lands on grid in the second row and the first column, the vertex should be labeled as [(0, 1), 1]; if the player lands on the top left grid, the vertex is labeled as [(0, 0), 2]. The sub-trees of a node in a tree shows all possible paths beginning with the grid stored inside the vertex with the step size d. We will use the algorithm similar to the BFS: we are going to create all possible children for a node before drawing children of other nodes.

The order of creating children depends on the direction of the child from the parent’s location, Similar to BFS, we will also use a queue to store all the nodes which are waiting to be handled. We will stop creating the sub-tree and abandon the current path in the following 4 situations:

​	*Case 1*: When we encounter the vertex on which we have landed before and the step size d is the same as any one of the previous times we landed there, we abandon that path.

​	*Case 2*: When we land on a blank grid, we abandon that path.

​	*Case 3*: When we exit the maze(go out of bounds), we abandon that path.

​	*Case 4*: When the step size becomes 0 during execution, we abandon that path.

Once the user successfully lands on the goal(creating a vertex that corresponds to the goal grid), the path from the root of the tree(the starting grid) to the leaf(corresponds to the goal) will be the shortest path from the starting point to the goal; however, if all paths are abandoned due to the 4 situations above before landing on the goal(queue becomes empty before finding the goal grid), the maze is unsolvable.

We are going to include the following **data structures**:

1. We will use List to implement the queue used for BFS. The enqueue() is equivalent to append() and the dequeue() is equivalent to pop(0).

2. Each grid in the maze is represented by an object Grid containing 10 fields: role(string) that has exactly 3 options - ”goal”, ”starting point”, or “normal”, color(string) that represents the color of the arrow, and eight direction fields(boolean) - if the grid contains arrows in these directions, the corresponding fields will be true and the rest are false.

3. The maze is an object that includes the starting point(tuple), a nested list storing all Grids, the width, and the height. The length of the list is height and the length of each inner list is width.

4. In the ”BFS tree”, each node is an object with fields: coordinate(tuple), step size(integer), and children(a list of nodes).
