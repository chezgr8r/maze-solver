from Structs import *
from GlobalVariables import *

# Create lists for keeping track of visited and unvisited nodes
# Create last_vis_nodes to keep track of most recently visited nodes because
#   don't need to check for the neighbors of nodes whose neighbors have been found
unvis_nodes = []
vis_nodes = []
last_vis_nodes = []

# Function to create a new, blank cell
def new_cell(pos):
    return Cell(WHITE, -1, pos, None)

# Create global grid
GRID = [[new_cell((0, 0))]]

# Recursive implementation of Dijkstra's algorithm, helper for dijkstra()
def dijkstra_recur():
    global GRID, unvis_nodes, vis_nodes, last_vis_nodes, RED

    # Keep track of neighbors of last_vis_nodes and if end has been found
    temp_neighbors = []
    found_red = False
    # Add all unvisited neighbors to temp_neighbors
    for vis_n in last_vis_nodes:
        r = vis_n[0]
        c = vis_n[1]
        if GRID[r][c].fill == RED:
            found_red = True
        for coor in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if coor in unvis_nodes:
                unvis_nodes.remove(coor)
                GRID[coor[0]][coor[1]].prevCell = vis_n
                temp_neighbors.append(coor)

    # Add last_vis_nodes to vis_nodes as a step and set last_vis_nodes to temp_neighbors
    vis_nodes.append(last_vis_nodes)
    last_vis_nodes = temp_neighbors

    # Recursion continues if red hasn't been found and there are more nodes to visit
    if not((found_red) or (not last_vis_nodes)):
        dijkstra_recur()

def dijkstra():
    global unvis_nodes, vis_nodes, last_vis_nodes, GREEN, RED, BLACK, BLUE, YELLOW

    # Reset node lists
    unvis_nodes = []
    vis_nodes = []
    last_vis_nodes = []

    # Check that start and end exist and that grid doesn't require reset
    startPos = None
    endPos = None
    anyBlue = False
    duplicate = False
    for r in range(len(GRID)):
        for c in range(len(GRID[0])):
            if GRID[r][c].fill == GREEN:
                if startPos == None:
                    startPos = (r, c)
                else:
                    duplicate = True
            elif GRID[r][c].fill == RED:
                if endPos == None:
                    endPos = (r, c)
                else:
                    duplicate == True
            elif (GRID[r][c].fill == BLUE) or (GRID[r][c].fill == YELLOW):
                anyBlue = True
    if (duplicate or anyBlue) or ((startPos == None) or (endPos == None)):
        return None
    else:
        # Add all non-black nodes to unvis_nodes
        for r in range(len(GRID)):
            for c in range(len(GRID[0])):
                if GRID[r][c].fill != BLACK:
                    unvis_nodes.append((r, c))

        # Manually set starting node
        GRID[startPos[0]][startPos[1]].prevCell = None
        last_vis_nodes.append(startPos)
        unvis_nodes.remove(startPos)
        dijkstra_recur()
        return vis_nodes
