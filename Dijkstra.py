from Structs import *
from GlobalVariables import *

# use ALgoRunning variable so buttons don't work while the algorithm is running
# create a set of unvisited nodes from a given list of lists
#   start by finding vistable neighbors of each white/green/red node, combining given structure and
#   neighbors into new structure, then adding new structures to unvisited nodes

@dataclass
class Node:
    cell: Cell
    neighbors: list

unvis_nodes = []
vis_nodes = []
last_vis_nodes = []

# Function to create a new, blank cell
def new_cell(pos):
    return Cell(WHITE, -1, pos, None)

# Create global grid
GRID = [[new_cell((0, 0))]]

#####################################################################################################
"""
def create_nodes(): #BROKEN: ONLY CREATES ONE NODE WITH NO NEIGHBORS
                    #FOUND ISSUE 1: COL_NUM/ROW_NUM == 1, EVEN WHEN THEY DON'T
                    #FOUND ISSUE 2: POSITIONS ARE MESSED UP SOMEHOW, PROBABLY NOT LOCALIZED TO THIS FILE
                    #ISSUE 2 UPDATE: .POS ONLY APPEARS TWICE OVERALL, SO CLEARLY I SCREWED SOMETHING UP
                    #ISSUE 2 LIKELY RESOLVED
    global GRID, BLACK, unvis_nodes
    print((len(GRID), len(GRID[0])))
    for r in range(len(GRID)):
        for c in range(len(GRID[0])):
            if GRID[r][c].fill != BLACK:
                print((r, c))
                nb = []
                # left
                if (c > 0) and (GRID[r][c - 1].fill != BLACK):
                    nb.append(GRID[r][c - 1])
                # right
                if (c < COL_NUM - 1) and (GRID[r][c + 1].fill != BLACK):
                    nb.append(GRID[r][c + 1])
                # top
                if (r > 0) and (GRID[r - 1][c].fill != BLACK):
                    nb.append(GRID[r - 1][c])
                # bottom
                if (r < ROW_NUM - 1) and (GRID[r + 1][c].fill != BLACK):
                    nb.append(GRID[r + 1][c])

                print(nb)
                unvis_nodes.append(Node(GRID[r][c], nb))

def dijkstra_recur(stp):
    global unvis_nodes, vis_nodes, last_vis_nodes
    if (not not unvis_nodes):
        # for loop check for all the neighbors of all the visited nodes in unvisited nodes
        # check the neighbors found for the red node, give them all their step value
        # add all of the unvisited node neighbors to the visited node list
        # if red node found, return that node, otherwise recur
        lvn_nbs = set()
        prev_poss = []
        lvn_nods = []
        red_nb = None
        for vn in last_vis_nodes:
            for neb in vn.neighbors:
                lvn_size = size(lvn_nbs)
                lvn_nbs.add(neb.pos)
                if lvn_size != size(lvn_nbs):
                    prev_poss.append((neb, vn.cell.pos))

        lvn_nbs = list(lvn_nbs)

        for nb in lvn_nbs:
            nb_node = list(n for n in unvis_nodes if n.cell == nb)[0]
            prv_ps = list(p for p in prev_pos if p[0] == nb_node.cell)[0]
            nb_node.cell.step = stp
            nb_node.cell.prevCell = prv_ps #########
            lvn_nods.append(nb_node)
            if nb_node.cell.fill == RED:
                red_nb = nb_node

        vis_nodes = vis_nodes + last_vis_nodes
        last_vis_nodes = lvn_nbs

        if red_nb != None:
            vis_nodes = vis_nodes + last_vis_nodes
            return red_nb
        else:
            dijkstra_recur(stp + 1)
    else:
        vis_nodes = vis_nodes + last_vis_nodes
        return None
        #do I have to check if red has been found? or can I just exit with None?
        # return none
"""
#################################################################################################################

"""
nb = []
# left
if (c > 0) and (GRID[r][c - 1].fill != BLACK):
    nb.append(GRID[r][c - 1])
# right
if (c < COL_NUM - 1) and (GRID[r][c + 1].fill != BLACK):
    nb.append(GRID[r][c + 1])
# top
if (r > 0) and (GRID[r - 1][c].fill != BLACK):
    nb.append(GRID[r - 1][c])
# bottom
if (r < ROW_NUM - 1) and (GRID[r + 1][c].fill != BLACK):
    nb.append(GRID[r + 1][c])
"""


def dijkstra_recur(step): # step might not even be necessary
    # ERROR: DOESN'T INCLUDE LAST STEP
    global GRID, unvis_nodes, vis_nodes, last_vis_nodes, RED

    # need to check 1. if red was found, 2. if unvis_nodes is empty
    temp_neighbors = []
    found_red = False
    for vis_n in last_vis_nodes:
        # search for neighbors in unvis_nodes, don't have to check for edges
        # dictionary?
        r = vis_n[0]
        c = vis_n[1]
        if GRID[r][c].fill == RED:
            found_red = True
        for coor in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if coor in unvis_nodes:
                unvis_nodes.remove(coor)
                GRID[coor[0]][coor[1]].prevCell = vis_n
                GRID[coor[0]][coor[1]].step = step
                temp_neighbors.append(coor)

    vis_nodes.append(last_vis_nodes)
    last_vis_nodes = temp_neighbors
    if (not last_vis_nodes) or (not found_red):
        dijkstra_recur(step + 1)
    else:
        print("unvis_nodes and found_red after recur")
        print(unvis_nodes)
        print(found_red)


def dijkstra():
    #global unvis_nodes, vis_nodes, last_vis_nodes, GREEN
    #create_nodes()
    #print(unvis_nodes)
    # MAKE START/END GLOBAL VARIABLES

    global unvis_nodes, vis_nodes, last_vis_nodes, GREEN, RED, BLACK

    unvis_nodes = []
    vis_nodes = []
    last_vis_nodes = []

    startPos = None
    endPos = None
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
    if (duplicate == True) or ((startPos == None) or (endPos == None)):
        return None # make sure to account for this in MazeSolver
    else:
        # now we know that only one start and one end exist
        # represent unvis_nodes as positions, create that list here
        # check for neighbors of each last_vis_node in unvis_nodes, get the cell from GRID
        # deal with duplicates and keep track of previous position and keep track of step
        #    store previous position as a tuple position
        for r in range(len(GRID)):
            for c in range(len(GRID[0])):
                if GRID[r][c].fill != BLACK:
                    unvis_nodes.append((r, c))

        print(startPos)
        print(startPos[0])
        print("unvis_nodes before recur")
        print(unvis_nodes)
        GRID[startPos[0]][startPos[1]].step = 0
        GRID[startPos[0]][startPos[1]].prevCell = None
        last_vis_nodes.append(startPos)
        unvis_nodes.remove(startPos)
        dijkstra_recur(1)
        return vis_nodes
    """
    start = next(n for n in unvis_nodes if n.cell.fill == GREEN) #make sure GREEN exists before getting here
    #print("GETS HERE")
    start.cell.step = 0
    #vis_nodes.append(start)
    last_vis_nodes.append(start)
    final = dijkstra_recur(1)
    print(vis_nodes)
    return (vis_nodes, final)
    """
