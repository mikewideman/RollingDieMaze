# MazeState.py
# Developed for CSCI-331 at RIT
# Authors: Mike Wideman, Dan Lavoie
# Description: Provides a class representing the state of a Rolling Die Maze.
# Also provides a Die class representing the state of a standard six-sided die.

from enum import Enum
import copy
from math import sqrt
import heapq

class Moves(Enum):
    north=1
    east=2
    south=3
    west=4

class Spaces:
    free=1
    obstacle=2
    current=3

class Heuristics:
    manhattan=1
    euclidean=2
    reachable_manhattan=3

class Die:
    def __init__(self):
        self.activeFace = 1
        self.westFace = 4
        self.northFace = 2
    
    def rotate(self, direction):
        startActive = self.activeFace
        startWest = self.westFace
        startNorth = self.northFace
        if direction == Moves.north:   
            self.activeFace = 7-startNorth
            self.northFace = startActive
        if direction == Moves.east:
            self.activeFace = startWest
            self.westFace = 7-startActive
        if direction == Moves.west:
            self.activeFace = 7-startWest
            self.westFace = startActive
        if direction == Moves.south:
            self.activeFace = startNorth
            self.startNorth = 7-startActive
    
    def canRotate(self, direction):
        """Ensures that the 6 is never face up on the die"""
        if direction == Moves.north:   
            return(self.northFace != 1)
        if direction == Moves.east:
            return(self.westFace != 6)
        if direction == Moves.west:
            return(self.westFace != 1)
        if direction == Moves.south:
            return(self.northFace != 6)
    
    def getActiveFace(self):
        return self.activeFace

class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell
        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
    def __lt__(self, other):
        return (self.f < other.f)
        
class AStar(object):
    def __init__(self, maze, die, start, end, heuristic):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = len(maze)
        self.grid_width = len(maze[0])
        self.maze = maze
        self.die = die
        self.important_points = []
        self.important_points.append(start)
        self.important_points.append(end)
        self.heuristic = heuristic
        
    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.maze[y][x] == Spaces.obstacle and self.die:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(self.important_points[0][0], self.important_points[0][1])
        self.end = self.get_cell(self.important_points[1][0], self.important_points[1][1])

    def get_heuristic(self, cell):
        if self.heuristic == 1:
            return self.get_heuristic_manhattan(cell)
        elif self.heuristic == 2:
            return self.get_heuristic_euclidean(cell)
        else:
            return self.get_heuristic_manhattan_reachable(cell)
    
    def get_heuristic_manhattan(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.
        @param cell
        @returns heuristic value H
        """
        return (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_heuristic_euclidean(self, cell):
        xdist = cell.x - self.end.x
        ydist = cell.y - self.end.y
        return math.sqrt(xdist*xdist + ydist*ydist)
    
    def get_heuristic_manhattan_reachable(self, cell):
        if cell.reachable:
            return (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
        else:
            return (abs(cell.x - self.end.x) + abs(cell.y - self.end.y)+3)

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        print(len(self.cells))
        print((x * self.grid_height + y))
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells
        
    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print('path: cell: %d,%d' % (cell.x, cell.y))
            
    def compare(self, cell1, cell2):
        """
        Compare 2 cells F values
        @param cell1 1st cell
        @param cell2 2nd cell
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if cell1.f < cell2.f:
            return -1
        elif cell1.f > cell2.f:
            return 1
        return 0
        
    def update_cell(self, adj, cell):
        """
        Update adjacent cell
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
        
    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))
class MazeState:
    
    def __init__(self, file):
        self.maze = []
        self.cells = []
        self.opened = []
        self.start = ()
        self.goal = ()
        self.readFile(file)
        self.die = Die()
        self.current = (0,0)
        
    def readFile(self, filename):
        file = open(filename)
        curLine = 0
        curChar = 0
        for line in file:
            self.maze.append([])
            for char in line:
                if char == 'S':
                    self.maze[curLine].append(Spaces.current)
                    self.start = (curLine, curChar)
                    self.current = (curLine, curChar)
                if char == '.':
                    self.maze[curLine].append(Spaces.free)
                if char == '*':
                    self.maze[curLine].append(Spaces.obstacle)
                if char == 'G':
                    self.maze[curLine].append(Spaces.free)
                    self.goal = (curLine,curChar)
                curChar+=1
            curLine+=1
            curChar=0

    def isValidSpace(self,x,y):
        return x >= 0 and y >=0 and x < len(self.maze) and \
        y < len(self.maze[x]) and not self.maze[x][y] == '*'

    def getChildStates(self):
        children = []
        possibleMoves = [Moves.north, Moves.east, Moves.south, Moves.west]
        for move in possibleMoves:
            childCandidate = copy.deepcopy(self)
            nextSpace = self.current
            if move == Moves.north:
                nextSpace = (self.current[0]-1, self.current[1])
            elif move == Moves.south:
                nextSpace = (self.current[0]+1, self.current[1])
            elif move == Moves.east:
                nextSpace = (self.current[0], self.current[1]+1)
            elif move == Moves.west:
                nextSpace = (self.current[0], self.current[1]-1)
            if self.isValidSpace(nextSpace[0], nextSpace[1]):
                childCandidate.maze[self.current[0]][self.current[1]] = Spaces.free
                childCandidate.maze[nextSpace[0]][nextSpace[1]] = Spaces.current
                childCandidate.current = nextSpace
                childCandidate.die.rotate(move)
                if not childCandidate.die.getActiveFace() == 6:
                    children.append(childCandidate)
        return children

    def isSolution(self):
        return self.current == self.goal
    
    def printMaze(self):
        curLine = 0
        curChar = 0
        for line in self.maze:
            for space in line:
                if space == Spaces.current:
                    print(str(self.die.getActiveFace()), end="")
                elif space == Spaces.obstacle:
                    print('*', end="")
                elif space == Spaces.free:
                    if (curLine,curChar) == self.start:
                        print('S', end="")
                    elif (curLine,curChar) == self.goal:
                        print('G', end="")
                    else:
                        print('.',end="")
                curChar+=1
            curLine+=1
            print() #print newline

#Test code for this module
my_maze = MazeState("maze.dat.txt")
astar = AStar(my_maze.maze, my_maze.die, my_maze.start, my_maze.goal, Heuristics.manhattan)
astar.init_grid()
astar.process()
#children = maze.getChildStates()
#nextChildren = children[0].getChildStates()
maze.printMaze()
#for child in children:
#    child.printMaze()
#for child in nextChildren:
#    child.printMaze()
